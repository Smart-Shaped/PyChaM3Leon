class SparkException(Exception):
    
    """
    Exception raised for errors related to Spark.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class MetaflowException(Exception):
    
    """
    Exception raised for errors related to Metaflow operations.

    Attributes:
        message -- explanation of the error
    """
    
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class DataSourceException(Exception):
    
    """
    Exception raised for errors related to data sources.

    Attributes:
        message -- explanation of the error
    """
    
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class MlflowException(Exception):
    
    """
    Exception raised for errors related to Mlflow operations.

    Attributes:
        message -- explanation of the error
    """
    
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
