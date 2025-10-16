from typing import Any
from pyspark.sql.connect.dataframe import DataFrame as PySparkDataFrame
from pandas import DataFrame as PandasDataFrame
from metaflow.plugins.datatools.s3.s3 import S3Object
from typing import List, Dict

from chameleon.ml.exceptions import DataSourceException
from chameleon.ml.data_sources.abstraction import DataSource, DataSourceFactory


ALLOWED_WRITE_MODES = ["append", "overwrite", "ignore", "error", "errorifexists"]

@DataSourceFactory.register("postgres")
class PostgresDataSource(DataSource):

    """
    Data source for PostgreSQL databases.
    """

    def __init__(self, spark, host, port, database, username, password, queries: dict = {}):
        
        super().__init__(queries)

        self.spark = spark
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password

        # mandatory inputs from the config file
        if not self.host or not self.port or not self.database or not self.username or not self.password:
            raise DataSourceException("PostgresDataSource requires host, port, database, username, and password")

    def read_with_spark(self, query_dict: Dict) -> PySparkDataFrame:

        """
        Reads data from the source using Spark.

        :param query_dict: The query dictionary from the configuration file.
        :return: The DataFrame read from the source.
        """

        query = query_dict

        # initialize spark datareader
        reader = self.spark.read.format("jdbc") \
            .option("url", f"jdbc:postgresql://{self.host}:{self.port}/{self.database}") \
            .option("user", self.username) \
            .option("password", self.password) \
            .option("driver", "org.postgresql.Driver")

        # add spark query options
        for key, value in query.items():
            reader = reader.option(key, value)

        try:
            return reader.load()
        except Exception as e:
            raise DataSourceException(f"Error reading with Spark: {e}")

    def write_with_spark(self, data: PySparkDataFrame, query_dict: Dict) -> None:

        """
        Writes data to the source using Spark.

        :param data: The DataFrame or pandas DataFrame to be written.
        :param query_dict: The query dictionary from the configuration file.
        """

        # check if data is provided correctly
        if not data:
            raise DataSourceException("DataFrame not provided")
        elif not isinstance(data, PySparkDataFrame):
            raise DataSourceException(f"Type {type(data)} not supported")

        query = query_dict
        
        # check if write mode is allowed
        write_mode = query.get("mode", "append")
        if write_mode not in ALLOWED_WRITE_MODES:
            raise DataSourceException(f"Write mode {write_mode} not supported")

        # initialize spark datawriter
        writer = data.write \
            .mode(write_mode) \
            .format("jdbc") \
            .option("url", f"jdbc:postgresql://{self.host}:{self.port}/{self.database}") \
            .option("user", self.username) \
            .option("password", self.password) \
            .option("driver", "org.postgresql.Driver") \

        # add spark query options   
        for key, value in query.items():
            writer = writer.option(key, value)

        try:
            writer.save()
            print("Data written to Postgres")
        except Exception as e:
            raise DataSourceException(f"Error writing with Spark: {e}")

    def read_without_spark(self, query_dict: Dict) -> PandasDataFrame:
        
        """
        Reads data from the source without using Spark.

        :param query_dict: The query dictionary from the configuration file.
        :return: The data read from the source.
        """

        import pandas as pd
        from sqlalchemy import create_engine

        query = query_dict

        engine = create_engine(f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}")
        
        return pd.read_sql(con=engine, **query)

    def write_without_spark(self, data: PandasDataFrame, query_dict: Dict) -> None:
        
        """
        Writes data to the source without using Spark.

        :param data: The DataFrame to be written.
        :param query_dict: The query dictionary from the configuration file.
        """

        from sqlalchemy import create_engine

        query = query_dict

        engine = create_engine(f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}")
        data.to_sql(con=engine, **query)
        print("Data written to Postgres")

    def close(self) -> None:

        """
        Closes the data source.
        """

        pass

