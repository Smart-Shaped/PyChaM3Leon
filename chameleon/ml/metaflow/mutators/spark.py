from metaflow import FlowMutator

from chameleon.ml.metaflow.decorators.spark import spark_session_step_wrapper, convert_dataframes_decorator
from chameleon.ml.exceptions import SparkException


class SparkMutator(FlowMutator):
    
    """
    Mutator to set up a Spark session for a Metaflow flow.
    
    This mutator adds the convert_dataframes_decorator and spark_session_step_wrapper 
    decorator to each step in the flow that contains the word "spark" in its name.

    The result is that every step that contains the word "spark" in its name,
    has a spark attribute, which is an instance of SparkSession.
    The spark attribute is deleted after the step execution.

    If the mutator is used directly, e.g. if you don't extend the SparkFlow class,
    the config file must be passed as a parameter to the flow, and the class must 
    at least extend ConfigurableFlow.

    The config file must be in json format and contain the following structure:

    ```
    {
        "spark": {
            "remote_url": "the url of the spark cluster",
            "app_name": "the name of the spark application"
        }
    }
    ```

    Example usage of a flow that uses this mutator:
    ```
    python <script> --config config <config> run
    ```
    """
    
    def mutate(self, mutable_flow):

        if not hasattr(mutable_flow, 'config'):
            raise SparkException("The flow must extend ConfigurableFlow to use the SparkMutator")
        
        if not hasattr(mutable_flow.config, 'spark'):
            raise SparkException("The config file must contain the spark section")
        
        session_attributes = mutable_flow.config.spark
        
        for step_name, step in mutable_flow.steps:
            if "spark" in step_name:
                step.add_decorator(
                    convert_dataframes_decorator,
                    duplicates=step.IGNORE
                    )
                step.add_decorator(
                    spark_session_step_wrapper,
                    deco_kwargs=session_attributes,
                    duplicates=step.IGNORE
                    )
