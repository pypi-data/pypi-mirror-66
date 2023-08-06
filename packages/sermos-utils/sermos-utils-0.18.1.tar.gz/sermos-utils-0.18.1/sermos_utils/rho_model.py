""" Methods used for interacting with RhoModels stored through Sermos.

    Most frequently, only two methods are used:

    `store_rho_model()` --> Ask Sermos to store a RhoModel for your deployments.
    `load_rho_model()`  --> Retrieve a stored model to use.
"""
import logging
import os
import pprint
from json.decoder import JSONDecodeError
from typing import Dict, Type, Optional, Tuple, Union

import boto3
import io
import re
import requests
from boto3.s3.transfer import TransferConfig

from rho_ml import RhoModel, StoredModel, LocalModelStorage, Version, \
    generate_model_locator, split_model_locator
from rho_ml.model_locator import DEFAULT_DELIMITER_PATTERN
from sermos_utils.constants import DEFAULT_STORE_MODEL_URL, S3_MODEL_BUCKET, \
    DEFAULT_GET_MODEL_URL

logger = logging.getLogger(__name__)


class ModelNotFoundError(Exception):
    """ Custom exception that is raised when no model is found.
    """
    pass


class ModelFailedToStoreError(Exception):
    """ Custom exception that is raised when a model is unable to be stored.
    """
    pass


def _get_sermos_api_headers(api_key: str) -> Dict[str, str]:
    """ Get basic headers required for interacting with Sermos Admin API.
    """
    return {
        'Content-Type': 'application/json',
        'apikey': api_key
    }


def _get_s3_client_from_api_response(response_data: Dict[str, str]):
    """ Get a valid s3 client based on credentials response from Sermos.

        This assumes the response data has been verified to be a 200 response,
        this will throw a keyerror otherwise.
    """
    try:
        access_key = response_data['aws_access_key']
        secret_key = response_data['aws_secret_key']
        session_token = response_data['aws_session_token']
        region = response_data['aws_region']
    except KeyError as e:
        logger.warning("Missing IAM keys in response:\n{0}"
                       .format(pprint.pformat(response_data)))
        raise e
    else:
        client = boto3.client('s3',
                              aws_access_key_id=access_key,
                              aws_secret_access_key=secret_key,
                              aws_session_token=session_token,
                              region_name=region)
        return client


def _get_transfer_config(max_concurrency: Optional[int] = None,
                         max_io_queue: Optional[int] = None,
                         multipart_chunksize: Optional[int] = None
                         ) -> TransferConfig:
    """ Create a boto3 s3 TransferConfig object. Default class doesn't handle
        None values to kwargs.
    """
    kwargs = {}
    if max_concurrency:
        kwargs['max_concurrency'] = max_concurrency
    if max_io_queue:
        kwargs['max_io_queue'] = max_io_queue
    if multipart_chunksize:
        kwargs['multipart_chunksize'] = multipart_chunksize
    config = TransferConfig(**kwargs)
    return config


def store_rho_model(model: Type[RhoModel],
                    deploy_key: Optional[str] = None,
                    store_model_endpoint: Optional[str] = None,
                    max_concurrency: Optional[int] = None,
                    max_io_queue: Optional[int] = None,
                    multipart_chunksize: Optional[int] = None):
    """ Get S3 credentials from the sermos-admin API, then use the credentials
        to store the model and metadata in the appropriate bucket / subfolder

        TODO: come up w/ way to compare hashes of stored models and loaded
        models
    """
    logger.info(f"Attempting to serialize {model.name}")

    # Given a RhoModel, create a StoredModel instance and pickle it to bytes
    stored_model = model.build_stored_model()
    store_bytes = stored_model.to_pickle()
    f = io.BytesIO()
    f.write(store_bytes)
    f.seek(0)

    logger.info("Serialization finished, requesting credentials from API...")

    # Get deployment key from environment if not explicitly provided. Fail here
    # if it's also not defined in environment.
    if not deploy_key:
        deploy_key = os.environ['SERMOS_DEPLOY_KEY']

    if not store_model_endpoint:
        store_model_endpoint = DEFAULT_STORE_MODEL_URL

    # Get our post headers and post data
    headers = _get_sermos_api_headers(api_key=deploy_key)
    model_locator = generate_model_locator(
        model.name, model.version.to_string())
    post_data = {'model_locator': model_locator}

    # Ask Sermos for credentials
    r = requests.post(url=store_model_endpoint, headers=headers, json=post_data)
    if r.status_code != 200:
        logger.error(f"Failed to store RhoModel: {r.content}")
        raise ModelFailedToStoreError("Unable to store RhoModel!")

    response_data = r.json()
    client = _get_s3_client_from_api_response(response_data=response_data)
    storage_key = response_data['model_key']

    logger.info(f"Uploading serialized {model_locator}")

    transfer_config = _get_transfer_config(
        max_concurrency=max_concurrency,
        max_io_queue=max_io_queue,
        multipart_chunksize=multipart_chunksize)

    client.upload_fileobj(
        f, Bucket=S3_MODEL_BUCKET, Key=storage_key, Config=transfer_config)


