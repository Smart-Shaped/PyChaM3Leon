from metaflow import user_step_decorator

from chameleon.ml_runner.spark.sessions import remote_spark_session, create_spark_session
from chameleon.ml_runner.exceptions import MetaflowException


@user_step_decorator
def spark_session_step_wrapper(step_name, flow, inputs=None, attributes=None):
    
    """
    Decorator to manage a Spark session for a Metaflow step.

    This decorator sets up a remote Spark session using the provided attributes
    and manages the session lifecycle for the decorated step.
    
    The Spark session is closed at the end of the step.

    :param remote_url: The URL of the remote Spark cluster.
    :param app_name: The name of the Spark application. Defaults to "spark app" if not provided.

    :raises MetaflowException: If remote_url is not provided.
    """

    remote_url = attributes.get('remote_url', None) if attributes else None
    app_name = attributes.get('app_name', "") if attributes else ""
    
    if remote_url is None:
        raise MetaflowException("Remote URL for Spark session is required in attributes.")
    
    with remote_spark_session(remote_url, app_name) as spark:
        flow.spark = spark
        try:
            yield
        finally:
            del flow.spark

@user_step_decorator
def convert_dataframes_decorator(step_name, flow, inputs=None, attributes=None):
    
    """
    Decorator to convert Spark DataFrames to Pandas DataFrames for a Metaflow step.

    This decorator automatically converts all Spark DataFrames to Pandas DataFrames
    after the decorated step has finished running.
    """

    yield
    
    members = [member for member in dir(flow) if not member.startswith("_") and not member.startswith("__")]
    
    from pyspark.sql.connect.dataframe import DataFrame
    
    for member in members:
        member_object = getattr(flow, member)
        if isinstance(member_object, DataFrame):
            setattr(flow, member, member_object.toPandas())
            print(f"Converted Spark DataFrame to Pandas DataFrame: {member}")
