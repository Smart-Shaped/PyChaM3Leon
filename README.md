# PyChaM3Leon

ChaM3Leon is a Python library of helpers, templates and workflow components to build reproducible MLOps pipelines using Metaflow, MLflow and Apache Spark. It provides templating for Metaflow flows, utilities for MLflow integration, and Spark session helpers to simplify building data engineering and machine learning workflows.

## Features

- **Declarative Workflow Generation**: Create Metaflow workflows using JSON configuration files and Jinja2 templates
- **Unified Data Access Layer**: Abstract data source interactions with support for data sources like PostgreSQL, MinIO, Cassandra, and HDFS
- **Spark Session Management**: Simplified remote Spark session lifecycle management with automatic cleanup
- **MLflow Integration**: Streamlined experiment tracking, model logging, and autologging for PyTorch, TensorFlow, and scikit-learn
- **Flexible Decorators**: Rich set of decorators for adding functionality to workflow steps without code changes
- **Configuration-Driven**: Behavior controlled through external configuration files for environment-agnostic deployments

## Quick Start

### Basic Workflow Generation

Generate a Metaflow workflow from a JSON configuration:

```python
from chameleon.ml_runner.metaflow.runner.templating.configuration_parser import generate_workflow
from chameleon.ml_runner.metaflow.runner.templating.workflow_runner import run_workflow

# Generate workflow from config
workflow_path = generate_workflow('flow_config.json', 'workflows/')

# Run the generated workflow
run_workflow(workflow_path)
```

### Using Spark in Workflows

Extend the SparkFlow base class for automatic Spark session management:

```python
from chameleon.ml_runner.metaflow.base_flows.spark import SparkFlow
from metaflow import step

class MySparkWorkflow(SparkFlow):
    @step
    def spark_processing(self):
        # Spark session automatically available
        df = self.spark.read.parquet("s3://bucket/data")
        # Process data...
        self.next(self.end)
```

### Data Source Integration

Use the data source decorator for seamless data access:

```python
from chameleon.ml_runner.metaflow.base_flows.config import ConfigurableFlow
from chameleon.ml_runner.metaflow.decorators.data_sources import data_source
from metaflow import step

class DataPipeline(ConfigurableFlow):
    @step
    @data_source(source_type="postgres", conn_id="my_db")
    def extract_data(self):
        # Access data via the connection
        data = self.my_db.read(query_id="customer_query")
        self.next(self.end)
```

## Architecture Overview

The library is organized into four main modules:

- **Data Sources** (`chameleon.ml_runner.data_sources`): Abstractions and implementations for PostgreSQL, MinIO, Cassandra, and HDFS
- **Spark** (`chameleon.ml_runner.spark`): Session management and lifecycle utilities
- **MLflow** (`chameleon.ml_runner.mlflow`): Experiment tracking and model management utilities
- **Metaflow** (`chameleon.ml_runner.metaflow`): Base flows, decorators, mutators, and template system

For detailed documentation, see [DOCUMENTATION.md](DOCUMENTATION.md).

## Installation

Install from PyPI (when published):

```powershell
pip install pycham3leon
```

Or install from the repository for development:

```powershell
pip install --no-cache-dir git+https://github.com/Smart-Shaped/PyChaM3Leon.git@public
```

Note: the package targets Python 3.9–3.12.

## Package Structure

```bash
chameleon/
├── __init__.py
└── ml_runner/
    ├── __init__.py
    ├── data_sources/
    │   ├── __init__.py
    │   ├── abstraction.py
    │   └── implementations.py
    ├── exceptions.py
    ├── metaflow/
    │   ├── __init__.py
    │   ├── base_flows/
    │   ├── decorators/
    │   ├── mutators/
    │   └── runner/
    ├── mlflow/
    │   ├── __init__.py
    │   └── utils.py
    └── spark/
        ├── __init__.py
        └── sessions.py
```

### Package Descriptions

- **chameleon**: Root package of the library.
  