# TODO implement methods
@DataSourceFactory.register("cassandra")
class CassandraDataSource(DataSource):

    """
    Data source for Cassandra.
    """

    def __init__(self, spark, host, port, keyspace, table, queries: dict = {}):
        
        super().__init__(queries)

        self.spark = spark
        self.host = host
        self.port = port
        self.keyspace = keyspace
        self.table = table

    def read_with_spark(self, query_dict: Dict) -> PySparkDataFrame:
        raise DataSourceException("read_with_spark not implemented for CassandraDataSource")

    def write_with_spark(self, data: Any, query_dict: Dict) -> None:
        raise DataSourceException("write_with_spark not implemented for CassandraDataSource")

    def read_without_spark(self, query_dict: Dict) -> Any:
        raise DataSourceException("read_without_spark not implemented for CassandraDataSource")

    def write_without_spark(self, data: Any, query_dict: Dict) -> None:
        raise DataSourceException("write_without_spark not implemented for CassandraDataSource")

    def close(self) -> None:

        """
        Closes the data source.
        """

        pass

# TODO implement methods
@DataSourceFactory.register("minio")
class MinioDataSource(DataSource):

    """
    Data source for MinIO.
    """

    def __init__(self, spark, host, port, access_key, secret_key, queries: dict = {}):
        
        super().__init__(queries)

        self.spark = spark
        self.host = host
        self.port = port
        self.access_key = access_key
        self.secret_key = secret_key

        if not host or not port or not access_key or not secret_key:
            raise DataSourceException("MinioDataSource requires host, port, access_key, secret_key")

    def read_with_spark(self, query_dict: Dict) -> PySparkDataFrame:

        """
        Reads data from the source using Spark.

        :param query_dict: The query dictionary from the configuration file.
        :return: The loaded data.
        """

        query = query_dict

        if "format" not in query:
            raise DataSourceException("MinioDataSource requires format")
        if "bucket" not in query:
            raise DataSourceException("MinioDataSource requires bucket")
        if "key" not in query:
            raise DataSourceException("MinioDataSource requires key")

        # define reader
        reader = self.spark.read \
            .format(query["format"]) \

        # add spark query options
        for key, value in query.items():
            reader = reader.option(key, value)
        
        return reader \
            .load(f"s3a://{query['bucket']}/{query['key']}")

    def write_with_spark(self, data: PySparkDataFrame, query_dict: Dict) -> None:

        """
        Writes data to the source using Spark.

        :param data: The DataFrame to be written.
        :param query_dict: The query dictionary from the configuration file.
        """

        # check if data is provided correctly
        if not data:
            raise DataSourceException("DataFrame not provided")
        elif not isinstance(data, PySparkDataFrame):
            raise DataSourceException(f"Type {type(data)} not supported")

        query = query_dict

        if "format" not in query:
            raise DataSourceException("MinioDataSource requires format")
        elif query["format"] == "binaryFile":
            raise DataSourceException("Spark does not support binaryFile format in write mode")
        if "bucket" not in query:
            raise DataSourceException("MinioDataSource requires bucket")
        if "key" not in query:
            raise DataSourceException("MinioDataSource requires key")

        # check if write mode is allowed
        write_mode = query.get("mode", "append")
        if write_mode not in ALLOWED_WRITE_MODES:
            raise DataSourceException(f"Write mode {write_mode} not supported")

        writer = data.write \
            .mode(write_mode) \
            .format(query["format"])

        # add spark query options
        for key, value in query.items():
            writer = writer.option(key, value)

        writer.save(f"s3a://{query['bucket']}/{query['key']}")
        print("Data written to Minio")

    def read_without_spark(self, query_dict: Dict) -> S3Object | List[S3Object]:

        """
        Reads data from the source without using Spark.

        :param query_dict: The query dictionary from the configuration file.
        :return: The loaded data.
        """
        
        import os
        from metaflow import S3

        query = query_dict
        
        if "key" not in query and "keys" not in query:
            raise DataSourceException("MinioDataSource requires key or keys")
        if "keys" in query and "key" in query:
            raise DataSourceException("MinioDataSource requires only one of key or keys")
        
        tmproot = query.get("tmproot", '.')

        # verify environment variables are set correctly
        if os.environ.get("AWS_ACCESS_KEY_ID") != self.access_key:
            raise DataSourceException("AWS_ACCESS_KEY_ID environment variable does not match provided access key")
        if os.environ.get("AWS_SECRET_ACCESS_KEY") != self.secret_key:
            raise DataSourceException("AWS_SECRET_ACCESS_KEY environment variable does not match provided secret key")
        if os.environ.get("METAFLOW_S3_ENDPOINT_URL") != f"http://{self.host}:{self.port}":
            raise DataSourceException("METAFLOW_S3_ENDPOINT_URL environment variable does not match provided host and port")

        # read object from minio
        self.s3 = S3(tmproot=tmproot)
        
        if "keys" in query:
            objs = self.s3.get_many(keys=query["keys"])
            return objs
        elif "key" in query:
            obj = self.s3.get(key=query['key'])
            return obj

    def write_without_spark(self, data: Any, query_dict: Dict) -> None:
        
        import os
        from metaflow import S3

        query = query_dict
        if "key" not in query and "key_objs" not in query and "key_paths" not in query:
            raise DataSourceException("MinioDataSource requires key or key_objs or key_paths")
        if "key" in query and ("key_objs" in query or "key_paths" in query):
            raise DataSourceException("MinioDataSource requires only one of key or key_objs or key_paths")
        if "key_objs" in query and "key_paths" in query:
            raise DataSourceException("MinioDataSource requires only one of key_objs or key_paths")

        # verify environment variables are set correctly
        if os.environ.get("AWS_ACCESS_KEY_ID") != self.access_key:
            raise DataSourceException("AWS_ACCESS_KEY_ID environment variable does not match provided access key")
        if os.environ.get("AWS_SECRET_ACCESS_KEY") != self.secret_key:
            raise DataSourceException("AWS_SECRET_ACCESS_KEY environment variable does not match provided secret key")
        if os.environ.get("METAFLOW_S3_ENDPOINT_URL") != f"http://{self.host}:{self.port}":
            raise DataSourceException("METAFLOW_S3_ENDPOINT_URL environment variable does not match provided host and port")

        # write object to minio
        self.s3 = S3()
        if "key" in query:
            self.s3.put(key=query['key'], obj=data)
        elif "key_objs" in query:
            self.s3.put_many(key_objs=query["key_objs"])
        elif "key_paths" in query:
            self.s3.put_files(key_paths=query["key_paths"])
        print("Data written to Minio")

    def close(self) -> None:

        """
        Closes the data source.
        """
        
        for query_id in self.queries.keys():
            query = self.queries[query_id]
            if hasattr(self, "s3") and query.get("close_s3", True):
                self.s3.close()

# TODO implement methods
@DataSourceFactory.register("hdfs")
class HdfsDataSource(DataSource):

    """
    Data source for HDFS.
    """

    def __init__(self, spark, host, port, path, queries: dict = {}):
        
        super().__init__(queries)

        self.spark = spark
        self.host = host
        self.port = port
        self.path = path

    def read_with_spark(self, query_dict: Dict) -> PySparkDataFrame:
        raise DataSourceException("read_with_spark not implemented for HdfsDataSource")

    def write_with_spark(self, data: Any, query_dict: Dict) -> None:
        raise DataSourceException("write_with_spark not implemented for HdfsDataSource")

    def read_without_spark(self, query_dict: Dict) -> Any:
        raise DataSourceException("read_without_spark not implemented for HdfsDataSource")

    def write_without_spark(self, data: Any, query_dict: Dict) -> None:
        raise DataSourceException("write_without_spark not implemented for HdfsDataSource")

    def close(self) -> None:

        """
        Closes the data source.
        """

        pass
