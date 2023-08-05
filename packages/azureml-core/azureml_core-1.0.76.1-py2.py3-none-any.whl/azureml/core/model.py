# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Contains functionality for managing machine learning models in Azure Machine Learning.

With the :class:`azureml.core.model.Model` class, you can accomplish the following main tasks:

* register your model with a workspace
* profile your model to understand deployment requirements
* package your model for use with Docker
* deploy your model to an inference endpoint as a web service

For more information on how
models are used, see [How Azure Machine Learning works: Architecture and
concepts](https://docs.microsoft.com/azure/machine-learning/service/concept-azure-machine-learning-architecture).
"""

from __future__ import print_function

import copy
import json
import logging
import os
import shutil
import tarfile
import tempfile
import time
import uuid

from collections import OrderedDict
from datetime import datetime
from operator import attrgetter

import requests

from azureml.core.container_registry import ContainerRegistry
from azureml.core.dataset import Dataset
from azureml.data._dataset import _Dataset
from azureml.data.dataset_snapshot import DatasetSnapshot
from azureml.data import TabularDataset, FileDataset

from azureml.core.environment import Environment
from azureml.core.experiment import Experiment
from azureml.core.run import get_run
from azureml.core.compute import AksCompute
from azureml.core.resource_configuration import ResourceConfiguration

from azureml.exceptions import (WebserviceException, RunEnvironmentException, ModelNotFoundException)
from azureml._model_management._constants import DATASET_SNAPSHOT_ID_FORMAT
from azureml._model_management._constants import MMS_SYNC_TIMEOUT_SECONDS
from azureml._model_management._constants import MMS_WORKSPACE_API_VERSION
from azureml._model_management._constants import WEBAPI_IMAGE_FLAVOR
from azureml._model_management._constants import ARCHITECTURE_AMD64
from azureml._model_management._constants import CUSTOM_BASE_IMAGE_SUPPORTED_RUNTIMES
from azureml._model_management._constants import SUPPORTED_CUDA_VERSIONS
from azureml._model_management._constants import AKS_ENDPOINT_TYPE
from azureml._model_management._constants import MIR_WEBSERVICE_TYPE, MIR_SINGLE_MODEL_WEBSERVICE_TYPE
from azureml._model_management._util import _get_mms_url
from azureml._model_management._util import get_paginated_results
from azureml._model_management._util import model_payload_template
from azureml._model_management._util import add_sdk_to_requirements
from azureml._model_management._util import upload_dependency
from azureml._model_management._util import wrap_execution_script_with_source_directory
from azureml._model_management._util import joinPath
from azureml._model_management._util import validate_entry_script_name
from azureml._model_management._util import check_duplicate_properties
from azureml._model_management._util import download_docker_build_context
from azureml._model_management._util import get_docker_client
from azureml._model_management._util import get_mms_operation
from azureml._model_management._util import get_requests_session
from azureml._model_management._util import get_workspace_registry_credentials
from azureml._model_management._util import login_to_docker_registry
from azureml._model_management._util import make_http_request
from azureml._model_management._util import pull_docker_image
from azureml._model_management._util import submit_mms_operation
from azureml._model_management._util import model_name_validation
from azureml._model_management._util import webservice_name_validation
from azureml._model_management._util import build_and_validate_no_code_environment_image_request
from azureml._model_management._util import convert_parts_to_environment

from azureml._restclient.clientbase import ClientBase
from azureml._restclient.artifacts_client import ArtifactsClient
from azureml._restclient.assets_client import AssetsClient
from dateutil.parser import parse

from azureml._file_utils import download_file
from azureml._model_management._util import validate_path_exists_or_throw
from azureml._model_management._constants import SUPPORTED_RUNTIMES
from azureml._model_management._constants import UNDOCUMENTED_RUNTIMES

from azureml.core.profile import ModelProfile

module_logger = logging.getLogger(__name__)
MODELS_DIR = "azureml-models"


class Model(object):
    """Represents the result of machine learning training.

    A *model* is the result of a Azure Machine learning training :class:`azureml.core.run.Run`
    or some other model training process outside of Azure. Regardless of how the model is produced,
    it can be registered in a workspace, where it is represented by a name and a version. With the
    Model class, you can package models for use with Docker and deploy them as an inference endpoint.

    For an end-to-end tutorial showing how models are created, managed, and consumed, see
    `Train image classification model with MNIST data and scikit-learn using Azure Machine
    Learning <https://docs.microsoft.com/azure/machine-learning/service/tutorial-train-models-with-aml>`_.

    .. remarks::

        The Model constructor is used to retrieve a cloud representation of a Model object associated
        with the specified workspace. At least the name or ID must be provided to retrieve models, but there
        are also other options for filtering including by tags, properties, run ID, and framework.

        .. code-block:: python

            from azureml.core.model import Model
            model = Model(ws, 'my_model_name')

        For example, if you have a model that is stored in multiple files, you can register them as a
        single model in your Azure Machine Learning workspace. After registration, you can then download
        or deploy the registered model and receive all the files that were registered.

        Registering a model creates a logical container for the one or more files that make up your model.
        In addition to the content of the model file itself, a registered model also stores model metadata,
        including model description, tags, and framework information, that is useful when managing and
        deploying the model in your workspace. For example, with tags you can categorize your models and
        apply filters when listing models in your workspace. After registration, you can then download
        or deploy the registered model and receive all the files and metadata that were registered.

        The following sample shows how to register a model specifying tags and a description.

        .. code-block:: python

            from azureml.core.model import Model

            model = Model.register(model_path="sklearn_regression_model.pkl",
                                   model_name="sklearn_regression_model_local_adv",
                                   tags={'area': "diabetes", 'type': "regression"},
                                   description="Ridge regression model to predict diabetes",
                                   workspace=ws)

        Full sample is available from
        https://github.com/Azure/MachineLearningNotebooks/blob/master/how-to-use-azureml/deployment/deploy-to-local/register-model-deploy-local-advanced.ipynb


        The following sample shows how to register a model specifying framework, input and output
        datasets, and resource configuration.

        .. code-block:: python

            from azureml.core import Model
            from azureml.core.resource_configuration import ResourceConfiguration

            model = Model.register(workspace=ws,
                                   model_name='my-sklearn-model',                # Name of the registered model in your workspace.
                                   model_path='./sklearn_regression_model.pkl',  # Local file to upload and register as a model.
                                   model_framework=Model.Framework.SCIKITLEARN,  # Framework used to create the model.
                                   model_framework_version='0.19.1',             # Version of scikit-learn used to create the model.
                                   sample_input_dataset=input_dataset,
                                   sample_output_dataset=output_dataset,
                                   resource_configuration=ResourceConfiguration(cpu=1, memory_in_gb=0.5),
                                   description='Ridge regression model to predict diabetes progression.',
                                   tags={'area': 'diabetes', 'type': 'regression'})

            print('Name:', model.name)
            print('Version:', model.version)

        Full sample is available from
        https://github.com/Azure/MachineLearningNotebooks/blob/master/how-to-use-azureml/deployment/deploy-to-cloud/model-register-and-deploy.ipynb


    :param workspace: The workspace object containing the model to retrieve.
    :type workspace: azureml.core.Workspace
    :param name: The name of the model to retrieve. The latest model with the specified name is returned,
        if it exists.
    :type name: str
    :param id: The ID of the model to retrieve. The model with the specified ID is returned, if it exists.
    :type id: str
    :param tags: An optional list of tags used to filter returned results. Results are filtered based on the
        provided list, searching by either 'key' or '[key, value]'. Ex. ['key', ['key2', 'key2 value']]
    :type tags: builtin.list
    :param properties: An optional list of properties used to filter returned results. Results are filtered
        based on the provided list, searching by either 'key' or '[key, value]'.
        Ex. ['key', ['key2', 'key2 value']]
    :type properties: builtin.list
    :param version: The model version to return. When provided along with ``name``, the specific
        version of the specified named model is returned, if it exists.
    :type version: int
    :param run_id: Optional ID used to filter returned results.
    :type run_id: str
    :param model_framework: Optional framework name used to filter returned results. If specified, results
        are returned for the models matching the specified framework. See :class:`azureml.core.model.Model.Framework`
        for allowed values.
    :type model_framework: str
    """

    _expected_payload_keys = ['createdTime', 'description', 'id', 'mimeType', 'name', 'properties', 'unpack', 'url',
                              'version', 'experimentName', 'runId', 'datasets']

    def __init__(self, workspace, name=None, id=None, tags=None, properties=None, version=None,
                 run_id=None, model_framework=None):
        """Model constructor.

        The Model constructor is used to retrieve a cloud representation of a Model object associated with the provided
        workspace. Must provide either name or ID.

        :param workspace: The workspace object containing the model to retrieve.
        :type workspace: azureml.core.Workspace
        :param name: The name of the model to retrieve. The latest model with the specified name is returned,
            if it exists.
        :type name: str
        :param id: The ID of the model to retrieve. The model with the specified ID is returned, if it exists.
        :type id: str
        :param tags: An optional list of tags used to filter returned results. Results are filtered based on the
            provided list, searching by either 'key' or '[key, value]'. Ex. ['key', ['key2', 'key2 value']]
        :type tags: builtin.list
        :param properties: An optional list of properties used to filter returned results. Results are filtered
            based on the provided list, searching by either 'key' or '[key, value]'.
            Ex. ['key', ['key2', 'key2 value']]
        :type properties: builtin.list
        :param version: The model version to return. When provided along with ``name``, the specific
            version of the specified named model is returned, if it exists.
        :type version: int
        :param run_id: Optional ID used to filter returned results.
        :type run_id: str
        :param model_framework: Optional framework name used to filter returned results. If specified, results
            are returned for the models matching the specified framework. See
            :class:`azureml.core.model.Model.Framework` for allowed values.
        :type model_framework: str
        :return: A model object, if one is found in the provided workspace
        :rtype: azureml.core.Model
        :raises: azureml.exceptions.ModelNotFoundException
        """
        self.created_time = None
        self.description = None
        self.id = None
        self.mime_type = None
        self.name = None
        self.model_framework = None
        self.tags = None
        self.properties = None
        self.unpack = None
        self.url = None
        self.version = None
        self.workspace = None
        self.experiment_name = None
        self.run_id = None
        self.run = None
        self.datasets = {}
        self._auth = None
        self._mms_endpoint = None
        self.sample_input_dataset = None
        self.sample_output_dataset = None
        self.resource_configuration = None

        if workspace:
            get_response_payload = self._get(workspace, name, id, tags, properties, version, model_framework, run_id)
            if get_response_payload:
                self._validate_get_payload(get_response_payload)
                self._initialize(workspace, get_response_payload)
            else:
                error_message = 'ModelNotFound: Model with '
                if id:
                    error_message += 'ID {}'.format(id)
                else:
                    error_message += 'name {}'.format(name)
                if tags:
                    error_message += ', tags {}'.format(tags)
                if properties:
                    error_message += ', properties {}'.format(properties)
                if version:
                    error_message += ', version {}'.format(version)
                if model_framework:
                    error_message += ', framework {}'.format(model_framework)
                if run_id:
                    error_message += ', Run ID {}'.format(run_id)
                error_message += ' not found in provided workspace'

                raise WebserviceException(error_message)

    def __repr__(self):
        """Return the string representation of the Model object.

        :return: String representation of the Model object
        :rtype: str
        """
        return "{}(workspace={}, name={}, id={}, version={}, tags={}, " \
               "properties={})".format(self.__class__.__name__,
                                       self.workspace.__repr__(), self.name, self.id, self.version,
                                       self.tags, self.properties)

    def _initialize(self, workspace, obj_dict):
        """Initialize the Model instance.

        This is used because the constructor is used as a getter.

        :param workspace:
        :type workspace: azureml.core.Workspace
        :param obj_dict:
        :type obj_dict: dict
        :return:
        :rtype: None
        """
        created_time = parse(obj_dict['createdTime'])
        model_id = obj_dict['id']
        self.created_time = created_time
        self.description = obj_dict['description']
        self.id = model_id
        self.mime_type = obj_dict['mimeType']
        self.name = obj_dict['name']
        self.model_framework = obj_dict['framework']
        self.model_framework_version = obj_dict['frameworkVersion']
        self.tags = obj_dict.get('kvTags', {})
        self.properties = obj_dict['properties']
        self.unpack = obj_dict['unpack']
        self.url = obj_dict['url']
        self.version = obj_dict['version']
        self.workspace = workspace
        self.experiment_name = obj_dict['experimentName']
        self.run_id = obj_dict['runId']
        self._auth = workspace._auth
        self._mms_endpoint = _get_mms_url(workspace) + '/models/{}'.format(model_id)
        self.parent_id = obj_dict.get('parentModelId')
        self.derived_model_ids = obj_dict.get('derivedModelIds')
        self.resource_configuration = ResourceConfiguration.deserialize(obj_dict.get('resourceRequirements'))

        if self.experiment_name and self.run_id:
            try:
                experiment = Experiment(workspace, self.experiment_name)
                run = get_run(experiment, self.run_id)
                self.run = run
            except Exception:
                pass

        for dataset_reference in obj_dict['datasets']:
            dataset_scenario = dataset_reference['name']
            dataset_id = dataset_reference['id']
            dataset = Model._get_dataset(workspace, dataset_id)
            if dataset is not None:
                self.datasets.setdefault(dataset_scenario, []).append(dataset)

        sample_input_dataset_url = obj_dict.get('sampleInputData')
        if sample_input_dataset_url is not None and sample_input_dataset_url.startswith('aml://dataset/'):
            sample_input_dataset_id = sample_input_dataset_url[len('aml://dataset/'):]
            self.sample_input_dataset = Model._get_dataset(workspace, sample_input_dataset_id)

        sample_output_dataset_url = obj_dict.get('sampleOutputData')
        if sample_output_dataset_url is not None and sample_output_dataset_url.startswith('aml://dataset/'):
            sample_output_dataset_id = sample_output_dataset_url[len('aml://dataset/'):]
            self.sample_output_dataset = Model._get_dataset(workspace, sample_output_dataset_id)

    @staticmethod
    def _get(workspace, name=None, id=None, tags=None, properties=None, version=None,
             model_framework=None, run_id=None):
        """Retrieve the Model object from the cloud.

        :param workspace:
        :type workspace: workspace: azureml.core.Workspace
        :param name:
        :type name: str
        :param id:
        :type id: str
        :param tags:
        :type tags: builtin.list
        :param properties:
        :type properties: builtin.list
        :param version:
        :type version: int
        :param run_id:
        :type run_id: str
        :return:
        :rtype: dict
        """
        if not id and not name:
            raise WebserviceException('Error, one of id or name must be provided.', logger=module_logger)

        headers = workspace._auth.get_authentication_header()
        params = {'api-version': MMS_WORKSPACE_API_VERSION, 'orderBy': 'CreatedAtDesc', 'count': 1}
        base_url = _get_mms_url(workspace)
        mms_url = base_url + '/models'

        if id:
            mms_url += '/{}'.format(id)
        else:
            params['name'] = name
        if tags:
            tags_query = ""
            for tag in tags:
                if type(tag) is list:
                    tags_query = tags_query + tag[0] + "=" + tag[1] + ","
                else:
                    tags_query = tags_query + tag + ","
            tags_query = tags_query[:-1]
            params['tags'] = tags_query
        if properties:
            properties_query = ""
            for prop in properties:
                if type(prop) is list:
                    properties_query = properties_query + prop[0] + "=" + prop[1] + ","
                else:
                    properties_query = properties_query + prop + ","
            properties_query = properties_query[:-1]
            params['properties'] = properties_query
        if version:
            params['version'] = version
        if model_framework:
            params['modelFramework'] = model_framework
        if run_id:
            params['runId'] = run_id

        resp = ClientBase._execute_func(get_requests_session().get, mms_url, headers=headers, params=params)
        if resp.status_code == 200:
            content = resp.content
            if isinstance(content, bytes):
                content = content.decode('utf-8')
            model_payload = json.loads(content)
            if id:
                return model_payload
            else:
                paginated_results = get_paginated_results(model_payload, headers)
                if paginated_results:
                    return paginated_results[0]
                else:
                    return None
        elif resp.status_code == 404:
            return None
        else:
            raise WebserviceException('Received bad response from Model Management Service:\n'
                                      'Response Code: {}\n'
                                      'Headers: {}\n'
                                      'Content: {}'.format(resp.status_code, resp.headers, resp.content),
                                      logger=module_logger)

    @staticmethod
    def register(workspace, model_path, model_name, tags=None, properties=None, description=None,
                 datasets=None, model_framework=None, model_framework_version=None, child_paths=None,
                 sample_input_dataset=None, sample_output_dataset=None, resource_configuration=None):
        """Register a model with the provided workspace.

        .. remarks::

            In addition to the content of the model file itself, a registered model also stores model metadata,
            including model description, tags, and framework information, that is useful when managing and
            deploying the model in your workspace. For example, with tags you can categorize your models and
            apply filters when listing models in your workspace.

            The following sample shows how to register a model specifying tags and a description.

            .. code-block:: python

                from azureml.core.model import Model

                model = Model.register(model_path="sklearn_regression_model.pkl",
                                       model_name="sklearn_regression_model_local_adv",
                                       tags={'area': "diabetes", 'type': "regression"},
                                       description="Ridge regression model to predict diabetes",
                                       workspace=ws)

            Full sample is available from
            https://github.com/Azure/MachineLearningNotebooks/blob/master/how-to-use-azureml/deployment/deploy-to-local/register-model-deploy-local-advanced.ipynb


        :param workspace: The workspace to register the model with.
        :type workspace: azureml.core.Workspace
        :param model_path: The path on the local file system where the model assets are
            located. This can be a direct pointer to a single file or folder. If pointing to a folder, the
            ``child_paths`` parameter can be used to specify individual files to bundle together as the Model object,
            as opposed to using the entire contents of the folder.
        :type model_path: str
        :param model_name: The name to register the model with.
        :type model_name: str
        :param tags: An optional dictionary of key value tags to assign to the model.
        :type tags: dict({str : str})
        :param properties: An optional dictionary of key value properties to assign to the model.
            These properties can't be changed after model creation, however new key value pairs can be added.
        :type properties: dict({str : str})
        :param description: A text description of the model.
        :type description: str
        :param datasets: A list of tuples where the first element describes the dataset-model relationship and
            the second element is the dataset.
        :type datasets: builtin.list[(str, azureml.data.abstract_dataset.AbstractDataset)]
        :param model_framework: The framework of the registered model. Using the system-supported constants
            from the :class:`azureml.core.model.Model.Framework` class allows for simplified deployment for
            some popular frameworks.
        :type model_framework: str
        :param model_framework_version: The framework version of the registered model.
        :type model_framework_version: str
        :param child_paths: If provided in conjunction with a ``model_path`` to a folder, only the specified
            files will be bundled into the Model object.
        :type child_paths: builtin.list[str]
        :param sample_input_dataset: Sample input dataset for the registered model.
        :type sample_input_dataset: azureml.data.abstract_dataset.AbstractDataset
        :param sample_output_dataset: Sample output dataset for the registered model.
        :type sample_output_dataset: azureml.data.abstract_dataset.AbstractDataset
        :param resource_configuration: A resource configuration to run the registered model.
        :type resource_configuration: azureml.core.resource_configuration.ResourceConfiguration
        :return: The registered model object.
        :rtype: azureml.core.Model
        """
        model_name_validation(model_name)
        if model_framework is None and model_framework_version is not None:
            raise WebserviceException("Model framework version cannot be provided without a valid framework",
                                      logger=module_logger)

        Model._validate_model_path(model_path, child_paths)

        aggregate_dir = None
        if child_paths:
            aggregate_dir = tempfile.TemporaryDirectory()
            for file in child_paths:
                file = file.rstrip(os.sep)
                cur_path = ''
                for dir in os.path.dirname(file).split(os.sep):
                    new_path = os.path.join(cur_path, dir)
                    target_path = os.path.join(aggregate_dir.name, new_path)
                    if not os.path.isdir(target_path):
                        os.mkdir(target_path)
                    cur_path = new_path
                shutil.copy2(os.path.join(model_path, file), os.path.join(aggregate_dir.name, cur_path))
            model_path = aggregate_dir.name
            arcname = model_name
        else:
            model_path = model_path.rstrip(os.sep)
            arcname = os.path.basename(os.path.abspath(model_path))

        artifact_client = ArtifactsClient(workspace.service_context)
        asset_client = AssetsClient(workspace.service_context)

        tar_name = arcname + '.tar.gz'
        tmpdir = tempfile.TemporaryDirectory()
        model_tar_path = os.path.join(tmpdir.name, tar_name)
        dependency_tar = tarfile.open(model_tar_path, 'w:gz')
        dependency_tar.add(model_path, arcname=arcname)
        dependency_tar.close()

        origin = 'LocalUpload'
        container = '{}-{}'.format(datetime.now().strftime('%y%m%dT%H%M%S'), str(uuid.uuid4())[:8])
        module_logger.debug('Uploading model {} with size {} bytes'.format(model_name,
                                                                           os.path.getsize(model_tar_path)))
        artifact_client.upload_artifact_from_path(model_tar_path, origin, container, tar_name)
        prefix_values = [{'prefix': '{}/{}/{}'.format(origin, container, tar_name)}]
        asset = asset_client.create_asset(model_name, prefix_values, None)
        asset_id = asset.id
        print('Registering model {}'.format(model_name))
        model = Model._register_with_asset(workspace, model_name, asset_id, tags, properties, description,
                                           datasets=datasets, model_framework=model_framework,
                                           model_framework_version=model_framework_version, unpack=True,
                                           sample_input_dataset=sample_input_dataset,
                                           sample_output_dataset=sample_output_dataset,
                                           resource_configuration=resource_configuration
                                           )

        if aggregate_dir:
            aggregate_dir.cleanup()
        if tmpdir:
            tmpdir.cleanup()

        return model

    @staticmethod
    def _validate_model_path(model_path, child_paths=None):
        """Validate that the provided model path exists.

        :param model_path:
        :type model_path: str
        :param child_paths:
        :type child_paths: builtin.list[str]
        :raises: azureml.exceptions.WebserviceException
        """
        if not os.path.exists(model_path):
            raise WebserviceException('Error, provided model path "{}" cannot be found'.format(model_path),
                                      logger=module_logger)

        if child_paths:
            for path in child_paths:
                if not os.path.exists(os.path.join(model_path, path)):
                    raise WebserviceException('Error, provided child path "{}" cannot be found'.format(path),
                                              logger=module_logger)

    @staticmethod
    def _get_dataset(workspace, dataset_id):
        """Get the datatset by id.

        :param workspace:
        :type workspace: azureml.core.Workspace
        :param dataset_id:
        :type dataset_id: str
        :raises: azureml.exceptions.WebserviceException
        """
        if '/datasetSnapshotName' in dataset_id:
            snapshot_pieces = dataset_id.split('/')
            dataset_id = snapshot_pieces[2]
            snapshot_name = snapshot_pieces[4]
            try:
                dataset_snapshot = DatasetSnapshot.get(workspace, snapshot_name, dataset_id=dataset_id)
                return dataset_snapshot
            except Exception as e:
                module_logger.warning('Unable to retrieve DatasetSnapshot with name {} and DatasetID {} due to '
                                      'the following exception.\n'
                                      '{}'.format(snapshot_name, dataset_id, e))
        else:
            try:
                dataset = _Dataset._get_by_id(workspace, dataset_id)
                return dataset
            except Exception as e:
                # Expect exception here if model is registered with legacy dataset, whose id is not the saved-id.
                module_logger.warning('Cannot find Saved Dataset with ID {} due to the following exception.\n'
                                      '{}'.format(dataset_id, e))
                # Fall back to retrieving dataset using id as registration-id
                try:
                    from azureml.data._dataset_deprecation import silent_deprecation_warning
                    with silent_deprecation_warning:
                        legacy_dataset = Dataset.get(workspace, id=dataset_id)
                    return legacy_dataset
                except Exception as e:
                    module_logger.warning('Unable to retrieve Dataset with ID {} due to the following exception.\n'
                                          '{}'.format(dataset_id, e))

    @staticmethod
    def _get_dataset_id(workspace, dataset, param_name):
        """Get the id of a datatset.

        :param workspace:
        :type workspace: azureml.core.Workspace
        :param dataset: datset whose id is to fetched
        :type dataset: FileDataset | TabularDataset
        :raises: azureml.exceptions.WebserviceException
        """
        if isinstance(dataset, TabularDataset) or isinstance(dataset, FileDataset):
            saved_id = dataset._ensure_saved(workspace)
            return saved_id
        else:
            raise WebserviceException(
                'Invalid {} of type {} passed, must be of type TabularDataset or FileDataset'
                .format(param_name, type(dataset)), logger=module_logger)

    @staticmethod
    def get_model_path(model_name, version=None, _workspace=None):
        """Return path to model.

        | The function will search for the model in the following locations.
        |
        | If ``version`` is None:
        | 1) Download from remote to cache
        | 2) Load from cache `azureml-models/$MODEL_NAME/$LATEST_VERSION/`
        | 3) ./$MODEL_NAME

        | If ``version`` is not None:
        | 1) Load from cache `azureml-models/$MODEL_NAME/$LATEST_VERSION/`
        | 2) Download from remote to cache

        :param model_name: The name of the model to retrieve.
        :type model_name: str
        :param version: The version of the model to retrieve. Defaults to the latest version.
        :type version: int
        :param _workspace: The workspace to retrieve a model from. Can't use remotely.
        :type _workspace: azureml.core.Workspace
        :return: The path on disk to the model.
        :rtype: str
        :raises: :class:`azureml.exceptions.ModelNotFoundException`
        """
        if version is not None and not isinstance(version, int):
            raise WebserviceException("version should be an int", logger=module_logger)
        # check if in preauthenticated env
        active_workspace = _workspace
        try:
            # get workspace from submitted run
            from azureml.core.run import Run
            run = Run.get_context(allow_offline=False)
            module_logger.debug("Run is {}".format(run))
            experiment = run.experiment
            module_logger.debug("RH is {}".format(experiment))
            active_workspace = experiment.workspace
        except RunEnvironmentException as ee:
            # Ignore RunEnvironmentException logging inside inference container.
            if 'SERVICE_NAME' not in os.environ:
                message = "RunEnvironmentException: {}".format(ee)
                module_logger.debug(message)

        if version is not None:
            try:
                return Model._get_model_path_local(model_name, version)
            except ModelNotFoundException as ee:
                module_logger.debug("Model not find in local")
                if active_workspace is not None:
                    module_logger.debug("Getting model from remote")
                    return Model._get_model_path_remote(model_name, version, active_workspace)
                raise WebserviceException(ee.message, logger=module_logger)
        else:
            if active_workspace is not None:
                return Model._get_model_path_remote(model_name, version, active_workspace)
            else:
                return Model._get_model_path_local(model_name, version)

    @staticmethod
    def _get_model_path_local(model_name, version=None):
        """Get the local path to the Model.

        :param model_name:
        :type model_name: str
        :param version:
        :type version: int
        :return:
        :rtype: str
        """
        if version is not None and not isinstance(version, int):
            raise WebserviceException("version should be an int", logger=module_logger)
        if model_name is None:
            raise WebserviceException("model_name is None", logger=module_logger)

        candidate_model_path = os.path.join(MODELS_DIR, model_name)
        # Probing azureml-models/<name>
        if not os.path.exists(candidate_model_path):
            return Model._get_model_path_local_from_root(model_name)
        else:
            # Probing azureml-models/<name> exists, probing version
            if version is None:
                latest_version = Model._get_latest_version(os.listdir(os.path.join(MODELS_DIR, model_name)))
                module_logger.debug("version is None. Latest version is {}".format(latest_version))
            else:
                latest_version = version
                module_logger.debug("Using passed in version {}".format(latest_version))

            candidate_model_path = os.path.join(candidate_model_path, str(latest_version))
            # Probing azureml-models/<name>/<version> exists
            if not os.path.exists(candidate_model_path):
                return Model._get_model_path_local_from_root(model_name)
            else:
                # Checking one file system node
                file_system_entries = os.listdir(candidate_model_path)
                if len(file_system_entries) != 1:
                    raise WebserviceException("Dir {} can contain only 1 file or folder. "
                                              "Found {}".format(candidate_model_path, file_system_entries),
                                              logger=module_logger)

                candidate_model_path = os.path.join(candidate_model_path, file_system_entries[0])
                module_logger.debug("Found model path at {}".format(candidate_model_path))
                return candidate_model_path

    @staticmethod
    def _get_model_path_local_from_root(model_name):
        """Get the path to the Model from the root of the directory.

        :param model_name:
        :type model_name: str
        :return:
        :rtype: str
        """
        paths_in_scope = Model._paths_in_scope(MODELS_DIR)
        module_logger.debug("Checking root for {} because candidate dir {} had {} nodes: {}".format(
            model_name, MODELS_DIR, len(paths_in_scope), "\n".join(paths_in_scope)))

        candidate_model_path = model_name
        if os.path.exists(candidate_model_path):
            return candidate_model_path
        raise ModelNotFoundException("Model not found in cache or in root at ./{}. For more info,"
                                     "set logging level to DEBUG.".format(candidate_model_path))

    @staticmethod
    def _paths_in_scope(dir):
        """Get a list of paths in the provided directory.

        :param dir:
        :type dir: str
        :return:
        :rtype: builtin.list[str]
        """
        paths_in_scope = []
        for root, dirs, files in os.walk(dir):
            for file in files:
                paths_in_scope.append(os.path.join(root, file))
        return paths_in_scope

    @staticmethod
    def _get_last_path_segment(path):
        """Get the last segment of the path.

        :param path:
        :type path: str
        :return:
        :rtype: str
        """
        last_segment = os.path.normpath(path).split(os.sep)[-1]
        module_logger.debug("Last segment of {} is {}".format(path, last_segment))
        return last_segment

    @staticmethod
    def _get_strip_prefix(prefix_id):
        """Get the prefix to strip from the path.

        :param prefix_id:
        :type prefix_id: str
        :return:
        :rtype: str
        """
        path = prefix_id.split("/", 2)[-1]
        module_logger.debug("prefix id {} has path {}".format(prefix_id, path))
        path_to_strip = os.path.dirname(path)
        module_logger.debug("prefix to strip from path {} is {}".format(path, path_to_strip))
        return path_to_strip

    def _get_asset(self):
        from azureml._restclient.assets_client import AssetsClient
        asset_id = self.url[len("aml://asset/"):]
        client = AssetsClient(self.workspace.service_context)
        asset = client.get_asset_by_id(asset_id)
        return asset

    def _get_sas_to_relative_download_path_map(self, asset):
        artifacts_client = ArtifactsClient(self.workspace.service_context)
        sas_to_relative_download_path = OrderedDict()
        for artifact in asset.artifacts:
            module_logger.debug("Asset has artifact {}".format(artifact))
            if artifact.id is not None:
                # download by id
                artifact_id = artifact.id
                module_logger.debug("Artifact has id {}".format(artifact_id))
                (path, sas) = artifacts_client.get_file_by_artifact_id(artifact_id)
                sas_to_relative_download_path[sas] = Model._get_last_path_segment(path)
            else:
                # download by prefix
                prefix_id = artifact.prefix
                module_logger.debug("Artifact has prefix id {}".format(prefix_id))
                paths = artifacts_client.get_files_by_artifact_prefix_id(prefix_id)
                prefix_to_strip = Model._get_strip_prefix(prefix_id)
                for path, sas in paths:
                    path = os.path.relpath(path, prefix_to_strip)  # same as stripping prefix from path per AK
                    sas_to_relative_download_path[sas] = path

        if len(sas_to_relative_download_path) == 0:
            raise WebserviceException("No files to download. Did you upload files?", logger=module_logger)
        module_logger.debug("sas_to_download_path map is {}".format(sas_to_relative_download_path))
        return sas_to_relative_download_path

    def _download_model_files(self, sas_to_relative_download_path, target_dir, exist_ok):
        for sas, path in sas_to_relative_download_path.items():
            target_path = os.path.join(target_dir, path)
            if not exist_ok and os.path.exists(target_path):
                raise WebserviceException("File already exists. To overwrite, set exist_ok to True. "
                                          "{}".format(target_path), logger=module_logger)
            sas_to_relative_download_path[sas] = target_path
            download_file(sas, target_path, stream=True)

        if self.unpack:
            # handle packed model
            tar_path = list(sas_to_relative_download_path.values())[0]
            file_paths = self._handle_packed_model_file(tar_path, target_dir, exist_ok)
        else:
            # handle unpacked model
            file_paths = list(sas_to_relative_download_path.values())
        return file_paths

    def _handle_packed_model_file(self, tar_path, target_dir, exist_ok):
        module_logger.debug("Unpacking model {}".format(tar_path))
        if not os.path.exists(tar_path):
            raise WebserviceException("tar file not found at {}. Paths in scope:\n"
                                      "{}".format(tar_path, "\n".join(Model._paths_in_scope(MODELS_DIR))),
                                      logger=module_logger)
        with tarfile.open(tar_path) as tar:
            if not exist_ok:
                for tar_file_path in tar.getnames():
                    candidate_path = os.path.join(target_dir, tar_file_path)
                    if os.path.exists(candidate_path):
                        raise WebserviceException("File already exists. To overwrite, set exist_ok to True. "
                                                  "{}".format(candidate_path), logger=module_logger)
            tar.extractall(path=target_dir)
            tar_paths = tar.getnames()
        file_paths = [os.path.join(target_dir, os.path.commonprefix(tar_paths))]
        if os.path.exists(tar_path):
            os.remove(tar_path)
        else:
            module_logger.warning("tar_path to unpack is already deleted: {}".format(tar_path))
        return file_paths

    def download(self, target_dir=".", exist_ok=False, exists_ok=None):
        """Download model to target directory of the local file system.

        :param target_dir: The path to a directory in which to download the model. Defaults to "."
        :type target_dir: str
        :param exist_ok: Indicates whether to replace downloaded dir/files if they exist. Defaults to False.
        :type exist_ok: bool
        :param exists_ok: DEPRECATED. Use ``exist_ok``.
        :type exists_ok: bool
        :return: The path to file or folder of the model.
        :rtype: str
        """
        if exists_ok is not None:
            if exist_ok is not None:
                raise WebserviceException("Both exists_ok and exist_ok are set. Please use exist_ok only.",
                                          logger=module_logger)
            module_logger.warning("exists_ok is deprecated. Please use exist_ok")
            exist_ok = exists_ok

        # use model to get asset
        asset = self._get_asset()

        # use asset.artifacts to get files to download
        sas_to_relative_download_path = self._get_sas_to_relative_download_path_map(asset)

        # download files using sas
        file_paths = self._download_model_files(sas_to_relative_download_path, target_dir, exist_ok)
        if len(file_paths) == 0:
            raise WebserviceException("Illegal state. Unpack={}, Paths in target_dir is "
                                      "{}".format(self.unpack, file_paths), logger=module_logger)
        model_path = os.path.commonpath(file_paths)
        return model_path

    @staticmethod
    def _get_model_path_remote(model_name, version, workspace):
        """Retrieve the remote path to the Model.

        :param model_name:
        :type model_name: str
        :param version:
        :type version: int
        :param workspace:
        :type workspace: azureml.core.Workspace
        :return:
        :rtype: str
        """
        if version is not None and not isinstance(version, int):
            raise WebserviceException("version should be an int", logger=module_logger)
        # model -> asset
        from azureml.core.workspace import Workspace
        assert isinstance(workspace, Workspace)

        try:
            model = Model(workspace=workspace, name=model_name, version=version)
        except WebserviceException as e:
            if 'ModelNotFound' in e.message:
                models = Model.list(workspace)
                model_infos = sorted(["{}/{}".format(model.name, model.version) for model in models])
                raise ModelNotFoundException("Model/Version {}/{} not found in workspace. "
                                             "{}".format(model_name, version, model_infos), logger=module_logger)
            else:
                raise WebserviceException(e.message, logger=module_logger)

        # downloading
        version = model.version
        module_logger.debug("Found model version {}".format(version))
        target_dir = os.path.join(MODELS_DIR, model_name, str(version))
        model_path = model.download(target_dir, exist_ok=True)
        if not os.path.exists(model_path):
            items = os.listdir(target_dir)
            raise ModelNotFoundException("Expected model path does not exist: {}. Found items in dir: "
                                         "{}".format(model_path, str(items)), logger=module_logger)
        return model_path

    @staticmethod
    def _register_with_asset(workspace, model_name, asset_id, tags=None, properties=None, description=None,
                             experiment_name=None, run_id=None, datasets=None, model_framework=None,
                             model_framework_version=None, unpack=False, sample_input_dataset=None,
                             sample_output_dataset=None, resource_configuration=None):
        """Register the asset as a Model.

        :param workspace:
        :type workspace: azureml.core.Workspace
        :param model_name:
        :type model_name: str
        :param asset_id:
        :type asset_id: str
        :param tags:
        :type tags: dict[str, str]
        :param properties:
        :type properties: dict[str, str]
        :param description:
        :type description: str
        :param experiment_name:
        :type experiment_name: str
        :param run_id:
        :type run_id: str
        :param datasets:
        :type datasets: builtin.list[(str, azureml.data.abstract_dataset.AbstractDataset)]
        :param model_framework:
        :type model_framework: str
        :param model_framework_version:
        :type model_framework_version: str
        :param unpack:
        :type unpack: bool
        :param sample_input_dataset: Sample input dataset for the registered model
        :type sample_input_dataset: azureml.data.abstract_dataset.AbstractDataset
        :param sample_output_dataset: Sample output dataset for the registered model
        :type sample_output_dataset: azureml.data.abstract_dataset.AbstractDataset
        :param resource_configuration: Resource configuration to run the registered model
        :type resource_configuration: azureml.core.ResourceConfiguration
        :return:
        :rtype: azureml.core.Model
        """
        if model_framework is None and model_framework_version is not None:
            raise WebserviceException("Model framework version cannot be provided without a valid framework",
                                      logger=module_logger)

        headers = {'Content-Type': 'application/json'}
        headers.update(workspace._auth.get_authentication_header())
        params = {'api-version': MMS_WORKSPACE_API_VERSION}
        mms_host = _get_mms_url(workspace)
        model_url = mms_host + '/models'

        json_payload = copy.deepcopy(model_payload_template)
        json_payload['name'] = model_name
        json_payload['url'] = 'aml://asset/{}'.format(asset_id)
        json_payload['experimentName'] = experiment_name
        json_payload['runId'] = run_id
        json_payload['unpack'] = unpack
        if tags:
            try:
                if not isinstance(tags, dict):
                    raise WebserviceException("Tags must be a dict", logger=module_logger)
                tags = json.loads(json.dumps(tags))
            except ValueError:
                raise WebserviceException('Error with JSON serialization for tags, '
                                          'be sure they are properly formatted.', logger=module_logger)
            json_payload['kvTags'] = tags
        if properties:
            try:
                if not isinstance(properties, dict):
                    raise WebserviceException("Properties must be a dict", logger=module_logger)
                properties = json.loads(json.dumps(properties))
            except ValueError:
                raise WebserviceException('Error with JSON serialization for properties, '
                                          'be sure they are properly formatted.', logger=module_logger)
            json_payload['properties'] = properties
        if description:
            json_payload['description'] = description

        if datasets:
            datasets_payload = []
            for dataset_pair in datasets:
                dataset_scenario = dataset_pair[0]
                dataset = dataset_pair[1]
                if type(dataset) is TabularDataset or type(dataset) is FileDataset:
                    saved_id = dataset._ensure_saved(workspace)
                    datasets_payload.append({'name': dataset_scenario, 'id': saved_id})
                elif type(dataset) is Dataset:
                    if not dataset.id:
                        raise WebserviceException('Unable to register Model with provided Dataset with ID "None". '
                                                  'This likely means that the Dataset is unregistered. Please '
                                                  'register the Dataset and try again.', logger=module_logger)
                    datasets_payload.append({'name': dataset_scenario, 'id': dataset.id})
                elif type(dataset) is DatasetSnapshot:
                    datasets_payload.append({'name': dataset_scenario, 'id': DATASET_SNAPSHOT_ID_FORMAT.format(
                        dataset_id=dataset.dataset_id, dataset_snapshot_name=dataset.name)})
                else:
                    raise WebserviceException('Invalid dataset of type {} passed, must be of type Dataset or '
                                              'DatasetSnapshot'.format(type(dataset)), logger=module_logger)

            json_payload['datasets'] = datasets_payload

        if model_framework:
            if model_framework == Model.Framework.TFKERAS:
                module_logger.warning("Tfkeras will be deprecated soon. Use Model.Framework.TENSORFLOW instead.")
            json_payload['framework'] = model_framework
        if model_framework_version:
            json_payload['frameworkVersion'] = model_framework_version

        if sample_input_dataset:
            saved_id = Model._get_dataset_id(workspace, sample_input_dataset, 'sample input dataset')
            json_payload["sampleInputData"] = 'aml://dataset/{}'.format(saved_id)

        if sample_output_dataset:
            saved_id = Model._get_dataset_id(workspace, sample_output_dataset, 'sample output dataset')
            json_payload["sampleOutputData"] = 'aml://dataset/{}'.format(saved_id)

        if resource_configuration:
            resource_configuration._validate_configuration()
            json_payload["resourceRequirements"] = resource_configuration.serialize()

        try:
            resp = ClientBase._execute_func(get_requests_session().post, model_url, params=params, headers=headers,
                                            json=json_payload)
            resp.raise_for_status()
        except requests.ConnectionError:
            raise WebserviceException('Error connecting to {}.'.format(model_url), logger=module_logger)
        except requests.exceptions.HTTPError:
            raise WebserviceException('Received bad response from Model Management Service:\n'
                                      'Response Code: {}\n'
                                      'Headers: {}\n'
                                      'Content: {}'.format(resp.status_code, resp.headers, resp.content),
                                      logger=module_logger)

        content = resp.content
        if isinstance(content, bytes):
            content = content.decode('utf-8')
        model_dict = json.loads(content)
        return Model.deserialize(workspace, model_dict)

    @staticmethod
    def _get_latest_version(versions):
        """Get the latest version of the provided model versions.

        :param versions:
        :type versions: builtin.list[int]
        :return:
        :rtype: int
        """
        if not len(versions) > 0:
            raise WebserviceException("versions is empty", logger=module_logger)
        versions = [int(version) for version in versions]
        version = max(versions)
        return version

    @staticmethod
    def _resolve_to_model_ids(workspace, models, name):
        """Convert a mixed list of model objects, IDs, or local file paths to a list of just model IDs."""
        model_objs = Model._resolve_to_models(workspace, models, name)
        model_ids = [model.id for model in model_objs]

        return model_ids

    @staticmethod
    def _resolve_to_models(workspace, models, name):
        """Convert a mixed list of model objects, IDs, or local file paths to a list of just model objects."""
        model_objs = []
        model_number = 1
        for model in models:
            if type(model) is str:
                try:
                    registered_model = Model(workspace, id=model)
                    model_objs.append(registered_model)
                except WebserviceException as e:
                    if 'ModelNotFound' in e.message:
                        if model.lower().startswith('http'):
                            model_name = '{}.model{}.httpmodel'.format(name[:10], model_number)
                        elif model.lower().startswith('wasb'):
                            model_name = '{}.model{}.wasbmodel'.format(name[:10], model_number)
                        else:
                            model_name = os.path.basename(model.rstrip(os.sep))[:30]
                        model_objs.append(Model.register(workspace, model, model_name, None, None, None))
                    else:
                        raise WebserviceException(e.message, logger=module_logger)
            elif type(model) is Model:
                model_objs.append(model)
            else:
                raise WebserviceException('Models must either be of type azureml.core.Model or a str '
                                          'path to a file or folder.', logger=module_logger)
            model_number += 1

        return model_objs

    @staticmethod
    def list(workspace, name=None, tags=None, properties=None, run_id=None, latest=False):
        """Retrieve a list of all models associated with the provided workspace, with optional filters.

        :param workspace: The workspace object to retrieve models from.
        :type workspace: azureml.core.Workspace
        :param name: If provided, will only return models with the specified name, if any.
        :type name: str
        :param tags: Will filter based on the provided list, by either 'key' or '[key, value]'.
            Ex. ['key', ['key2', 'key2 value']]
        :type tags: builtin.list
        :param properties: Will filter based on the provided list, by either 'key' or '[key, value]'.
            Ex. ['key', ['key2', 'key2 value']]
        :type properties: builtin.list
        :param run_id: Will filter based on the provided run ID.
        :type run_id: str
        :param latest: If true, will only return models with the latest version.
        :type latest: bool
        :return: A list of models, optionally filtered.
        :rtype: builtin.list[azureml.core.Model]
        :raises: :class:`azureml.exceptions.WebserviceException`
        """
        headers = workspace._auth.get_authentication_header()
        params = {'api-version': MMS_WORKSPACE_API_VERSION}
        base_url = _get_mms_url(workspace)
        mms_url = base_url + '/models'

        if name:
            params['name'] = name
        if tags:
            tags_query = ""
            for tag in tags:
                if type(tag) is list:
                    tags_query = tags_query + tag[0] + "=" + tag[1] + ","
                else:
                    tags_query = tags_query + tag + ","
            tags_query = tags_query[:-1]
            params['tags'] = tags_query
        if properties:
            properties_query = ""
            for prop in properties:
                if type(prop) is list:
                    properties_query = properties_query + prop[0] + "=" + prop[1] + ","
                else:
                    properties_query = properties_query + prop + ","
            properties_query = properties_query[:-1]
            params['properties'] = properties_query
        if run_id:
            params['runId'] = run_id

        try:
            resp = ClientBase._execute_func(get_requests_session().get, mms_url, headers=headers, params=params)
            resp.raise_for_status()
        except requests.exceptions.HTTPError:
            raise WebserviceException('Received bad response from Model Management Service:\n'
                                      'Response Code: {}\n'
                                      'Headers: {}\n'
                                      'Content: {}'.format(resp.status_code, resp.headers, resp.content),
                                      logger=module_logger)

        content = resp.content
        if isinstance(content, bytes):
            content = content.decode('utf-8')
        model_payload = json.loads(content)
        paginated_results = get_paginated_results(model_payload, headers)
        models = [Model.deserialize(workspace, model_dict) for model_dict in paginated_results]
        if latest:
            grouped_models = {}
            for model in models:
                if model.name in grouped_models:
                    grouped_models[model.name].append(model)
                else:
                    grouped_models[model.name] = [model]

            return [max(grouped_models[name], key=attrgetter('version')) for name in grouped_models]
        else:
            return models

    def serialize(self):
        """Convert this Model into a json serialized dictionary.

        :return: The json representation of this Model
        :rtype: dict
        """
        created_time = self.created_time.isoformat() if self.created_time else None
        datasets = {}
        for dataset_scenario, dataset_list in self.datasets.items():
            for dataset in dataset_list:
                datasets.setdefault(dataset_scenario, []).append(dataset.__str__())

        sample_input_dataset_id = None
        if self.sample_input_dataset:
            sample_input_dataset_id = self.sample_input_dataset.id

        sample_output_dataset_id = None
        if self.sample_output_dataset:
            sample_output_dataset_id = self.sample_output_dataset.id

        return {'createdTime': created_time,
                'description': self.description,
                'id': self.id,
                'mimeType': self.mime_type,
                'name': self.name,
                'framework': self.model_framework,
                'frameworkVersion': self.model_framework_version,
                'tags': self.tags,
                'properties': self.properties,
                'unpack': self.unpack,
                'url': self.url,
                'version': self.version,
                'experimentName': self.experiment_name,
                'runId': self.run_id,
                'runDetails': self.run.__str__(),
                'datasets': datasets,
                'resourceConfiguration': self.resource_configuration.serialize()
                if self.resource_configuration else None,
                'sampleInputDatasetId': sample_input_dataset_id,
                'sampleOutputDatasetId': sample_output_dataset_id}

    @staticmethod
    def deserialize(workspace, model_payload):
        """Convert a JSON object into a model object.

        Conversion fails if the specified workspace is not the workspace the model is registered with.

        :param workspace: The workspace object the model is registered with.
        :type workspace: azureml.core.Workspace
        :param model_payload: A JSON object to convert to a Model object.
        :type model_payload: dict
        :return: The Model representation of the provided JSON object.
        :rtype: azureml.core.Model
        """
        Model._validate_get_payload(model_payload)
        model = Model(None)
        model._initialize(workspace, model_payload)
        return model

    def update(self, tags=None, description=None, sample_input_dataset=None, sample_output_dataset=None,
               resource_configuration=None):
        """Perform an in-place update of the model.

        Existing values of specified parameters are replaced.

        :param tags: A dictionary of tags to update the model with. These tags replace existing tags
            for the model.
        :type tags: dict({str : str})
        :param description: The new description to use for the model. This name replaces the existing name.
        :type description: str
        :param sample_input_dataset: The sample input dataset to use for the registered model. This sample
            input dataset replaces the existing dataset.
        :type sample_input_dataset: azureml.data.abstract_dataset.AbstractDataset
        :param sample_output_dataset: The sample output dataset to use for the registered model. This sample
            output dataset replaces the existing dataset.
        :type sample_output_dataset: azureml.data.abstract_dataset.AbstractDataset
        :param resource_configuration: The resource configuration to use to run the registered model.
        :type resource_configuration: azureml.core.resource_configuration.ResourceConfiguration
        :raises: :class:`azureml.exceptions.WebserviceException`
        """
        headers = {'Content-Type': 'application/json-patch+json'}
        headers.update(self._auth.get_authentication_header())
        params = {'api-version': MMS_WORKSPACE_API_VERSION}

        patch_list = []
        if tags:
            patch_list.append({'op': 'replace', 'path': '/kvTags', 'value': tags})
        if description:
            patch_list.append({'op': 'replace', 'path': '/description', 'value': description})

        if sample_input_dataset:
            saved_id = Model._get_dataset_id(self.workspace, sample_input_dataset, 'sample input dataset')
            patch_list.append(
                {'op': 'replace', 'path': '/sampleInputData', 'value': 'aml://dataset/{}'.format(saved_id)})

        if sample_output_dataset:
            saved_id = Model._get_dataset_id(self.workspace, sample_output_dataset, 'sample output dataset')
            patch_list.append(
                {'op': 'replace', 'path': '/sampleOutputData', 'value': 'aml://dataset/{}'.format(saved_id)})

        if resource_configuration:
            resource_configuration._validate_configuration()
            patch_list.append(
                {'op': 'replace', 'path': '/resourceRequirements', 'value': resource_configuration.serialize()})

        resp = ClientBase._execute_func(get_requests_session().patch, self._mms_endpoint, headers=headers,
                                        params=params, json=patch_list, timeout=MMS_SYNC_TIMEOUT_SECONDS)

        if resp.status_code >= 400:
            raise WebserviceException('Received bad response from Model Management Service:\n'
                                      'Response Code: {}\n'
                                      'Headers: {}\n'
                                      'Content: {}'.format(resp.status_code, resp.headers, resp.content),
                                      logger=module_logger)
        else:
            if tags:
                self.tags = tags
            if description:
                self.description = description
            if resource_configuration:
                self.resource_configuration = resource_configuration
            if sample_input_dataset:
                self.sample_input_dataset = sample_input_dataset
            if sample_output_dataset:
                self.sample_output_dataset = sample_output_dataset

    def update_tags_properties(self, add_tags=None, remove_tags=None, add_properties=None):
        """Perform an update of the tags and properties of the model.

        :param add_tags: A dictionary of tags to add.
        :type add_tags: dict({str : str})
        :param remove_tags: A list of tag names to remove.
        :type remove_tags: builtin.list[str]
        :param add_properties: A dictionary of properties to add.
        :type add_properties: dict({str : str})
        :raises: :class:`azureml.exceptions.WebserviceException`
        """
        check_duplicate_properties(self.properties, add_properties)

        headers = {'Content-Type': 'application/json-patch+json'}
        headers.update(self._auth.get_authentication_header())
        params = {'api-version': MMS_WORKSPACE_API_VERSION}

        patch_list = []

        # handle tags update, if a tag is in both add_tags and remove_tags,
        # the expected behavior is undefined. So it doesn't matter how we solve such confliction.
        tag_update = False

        # handle add_tags
        if add_tags is not None:
            tag_update = True
            if self.tags is None:
                self.tags = copy.deepcopy(add_tags)
            else:
                for key in add_tags:
                    if key in self.tags:
                        print("Replacing tag {} -> {} with {} -> {}".format(key, self.tags[key],
                                                                            key, add_tags[key]))
                    self.tags[key] = add_tags[key]

        # handle remove_tags
        if remove_tags is not None:
            if self.tags is None:
                print('Model has no tags to remove.')
            else:
                tag_update = True
                if not isinstance(remove_tags, list):
                    remove_tags = [remove_tags]
                for key in remove_tags:
                    if key in self.tags:
                        del self.tags[key]
                    else:
                        print('Tag with key {} not found.'.format(key))

        # add add "tag replace" op when there's tag update
        if tag_update:
            patch_list.append({'op': 'replace', 'path': '/kvTags', 'value': self.tags})

        # handle add_properties
        if add_properties is not None:
            if self.properties is None:
                self.properties = copy.deepcopy(add_properties)
            else:
                for key in add_properties:
                    self.properties[key] = add_properties[key]

            patch_list.append({'op': 'add', 'path': '/properties', 'value': self.properties})

        # only call MMS REST API where patch_list is not empty
        if not patch_list:
            return

        resp = ClientBase._execute_func(get_requests_session().patch, self._mms_endpoint, headers=headers,
                                        params=params, json=patch_list, timeout=MMS_SYNC_TIMEOUT_SECONDS)

        if resp.status_code >= 400:
            raise WebserviceException('Received bad response from Model Management Service:\n'
                                      'Response Code: {}\n'
                                      'Headers: {}\n'
                                      'Content: {}'.format(resp.status_code, resp.headers, resp.content),
                                      logger=module_logger)

    def add_tags(self, tags):
        """Add key value pairs to the tags dictionary of this model.

        :param tags: The dictionary of tags to add.
        :type tags: dict({str : str})
        :raises: :class:`azureml.exceptions.WebserviceException`
        """
        self.update_tags_properties(add_tags=tags)
        print('Model tag add operation complete.')

    def remove_tags(self, tags):
        """Remove the specified keys from tags dictionary of this model.

        :param tags: The list of keys to remove
        :type tags: builtin.list[str]
        """
        self.update_tags_properties(remove_tags=tags)
        print('Model tag remove operation complete.')

    def add_properties(self, properties):
        """Add key value pairs to properties dictionary of this model.

        :param properties: The dictionary of properties to add.
        :type properties: dict({str : str})
        """
        self.update_tags_properties(add_properties=properties)
        print('Model properties add operation complete.')

    def add_dataset_references(self, datasets):
        """Associate the provided datasets with this Model.

        :param datasets: A list of tuples representing a pairing of dataset purpose to Dataset object.
        :type datasets: builtin.list[tuple({str : (azureml.core.Dataset or
            azureml.data.dataset_snapshot.DatasetSnapshot)})]
        :raises: azureml.exceptions.WebserviceException
        """
        headers = {'Content-Type': 'application/json-patch+json'}
        headers.update(self._auth.get_authentication_header())
        params = {'api-version': MMS_WORKSPACE_API_VERSION}

        dataset_dicts = []
        for dataset_pair in datasets:
            dataset_scenario = dataset_pair[0]
            dataset = dataset_pair[1]
            if type(dataset) is Dataset:
                dataset_dicts.append({'name': dataset_scenario, 'id': dataset.id})
            elif type(dataset) is DatasetSnapshot:
                dataset_dicts.append({'name': dataset_scenario, 'id': DATASET_SNAPSHOT_ID_FORMAT.format(
                    dataset_id=dataset.dataset_id, dataset_snapshot_name=dataset.name)})
            else:
                raise WebserviceException('Invalid dataset of type {} passed, must be of type Dataset or '
                                          'DatasetSnapshot'.format(type(dataset)), logger=module_logger)

        patch_list = [{'op': 'add', 'path': '/datasets', 'value': dataset_dicts}]

        resp = ClientBase._execute_func(get_requests_session().patch, self._mms_endpoint, headers=headers,
                                        params=params, json=patch_list, timeout=MMS_SYNC_TIMEOUT_SECONDS)

        if resp.status_code >= 400:
            raise WebserviceException('Received bad response from Model Management Service:\n'
                                      'Response Code: {}\n'
                                      'Headers: {}\n'
                                      'Content: {}'.format(resp.status_code, resp.headers, resp.content),
                                      logger=module_logger)

        for dataset_pair in datasets:
            dataset_scenario = dataset_pair[0]
            dataset = dataset_pair[1]

            self.datasets.setdefault(dataset_scenario, []).append(dataset)

    def delete(self):
        """Delete this model from its associated workspace.

        :raises: azureml.exceptions.WebserviceException
        """
        headers = self._auth.get_authentication_header()
        params = {'api-version': MMS_WORKSPACE_API_VERSION}

        resp = ClientBase._execute_func(get_requests_session().delete, self._mms_endpoint, headers=headers,
                                        params=params)

        if resp.status_code >= 400:
            if resp.status_code == 412 and "DeletionRequired" in resp.content:
                raise WebserviceException('The model cannot be deleted because it is currently being used in one or '
                                          'more images. To know what images contain the model, run '
                                          '"Image.list(<workspace>, model_id={})"'.format(self.id),
                                          logger=module_logger)

            raise WebserviceException('Received bad response from Model Management Service:\n'
                                      'Response Code: {}\n'
                                      'Headers: {}\n'
                                      'Content: {}'.format(resp.status_code, resp.headers, resp.content),
                                      logger=module_logger)

    @staticmethod
    def _validate_get_payload(payload):
        """Validate the returned model payload.

        :param payload:
        :type payload: dict
        :return:
        :rtype: None
        """
        for payload_key in Model._expected_payload_keys:
            if payload_key not in payload:
                raise WebserviceException('Invalid model payload, missing {} for model:\n'
                                          '{}'.format(payload_key, payload), logger=module_logger)

    @staticmethod
    def deploy(workspace, name, models, inference_config=None, deployment_config=None, deployment_target=None,
               overwrite=False):
        """Deploy a Webservice from zero or more model objects.

        This function is similar to the ``deploy`` function of the :class:`azureml.core.Webservice` class, but does
        not register the models. Use this function if you have model objects that are
        already registered.

        :param workspace: A Workspace object to associate the Webservice with.
        :type workspace: azureml.core.Workspace
        :param name: The name to give the deployed service. Must be unique to the workspace, only consist of lowercase
            letters, numbers, or dashes, start with a letter, and be between 3 and 32 characters long.
        :type name: str
        :param models: A list of model objects. Can be an empty list.
        :type models: builtin.list[azureml.core.Model]
        :param inference_config: An InferenceConfig object used to determine required model properties.
        :type inference_config: azureml.core.model.InferenceConfig
        :param deployment_config: A WebserviceDeploymentConfiguration used to configure the webservice. If one is not
            provided, an empty configuration object will be used based on the desired target.
        :type deployment_config: azureml.core.webservice.webservice.WebserviceDeploymentConfiguration
        :param deployment_target: A :class:`azureml.core.ComputeTarget` to deploy the Webservice to.
            As Azure Container Instances has no associated :class:`azureml.core.ComputeTarget`, leave
            this parameter as None to deploy to Azure Container Instances.
        :type deployment_target: azureml.core.ComputeTarget
        :param overwrite: Indicates whether to overwrite the existing service if a service with the
            specified name already exists.
        :type overwrite: bool
        :return: A Webservice object corresponding to the deployed webservice.
        :rtype: azureml.core.Webservice
        :raises: :class:`azureml.exceptions.WebserviceException`
        """
        from azureml.core.webservice import Webservice
        from azureml.core.webservice.local import LocalWebserviceDeploymentConfiguration

        webservice_name_validation(name)
        Webservice._check_for_existing_webservice(workspace, name, overwrite)

        # Local webservice.
        if deployment_config and isinstance(deployment_config, LocalWebserviceDeploymentConfiguration):
            return deployment_config._webservice_type._deploy(workspace, name, models,
                                                              inference_config=inference_config,
                                                              deployment_config=deployment_config)

        # IotWebservice does not support environment-style deployment,
        # so make sure we don't deploy IotWebservice with environment;
        # We only support ACI, AKS, AKS endpoint, and MIR for now.
        from azureml._model_management._constants import IOT_WEBSERVICE_TYPE

        # No-code-deploy webservice.
        if inference_config is None:
            if deployment_config and deployment_config._webservice_type._webservice_type == IOT_WEBSERVICE_TYPE:
                raise WebserviceException('IoT Webservices must be deployed with an InferenceConfig.',
                                          logger=module_logger)

            return Model._deploy_no_code(workspace, name, models, deployment_config, deployment_target, overwrite)

        # Environment-based webservice.
        if not deployment_config or deployment_config._webservice_type._webservice_type != IOT_WEBSERVICE_TYPE:
            inference_config, use_env_path = convert_parts_to_environment(name, inference_config)
        else:
            use_env_path = inference_config.environment is not None

        if use_env_path:
            return Model._deploy_with_environment(workspace, name, models, inference_config, deployment_config,
                                                  deployment_target, overwrite)

        # ContainerImage-based webservice.
        if deployment_config._webservice_type._webservice_type in \
           (MIR_WEBSERVICE_TYPE, AKS_ENDPOINT_TYPE, MIR_SINGLE_MODEL_WEBSERVICE_TYPE):
            raise WebserviceException('MIR Webservices and AKS Endpoint must be deployed with an environment',
                                      logger=module_logger)

        return Webservice.deploy_from_model(workspace, name, models, inference_config, deployment_config,
                                            deployment_target, overwrite)

    @staticmethod
    def package(workspace, models, inference_config=None, generate_dockerfile=False):
        """Create a model package in the form of a Docker image or Dockerfile build context.

        :param workspace: The workspace in which to create the package.
        :type workspace: azureml.core.Workspace
        :param models: A list of Model objects to include in the package. Can be an empty list.
        :type models: builtin.list[azureml.core.Model]
        :param inference_config: An InferenceConfig object to configure the operation of the models.
            This must include an Environment object.
        :type inference_config: azureml.core.model.InferenceConfig
        :param generate_dockerfile: Whether to create a Dockerfile that can be run locally
            instead of building an image.
        :type generate_dockerfile: bool
        :return: A ModelPackage object.
        :rtype: azureml.core.model.ModelPackage
        """
        models = Model._resolve_to_models(workspace, models, 'package.{}'.format(uuid.uuid4()))

        if inference_config is not None:
            inference_config, use_env_path = convert_parts_to_environment('package', inference_config)

            if not use_env_path:
                raise WebserviceException('Error, model packaging requires an InferenceConfig containing '
                                          'an Environment object.')

            model_ids = [model.id for model in models]

            environment = inference_config.environment
            image_request = inference_config._build_environment_image_request(workspace, model_ids)
        else:
            environment = None
            image_request = build_and_validate_no_code_environment_image_request(models)

        package_request = {
            'imageRequest': image_request,
            'packageType': 'DockerBuildContext' if generate_dockerfile else 'DockerImage',
        }

        operation_id = submit_mms_operation(workspace, 'POST', '/packages', package_request)

        return ModelPackage(workspace, operation_id, environment)

    @staticmethod
    def profile(workspace, profile_name, models, inference_config, input_data):
        """Profiles this model to get resource configuration recommendations.

        :param workspace: A Workspace object in which to profile the model
        :type workspace: azureml.core.Workspace
        :param profile_name: The name of the profiling run
        :type profile_name: str
        :param models: A list of model objects. Can be an empty list.
        :type models: builtin.list[azureml.core.Model]
        :param inference_config: An InferenceConfig object used to determine required model properties.
        :type inference_config: azureml.core.model.InferenceConfig
        :param input_data: The input data for profiling
        :type input_data: str
        :rtype: azureml.core.profile.ModelProfile
        :raises: azureml.exceptions.WebserviceException
        """
        from azureml.core.image import Image
        image = Image.create(workspace, profile_name, models, inference_config)
        image.wait_for_creation(True)
        if image.creation_state != 'Succeeded':
            raise WebserviceException('Error occurred creating model package {} for profiling. More information can '
                                      'be found here: {}, generated DockerFile can be found here: {}'
                                      .format(image.id, image.image_build_log_uri, image.generated_dockerfile_uri),
                                      logger=module_logger)

        headers = {'Content-Type': 'application/json'}
        headers.update(workspace._auth.get_authentication_header())
        params = {'api-version': MMS_WORKSPACE_API_VERSION}
        base_endpoint = _get_mms_url(workspace)
        profile_url = '{0}/images/{1}/profiles'.format(base_endpoint, image.id)

        json_payload = inference_config.build_profile_payload(profile_name, input_data)

        module_logger.info('Profiling model')
        resp = ClientBase._execute_func(get_requests_session().post, profile_url, params=params, headers=headers,
                                        json=json_payload)
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError:
            raise WebserviceException('Received bad response from Model Management Service:\n'
                                      'Response Code: {}\n'
                                      'Headers: {}\n'
                                      'Content: {}'.format(resp.status_code, resp.headers, resp.content),
                                      logger=module_logger)
        if resp.status_code >= 400:
            raise WebserviceException('Error occurred profiling model:\n'
                                      'Response Code: {}\n'
                                      'Headers: {}\n'
                                      'Content: {}'.format(resp.status_code, resp.headers, resp.content),
                                      logger=module_logger)

        if 'Operation-Location' in resp.headers:
            operation_location = resp.headers['Operation-Location']
        else:
            raise WebserviceException('Missing response header key: Operation-Location', logger=module_logger)

        create_operation_status_id = operation_location.split('/')[-1]
        operation_url = base_endpoint + '/operations/{}'.format(create_operation_status_id)
        operation_headers = workspace._auth.get_authentication_header()

        operation_resp = ClientBase._execute_func(get_requests_session().get, operation_url, params=params,
                                                  headers=operation_headers, timeout=MMS_SYNC_TIMEOUT_SECONDS)
        try:
            operation_resp.raise_for_status()
        except requests.Timeout:
            raise WebserviceException('Error, request to {} timed out.'.format(operation_url), logger=module_logger)
        except requests.exceptions.HTTPError:
            raise WebserviceException('Received bad response from Model Management Service:\n'
                                      'Response Code: {}\n'
                                      'Headers: {}\n'
                                      'Content: {}'.format(operation_resp.status_code,
                                                           operation_resp.headers,
                                                           operation_resp.content), logger=module_logger)

        content = operation_resp.content
        if isinstance(content, bytes):
            content = content.decode('utf-8')
        operation_content = json.loads(content)
        if 'resourceLocation' in operation_content:
            profiling_name = operation_content['resourceLocation'].split('/')[-1]
        else:
            raise WebserviceException('Invalid operation payload, missing resourceLocation:\n'
                                      '{}'.format(operation_content), logger=module_logger)

        profile = ModelProfile(workspace, image.id, profiling_name)
        profile._operation_endpoint = operation_url
        return profile

    @staticmethod
    def _deploy_no_code(workspace, name, models, deployment_config, deployment_target, overwrite):
        """Deploy the model without an explicit environment object or scoring code.

        :param workspace:
        :type workspace: azureml.core.Workspace
        :param name:
        :type name: str
        :param models:
        :type models: builtin.list[azureml.core.Model]
        :param deployment_config:
        :type deployment_config: azureml.core.webservice.webservice.WebserviceDeploymentConfiguration
        :param deployment_target:
        :type deployment_target: azureml.core.ComputeTarget
        :return:
        :rtype: azureml.core.Webservice
        """
        environment_image_request = build_and_validate_no_code_environment_image_request(models)

        return Model._deploy_with_environment_image_request(workspace, name, environment_image_request,
                                                            deployment_config, deployment_target, overwrite)

    @staticmethod
    def _deploy_with_environment(workspace, name, models, inference_config, deployment_config, deployment_target,
                                 overwrite):
        """Deploy the model using an environment object.

        :param workspace:
        :type workspace: azureml.core.Workspace
        :param name:
        :type name: str
        :param models:
        :type models: :class:`list[azureml.core.Model]`
        :param inference_config:
        :type inference_config: azureml.core.model.InferenceConfig
        :param deployment_config:
        :type deployment_config: azureml.core.webservice.webservice.WebserviceDeploymentConfiguration
        :param deployment_target:
        :type deployment_target: azureml.core.ComputeTarget
        :param overwrite: Overwrite the existing service if service with name already exists.
        :type overwrite: bool
        :return:
        :rtype: azureml.core.Webservice
        """
        environment_image_request = \
            inference_config._build_environment_image_request(workspace, [model.id for model in models])

        return Model._deploy_with_environment_image_request(workspace, name, environment_image_request,
                                                            deployment_config, deployment_target, overwrite)

    @staticmethod
    def _deploy_with_environment_image_request(workspace, name, environment_image_request, deployment_config,
                                               deployment_target, overwrite):
        """Deploy a service from an environment image request.

        :param workspace:
        :type workspace: azureml.core.Workspace
        :param name:
        :type name: str
        :param environment_image_request:
        :type environment_image_request: dict
        :param models:
        :type models: builtin.list[azureml.core.Model]
        :param inference_config:
        :type inference_config: azureml.core.model.InferenceConfig
        :param deployment_config:
        :type deployment_config: azureml.core.webservice.webservice.WebserviceDeploymentConfiguration
        :param deployment_target:
        :type deployment_target: azureml.core.ComputeTarget
        :return:
        :rtype: azureml.core.Webservice
        """
        from azureml.core.webservice import Webservice, AciWebservice, AksWebservice

        if not deployment_target and not deployment_config:
            deployment_config = AciWebservice.deploy_configuration()
        elif not deployment_config:

            # TODO: after AKSWebservice deprecation is completed, replace this with AksEndpoint config
            if type(deployment_target) is AksCompute:
                deployment_config = AksWebservice.deploy_configuration()
            else:
                raise WebserviceException("Must provide deployment configuration when not deploying to AKS or ACI")

        webservice_payload = deployment_config._build_create_payload(name, environment_image_request,
                                                                     overwrite=overwrite)
        webservice_class = deployment_config._webservice_type
        if 'computeName' in webservice_payload and deployment_target is not None:
            webservice_payload['computeName'] = deployment_target.name

        return Webservice._deploy_webservice(workspace, name, webservice_payload, webservice_class)

    def get_sas_urls(self):
        """Return a dictionary of key value pairs containing filenames and corresponding SAS URLs.

        :return: Dictionary of K,V pairs containing filenames and corresponding SAS URLs
        :rtype: dict
        """
        asset = self._get_asset()
        sas_to_artifact_dict = self._get_sas_to_relative_download_path_map(asset)
        name_to_url_dict = {v: k for k, v in sas_to_artifact_dict.items()}
        return name_to_url_dict

    class Framework(object):
        """Represents constants for supported framework types.

        Framework constants simplify deployment for some popular frameworks. Use the framework constants
        in the :class:`azureml.core.model.Model` class when registering or searching for models.
        """

        CUSTOM = "Custom"
        TENSORFLOW = "TensorFlow"
        SCIKITLEARN = "ScikitLearn"
        ONNX = "Onnx"
        TFKERAS = "TfKeras"

    _SUPPORTED_FRAMEWORKS_FOR_NO_CODE_DEPLOY = [
        Framework.ONNX,
        Framework.SCIKITLEARN,
        Framework.TENSORFLOW
    ]


class InferenceConfig(object):
    """Represents configuration settings for a custom environment used for deployment.

    Inference configuration is an input parameter for :class:`azureml.core.model.Model` deployment-related
    actions:

    * :meth:`azureml.core.model.Model.deploy`
    * :meth:`azureml.core.model.Model.profile`
    * :meth:`azureml.core.model.Model.package`

    .. remarks::

        The following sample shows how to create an InferenceConfig object and use it to deploy a model.

        .. code-block:: python

            from azureml.core import Webservice
            from azureml.core.model import InferenceConfig
            from azureml.exceptions import WebserviceException

            service_name = 'my-custom-env-service'

            # Remove any existing service under the same name.
            try:
                Webservice(ws, service_name).delete()
            except WebserviceException:
                pass

            inference_config = InferenceConfig(entry_script='score.py',
                                               source_directory='.',
                                               environment=environment)

            service = Model.deploy(ws, service_name, [model], inference_config)
            service.wait_for_deployment(show_output=True)

        Full sample is available from
        https://github.com/Azure/MachineLearningNotebooks/blob/master/how-to-use-azureml/deployment/deploy-to-cloud/model-register-and-deploy.ipynb


    :param entry_script: The path to a local file that contains the code to run for the image.
    :type entry_script: str
    :param runtime: The runtime to use for the image. Current supported runtimes are 'spark-py' and 'python'.
    :type runtime: str
    :param conda_file: The path to a local file containing a conda environment definition to use for the image.
    :type conda_file: str
    :param extra_docker_file_steps: The path to a local file containing additional Docker steps to run when
        setting up the image.
    :type extra_docker_file_steps: str
    :param source_directory: The path to the folder that contains all files to create the image.
    :type source_directory: str
    :param enable_gpu: Indicates whether to enable GPU support in the image. The GPU image must be used on
        Microsoft Azure Services such as Azure Container Instances, Azure Machine Learning Compute,
        Azure Virtual Machines, and Azure Kubernetes Service.
    :type enable_gpu: bool
    :param description: A description to give this image.
    :type description: str
    :param base_image: A custom image to be used as base image. If no base image is given then the base image
        will be used based off of given runtime parameter.
    :type base_image: str
    :param base_image_registry: The image registry that contains the base image.
    :type base_image_registry: azureml.core.container_registry.ContainerRegistry
    :param cuda_version: The version of CUDA to install for images that need GPU support. The GPU image must be
        used on Microsoft Azure Services such as Azure Container Instances, Azure Machine Learning Compute,
        Azure Virtual Machines, and Azure Kubernetes Service. Supported versions are 9.0, 9.1, and 10.0.
        If ``enable_gpu`` is set, this defaults to '9.1'.
    :type cuda_version: str
    :param environment: An environment object to use for the deployment. The environment doesn't have to be
        registered.

        Provide either this parameter, or the other parameters, but not both. The individual parameters will
        NOT serve as an override for the environment object. Exceptions include ``entry_script``,
        ``source_directory``, and ``description``.
    :type environment: azureml.core.Environment
    """

    def __init__(self, entry_script, runtime=None, conda_file=None, extra_docker_file_steps=None,
                 source_directory=None, enable_gpu=None, description=None,
                 base_image=None, base_image_registry=None, cuda_version=None, environment=None):
        """Initialize the config object.

        :param entry_script: The path to a local file that contains the code to run for the image.
        :type entry_script: str
        :param runtime: The runtime to use for the image. Current supported runtimes are 'spark-py' and 'python'.
        :type runtime: str
        :param conda_file: The path to a local file containing a conda environment definition to use for the image.
        :type conda_file: str
        :param extra_docker_file_steps: The path to a local file containing additional Docker steps to run when
            setting up image.
        :type extra_docker_file_steps: str
        :param source_directory: The path to the folder that contains all files to create the image.
        :type source_directory: str
        :param enable_gpu: Indicates whether to enable GPU support in the image. The GPU image must be used on
            Microsoft Azure Services such as Azure Container Instances, Azure Machine Learning Compute,
            Azure Virtual Machines, and Azure Kubernetes Service. Defaults to False.
        :type enable_gpu: bool
        :param description: A description to give this image.
        :type description: str
        :param base_image: A custom image to be used as base image. If no base image is given then the base image
            will be used based off of given runtime parameter.
        :type base_image: str
        :param base_image_registry: The image registry that contains the base image.
        :type base_image_registry: azureml.core.container_registry.ContainerRegistry
        :param cuda_version: The Version of CUDA to install for images that need GPU support. The GPU image must be
            used on Microsoft Azure Services such as Azure Container Instances, Azure Machine Learning Compute,
            Azure Virtual Machines, and Azure Kubernetes Service. Supported versions are 9.0, 9.1, and 10.0.
            If ``enable_gpu`` is set, this defaults to '9.1'.
        :type cuda_version: str
        :type cuda_version: str
        :param environment: An environment object to use for the deployment. The environment doesn't have to be
            registered.

            Provide either this parameter, or the other parameters, but not both. The individual parameters will
            NOT serve as an override for the environment object. Exceptions include ``entry_script``,
        ``source_directory``, and ``description``.
        :type environment: azureml.core.Environment
        :raises: azureml.exceptions.WebserviceException
        """
        self.entry_script = entry_script
        self.runtime = runtime
        self.conda_file = conda_file
        self.extra_docker_file_steps = extra_docker_file_steps
        self.source_directory = source_directory
        self.enable_gpu = enable_gpu
        self.cuda_version = cuda_version
        self.description = description
        self.base_image = base_image
        self.base_image_registry = base_image_registry or ContainerRegistry()
        self.environment = environment

        self.validate_configuration()

    def __repr__(self):
        """Return the string representation of the InferenceConfig object.

        :return: String representation of the InferenceConfig object
        :rtype: str
        """
        return "{}(entry_script={}, runtime={}, conda_file={}, extra_docker_file_steps={}, source_directory={}, " \
               "enable_gpu={}, base_image={}, base_image_registry={})".format(self.__class__.__name__,
                                                                              self.entry_script, self.runtime,
                                                                              self.conda_file,
                                                                              self.extra_docker_file_steps,
                                                                              self.source_directory, self.enable_gpu,
                                                                              self.base_image,
                                                                              self.base_image_registry)

    def _convert_to_image_conf_for_local(self):
        """ONLY FOR LOCAL DEPLOYMENT USE.

        Return an image configuration class using the attributes of this Inference config class.

        :return: ContainerImage configuration class
        :rtype: azureml.core.image.container.ContainerImageConfig
        """
        dependencies = []
        if self.source_directory:
            dependencies = [self.source_directory] if self.source_directory else []

        from azureml.core.image.container import ContainerImageConfig
        return ContainerImageConfig(joinPath(self.source_directory, self.entry_script),
                                    self.runtime,
                                    joinPath(self.source_directory, self.conda_file),
                                    joinPath(self.source_directory, self.extra_docker_file_steps),
                                    None, dependencies, self.enable_gpu, None, None, self.description,
                                    self.base_image, self.base_image_registry, True, self.cuda_version)

    def validate_configuration(self):
        """Check that the specified configuration values are valid.

        Raises a :class:`azureml.exceptions.WebserviceException` if validation fails.

        :raises: :class:`azureml.exceptions.WebserviceException`
        """
        if not self.entry_script:
            raise WebserviceException('Error, need to specify entry_script.')

        if self.environment:
            if self.runtime or self.conda_file or self.extra_docker_file_steps or \
                    self.enable_gpu or self.cuda_version or self.base_image:
                raise WebserviceException('Error, unable to provide runtime, conda_file, extra_docker_file_steps, '
                                          'enable_gpu, cuda_version, or base_image along with an environment object.')

            if 'azureml-defaults' not in self.environment.python.conda_dependencies.serialize_to_string():
                module_logger.warning('Warning, azureml-defaults not detected in provided environment pip '
                                      'dependencies. The azureml-defaults package contains requirements for the '
                                      'inference stack to run, and should be included.')
            if self.environment.docker.base_dockerfile and self.environment.docker.base_image:
                raise WebserviceException('Error, only one of base_dockerfile or base_image should be provided to the '
                                          'environment.docker object.')
            if not self.environment.inferencing_stack_version and \
                    (self.environment.docker.base_dockerfile or
                     not self.environment.docker.base_image.startswith('mcr.microsoft.com/azureml/base')):
                module_logger.warning('Warning, custom base image or base dockerfile detected without a specified '
                                      '`inferencing_stack_version`. Please set '
                                      'environment.inferencing_stack_version=\'latest\'')

        if self.source_directory:
            self.source_directory = os.path.realpath(self.source_directory)
            validate_path_exists_or_throw(self.source_directory, "source directory")

        validate_path_exists_or_throw(joinPath(self.source_directory, self.entry_script),
                                      'entry_script',
                                      extra_message='entry_script should be path relative to '
                                                    ' current working directory')

        script_name, script_extension = os.path.splitext(os.path.basename(self.entry_script))
        if script_extension != '.py':
            raise WebserviceException('Invalid driver type. Currently only Python drivers are supported.',
                                      logger=module_logger)
        validate_entry_script_name(script_name)

        if self.runtime and (self.runtime.lower() not in SUPPORTED_RUNTIMES.keys()):
            runtimes = '|'.join(x for x in SUPPORTED_RUNTIMES.keys() if x not in UNDOCUMENTED_RUNTIMES)
            raise WebserviceException('Provided runtime not supported. '
                                      'Possible runtimes are: {}'.format(runtimes),
                                      logger=module_logger)

        if self.cuda_version is not None:
            if self.cuda_version.lower() not in SUPPORTED_CUDA_VERSIONS:
                cuda_versions = '|'.join(SUPPORTED_CUDA_VERSIONS)
                raise WebserviceException('Provided cuda_version not supported. '
                                          'Possible cuda_versions are: {}'.format(cuda_versions),
                                          logger=module_logger)

        if self.conda_file:
            validate_path_exists_or_throw(joinPath(self.source_directory, self.conda_file), "Conda file")

        if self.extra_docker_file_steps:
            validate_path_exists_or_throw(joinPath(self.source_directory, self.extra_docker_file_steps),
                                          "extra docker file steps")

    def build_create_payload(self, workspace, name, model_ids):
        """Build the creation payload for the Container image.

        :param workspace: The workspace object to create the image in.
        :type workspace: azureml.core.Workspace
        :param name: The name of the image.
        :type name: str
        :param model_ids: A list of model IDs to package into the image.
        :type model_ids: builtin.list[str]
        :return: The container image creation payload.
        :rtype: dict
        :raises: :class:`azureml.exceptions.WebserviceException`
        """
        from azureml._model_management._util import image_payload_template
        json_payload = copy.deepcopy(image_payload_template)
        json_payload['name'] = name
        json_payload['imageFlavor'] = WEBAPI_IMAGE_FLAVOR
        json_payload['description'] = self.description
        json_payload['targetRuntime']['runtimeType'] = SUPPORTED_RUNTIMES[self.runtime.lower()]
        json_payload['targetRuntime']['targetArchitecture'] = ARCHITECTURE_AMD64

        if self.enable_gpu:
            json_payload['targetRuntime']['properties']['installCuda'] = self.enable_gpu
        if self.cuda_version:
            json_payload['targetRuntime']['properties']['cudaVersion'] = self.cuda_version
        requirements = add_sdk_to_requirements()
        (json_payload['targetRuntime']['properties']['pipRequirements'], _) = \
            upload_dependency(workspace, requirements)
        if self.conda_file:
            self.conda_file = self.conda_file.rstrip(os.sep)
            self.conda_file = joinPath(self.source_directory, self.conda_file)
            (json_payload['targetRuntime']['properties']['condaEnvFile'], _) = \
                upload_dependency(workspace, self.conda_file)
        if self.extra_docker_file_steps:
            self.extra_docker_file_steps = self.extra_docker_file_steps.rstrip(os.sep)
            self.extra_docker_file_steps = joinPath(self.source_directory, self.extra_docker_file_steps)
            (json_payload['dockerFileUri'], _) = upload_dependency(workspace, self.extra_docker_file_steps)

        if model_ids:
            json_payload['modelIds'] = model_ids

        self._handle_assets(workspace, json_payload)

        self._add_base_image_to_payload(json_payload)

        return json_payload

    def _build_environment_image_request(self, workspace, model_ids):
        """Build the json payload for the environment image.

        :param workspace:
        :type workspace: azureml.core.Workspace
        :param model_ids:
        :type model_ids: :class:`list[str]`
        :return:
        :rtype: dict
        """
        from azureml._model_management._util import environment_image_payload_template
        json_payload = copy.deepcopy(environment_image_payload_template)

        if model_ids:
            json_payload['modelIds'] = model_ids

        self._handle_assets(workspace, json_payload)

        if self.environment:
            json_payload['environment'] = Environment._serialize_to_dict(self.environment)
        else:
            del json_payload['environment']

        return json_payload

    def _handle_assets(self, workspace, json_payload):
        """Handle uploading the necessary assets for the inference config and add them to the provided payload.

        :param workspace:
        :type workspace: azureml.core.Workspace
        :param json_payload:
        :type json_payload: dict
        """
        self.entry_script = self.entry_script.rstrip(os.sep)

        driver_mime_type = 'application/x-python'
        scoring_base_name = ''
        script_location = os.path.basename(self.entry_script)

        if self.source_directory:
            scoring_base_name = os.path.basename(self.source_directory)
            script_location = self.entry_script

        wrapped_execution_script = wrap_execution_script_with_source_directory(scoring_base_name,
                                                                               script_location,
                                                                               True)

        (driver_package_location, _) = upload_dependency(workspace, wrapped_execution_script)
        wrapped_driver_program_id = os.path.basename(wrapped_execution_script)
        json_payload['assets'].append({'id': wrapped_driver_program_id, 'url': driver_package_location,
                                       'mimeType': driver_mime_type})
        json_payload['driverProgram'] = wrapped_driver_program_id

        if self.source_directory:
            (artifact_url, artifact_id) = upload_dependency(workspace, self.source_directory,
                                                            True, os.path.basename(self.source_directory))
            json_payload['assets'].append({'mimeType': 'application/octet-stream', 'id': artifact_id,
                                           'url': artifact_url, 'unpack': True})
        else:
            (artifact_url, artifact_id) = upload_dependency(workspace, self.entry_script)
            json_payload['assets'].append({'mimeType': 'application/octet-stream',
                                           'id': artifact_id,
                                           'url': artifact_url})

    def _add_base_image_to_payload(self, json_payload):
        if self.base_image:
            if not self.runtime.lower() in CUSTOM_BASE_IMAGE_SUPPORTED_RUNTIMES.keys():
                runtimes = '|'.join(CUSTOM_BASE_IMAGE_SUPPORTED_RUNTIMES.keys())
                raise WebserviceException('Custom base image is not supported for {} run time. '
                                          'Supported runtimes are: {}'.format(self.runtime, runtimes),
                                          logger=module_logger)
            json_payload['baseImage'] = self.base_image
            json_payload['targetRuntime']['runtimeType'] = CUSTOM_BASE_IMAGE_SUPPORTED_RUNTIMES[self.runtime.lower()]

            if self.base_image_registry.address and \
                    self.base_image_registry.username and \
                    self.base_image_registry.password:
                json_payload['baseImageRegistryInfo'] = {'location': self.base_image_registry.address,
                                                         'user': self.base_image_registry.username,
                                                         'password': self.base_image_registry.password}
            elif self.base_image_registry.address or \
                    self.base_image_registry.username or \
                    self.base_image_registry.password:
                raise WebserviceException('Address, Username and Password '
                                          'must be provided for base image registry', logger=module_logger)

    def build_profile_payload(self, profile_name, input_data):
        """Build the profiling payload for the Model package.

        :param profile_name: The name of the profile.
        :type profile_name: str
        :param input_data: The input data for profiling.
        :type input_data: str
        :return: The Model profile payload.
        :rtype: dict
        :raises: :class:`azureml.exceptions.WebserviceException`
        """
        from azureml._model_management._util import profile_payload_template
        json_payload = copy.deepcopy(profile_payload_template)
        json_payload['name'] = profile_name
        json_payload['description'] = self.description
        json_payload['inputData'] = input_data
        return json_payload


class ModelPackage(object):
    """
    Represents a packaging of one or more models and their dependencies into either a Docker image or Dockerfile.

    A ModelPackage object is returned from the :meth:`azureml.core.model.Model.package` method of the Model
    class. The ``generate_dockerfile`` parameter of the package method determines if a Docker image or
    Dockerfile is created.

    .. remarks::

        To build a Docker image that encapsulates your model and its dependencies, you can use the
        model packaging option. The output image will be pushed to your workspace's ACR.

        You must include an Environment object in your inference configuration to use the Model
        package method.

        .. code:: python

            package = Model.package(ws, [model], inference_config)
            package.wait_for_creation(show_output=True)  # Or show_output=False to hide the Docker build logs.
            package.pull()

        Instead of a fully-built image, you can instead generate a Dockerfile and download all the assets needed
        to build an image on top of your Environment.

        .. code:: python

            package = Model.package(ws, [model], inference_config, generate_dockerfile=True)
            package.wait_for_creation(show_output=True)
            package.save("./local_context_dir")

    :param workspace: The workspace in which the package is created.
    :type workspace: azureml.core.Workspace
    :param operation_id: The internal ID of the package creation operation.
    :type operation_id: str
    :param environment: The environment in which the model is packaged.
    :type environment: azureml.core.Environment
    """

    def __init__(self, workspace, operation_id, environment):
        """
        Initialize package created with model(s) and dependencies.

        :param workspace: The workspace in which the package exists.
        :type workspace: azureml.core.Workspace
        :param operation_id: ID of the package creation operation.
        :type operation_id: str
        :param environment: Environment in which the model is being packaged.
        :type environment: azureml.core.Environment
        """
        self.workspace = workspace
        self._operation_id = operation_id
        self._environment = environment

        self.update_creation_state()

    def __repr__(self):
        """
        Return the string representation of the ModelPackage object.

        :return: String representation of the ModelPackage object.
        :rtype: str
        """
        properties = [
            ('workspace', self.workspace.__repr__()),
            ('generate_dockerfile', self.generate_dockerfile),
            ('state', self.state),
        ]

        if not self.generate_dockerfile and self.state == 'Succeeded':
            properties.append(('location', self.location))

        return '{}({})'.format(self.__class__.__name__,
                               ', '.join('{}={}'.format(name, value) for name, value in properties))

    def get_container_registry(self):
        """
        Return a ContainerRegistry object indicating where the image or base image (Dockerfile packages) is stored.

        :return: The address and login credentials for the container registry.
        :rtype: azureml.core.ContainerRegistry
        """
        # Make sure the package has been created successfully.
        if self.state != 'Succeeded':
            self.wait_for_creation(show_output=True)

        registry = ContainerRegistry()

        if self.generate_dockerfile:
            # Get the base image credentials from EMS.
            manifest = make_http_request('GET', self.location).json()
            env_info = manifest.get('environment')

            if env_info:
                environment = Environment.get(self.workspace, env_info['name'], env_info['version'])
            else:
                environment = self._environment.register(self.workspace) \
                    if not self._environment.version else self._environment

            image_details = environment.get_image_details(self.workspace)
            registry_details = image_details.get('dockerImage')['registry']

            registry.address = registry_details['address']
            registry.password = registry_details['password']
            registry.username = registry_details['username']
        else:
            # Get the workspace ACR credentials.
            registry.username, registry.password = get_workspace_registry_credentials(self.workspace)
            registry.address = '{}.azurecr.io'.format(registry.username.lower())

        return registry

    def get_logs(self, decode=True, offset=0):
        """
        Retrieve the package creation logs.

        :param decode: Indicates whether to decode the raw log bytes to a string.
        :type decode: bool
        :param offset: The byte offset from which to start reading the logs.
        :type offset: int
        :return: The package creation logs.
        :rtype: bytes or str
        :raises: :class:`azureml.exceptions.WebserviceException`
        """
        headers = {'Range': 'bytes={}-'.format(offset)}
        response = make_http_request('GET', self.package_build_log_uri, headers=headers,
                                     check_response=lambda r: r.status_code in (404, 416) or not r.raise_for_status())

        if 200 <= response.status_code <= 299:
            return response.text if decode else response.content
        else:
            return str() if decode else bytes()

    def pull(self):
        """
        Pull the package output to the local machine.

        This can only be used with a Docker image package.

        :raises: :class:`azureml.exceptions.WebserviceException`
        """
        if self.generate_dockerfile:
            raise WebserviceException('A Dockerfile package cannot be pulled. Use save() instead.')

        # Make sure the package has been created successfully.
        if self.state != 'Succeeded':
            self.wait_for_creation(show_output=True)

        registry = self.get_container_registry()
        pull_docker_image(get_docker_client(), self.location, registry.username, registry.password)

    def save(self, output_directory):
        """
        Save the package output to a local directory.

        This can only be used with a Dockerfile package.

        :param output_directory: The local directory that will be created to contain the contents of the package.
        :type output_directory: str
        :raises: :class:`azureml.exceptions.WebserviceException`
        """
        if not self.generate_dockerfile:
            raise WebserviceException('Docker images cannot be saved to a local directory. Use pull() instead.')

        if os.path.exists(output_directory) and not os.path.isdir(output_directory):
            raise WebserviceException('Error, output path is not a directory: {}'.format(output_directory),
                                      logger=module_logger)

        # Make sure the package has been created successfully.
        if self.state != 'Succeeded':
            self.wait_for_creation(show_output=True)

        manifest = make_http_request('GET', self.location).json()
        download_docker_build_context(self.workspace, manifest, output_directory)
        module_logger.debug('Successfully saved Dockerfile package to {}'.format(output_directory))

        # Log into the base image registry, if we can, so `docker build` will work automatically.
        try:
            registry = self.get_container_registry()
            login_to_docker_registry(get_docker_client(), registry.username, registry.password, registry.address)
            module_logger.debug('Logged into base image registry for package.')
        except:
            module_logger.warning('Unable to log into Docker registry (is Docker installed and running?). '
                                  'Building the saved Dockerfile may fail when pulling the base image. '
                                  'To login manually, or on another machine, use the credentials returned by '
                                  'package.get_container_registry().')

    def update_creation_state(self):
        """
        Refresh the current state of the in-memory object.

        This method performs an in-place update of the properties of the object based on the current state of the
        corresponding cloud object. This is primarily used for manual polling of creation state.

        :raises: :class:`azureml.exceptions.WebserviceException`
        """
        operation = get_mms_operation(self.workspace, self._operation_id)

        self.generate_dockerfile = operation['operationType'] == 'PackageDockerBuildContext'
        self.error = operation.get('error')  # Only present if the operation fails.
        self.location = operation.get('resourceLocation')  # Only present if the operation succeeds.
        self.package_build_log_uri = operation['operationLog']
        self.state = operation['state']

    def wait_for_creation(self, show_output=False):
        """
        Wait for the package to finish creating.

        This method waits for package creation to reach a terminal state. Will throw a
        :class:`azureml.exceptions.WebserviceException` if it reaches a non-successful terminal state.

        :param show_output: Indicates whether to print more verbose output.
        :type show_output: bool
        :raises: :class:`azureml.exceptions.WebserviceException`
        """
        logs_offset = 0

        # Poll for status.
        while self.state == 'NotStarted' or self.state == 'Running':
            time.sleep(5)

            self.update_creation_state()

            if show_output:
                logs = self.get_logs(decode=False, offset=logs_offset)
                logs_offset += len(logs)
                print(logs.decode('utf-8', 'replace'), end='')

        if show_output:
            print('Package creation {}'.format(self.state))

        # Raise if the package failed.
        if self.state != 'Succeeded':
            if self.error and 'statusCode' in self.error and 'message' in self.error:
                error_message = ('StatusCode: {}\n'
                                 'Message: {}'.format(self.error['statusCode'], self.error['message']))
            else:
                error_message = self.error

            raise WebserviceException('Package creation reached non-successful terminal state.\n'
                                      'State: {}\n'
                                      'Error:\n'
                                      '{}\n'.format(self.state, error_message))

    def serialize(self):
        """
        Convert this ModelPackage into a JSON-serializable dictionary for display by the CLI.

        :return: The JSON representation of this ModelPackage.
        :rtype: dict
        """
        return {"generateDockerfile": self.generate_dockerfile,
                "state": self.state,
                "location": self.location}
