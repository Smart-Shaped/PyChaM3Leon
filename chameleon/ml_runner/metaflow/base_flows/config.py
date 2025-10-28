from metaflow import FlowSpec, Config


class ConfigurableFlow(FlowSpec):

    """
    Base class for flows that require a configuration file.

    Example usage of a flow that uses this base flow:
    ```
    python <script> --config config <config> run
    ```
    """

    config = Config(
        name="config",
        help="Configuration file", 
        required=True,
        )
