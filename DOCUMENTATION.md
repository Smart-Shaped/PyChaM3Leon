# PyChaM3Leon - Complete Documentation

## Table of Contents

1. [Introduction](#introduction)
2. [Architecture Overview](#architecture-overview)
3. [Core Components](#core-components)
4. [Exception Handling](#exception-handling)
5. [Data Sources](#data-sources)
6. [Spark Integration](#spark-integration)
7. [MLflow Integration](#mlflow-integration)
8. [Metaflow Integration](#metaflow-integration)
9. [Template System](#template-system)
10. [Configuration Guide](#configuration-guide)
11. [Usage Patterns](#usage-patterns)
12. [Best Practices](#best-practices)

---

## Introduction

PyChaM3Leon is a comprehensive Python library designed to streamline the development of reproducible MLOps pipelines. It integrates three powerful frameworks (Metaflow, MLflow, and Apache Spark) into a unified development experience. The library provides abstractions, templates, and utilities that enable data scientists and engineers to build scalable, production-ready machine learning workflows with minimal boilerplate code.

### Key Features

- **Declarative Workflow Generation**: Create Metaflow workflows using JSON configuration files and Jinja2 templates
- **Unified Data Access Layer**: Abstract data source interactions with support for data sources like PostgreSQL, MinIO, Cassandra, and HDFS
- **Spark Session Management**: Simplified remote Spark session lifecycle management with automatic cleanup
- **MLflow Integration**: Streamlined experiment tracking, model logging, and autologging for PyTorch, TensorFlow, and scikit-learn
- **Flexible Decorators**: Rich set of decorators for adding functionality to workflow steps without code changes
- **Configuration-Driven**: Behavior controlled through external configuration files for environment-agnostic deployments

### Target Python Versions

The library supports Python versions from 3.9 to 3.12, ensuring compatibility with modern Python environments while maintaining stability.

---

## Architecture Overview

PyChaM3Leon follows a modular architecture organized into distinct functional domains:

### Package Structure

The library is organized under the `chameleon.ml_runner` namespace with the following major modules:

- **Data Sources Module**: Provides abstractions and implementations for various data storage systems
- **Spark Module**: Manages Spark session lifecycle and configuration
- **MLflow Module**: Utilities for experiment tracking and model management
- **Metaflow Module**: Contains base flows, decorators, mutators, and the template rendering system

### Design Principles

The architecture adheres to several key design principles:

- **Separation of Concerns**: Each module handles a specific aspect of the MLOps pipeline
- **Abstraction**: Common patterns are abstracted into reusable components
- **Extensibility**: Factory patterns and abstract base classes allow easy addition of new implementations
- **Configuration-Driven**: Behavior is controlled through configuration files rather than code changes
- **Context Management**: Resources are properly managed using context managers and decorators

---

## Core Components

### Exception Hierarchy

The library defines a comprehensive exception hierarchy for clear error handling across different components:

#### SparkException

Raised when errors occur during Spark operations, such as missing configuration, connection failures, or invalid Spark session states.

#### MetaflowException

Indicates errors related to Metaflow workflow execution, including missing required parameters, invalid step configurations, or flow execution failures.

#### DataSourceException

Thrown when data source operations fail, including connection issues, invalid queries, or unsupported data source types.

#### MlflowException

Signals errors in MLflow operations, such as experiment creation failures, model logging issues, or tracking URI configuration problems.

These exceptions provide specific context about failures, making debugging and error handling more straightforward.

---

## Data Sources

The data sources module provides a unified interface for interacting with various storage systems, supporting both Spark-based and non-Spark data operations.

### Abstract Data Source Interface

The `DataSource` abstract base class defines the contract that all data source implementations must follow. It provides both Spark-enabled and non-Spark methods for reading and writing data.

#### Core Capabilities

- **Dual-Mode Operation**: Automatically uses Spark when available, falls back to native libraries otherwise
- **Query Management**: Supports predefined queries stored in configuration files
- **Flexible Parameterization**: Allows runtime query customization through query dictionaries
- **Resource Management**: Provides cleanup methods for proper resource disposal

#### Read Operations

Data can be read using either a query identifier from the configuration file or a runtime-provided query dictionary. The system automatically determines whether to use Spark based on session availability.

#### Write Operations

Writing data follows the same pattern as reading, with support for different write modes including append, overwrite, and error-on-exists strategies.

### Data Source Factory

The `DataSourceFactory` uses the registry pattern to manage data source implementations. New data sources can be registered using a decorator, making the system easily extensible.

### Supported Data Sources

#### PostgreSQL Data Source

Provides connectivity to PostgreSQL databases with full support for both Spark DataFrames and Pandas DataFrames.

**Spark Mode**: Uses JDBC connections with the PostgreSQL driver for distributed data processing
**Non-Spark Mode**: Leverages SQLAlchemy and Pandas for direct database access

**Configuration Requirements**: Host, port, database name, username, and password must be provided

**Query Options**: Supports table names, SQL queries, and various JDBC/Pandas options

#### MinIO Data Source

Enables interaction with MinIO object storage, compatible with S3 API.

**Spark Mode**: Reads and writes data using Spark's S3 connector with support for multiple file formats
**Non-Spark Mode**: Uses Metaflow's S3 client for object operations

**Capabilities**: Supports single object operations and batch operations for multiple objects

**Format Support**: Parquet, CSV, JSON, Avro, and binary files in Spark mode

**Environment Requirements**: AWS credentials and endpoint URL must be set as environment variables

#### Cassandra Data Source

Placeholder implementation for Apache Cassandra integration. Methods are defined but not yet implemented, allowing for future expansion.

#### HDFS Data Source

Placeholder implementation for Hadoop Distributed File System integration. Methods are defined but not yet implemented, allowing for future expansion.

### Write Modes

All data sources support standard write modes:

- **append**: Adds data to existing tables or files
- **overwrite**: Replaces existing data
- **ignore**: Skips writing if data already exists
- **error/errorifexists**: Raises an error if data already exists

---

## Spark Integration

The Spark module provides utilities for managing remote Spark sessions with proper lifecycle management.

### Spark Session Creation

The library supports creating remote Spark sessions connected to a Spark cluster. Sessions are configured with a remote URL and an application name.

**Validation**: The remote URL is mandatory; missing URLs raise a SparkException

**Defaults**: If no application name is provided, a default name is used

### Session Lifecycle Management

#### Context Manager Pattern

The `remote_spark_session` context manager ensures proper session lifecycle:

- **Automatic Creation**: Session is created when entering the context
- **Resource Cleanup**: Session is automatically stopped when exiting the context
- **Exception Safety**: Cleanup occurs even if exceptions are raised
- **Manual Management**: For scenarios requiring manual control, explicit session creation and closure functions are provided.
- **Spark Configuration**: Spark configuration is managed through JSON configuration files, specifying the remote cluster URL and application name. This approach keeps infrastructure details separate from code.

---

## MLflow Integration

The MLflow module provides utilities for experiment tracking, model logging, and integration with popular machine learning frameworks.

### MLflow Utilities Class

The `MlflowUtils` class encapsulates common MLflow operations:

#### Initialization

Configures the MLflow tracking URI and sets up the experiment. The tracking server location and experiment name are specified during initialization.

#### PyTorch Autologging

Enables automatic logging of PyTorch training metrics, parameters, and models. The logging frequency can be configured to capture metrics at specified epoch intervals.

#### Dataset Logging

Provides methods to log training and validation datasets, ensuring complete reproducibility of experiments.

#### Dataset Splitting Utilities

Helper methods convert PyTorch datasets into MLflow-compatible format for logging features and targets from NumPy arrays.

### Decorators for MLflow Integration

The library provides several decorators for seamless MLflow integration in Metaflow workflows:

#### MLflow Setup Decorator

Configures the complete MLflow environment in a single step, including tracking URI, experiment name, and autologging settings. This decorator handles the initial setup before training begins.

#### Autolog Decorator

Enables framework-specific autologging for PyTorch, scikit-learn, or TensorFlow. Additional autologging parameters can be passed to customize behavior.

#### Experiment Management Decorators

Separate decorators allow setting the tracking URI and experiment name independently, providing fine-grained control over MLflow configuration.

#### Run Management Decorator

Starts an MLflow run with configurable tags, nested run support, system metrics logging, and run descriptions. The run is automatically closed after step execution.

#### Model Logging Decorator

Automatically logs PyTorch models with inferred signatures and input examples. The decorator extracts a sample batch from the dataloader, performs a forward pass to infer the model signature, and logs the complete model artifact.

---

## Metaflow Integration

The Metaflow module is the core of PyChaM3Leon, providing base flows, decorators, mutators, and a sophisticated template system for workflow generation.

### Base Flows

#### Configurable Flow

The `ConfigurableFlow` base class enables workflows to accept configuration files as parameters. This pattern externalizes configuration from code, making workflows more flexible and environment-agnostic.

**Configuration Parameter**: Requires a configuration file path via the `--config` parameter
**Required Parameter**: The configuration is mandatory for flow execution

#### Spark Flow

The `SparkFlow` extends `ConfigurableFlow` with automatic Spark session management. Steps containing the word "spark" in their name automatically receive a Spark session attribute.

**Automatic Session Lifecycle**: Spark sessions are created before step execution and cleaned up afterward
**Configuration Requirements**: The config file must include Spark connection details
**Step Naming Convention**: Only steps with "spark" in the name receive Spark sessions

### Decorators

The library provides a rich collection of decorators that add functionality to workflow steps:

#### Data Source Decorator

The `data_source` decorator abstracts data access by creating data source instances within workflow steps.

**Connection Management**: Automatically instantiates the appropriate data source class
**Configuration-Driven**: Reads connection parameters from the config file
**Step Isolation**: Data source instances exist only during step execution
**Spark Integration**: Automatically uses Spark when available

**Configuration Structure**: Requires a `data_sources` section in the config file with source type, connection ID, and connection parameters

**Attribute Creation**: Creates a named attribute on the flow object with read and write methods

#### Spark Session Decorator

The `spark_session_step_wrapper` manages Spark session lifecycle for individual steps.

**Remote Connection**: Creates a session connected to the specified remote cluster
**Application Naming**: Supports custom application names
**Automatic Cleanup**: Ensures sessions are properly closed after step execution

#### DataFrame Conversion Decorator

The `convert_dataframes_decorator` automatically converts Spark DataFrames to Pandas DataFrames after step execution, facilitating data transfer between Spark and non-Spark steps.

**Automatic Detection**: Scans all flow attributes for Spark DataFrames
**In-Place Conversion**: Replaces Spark DataFrames with Pandas equivalents
**Logging**: Reports each conversion for transparency

#### PyTorch Trainer Decorator

The `trainer_fit` decorator automates PyTorch model training by calling the trainer's fit method with the model and datamodule.

**Attribute Requirements**: Expects `model`, `datamodule`, and `trainer` attributes on the flow
**Error Handling**: Gracefully handles training failures with informative messages

### Mutators

#### Spark Mutator

The `SparkMutator` is a FlowMutator that automatically adds Spark functionality to workflow steps based on naming conventions.

**Step Detection**: Identifies steps with "spark" in their name
**Decorator Injection**: Automatically adds Spark session and DataFrame conversion decorators
**Configuration Validation**: Ensures the config file contains required Spark parameters

**Usage Pattern**: Can be used by extending `SparkFlow` or applied directly to `ConfigurableFlow` subclasses

---

## Template System

The template system is one of PyChaM3Leon's most powerful features, enabling declarative workflow generation through JSON configuration and Jinja2 templates.

### Template Architecture

The template system uses a hierarchical model architecture:

#### Template Rendering Model

The base abstraction for all template rendering, providing configuration processing and template rendering capabilities.

**Processing Pipeline**: Configuration data is processed before rendering
**Template Loading**: Uses Jinja2's file system loader with automatic whitespace control
**Rendering**: Combines processed data with templates to generate output

#### Template Aggregation Model

Extends the rendering model to compose multiple sub-models into a complete template.

**Sub-Model Management**: Coordinates multiple template models
**Processing Coordination**: Calls processing methods on sub-models before rendering

### Workflow Template Components

#### Metaflow Template

The top-level template that generates complete Metaflow workflow files.

**Components**: Combines imports and workflow class templates
**Processing**: Coordinates sub-model rendering and data flow
**Output**: Produces a complete Python file ready for execution

#### Imports Template

Manages import statement generation with conditional imports based on workflow features.

**Conditional Logic**: Adds imports only when corresponding features are used
**Feature Flags**: Responds to flags indicating parameter, config, or include file usage

#### Workflow Class Template

Generates the workflow class definition including all its components.

**Sub-Components**: Parameters, include files, configs, constructor, and steps
**Feature Detection**: Automatically determines which components to include based on configuration

#### Parameters Template

Renders Metaflow parameter declarations with proper formatting.

**Parameter Objects**: Converts parameter specifications into Metaflow Parameter objects
**Type Support**: Handles various parameter types including strings, integers, and floats

#### Include Files Template

Generates IncludeFile declarations for artifact dependencies.

**File References**: Specifies files that should be included in the workflow package
**Artifact Management**: Ensures required files are available during workflow execution

#### Configs Template

Renders Config parameter declarations for configuration file handling.

**Config Objects**: Creates Metaflow Config parameters
**Validation**: Ensures proper configuration structure

#### Steps Template

The most complex template, generating all step definitions with their decorators and logic.

**Step Detection**: Identifies the last step for automatic next step assignment
**Decorator Processing**: Formats decorator parameters and arguments
**Join Step Handling**: Adds input parameters to join steps
**Next Step Logic**: Automatically connects steps in the workflow graph

### Template File Structure

The template system uses eight Jinja2 template files:

- **metaflow_template.py.jinja**: Main template combining imports and workflow class
- **imports.py.jinja**: Import statement template
- **workflow_class.py.jinja**: Workflow class structure template
- **parameters.py.jinja**: Parameter declarations template
- **include_files.py.jinja**: IncludeFile declarations template
- **configs.py.jinja**: Config declarations template
- **steps.py.jinja**: Step definitions template

### Configuration Parser

The configuration parser reads JSON configuration files and generates workflow files through the template system.

**File Reading**: Loads JSON configuration with proper error handling
**Template Processing**: Instantiates the MetaflowTemplate with configuration data
**File Writing**: Saves rendered templates to specified output directories
**Path Management**: Creates output directories if they don't exist

**Workflow Directory**: Defaults to a workflows directory within the package but accepts custom paths

### Workflow Runner

The workflow runner executes generated workflows using Metaflow's Runner API.

**Execution**: Runs workflows from rendered template files
**Status Reporting**: Provides clear success or failure messages
**Integration**: Works seamlessly with generated workflow files

---

## Configuration Guide

PyChaM3Leon relies heavily on configuration files to control behavior without code changes.

### Configuration File Format

All configuration files use JSON format with a hierarchical structure.

### Spark Configuration

Spark configuration resides in a `spark` section:

**Required Fields**:

- `remote_url`: The URL of the Spark cluster
- `app_name`: The application name for Spark sessions

### Data Source Configuration

Data sources are configured in a `data_sources` section organized by source type and connection ID:

**Structure Hierarchy**:

1. Data sources section
2. Source type (postgres, minio, cassandra, hdfs)
3. Connection ID (user-defined identifier)
4. Connection parameters (host, port, credentials, etc.)
5. Queries section (optional, for predefined query configurations)

**Query Configuration**:
Each query has a unique query ID and contains parameters specific to the operation and data source type.

**PostgreSQL Query Parameters**:

- `dbtable`: Table name or SQL query
- `fetchsize`: Number of rows to fetch per round trip
- Additional JDBC or Pandas options

**MinIO Query Parameters**:

- `format`: Data format (parquet, csv, json, etc.)
- `bucket`: S3 bucket name
- `key` or `keys`: Object key(s)
- `mode`: Write mode (append, overwrite, etc.)
- Additional Spark or S3 options

### Workflow Template Configuration

Workflow templates use a structured JSON format:

**Top-Level Sections**:

- `imports`: List of import statements
- `class`: Workflow class definition

**Imports Structure**:
Can be simple strings for standard imports or objects with `from` and `elements` for selective imports.

**Class Structure**:

- `name`: Workflow class name
- `parameters`: List of parameter definitions (optional)
- `include_files`: List of included files (optional)
- `configs`: List of config parameters (optional)
- `constructor`: Constructor parameters (optional)
- `steps`: List of step definitions (required)

**Parameter Definition**:

- `variable_name`: Parameter variable name
- `object`: Dictionary of parameter properties (type, default, help, etc.)

**Step Definition**:

- `name`: Step name
- `decorators`: List of decorator specifications (optional)
- `next`: Next step name or list of next steps (optional)

**Decorator Specification**:

- `name`: Decorator name
- `parameters`: Dictionary of decorator parameters (optional)

---

## Usage Patterns

### Creating a Data Pipeline with Spark

A typical data pipeline using Spark involves extending the `SparkFlow` base class and configuring data sources in the config file. Steps with "spark" in their name automatically receive Spark sessions, allowing distributed data processing.

The workflow reads data from a source, processes it using Spark transformations, and writes results to a destination, all managed through decorators and configuration.

### Building an MLflow-Tracked Training Pipeline

Training pipelines benefit from MLflow integration for experiment tracking. The workflow starts by setting up MLflow with the tracking URI and experiment name, then uses autologging to capture metrics during training.

The training step receives a model and datamodule, with the trainer automatically logging metrics, parameters, and the final model to MLflow.

### Generating Workflows from Configuration

The most powerful pattern involves generating workflows from JSON configuration files. This approach separates workflow structure from implementation logic.

The configuration parser reads the JSON file, processes it through the template system, and generates a complete Python workflow file. This file can be executed immediately or modified for custom logic.

### Multi-Source Data Integration

Complex pipelines often need data from multiple sources. The data source decorator supports multiple connection IDs, allowing a single step to access different databases or storage systems.

Each data source is configured independently in the config file, and the decorator instantiates the appropriate connection for each source type.

### Environment-Specific Configuration

Using configuration files enables environment-specific deployments without code changes. Separate config files for development, staging, and production contain different connection parameters, cluster URLs, and resource allocations.

The same workflow code works across environments by simply changing the config file parameter.

---

## Best Practices

### Configuration Management

Always externalize environment-specific settings to configuration files. This includes database connections, Spark cluster URLs, MLflow tracking URIs, and resource allocations.

Use meaningful connection IDs that indicate the data source purpose rather than technical details. This improves configuration readability.

Validate configuration files before workflow execution to catch missing required fields early.

### Resource Management

Always use context managers or decorators for resource management. Spark sessions, database connections, and S3 clients should be automatically cleaned up after use.

Avoid manual resource management in workflow steps. Let decorators and mutators handle lifecycle concerns.

### Step Design

Keep steps focused on single responsibilities. Use the decorator pattern to add cross-cutting concerns like logging, data access, and resource management.

Name steps descriptively to indicate their purpose. Use the "spark" naming convention for steps requiring Spark sessions.

### Error Handling

Leverage the library's exception hierarchy for specific error handling. Catch specific exception types rather than generic exceptions to handle different failures appropriately.

Provide informative error messages in custom exceptions to aid debugging.

### Template Development

When creating workflow templates, start with simple configurations and incrementally add complexity. Test each component independently before composing complete workflows.

Use the template system for repeated workflow patterns. Custom templates can be created for organization-specific patterns.

### Testing

Test workflows with small datasets before scaling to production data volumes. Verify data source connections, Spark configurations, and MLflow tracking separately.

Use the workflow runner's status reporting to validate successful execution.

### Version Control

Store configuration files in version control alongside workflow code. This ensures reproducibility and enables tracking of configuration changes over time.

Separate sensitive credentials from configuration files. Use environment variables or secret management systems for passwords and API keys.

### Performance Optimization

When using Spark, configure appropriate partition sizes and executor resources in the Spark config. Monitor Spark UI to identify performance bottlenecks.

For data sources, use query options to limit data transfer. Fetch only required columns and apply filters at the source when possible.

Enable MLflow autologging selectively to avoid performance overhead from excessive logging.

### Documentation

Document custom decorators, data sources, and workflow templates for team collaboration. Include configuration examples and expected data formats.

Maintain a catalog of available data sources and their connection IDs for easy reference.

---

## Conclusion

PyChaM3Leon provides a comprehensive framework for building reproducible, scalable MLOps pipelines by integrating Metaflow, MLflow, and Apache Spark. Its declarative approach, powered by configuration files and templates, enables rapid development while maintaining code quality and operational excellence.

The library's modular architecture, extensive decorator system, and flexible data source abstractions support diverse use cases from simple training pipelines to complex multi-source data processing workflows. By following the patterns and practices outlined in this documentation, teams can build production-ready machine learning systems with confidence and efficiency.
