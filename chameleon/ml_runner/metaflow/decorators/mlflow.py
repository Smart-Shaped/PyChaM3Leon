from metaflow import user_step_decorator
from chameleon.ml_runner.exceptions import MetaflowException, MlflowException


@user_step_decorator
def mlflow_autolog_decorator(step_name, flow, inputs=None, attributes=None):
    
    """
    Decorator to enable MLflow autologging for a Metaflow step.

    This decorator enables MLflow autologging for a Metaflow step based on the
    specified flavor (pytorch, sklearn, or tensorflow).

    :param flavor: The MLflow flavor to be used for autologging. Must be one of 'pytorch', 'sklearn', or 'tensorflow'.
    :param autolog_params: Additional keyword arguments to be passed to the MLflow
            autologging function.

    :raises MetaflowException: If flavor is not provided or required keys are
        missing.
    """
    
    
    import mlflow
    
    flavor = attributes.get('flavor', None) if attributes else None
    autolog_params = attributes.get('autolog_params', {}) if attributes else {}
    
    if flavor is None:
        raise MetaflowException("Flavor must be specified for MLflow autologging.")
    
    # Enable autologging based on flavor
    if flavor == 'pytorch':
        mlflow.pytorch.autolog(**autolog_params)
        print("PyTorch autologging enabled")
    elif flavor == 'sklearn':
        mlflow.sklearn.autolog(**autolog_params)
        print("scikit-learn autologging enabled")
    elif flavor == 'tensorflow':
        mlflow.tensorflow.autolog(**autolog_params)
        print("TensorFlow autologging enabled")
    else:
        print(f"Warning: Autologging not configured for flavor: {flavor}")

    yield
    
@user_step_decorator
def set_experiment_decorator(step_name, flow, inputs=None, attributes=None):

    """
    Decorator to set the MLflow experiment name.

    This decorator sets the MLflow experiment name to the value provided in the
    'experiment_name' attribute of the step.

    :param experiment_name: The name of the MLflow experiment to be set.

    :raises MetaflowException: If experiment_name is not provided.
    """
    
    
    import mlflow

    experiment_name = attributes.get('experiment_name', None) if attributes else None
    
    if experiment_name is not None:
        mlflow.set_experiment(experiment_name)
        print(f"MLflow experiment set to: {experiment_name}")
        yield
    else:
        raise MetaflowException("MLflow experiment name not set.")

@user_step_decorator
def set_uri_decorator(step_name, flow, inputs=None, attributes=None):
            
    """
    Set the MLflow tracking URI for a Metaflow step.

    This decorator assigns a tracking URI to the decorated Metaflow step
    using the URI provided in the attributes.

    :param uri: The tracking URI to set for MLflow.
    
    :raises MetaflowException: If uri is not provided.
    """
    
    
    import mlflow

    uri = attributes.get('uri', None) if attributes else None        
    
    if uri is not None:
        mlflow.set_tracking_uri(uri)
        print(f"MLflow tracking URI set to: {uri}")
        yield
    else:
        raise MetaflowException("MLflow tracking URI not set.")
        
@user_step_decorator
def start_run_decorator(step_name, flow, inputs=None, attributes=None):
    
    """
    Start an MLflow run for a Metaflow step.

    This decorator starts an MLflow run for the decorated Metaflow step
    using the attributes provided in the attributes dictionary.

    :param step_name: The name of the step to be decorated.
    :param flow: The Metaflow flow object.
    :param inputs: The inputs to the step.
    :param attributes: A dictionary of attributes for the step. Must include:
        - tags: The tags to assign to the MLflow run.
        - nested: Whether the MLflow run should be nested.
        - log_system_metrics: Whether system metrics should be logged.
        - description: A description for the MLflow run.

    :yield: The result of the step after starting the MLflow run.
    """
    
    
    import mlflow
    
    tags = attributes.get('tags', {}) if attributes else {}
    nested = attributes.get('nested', False) if attributes else False
    log_system_metrics = attributes.get('log_system_metrics', True) if attributes else True
    description = attributes.get('description', "") if attributes else ""

    print(f"Starting MLflow run: {flow.model_class.__name__}")
    with mlflow.start_run(run_name=flow.model_class.__name__, nested=nested, tags=tags, log_system_metrics=log_system_metrics, description=description) as run:
        yield


# TODO condensare tutti questi decoratori in uno che effettua il setup di mlflow e uno che avvia la run e dopo fa il logging completo, sia del modello che della signature

