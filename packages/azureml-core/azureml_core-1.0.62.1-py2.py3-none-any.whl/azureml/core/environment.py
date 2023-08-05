# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Classes for managing environment definition."""
from __future__ import print_function
import collections
import logging
import json
import base64
import os
import subprocess
import zipfile
import tempfile
import sys
import time
import requests

from collections import OrderedDict
from azureml._base_sdk_common.abstract_run_config_element import _AbstractRunConfigElement
from azureml._base_sdk_common.field_info import _FieldInfo
from azureml.core.conda_dependencies import CondaDependencies, PYTHON_DEFAULT_VERSION
from azureml.core.container_registry import ContainerRegistry
from azureml.core._databricks import DatabricksSection
from azureml.exceptions import UserErrorException, AzureMLException

from azureml._restclient.environment_client import EnvironmentClient
from azureml.core._serialization_utils import _serialize_to_dict, _deserialize_and_add_to_object


module_logger = logging.getLogger(__name__)

DEFAULT_CPU_IMAGE = "mcr.microsoft.com/azureml/base:intelmpi2018.3-ubuntu16.04"
DEFAULT_GPU_IMAGE = "mcr.microsoft.com/azureml/base-gpu:intelmpi2018.3-cuda10.0-cudnn7-ubuntu16.04"
_DEFAULT_SHM_SIZE = "2g"

_CONDA_DEPENDENCIES_FILE_NAME = "conda_dependencies.yml"
_BASE_DOCKERFILE_FILE_NAME = "BaseDockerfile"
_DEFINITION_FILE_NAME = "azureml_environment.json"
_PRIVATE_PKG_CONTAINER_NAME = "azureml-private-packages"
_EMS_ORIGIN_NAME = "Environment"


class PythonSection(_AbstractRunConfigElement):
    """A class for managing PythonSection.

    :param user_managed_dependencies: True means that AzureML reuses an existing python environment, False means
        that AzureML will create a python environment based on the Conda dependencies specification.
    :type user_managed_dependencies: bool

    :param interpreter_path: The python interpreter path. This is only used when user_managed_dependencies=True
    :type interpreter_path: str

    :param conda_dependencies_file: Path to the conda dependencies file to use for this run. If a project
        contains multiple programs with different sets of dependencies, it may be convenient to manage
        those environments with separate files.
    :type conda_dependencies_file: str
    """

    # This is used to deserialize.
    # This is also the order for serialization into a file.
    _field_to_info_dict = collections.OrderedDict([
        ("user_managed_dependencies", _FieldInfo(bool, "user_managed_dependencies=True indicates that the environment"
                                                       "will be user managed. False indicates that AzureML will"
                                                       "manage the user environment.")),
        ("interpreter_path", _FieldInfo(str, "The python interpreter path")),
        ("conda_dependencies_file", _FieldInfo(
            str, "Path to the conda dependencies file to use for this run. If a project\n"
                 "contains multiple programs with different sets of dependencies, it may be\n"
                 "convenient to manage those environments with separate files.")),
        ("_base_conda_environment", _FieldInfo(
            str, "The base conda environment used for incremental environment creation.",
            serialized_name="base_conda_environment")),
    ])

    def __init__(self, _skip_defaults=False):
        """Class PythonSection constructor."""
        super(PythonSection, self).__init__()

        self.interpreter_path = "python"
        self.user_managed_dependencies = False
        self.conda_dependencies_file = None
        self.conda_dependencies = None
        self._base_conda_environment = None

        if not _skip_defaults:
            self.conda_dependencies = CondaDependencies()

        self._initialized = True


class PythonEnvironment(PythonSection):
    """DEPRECATED - A class for managing PythonEnvironment.

    .. remarks::

        This class is deprecated and replaced by azureml.core.environment.PythonSection
    """

    def __init__(self):
        """Class PythonEnvironment constructor."""
        super(PythonEnvironment, self).__init__()
        module_logger.warning(
            "'PythonEnvironment' will be deprecated soon. Please use PythonSection from 'azureml.core.environment'.")


