# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""constants in azureml.data package."""

AZURE_DATA_LAKE = "AzureDataLake"
AZURE_FILE = "AzureFile"
AZURE_BLOB = "AzureBlob"
AZURE_SQL_DATABASE = "AzureSqlDatabase"
AZURE_POSTGRESQL = "AzurePostgreSql"
AZURE_MYSQL = "AzureMySql"
DBFS = "DBFS"
AZURE_DATA_LAKE_GEN2 = "AzureDataLakeGen2"

ACCOUNT_KEY = "AccountKey"
SAS = "Sas"
CLIENT_CREDENTIALS = "ClientCredentials"
NONE = "None"

STORAGE_RESOURCE_URI = "https://storage.azure.com/"
ADLS_RESOURCE_URI = "https://datalake.azure.net/"

WORKSPACE_BLOB_DATASTORE = "workspaceblobstore"
WORKSPACE_FILE_DATASTORE = "workspacefilestore"

CONFLICT_MESSAGE = "Another datastore with the same name already exists"

_HYPERDRIVE_SUBMIT_ACTIVITY = "HyperDriveSubmit"
_SCRIPT_RUN_SUBMIT_ACTIVITY = "ScriptRunSubmit"

_AUTOML_SUBMIT_ACTIVITY = "AutoMLSubmit"
_AUTOML_INPUT_TYPE = "InputType"
_AUTOML_DATSET_ID = "DatasetId"
_AUTOML_COMPUTE = "Compute"
_AUTOML_DATASETS = "Datasets"
_AUTOML_SPARK = "IsSpark"
_AUTOML_DATASETS_COUNT = "DatasetCount"
_AUTOML_TABULAR_DATASETS_COUNT = "TabularDatasetCount"
_AUTOML_DATAFLOW_COUNT = "DataflowCount"
_AUTOML_OTHER_COUNT = "OtherCount"

_PUBLIC_API = 'PublicApi'

_DATASET_TYPE_TABULAR = 'tabular'
_DATASET_TYPE_FILE = 'file'

"""
Naming convention for trait property:
'_{trait}_{mark}{property}_'
    .format(
        trait='TimeSeries',
        mark='Column:' if True else ''
        property='FineGrainTimestamp')
"""
_DATASET_PROP_TIMESTAMP_FINE = '_TimeSeries_Column:FineGrainTimestamp_'
_DATASET_PROP_TIMESTAMP_COARSE = '_TimeSeries_Column:CoarseGrainTimestamp_'