@user_step_decorator
def mlflow_setup(step_name, flow, inputs=None, attributes=None):
    
    """
    Decorator to set up MLflow for a Metaflow step.

    :param uri: The tracking URI to set for MLflow.
    :param experiment_name: The name of the MLflow experiment to be set.
    :param flavor: The MLflow flavor to be used for autologging. Must be one of 'pytorch', 'sklearn', or 'tensorflow'.
    :param autolog_args: Additional keyword arguments to be passed to the MLflow
            autologging function.

    :raises MetaflowException: If uri is not provided.
    """
    
    import mlflow
    
    uri = attributes.get('uri', None) if attributes else None
    experiment_name = attributes.get('experiment_name', None) if attributes else None
    flavor = attributes.get('flavor', None) if attributes else None
    autolog_args = attributes.get('autolog_params', {}) if attributes else {}
    
    # Set up MLflow
    if uri is not None:
        mlflow.set_tracking_uri(uri=uri)
        print(f"MLflow tracking URI set to: {uri}")
    else:
        raise MetaflowException("MLflow tracking URI not set.")

    # Set up MLflow experiment
    if experiment_name is not None:
        mlflow.set_experiment(experiment_name=experiment_name)
        print(f"MLflow experiment set to: {experiment_name}")
    else:
        print("MLflow experiment name not set. Using default experiment.")

    # Enable autologging
    if flavor is not None:
        if flavor == 'pytorch':
            mlflow.pytorch.autolog(**autolog_args)
            print("PyTorch autologging enabled")
        elif flavor == 'sklearn':
            mlflow.sklearn.autolog(**autolog_args)
            print("scikit-learn autologging enabled")
        elif flavor == 'tensorflow':
            mlflow.tensorflow.autolog(**autolog_args)
            print("TensorFlow autologging enabled")
        else:
            mlflow.autolog(**autolog_args)
            print("Default MLflow autologging enabled")
    else:
        print("MLflow flavor not set. Skipping autologging.")
    
    yield
    
@user_step_decorator
def mlflow_log_model_decorator(step_name, flow, inputs=None, attributes=None):
    """
    Decorator to log a PyTorch model to MLflow.

    This decorator logs a PyTorch model to MLflow along with its input example and signature.
    It automatically infers the model signature by running a forward pass on a sample batch
    from the training dataloader.
    Accepted Batch structures are: torch.Tensor, dict, list, tuple, dataclasses.

    Args:
        step_name (str): Name of the Metaflow step
        flow (FlowSpec): The Metaflow flow object containing model and datamodule
        inputs (dict, optional): Input parameters to the step. Defaults to None.
        attributes (dict, optional): Additional attributes for logging. Defaults to None.

    Raises:
        MlflowException: If no tensor is found in the batch structure from dataloader
    """
    
    yield

    import mlflow
    import torch
    from mlflow.models.signature import infer_signature
    
    input_example = None
    if hasattr(flow, 'datamodule') and callable(flow.datamodule.train_dataloader) and flow.datamodule.train_dataloader() is not None:
        batch = next(iter(flow.datamodule.train_dataloader()))

        input_example = find_first_tensor(batch)

        if input_example is None:
            raise MlflowException("No tensor found in the batch structure. Accepted batch structures are: torch.Tensor, dict, list, tuple, dataclasses.")
        
        if hasattr(flow, 'model') and flow.model is not None:
            model = flow.model
            model.eval()
            with torch.no_grad():
                y = model(input_example)

            input_example = input_example.detach().cpu().numpy()

            signature = infer_signature(
                input_example,
                y.detach().cpu().numpy()
            )
        
            mlflow.pytorch.log_model(
                pytorch_model=flow.model,
                name="model",
                input_example=input_example,
                signature=signature
            )


def find_first_tensor(obj):
    """
    Recursively traverse batch-like structures until a tensor is found.
    Returns the first tensor (or a structure of tensors if directly at leaf).
    """
    import torch
 
    if isinstance(obj, torch.Tensor):
        return obj

    if isinstance(obj, dict):
        first_value = next(iter(obj.values()), None)
        return find_first_tensor(first_value) if first_value is not None else None

    if isinstance(obj, (list, tuple)):
        first_item = next(iter(obj), None)
        return find_first_tensor(first_item) if first_item is not None else None

    if hasattr(obj, "__dataclass_fields__"):
        first_field = next(iter(obj.__dataclass_fields__.keys()), None)
        if first_field is not None:
            return find_first_tensor(getattr(obj, first_field))

    return None