class DockerSection(_AbstractRunConfigElement):
    """A class for managing DockerSection.

    :param enabled: Set True to perform this run inside a Docker container.
    :type enabled: bool

    :param base_image: Base image used for Docker-based runs. Mutually exclusive with base_dockerfile. Example:
        "ubuntu:latest"
    :type base_image: str

    :param base_dockerfile: Base Dockerfile used for Docker-based runs. Mutually exclusive with base_image. Example:
        FROM ubuntu:latest
        RUN echo 'Hello world!'
    :type base_dockerfile: str

    :param shared_volumes: Set False if necessary to work around shared volume bugs on Windows.
    :type shared_volumes: bool

    :param gpu_support: Deprecated config. We now automatically detect and use nvidia docker extension when available.
    :type gpu_support: bool

    :param arguments: Extra arguments to the Docker run command.
    :type arguments: builtin.list

    :param base_image_registry: Image registry that contains the base image.
    :type base_image_registry: azureml.core.container_registry.ContainerRegistry
    """

    # This is used to deserialize.
    # This is also the order for serialization into a file.
    _field_to_info_dict = collections.OrderedDict([
        ("enabled", _FieldInfo(
            bool, "Set True to perform this run inside a Docker container.")),
        ("base_image", _FieldInfo(
            str, "Base image used for Docker-based runs. Mutually exclusive with base_dockerfile.")),
        ("base_dockerfile", _FieldInfo(
            str, "Base Dockerfile used for Docker-based runs. Mutually exclusive with base_image")),
        ("shared_volumes", _FieldInfo(
            bool, "Set False if necessary to work around shared volume bugs.")),
        ("shm_size", _FieldInfo(
            str, "Shared memory size for Docker container. Default is {}.".format(_DEFAULT_SHM_SIZE))),
        ("arguments", _FieldInfo(
            list, "Extra arguments to the Docker run command.", list_element_type=str)),
        ("base_image_registry", _FieldInfo(ContainerRegistry,
                                           "Image registry that contains the base image.")),
    ])

    def __init__(self, _skip_defaults=False):
        """Class DockerSection constructor."""
        super(DockerSection, self).__init__()
        self.enabled = False
        self.shm_size = None
        self.shared_volumes = True
        self.arguments = list()
        self.base_image = None
        self.base_image_registry = ContainerRegistry()
        self.base_dockerfile = None

        if not _skip_defaults:
            self.shm_size = _DEFAULT_SHM_SIZE
            self.base_image = DEFAULT_CPU_IMAGE

        self._initialized = True

    @property
    def gpu_support(self):
        """Get gpu_support is now an unused config."""
        module_logger.warning("'gpu_support' is no longer necessary; AzureML now automatically detects and uses "
                              "nvidia docker extension when it is available. It will be removed in a future release.")
        return True

    @gpu_support.setter
    def gpu_support(self, _):
        """Get gpu_support is now an unused config."""
        module_logger.warning("'gpu_support' is no longer necessary; AzureML now automatically detects and uses "
                              "nvidia docker extension when it is available. It will be removed in a future release.")


class DockerEnvironment(DockerSection):
    """DEPRECATED - A class for managing DockerEnvironment.

    .. remarks::

        This class is deprecated and replaced by azureml.core.environment.DockerSection
    """

    def __init__(self):
        """Class DockerEnvironment constructor."""
        super(DockerEnvironment, self).__init__()
        module_logger.warning(
            "'DockerEnvironment' will be deprecated soon. Please use DockerSection from 'azureml.core.environment'.")


class SparkPackage(_AbstractRunConfigElement):
    """A class for managing SparkPackage.

    :param group:
    :type group: str
    :param artifact:
    :type artifact: str
    :param version:
    :type version: str
    """

    # This is used to deserialize.
    # This is also the order for serialization into a file.
    _field_to_info_dict = collections.OrderedDict([
        ("group", _FieldInfo(str, "")),
        ("artifact", _FieldInfo(str, "")),
        ("version", _FieldInfo(str, ""))
    ])

    def __init__(self, group=None, artifact=None, version=None):
        """Class SparkPackage constructor."""
        super(SparkPackage, self).__init__()
        self.group = group
        self.artifact = artifact
        self.version = version
        self._initialized = True