def _get_model_api_response(model_name: str,
                            version_pattern: str,
                            deploy_key: str,
                            get_model_endpoint: Optional[str] = None
                            ) -> Dict[str, str]:
    """ Ask Sermos' get-model/ api endpoint for credentials and location
        of a specific model. Allows version pattern to be an exact version
        (e.g. 1.2.0) or a pattern with wildcard search (e.g. 1.*.*), which
        will return the highest compatible version.
    """
    headers = _get_sermos_api_headers(api_key=deploy_key)

    if not get_model_endpoint:
        get_model_endpoint = DEFAULT_GET_MODEL_URL

    query_params = {
        'model_name': model_name,
        'version_pattern': version_pattern
    }

    logger.debug("Requesting storage info from Admin API...")

    try:
        r = requests.post(
            url=get_model_endpoint, headers=headers, json=query_params)
        response_data = r.json()
    except Exception as e:
        logger.error("Failed to communicate with /get-model/ API ...")
        logger.exception(e)
        raise e

    if r.status_code == 404:
        raise ModelNotFoundError(response_data['message'])

    return response_data


def _get_stored_model_bytes_from_api_response(response_data: Dict[str, str]) \
        -> bytes:
    """ Given a model 'get' response from Sermos, retrieve the StoredModel
        from cloud storage.
    """
    client = _get_s3_client_from_api_response(response_data=response_data)
    model_key = response_data['model_key']

    logger.debug("Retrieving {0} from storage...".format(model_key))

    s3_response = client.get_object(Bucket=S3_MODEL_BUCKET, Key=model_key)
    model_bytes = s3_response['Body'].read()

    return model_bytes


def _determine_load_local_or_remote(
        model_name: str,
        version_pattern: str,
        delimiter_pattern: Optional[str] = DEFAULT_DELIMITER_PATTERN,
        deploy_key: Optional[str] = None,
        local_base_path: Optional[str] = None,
        get_model_endpoint: Optional[str] = None,
        force_search: bool = False
        ) -> Tuple[Union['local', 'remote'], Union[str, dict]]:
    """ Determine whether to load the RhoModel from local disk or from the cloud

        Return value is either
            ('local', '/full/path/to/Model_0.1.0')
        or
            ('remote', {'api': 'response from sermos'})
    """
    # Get a properly initialized LocalModelStorage() instance
    local_storage = LocalModelStorage(base_path=local_base_path)

    # Check to see if a compatible model already exists locally (don't load it)
    local_model_path = local_storage.get_key_from_pattern(
        model_name=model_name, version_pattern=version_pattern)

    # If a local model exists and there is not a forced-search, proceed to load
    if local_model_path is not None and not force_search:
        logger.info(f"Local model found at: {local_model_path}. "
                    "Loading due to no force_search.")
        load_from = 'local'
        retrieval_info = local_model_path
    else:
        # Get deploy key from environment if not provided. Fail if can't find there.
        if not deploy_key:
            deploy_key = os.environ['SERMOS_DEPLOY_KEY']

        # If force_search is True AND/OR we didn't find a local_model_path,
        # retrieve the highest compatible version of this model from cloud.
        api_response = _get_model_api_response(
            model_name=model_name, version_pattern=version_pattern,
            deploy_key=deploy_key, get_model_endpoint=get_model_endpoint)
        remote_model_version = api_response['model_version']

        # If we did find a local model, parse it's local key to find the
        # version. This is way more CPU/memory so we don't need to load/unpickle
        # if the local model is actually outdated
        if local_model_path is not None:
            _model_name, local_model_version = split_model_locator(
                local_model_path, delimiter_pattern=delimiter_pattern
            )
        else:
            local_model_version = None

        # If remote has a newer version of the model, load it
        if (local_model_version is None)\
                or (local_model_version < remote_model_version):
            logger.info(f"Loading {model_name} from REMOTE due to higher "
                        f"version: {remote_model_version} vs "
                        f"{local_model_version}")
            load_from = 'remote'
            retrieval_info = api_response
        else:
            # Otherwise, load up the model from disk
            logger.info(f"Local model found at: {local_model_path}. "
                        "Loading due to no higher version found on remote.")
            load_from = 'local'
            retrieval_info = local_model_path

    return load_from, retrieval_info


def load_rho_model(model_name: str,
                   version_pattern: str,
                   delimiter_pattern: Optional[str] = DEFAULT_DELIMITER_PATTERN,
                   deploy_key: Optional[str] = None,
                   local_base_path: Optional[str] = None,
                   save_to_local_disk: bool = True,
                   get_model_endpoint: Optional[str] = None,
                   force_search: bool = False) -> Type[RhoModel]:
    """ Retrieve models stored using the Sermos Admin API by name and
        version.

        Optionally cache the result locally for later use (caching is ON by
        default).

        If force_search == True, always check cloud storage for latest version,
        regardless of whether a local model exists.

        Will raise `ModelNotFoundError` in the event no matching model is found.
    """
    # Get deploy key from environment if not provided. Fail if can't find there.
    if not deploy_key:
        deploy_key = os.environ['SERMOS_DEPLOY_KEY']

    local_or_remote, retrieval_info = _determine_load_local_or_remote(
        model_name=model_name, version_pattern=version_pattern,
        delimiter_pattern=delimiter_pattern, deploy_key=deploy_key,
        local_base_path=local_base_path, get_model_endpoint=get_model_endpoint,
        force_search=force_search
    )

    if local_or_remote == 'local':
        local_storage = LocalModelStorage(base_path=local_base_path)
        model = local_storage.retrieve(retrieval_info)

    elif local_or_remote == 'remote':
        stored_bytes = _get_stored_model_bytes_from_api_response(
            response_data=retrieval_info)
        stored_model = StoredModel.from_pickle(stored_bytes=stored_bytes)
        model = stored_model.load_model()

        if save_to_local_disk and model is not None:
            logger.info("Caching retrieved model {0} locally..."
                        .format(model.name))
            local_storage = LocalModelStorage(base_path=local_base_path)
            local_storage.store(model=model)

    return model
