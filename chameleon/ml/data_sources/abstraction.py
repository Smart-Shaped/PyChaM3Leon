from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pandas import DataFrame as PandasDataFrame
from pyspark.sql.connect.dataframe import DataFrame as PySparkDataFrame
from pyspark.sql.connect.session import SparkSession

from chameleon.ml.exceptions import DataSourceException


class DataSource(ABC):

    """
    Abstract base class for data sources.
    
    This interface defines the contract for data sources that can be loaded.
    Concrete implementations should handle the specifics of connecting to and retrieving
    data from their respective sources.
    """
    
    def __init__(self, queries: Dict = {}):

        """
        Initializes the data source with optional queries.

        :param queries: A dictionary of predefined queries or configurations.
        """

        self.queries = queries

    def read(self, query_id: Optional[str] = None, query_dict: Optional[Dict] = None) -> Any:
        
        """
        Reads data from the source.
        
        :param query_id: The query id from the configuration file.
        :param query_dict: A dictionary of parameters to override the query configuration.
        :return: The data read from the source.
        """
        
        if query_dict and query_id:
            raise DataSourceException("Only one of query_id or query_dict should be provided")
        elif not query_dict and not query_id:
            raise DataSourceException("One of query_id or query_dict must be provided")

        if query_id and query_id not in self.queries:
            raise DataSourceException(f"Query id {query_id} not found in configuration")

        if query_id:
            query_dict = self.queries.get(query_id, {})

        if self.spark and isinstance(self.spark, SparkSession):
            print("Reading with Spark")
            return self.read_with_spark(query_dict)
        else:
            print("Reading without Spark")
            return self.read_without_spark(query_dict)

    def write(self, data: Any, query_id: Optional[str] = None, query_dict: Optional[Dict] = None) -> None:
        
        """
        Writes data to the source.
        
        :param data: The data to be written.
        :param query_id: The query id from the configuration file.
        :param query_dict: A dictionary of parameters to override the query configuration.
        """
        
        if query_dict and query_id:
            raise DataSourceException("Only one of query_id or query_dict should be provided")
        elif not query_dict and not query_id:
            raise DataSourceException("One of query_id or query_dict must be provided")

        if query_id:
            query_dict = self.queries.get(query_id, {})

        if self.spark and isinstance(self.spark, SparkSession):
            print("Writing with Spark")
            self.write_with_spark(data, query_dict)
        else:
            print("Writing without Spark")
            self.write_without_spark(data, query_dict)

    @abstractmethod
    def read_with_spark(self, query_dict: Dict) -> PySparkDataFrame:

        """
        Reads data from the source using Spark.

        :param query_dict: The query dictionary from the configuration file.
        :return: The loaded data.
        """

        pass

    @abstractmethod
    def write_with_spark(self, data: PySparkDataFrame, query_dict: Dict) -> None:

        """
        Writes data to the source using Spark.
        
        :param data: The data to be written.
        :param query_dict: The query dictionary from the configuration file.
        """

        pass

    @abstractmethod
    def read_without_spark(self, query_dict: Dict) -> Any:

        """
        Reads data from the source without using Spark.

        :param query_dict: The query dictionary from the configuration file.
        :return: The loaded data.
        """

        pass

    @abstractmethod
    def write_without_spark(self, data: Any, query_dict: Dict) -> None:

        """
        Writes data to the source without using Spark.
        
        :param data: The data to be written.
        :param query_dict: The query dictionary from the configuration file.
        """

        pass

    @abstractmethod
    def close(self) -> None:

        """
        Closes the data source.
        """

        pass

class DataSourceFactory:
    
    """
    Factory class to create data source objects.
    """
    
    registry = {}
    
    @classmethod
    def register(cls, source_type):

        """
        Registers a data source class to the factory.
        
        :param source_type: The type of the data source.
        :return: Decorator function.
        """

        def inner_wrapper(wrapped_class):
            cls.registry[source_type] = wrapped_class
            return wrapped_class
        return inner_wrapper
    
    @classmethod
    def create(cls, source_type, spark, **kwargs):

        """
        Creates a data source instance.
        
        :param source_type: The type of the data source.
        :param spark: The Spark session.
        :param kwargs: Additional arguments for the data source constructor.
        :return: An instance of the data source.
        :raises DataSourceException: If the source type is not supported.
        """

        if source_type not in cls.registry:
            raise DataSourceException(f"Data source type not supported: {source_type}")
        return cls.registry[source_type](spark, **kwargs)