class SparkSection(_AbstractRunConfigElement):
    """A class for managing SparkSection.

    :param repositories: List of spark repositories.
    :type repositories: builtin.list

    :param packages: The packages to use.
    :type packages: builtin.list

    :param precache_packages: Whether to preckage the packages.
    :type precache_packages: bool
    """

    # This is used to deserialize.
    # This is also the order for serialization into a file.
    _field_to_info_dict = collections.OrderedDict([
        ("repositories", _FieldInfo(
            list, "List of spark repositories.", list_element_type=str)),
        ("packages", _FieldInfo(list, "The packages to use.",
                                list_element_type=SparkPackage)),
        ("precache_packages", _FieldInfo(bool, "Whether to precache the packages."))
    ])

    def __init__(self, _skip_defaults=False):
        """Class SparkSection constructor."""
        super(SparkSection, self).__init__()
        self.repositories = []
        self.packages = []
        self.precache_packages = True
        self._initialized = True


class SparkEnvironment(SparkSection):
    """DEPRECATED - A class for managing SparkEnvironment.

    .. remarks::

        This class is deprecated and replaced by azureml.core.environment.SparkSection
    """

    def __init__(self):
        """Class SparkEnvironment constructor."""
        super(SparkEnvironment, self).__init__()
        module_logger.warning(
            "'SparkEnvironment' will be deprecated soon. Please use SparkSection from 'azureml.core.environment'.")


class _ImageDetails(object):
    """A class for image details.

    :param data: Dictionary response from the request
    :type data: dict
    """

    def __init__(self, data):
        """Class _ImageDetails constructor."""
        self.__dict__ = data

    def __repr__(self):
        """Representation of the object.

        :return: Return the string form of the ImageDetails object
        :rtype: str
        """
        return json.dumps(self.__dict__, indent=4)


class _ImageBuildStatus(object):
    """Class for Image build Status."""

    def __init__(self, status):
        """Class _ImageBuildStatus constructor."""
        self.status = status


class _ImageBuildDetails(object):
    """Class for Image build details."""

    def __init__(self, environment_client, log_url, build_id):
        """Class _ImageBuildDetails constructor."""
        self.environment_client = environment_client
        self.log_url = log_url
        self.build_id = build_id

    def wait_for_completion(self, show_output=True):
        """
        Wait for the completion of this cloud environment build.

        Returns the status after the wait.

        :param show_output: show_output=True shows the build status on sys.stdout.
        :type show_output: bool

        :return: The Image build status object.
        :rtype: azureml.core.environment._ImageBuildStatus
        """
        def _incremental_print(log, printed, fileout):
            count = 0
            for line in log.splitlines():
                if count >= printed:
                    print(line, file=fileout)
                    printed += 1
                count += 1

            return printed

        timeout_seconds = sys.maxsize
        file_handle = sys.stdout

        client = self.environment_client
        build_id = self.build_id
        log_url = self.log_url

        status = client._get_cloud_image_build_status(build_id)["status"]
        last_status = None
        separator = ''
        time_run = 0
        sleep_period = 5
        printed = 0
        while status == 'Running':
            if time_run + sleep_period > timeout_seconds:
                if show_output:
                    print('Timed out of waiting, %sStatus: %s.' %
                          (separator, status), flush=True)
                break
            time_run += sleep_period
            time.sleep(sleep_period)
            status = client._get_cloud_image_build_status(build_id)["status"]
            if last_status != status:
                if show_output:
                    print('Image Build Status: {0}\n'.format(status))
                last_status = status
                separator = ''
            else:
                if show_output:
                    content = requests.get(log_url, stream=True).text
                    printed = _incremental_print(content, printed, file_handle)
                else:
                    print('.', end='', flush=True)
                separator = '\n'

        return _ImageBuildStatus(status)


