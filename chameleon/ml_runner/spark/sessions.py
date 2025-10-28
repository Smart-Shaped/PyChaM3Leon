from pyspark.sql import SparkSession

from chameleon.ml_runner.exceptions import SparkException


APP_NAME_DEFAULT = "spark app"

def create_spark_session(remote_url: str, app_name: str = "") -> SparkSession:
    
    """
    Create and return a SparkSession connected to a remote cluster.

    This function initializes a SparkSession using a specified remote URL and
    application name. If no remote URL is provided, it raises a SparkException.

    :param remote_url: The URL of the remote Spark cluster.
    :param app_name: The name of the Spark application. Defaults to "spark app".
    :return: The created SparkSession.
    :raises SparkException: If the remote URL is not provided.
    """

    if not remote_url:
        raise SparkException("Remote URL must be provided to create a Spark session.")
    
    if app_name.strip() == "":
        app_name = APP_NAME_DEFAULT
    
    spark = SparkSession.builder \
        .remote(remote_url) \
        .appName(app_name) \
        .getOrCreate()
        
    return spark

def close_spark_session(spark: SparkSession):
    
    """
    Close the given SparkSession.

    :param spark: the SparkSession to close
    """
    
    spark.stop()
    
class remote_spark_session():
    
    def __init__(self, remote_url: str, app_name: str = APP_NAME_DEFAULT):
        
        """
        Initialize the remote_spark_session context manager.

        :param remote_url: the url of the Spark cluster
        :param app_name: the name of the Spark application
        """
        
        self.remote_url = remote_url
        self.app_name = app_name
    
    def __enter__(self) -> SparkSession:
        
        """
        Enter the runtime context related to this object.

        This method creates and returns a remote SparkSession with the specified 
        remote URL and application name. It also prints a message indicating that 
        a Spark session has been created.

        :return: The created SparkSession.
        """

        self.spark = create_spark_session(remote_url=self.remote_url, app_name=self.app_name)
        print("spark session created")
        return self.spark
    
    def __exit__(self, exc_type, exc_value, traceback):
        
        """
        Exit the runtime context related to this object.

        This method closes the SparkSession and prints a message indicating 
        that the Spark session has been closed.

        :param exc_type: The exception type (if an exception is raised).
        :param exc_value: The exception value (if an exception is raised).
        :param traceback: The traceback object (if an exception is raised).
        :return: None
        """

        close_spark_session(self.spark)
        print("spark session closed")