- **ml_runner**: Core module containing all the MLOps components.
  
  - **data_sources**: Abstractions and implementations for various data sources.
    - `abstraction.py`: Defines base classes and interfaces for data source connections.
    - `implementations.py`: Concrete implementations for PostgreSQL, MinIO, Cassandra, and HDFS.
  
  - **exceptions.py**: Custom exception classes for error handling across the library.
  
  - **metaflow**: Components for Metaflow integration and workflow management.
    - **base_flows**: Base flow classes that can be extended for different workflow types.
    - **decorators**: Function decorators to enhance workflow steps with additional capabilities.
    - **mutators**: Metaflow mutators for modifying flow behavior at runtime.
    - **runner**: Utilities for generating, executing, and managing workflows.
  
  - **mlflow**: MLflow integration components for experiment tracking and model management.
    - `utils.py`: Utility functions for MLflow experiment tracking, model logging, and autologging.
  
  - **spark**: Apache Spark integration and session management.
    - `sessions.py`: Utilities for creating, configuring, and managing Spark sessions.

## Documentation

For comprehensive documentation including:

- Detailed architecture overview
- Complete API reference for all components
- Advanced configuration examples
- Usage patterns and best practices
- Integration guides for Metaflow, MLflow, and Spark

See [DOCUMENTATION.md](DOCUMENTATION.md).

## Configuration

PyChaM3Leon uses JSON configuration files to control workflow behavior. Configuration files can include:

### Spark Configuration

```json
{
  "spark": {
    "remote_url": "sc://spark-cluster:15002",
    "app_name": "MySparkApp"
  }
}
```

### Data Source Configuration

```json
{
  "data_sources": {
    "postgres": {
      "my_db": {
        "host": "localhost",
        "port": 5432,
        "database": "mydb",
        "username": "user",
        "password": "pass",
        "queries": {
          "customer_query": {
            "dbtable": "customers"
          }
        }
      }
    },
    "minio": {
      "my_storage": {
        "host": "localhost",
        "port": 9000,
        "access_key": "minioadmin",
        "secret_key": "minioadmin",
        "queries": {
          "parquet_data": {
            "format": "parquet",
            "bucket": "data-lake",
            "key": "processed/data.parquet"
          }
        }
      }
    }
  }
}
```

## Key Components

### Base Flows

- **ConfigurableFlow**: Base class for workflows that accept configuration files
- **SparkFlow**: Extends ConfigurableFlow with automatic Spark session management

### Decorators

Here is a list of some of the available decorators:

- **@data_source**: Provides data access with automatic connection management
- **@mlflow_setup**: Configures MLflow tracking and autologging
- **@spark_session_step_wrapper**: Manages Spark session lifecycle for individual steps
- **@trainer_fit**: Automates PyTorch model training with MLflow logging

### Data Sources

All data sources support both Spark and non-Spark operations:

- **PostgreSQL**: JDBC/SQLAlchemy connectivity
- **MinIO**: S3-compatible object storage
- **Cassandra**: NoSQL database (placeholder)
- **HDFS**: Hadoop distributed file system (placeholder)

### Template System

Generate complete Metaflow workflows from JSON configurations:

- Automatic import management
- Parameter and configuration handling
- Step generation with decorator support

For complete documentation on all features, configuration options, and usage patterns, see [DOCUMENTATION.md](DOCUMENTATION.md).

This project is licensed under the Apache-2.0 License — see the `LICENSE` file for details.

## Publications

Article link — [ChaM3Leon announcement](https://www.smartshaped.com/blog/cham3leon-new-python-library)

## Contacts

Smart-Shaped Srl — [AI & Big Data service](https://www.smartshaped.com/servizio/ai-and-big-data)

## Workflow Template Example

The package includes Jinja2-based templates to generate Metaflow workflows. Below is a minimal example of the JSON structure:

```json
{
  "imports": [
    "mlflow",
    {
      "from": "chameleon.ml_runner.metaflow.decorators.data_sources",
      "elements": ["data_source"]
    }
  ],
  "class": {
    "name": "ExampleWorkflow",
    "parameters": [
      {
        "variable_name": "input_path",
        "object": {
          "type": "str",
          "default": "\"s3://my-bucket/data/\"",
          "help": "\"Path to input data\""
        }
      }
    ],
    "steps": [
      {
        "name": "start",
        "decorators": [
          {
            "name": "data_source",
            "parameters": {
              "source_type": "minio",
              "conn_id": "my_storage"
            }
          }
        ],
        "next": "process"
      },
      {
        "name": "process",
        "next": "end"
      },
      {
        "name": "end"
      }
    ]
  }
}
```

This configuration generates a complete, executable Metaflow workflow with proper imports, parameters, and step definitions, ready to be populated with the user-specific data processing logic.