class Environment(_AbstractRunConfigElement):
    """Configure the python environment where the experiment is executed.

    :param name: The name of the environment
    :type name: string

    :param version: The version of the environment
    :type version: string

    :param environment_variables: A dictionary of environment variables names and values.
        These environment variables are set on the process where user script is being executed.
    :type environment_variables: dict

    :param python: This section specifies which python environment and interpreter to use on the target compute.
    :type python: azureml.core.environment.PythonSection

    :param docker: This section configures if and how Docker containers are used by the run.
    :type docker: azureml.core.environment.DockerSection

    :param spark: The section configures Spark settings. It is only used when framework is set to PySpark.
    :type spark: azureml.core.environment.SparkSection

    :param databricks: The section configures Databricks library dependencies.
    :type databricks: azureml.core._databricks.DatabricksSection

    :param inferencing_stack_version: This section specifies the inferencing stack version added to the image.
        To avoid adding an inferencing stack, do not set this value. Valid values: "latest"
    :type inferencing_stack_version: string
    """

    # This is used to deserialize.
    # This is also the order for serialization into a file.
    _field_to_info_dict = collections.OrderedDict([
        # In dict, values are assumed to be str
        ("name", _FieldInfo(str, "Environment name")),
        ("version", _FieldInfo(str, "Environment version")),
        ("environment_variables", _FieldInfo(
            dict, "Environment variables set for the run.", user_keys=True)),
        ("python", _FieldInfo(PythonSection, "Python details")),
        ("docker", _FieldInfo(DockerSection, "Docker details")),
        ("spark", _FieldInfo(SparkSection, "Spark details")),
        ("databricks", _FieldInfo(DatabricksSection, "Databricks details")),
        ("inferencing_stack_version", _FieldInfo(str, "Inferencing stack version"))
    ])

    def __init__(self, name, _skip_defaults=False):
        """Class Environment constructor."""
        super(Environment, self).__init__()

        # Add Name/version validation for env management
        self.name = name
        self.version = None
        self.python = PythonSection(_skip_defaults=_skip_defaults)
        self.docker = DockerSection(_skip_defaults=_skip_defaults)
        self.spark = SparkSection(_skip_defaults=_skip_defaults)
        self.databricks = DatabricksSection(_skip_defaults=_skip_defaults)
        self.environment_variables = dict()
        self.inferencing_stack_version = None

        if not _skip_defaults:
            self.environment_variables = {"EXAMPLE_ENV_VAR": "EXAMPLE_VALUE"}

        self._initialized = True

    def _get_base_info_dict(self):
        """Return base info dictionary.

        :return:
        :rtype: OrderedDict
        """
        return OrderedDict([
            ('Name', self.name),
            ('Version', self.version)
        ])

    def __str__(self):
        """Format Environment data into a string.

        :return:
        :rtype: str
        """
        info = self._get_base_info_dict()
        formatted_info = ',\n'.join(
            ["{}: {}".format(k, v) for k, v in info.items()])
        return "Environment({0})".format(formatted_info)

    def __repr__(self):
        """Representation of the object.

        :return: Return the string form of the Environment object
        :rtype: str
        """
        environment_dict = Environment._serialize_to_dict(self)
        return json.dumps(environment_dict, indent=4)

    def register(self, workspace):
        """Register the environment object in your workspace.

        :param workspace: The workspace
        :type workspace: azureml.core.workspace.Workspace
        :param name:
        :type name: str
        :return: Returns the environment object
        :rtype: azureml.core.environment.Environment
        """
        environment_client = EnvironmentClient(workspace.service_context)
        environment_dict = Environment._serialize_to_dict(self)
        response = environment_client._register_environment_definition(environment_dict)
        env = Environment._deserialize_and_add_to_object(response)

        return env

    @staticmethod
    def get(workspace, name, version=None):
        """Return the environment object.

        :param workspace: The workspace
        :type workspace: azureml.core.workspace.Workspace
        :param name:
        :type name: str
        :param version:
        :type version: str
        :return: Returns the environment object
        :rtype: azureml.core.environment.Environment
        """
        environment_client = EnvironmentClient(workspace.service_context)
        environment_dict = environment_client._get_environment_definition(name=name, version=version)
        env = Environment._deserialize_and_add_to_object(environment_dict)

        return env

    @staticmethod
    def list(workspace):
        """Return the list of environments in the workspace.

        :param workspace: The workspace from which to list the environments.
        :type workspace: azureml.core.workspace.Workspace
        :return: list of environment objects.
        :rtype: builtin.list[azureml.core.Environment]
        """
        environment_client = EnvironmentClient(workspace.service_context)
        environment_list = environment_client._list_definitions()

        result = {environment["name"]: Environment._deserialize_and_add_to_object(environment)
                  for environment in environment_list}

        return result

    @staticmethod
    def from_conda_specification(name, file_path):
        """Create an environment object created from a environment specification yaml file.

        To get an environment specification yaml file, please refer to the conda docs link below.
        https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#exporting-the-environment-file

        :param name: The environment name
        :type name: str
        :param file_path: The conda environment specification yaml file path.
        :type file_path: str
        :return: Returns the environment object
        :rtype: azureml.core.environment.Environment
        """  # noqa: E501
        conda_dependencies = CondaDependencies(conda_dependencies_file_path=file_path)
        if not conda_dependencies._python_version:
            module_logger.warning('No Python version provided, defaulting to "{}"'.format(PYTHON_DEFAULT_VERSION))
            conda_dependencies.set_python_version(PYTHON_DEFAULT_VERSION)
        env = Environment(name=name)
        env.python.conda_dependencies = conda_dependencies

        return env

    @staticmethod
    def from_existing_conda_environment(name, conda_environment_name):
        """Create an environment object created from a locally existing conda environment.

        To get a list of existing conda environments, run "conda env list"
        https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#viewing-a-list-of-your-environments

        :param name: The environment name
        :type name: str
        :param conda_environment_name: The name of a locally existing conda environment.
        :type conda_environment_name: str
        :return: Returns the environment object or None if exporting the conda specification file fails.
        :rtype: azureml.core.environment.Environment
        """  # noqa: E501
        env = None
        if Environment._check_conda_installation() and Environment._check_conda_env_existance(conda_environment_name):
            try:
                print("Exporting conda specifications for " +
                      "existing conda environment: {}".format(conda_environment_name))
                export_existing_env_cmd = ["conda", "env", "export", "--no-builds", "--name", conda_environment_name]
                conda_specifications = subprocess.check_output(export_existing_env_cmd)

                tmp_conda_spec_file = tempfile.NamedTemporaryFile(suffix=".yml", delete=False)
                tmp_conda_spec_file.write(conda_specifications)
                tmp_conda_spec_file.seek(0)
                tmp_conda_spec_file_name = tmp_conda_spec_file.name

                env = Environment.from_conda_specification(name, tmp_conda_spec_file_name)

                tmp_conda_spec_file.close()
            except subprocess.CalledProcessError as ex:
                print("Exporting conda specifications failed with exit code: {}".format(ex.returncode))
            finally:
                if os.path.isfile(tmp_conda_spec_file_name):
                    os.remove(tmp_conda_spec_file_name)

        return env

    @staticmethod
    def from_pip_requirements(name, file_path):
        """Create an environment object created from a pip requirements file.

        :param name: The environment name
        :type name: str
        :param file_path: The pip requirements file path.
        :type file_path: str
        :return: Returns the environment object
        :rtype: azureml.core.environment.Environment
        """
        requirements_list = []
        with open(file_path) as in_file:
            requirements_list = in_file.read().splitlines()

        conda_dependencies = CondaDependencies.create(pip_packages=requirements_list)
        env = Environment(name=name)
        env.python.conda_dependencies = conda_dependencies

        return env

    @staticmethod
    def add_private_pip_wheel(workspace, file_path, exist_ok=False):
        """Upload the private pip wheel file on disk to the Azure storage blob attached to the workspace.

        Throws an exception if a private pip wheel with the same name already exists in the workspace storage blob.

        :param workspace: Workspace object to use to register the private pip wheel.
        :type workspace: azureml.core.workspace.Workspace
        :param file_path: Path to the local pip wheel on disk, including the file extension.
        :type file_path: str
        :param exist_ok: If set to True, the method will not throw an exception if the wheel already exists.
        :type exist_ok: bool
        :return: Returns the full URI to the uploaded pip wheel on Azure blob storage to use in conda dependencies.
        :rtype: str
        """
        if not os.path.isfile(file_path):
            raise UserErrorException("Please make sure the wheel file exists at: {}".format(file_path))

        # since we're guaranteeing that the file_path points to a file, os.path.basename should return the file name.
        wheel_name = os.path.basename(file_path)

        try:
            from azureml._restclient.artifacts_client import ArtifactsClient
            artifacts_client = ArtifactsClient(workspace.service_context)

            batch_artifact_info = artifacts_client.create_empty_artifacts(
                origin=_EMS_ORIGIN_NAME,
                container=_PRIVATE_PKG_CONTAINER_NAME,
                paths=[wheel_name])
            wheel_artifact = batch_artifact_info.artifacts[wheel_name]
            wheel_artifact_content_info = batch_artifact_info.artifact_content_information[wheel_name]

            with open(file_path, "rb") as stream:
                artifacts_client.upload_stream_to_existing_artifact(
                    stream=stream,
                    artifact=wheel_artifact,
                    content_information=wheel_artifact_content_info)

            content_uri = wheel_artifact_content_info.content_uri
        except AzureMLException as error:
            if "Resource Conflict: ArtifactId" in repr(error):
                if exist_ok:
                    # wheel already exists so we'll just fetch the existing artifact to get the URI
                    content_uri = artifacts_client.get_file_uri(
                        origin=_EMS_ORIGIN_NAME,
                        container=_PRIVATE_PKG_CONTAINER_NAME,
                        path=wheel_name)
                else:
                    error_msg = """
A wheel with the name {} already exists.
Please make sure {} is the private wheel you would like to add to the workspace.
If you would like to have it be a no-op instead of throwing an exception for duplicate entries,
please set exist_ok=True""".format(wheel_name, wheel_name)
                    raise UserErrorException(error_msg)
            else:
                raise error

        from six.moves.urllib import parse
        parsed = parse.urlparse(content_uri)
        normalized_uri = parsed.scheme + "://" + parsed.netloc + parsed.path
        return normalized_uri

    def get_image_details(self, workspace):
        """Return the Image details.

        :param workspace: The workspace
        :type workspace: azureml.core.workspace.Workspace
        :return: Returns the image details object
        :rtype: azureml.core.environment._ImageDetails
        """
        environment_client = EnvironmentClient(workspace.service_context)
        image_details_dict = environment_client._get_image_details(
            name=self.name, version=self.version)

        image_details_object = _ImageDetails(image_details_dict)

        return image_details_object

    def build(self, workspace):
        """Build a Docker image for this environment in the cloud.

        :param workspace: The workspace
        :type workspace: azureml.core.workspace.Workspace
        :return: Returns the image build details object
        :rtype: azureml.core.environment._ImageBuildDetails
        """
        environment_client = EnvironmentClient(workspace.service_context)
        image_build_details = environment_client._start_cloud_image_build(name=self.name, version=self.version)

        log_url = image_build_details["logUrl"]
        build_id = image_build_details["buildId"]

        return _ImageBuildDetails(environment_client, log_url, build_id)

    def build_local(self, workspace):
        """Build the local docker or conda environment.

        :param workspace: The workspace
        :type workspace: azureml.core.workspace.Workspace
        :return: Streams the build environment output
        :rtype: str
        """
        environment_client = EnvironmentClient(workspace.service_context)
        recipe = environment_client._get_recipe_for_build(name=self.name, version=self.version)

        setup_content = base64.b64decode(recipe["setupContentZip"])
        build_script = recipe["buildEnvironmentScriptName"]
        check_script = recipe["checkEnvironmentScriptName"]
        environment_variables = recipe["environmentVariables"]

        with tempfile.TemporaryDirectory() as setup_temp_dir:
            try:
                setup_content_zip_file = os.path.join(setup_temp_dir, "Setupcontent.zip")
                with open(setup_content_zip_file, "wb") as file:
                    file.write(setup_content)

                with zipfile.ZipFile(setup_content_zip_file, 'r') as zip_ref:
                    zip_ref.extractall(setup_temp_dir)

                self._build_environment(setup_temp_dir, check_script, build_script, environment_variables)
            except subprocess.CalledProcessError as ex:
                print("Building environment failed with exit code : {}".format(ex.returncode))

    def save_to_directory(self, path, overwrite=False):
        """Save an environment definition to a directory in an easily editable format.

        :param path: Path to the destination directory.
        :type path: str
        :param overwrite: If an existing directory should be overwritten. Defaults false.
        :type overwrite: bool
        """
        os.makedirs(path, exist_ok=overwrite)
        if self.python and self.python.conda_dependencies:
            self.python.conda_dependencies.save_to_file(path, _CONDA_DEPENDENCIES_FILE_NAME)

        if self.docker and self.docker.base_dockerfile:
            with open(os.path.join(path, _BASE_DOCKERFILE_FILE_NAME), "w") as base_dockerfile:
                base_dockerfile.write(self.docker.base_dockerfile)

        with open(os.path.join(path, _DEFINITION_FILE_NAME), "w") as definition:
            environment_dict = Environment._serialize_to_dict(self)

            # Don't serialize properties that got saved to separate files.
            if environment_dict.get("python") and environment_dict["python"].get("condaDependencies"):
                del environment_dict["python"]["condaDependencies"]
            if environment_dict.get("docker") and environment_dict["docker"].get("baseDockerfile"):
                del environment_dict["docker"]["baseDockerfile"]

            json.dump(environment_dict, definition, indent=4)

    @staticmethod
    def load_from_directory(path):
        """Load an environment definition from the files in a directory.

        :param path: Path to the source directory.
        :type path: str
        """
        definition_path = os.path.join(path, _DEFINITION_FILE_NAME)
        if not os.path.isfile(definition_path):
            raise FileNotFoundError(definition_path)

        with open(definition_path, "r") as definition:
            environment_dict = json.load(definition)
        env = Environment._deserialize_and_add_to_object(environment_dict)

        conda_file_path = os.path.join(path, _CONDA_DEPENDENCIES_FILE_NAME)
        if os.path.isfile(conda_file_path):
            env.python = env.python or PythonSection(_skip_defaults=True)
            env.python.conda_dependencies = CondaDependencies(conda_file_path)

        base_dockerfile_path = os.path.join(path, _BASE_DOCKERFILE_FILE_NAME)
        if os.path.isfile(base_dockerfile_path):
            with open(base_dockerfile_path, "r") as base_dockerfile:
                env.docker = env.docker or DockerSection(_skip_defaults=True)
                env.docker.base_dockerfile = base_dockerfile.read()

        return env

    @staticmethod
    def _check_conda_installation():
        is_conda_installed = True
        try:
            conda_version_cmd = ["conda", "--version"]
            conda_version = subprocess.check_output(conda_version_cmd).decode("UTF-8").replace("conda", "").strip()

            from distutils.version import LooseVersion
            installed_version = LooseVersion(conda_version)
            required_version = LooseVersion("4.4.0")
            if installed_version < required_version:
                print("AzureML requires Conda version {} or later.".format(required_version))
                print("You can update your installed conda version {} by running:".format(installed_version))
                print("    conda update conda")
                is_conda_installed = False
        except subprocess.CalledProcessError:
            print("Unable to run Conda package manager. Please make sure Conda (>= 4.4.0) is installed.")
            is_conda_installed = False

        return is_conda_installed

    @staticmethod
    def _check_conda_env_existance(conda_env_name):
        # Helper method to check if the conda environment exists as conda env export works for envs that don't exist.
        env_exists = False
        try:
            get_conda_env_list_cmd = ["conda", "env", "list", "--json"]
            conda_env_list_json = subprocess.check_output(get_conda_env_list_cmd)
            conda_env_list = json.loads(conda_env_list_json)["envs"]
            # NOTE: conda env list --json returns the full path for the env
            if any(conda_env_name == os.path.basename(os.path.normpath(conda_env)) for conda_env in conda_env_list):
                env_exists = True
            else:
                print("Could not find existing conda environment named: {}".format(conda_env_name))
                print("Please make sure the conda environment {} exists.".format(conda_env_name))
        except subprocess.CalledProcessError as ex:
            print("Getting the list of existing conda environments failed with exit code: {}".format(ex.returncode))

        return env_exists

    @staticmethod
    def _discriminate_variations(raw_object):
        keys = [x[0] for x in raw_object.items()]

        reference_keys = ["name", "version"]
        if all(x in reference_keys for x in keys):
            return EnvironmentReference

        return Environment

    @staticmethod
    def _serialize_to_dict(environment, use_commented_map=False):
        environment_dict = _serialize_to_dict(environment, use_commented_map)

        # _serialization_utils._serialize_to_dict does not serialize condadependencies correctly.
        # Hence the work around to copy this in to the env object
        if not isinstance(environment, EnvironmentReference):
            if environment.python.conda_dependencies is not None:
                inline = environment.python.conda_dependencies._conda_dependencies
                environment_dict["python"]["condaDependencies"] = inline

        return environment_dict

    @staticmethod
    def _deserialize_and_add_to_object(serialized_dict):
        environment_name = serialized_dict.get("name")
        environment_version = serialized_dict.get("version")

        if Environment._discriminate_variations(serialized_dict) == EnvironmentReference:
            return EnvironmentReference(environment_name, environment_version)

        # _serialization_utils._deserialize_and_add_to_object does deserialize condaDependencies correctly.
        # Hence the work around to inject it to env object
        environment_object = Environment(environment_name, _skip_defaults=True)
        environment_object.version = environment_version

        env = _deserialize_and_add_to_object(Environment, serialized_dict, environment_object)

        inline_conda_dependencies = serialized_dict.get("python", {}).get("condaDependencies", None)
        if inline_conda_dependencies is not None:
            conda_dependencies = CondaDependencies(_underlying_structure=inline_conda_dependencies)
            env.python.conda_dependencies = conda_dependencies

        return env

    def _build_environment(self, setup_temp_dir, check_script, build_script, environment_variables=None):
        check_env_command = self._get_command(setup_temp_dir, check_script)
        build_env_command = self._get_command(setup_temp_dir, build_script)

        env = os.environ
        if environment_variables:
            env.update(environment_variables)

        try:
            # Check if environment exists
            subprocess.check_call(check_env_command, stdout=sys.stdout,
                                  stderr=sys.stderr, cwd=setup_temp_dir, env=env)
        except subprocess.CalledProcessError:
            # else build Environment
            subprocess.check_call(build_env_command, stdout=sys.stdout,
                                  stderr=sys.stderr, cwd=setup_temp_dir, env=env)

    def _get_command(self, setup_temp_dir, script):
        script_path = os.path.join(setup_temp_dir, "azureml-setup", script)

        if os.name == "nt":
            command = ["cmd.exe", "/c", script_path]
        else:
            command = ["/bin/bash", "-c", script_path]

        return command


class EnvironmentReference(_AbstractRunConfigElement):
    """Reference to an existing environment definition stored in the workspace.

    Can be used in place of an Environment object.

    :param name: The name of the environment
    :type name: string

    :param version: The version of the environment
    :type version: string
    """

    _field_to_info_dict = collections.OrderedDict([
        ("name", _FieldInfo(str, "Environment name")),
        ("version", _FieldInfo(str, "Environment version"))
    ])

    def __init__(self, name, version=None):
        """Class EnvironmentReference constructor."""
        super(EnvironmentReference, self).__init__()

        self.name = name
        self.version = version
        self._initialized = True

    def __repr__(self):
        """Representation of the object.

        :return: Return the string form of the EnvironmentReference object
        :rtype: str
        """
        environment_dict = _serialize_to_dict(self)
        return json.dumps(environment_dict, indent=4)

    def get_environment(self, workspace):
        """Return the Environment object pointed at by this reference.

        :param workspace: The workspace that contains the persisted environment
        :type workspace: azureml.core.workspace.Workspace
        :return: The referenced Environment object
        :rtype: azureml.core.environment.Environment
        """
        return Environment.get(workspace, self.name, self.version)
