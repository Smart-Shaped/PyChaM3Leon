from metaflow import user_step_decorator

from chameleon.ml.exceptions import DataSourceException
from chameleon.ml.data_sources.abstraction import DataSourceFactory
from chameleon.ml.data_sources.implementations import *


@user_step_decorator
def data_source(step_name, flow, inputs=None, attributes=None):

    """
    Decorator to access data from different sources.

    The decorator will try to use Spark if available.
    
    This decorator provides a way to read datasets from different sources
    and abstract away the underlying complexity of the source.

    The decorator create a {conn_id} attribute, accessible only in the decorated step.
    The attribute is an instance of the data source class and it provides a read and a write method.
    The {conn_id} attribute is deleted after the step execution.

    This decorator requires that connection parameters are defined in the config file, so the flow must extend the ConfigurableFlow class.
    The config file must be in json format and contain the following structure:

    ```
    {
        "data_sources": {
            "source_type": {
                "conn_id": {
                    "param1": "value1",
                    "param2": "value2",
                    ...
                    "queries": {
                        "query_id": {
                            ...
                        }
                    }
                }
            }
        }
    }
    ```

    Where the dictionary bound assigned to conn_id contains the connection parameters, like host and port.
    The queries key is used to store different combinations of additional parameters to pass to the data source constructor.
    Every query has a query_id that must be passed to the read and write methods of the DataSource object.
    - if spark is used to read or write, the query_id key is used to pass additional options to the spark DataFrameReader or DataFrameWriter.
    - if spark is not used, the query_id key is used to pass additional parameters to the specific method.
        - in case of relational databases, the query_id key is used to pass additional parameters to the 
        pandas.read_sql() and pandas.DataFrame.to_sql() methods.
    
    :param source_type: The type of the source.
    :param conn_id: The id of the connection.
    """

    source_type = attributes.get('source_type', None) if attributes else None
    conn_id = attributes.get('conn_id', None) if attributes else None

    # validation
    if source_type is None:
        raise DataSourceException("source_type is required")
    elif source_type not in DataSourceFactory.registry:
        raise DataSourceException(f"Data source type not supported: {source_type}")
    if conn_id is None:
        raise DataSourceException("conn_id is required")
    elif conn_id in dir(flow):
        raise DataSourceException(f"Variable {conn_id} already exists")
    if not hasattr(flow, 'config'):
        raise DataSourceException("The flow must extend ConfigurableFlow to use the data_source decorator")
    elif not hasattr(flow.config, 'data_sources'):
        raise DataSourceException("The config file must contain the data_sources section")
    elif not hasattr(flow.config.data_sources, source_type):
        raise DataSourceException(f"The config file must contain the {source_type} section")
    elif not hasattr(flow.config.data_sources[source_type], conn_id):
        raise DataSourceException(f"The config file must contain the {conn_id} section for {source_type}")
    if not hasattr(flow, 'spark'):
        flow.spark = None

    connection_params = flow.config.data_sources[source_type][conn_id]

    print(f"Instantiating data source {source_type} with name {conn_id}")
    
    data_source = DataSourceFactory.create(source_type, flow.spark, **connection_params)
    setattr(flow, conn_id, data_source)

    try:
        yield
    finally:
        data_source.close()
        delattr(flow, conn_id)
