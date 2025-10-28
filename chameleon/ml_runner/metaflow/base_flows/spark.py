from chameleon.ml_runner.metaflow.mutators.spark import SparkMutator
from chameleon.ml_runner.metaflow.base_flows.config import ConfigurableFlow


@SparkMutator
class SparkFlow(ConfigurableFlow):
    
    """
    Base class for Spark flows, it requires a Spark configuration file, set via the config parameter.

    In every step of the flow that contains the word "spark" in its name, a spark attribute is available, 
    which is an instance of SparkSession.
    The spark attribute is deleted after the step execution.
    
    The config file must be in json format and contain the following structure:

    ```
    {
        "spark": {
            "remote_url": "the url of the spark cluster",
            "app_name": "the name of the spark application"
        }
    }
    ```

    Example usage of a flow that extends this class:
    ```
    python <script> --config config <config> run
    ```
    """
