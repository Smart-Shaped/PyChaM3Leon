import mlflow


class MlflowUtils:

    def __init__(self, mlflow_uri: str, experiment_name: str):
        
        """
        Initialize the MlflowUtils instance.

        :param mlflow_uri: The URI for the MLflow tracking server.
        :param experiment_name: The name of the experiment to be set in MLflow.
        """

        self.mlflow_uri = mlflow_uri
        mlflow.set_tracking_uri(uri=self.mlflow_uri)
        self.experiment_name = experiment_name
        self.experiment = mlflow.set_experiment(experiment_name=self.experiment_name)

    def pytorch_autolog(self, log_every_n_epoch: int):
        
        """
        Enable automatic logging of PyTorch metrics and parameters.

        :param log_every_n_epoch: How often to log in terms of epochs
        :type log_every_n_epoch: int
        """
        
        mlflow.pytorch.autolog(log_every_n_epoch=log_every_n_epoch)

    def log_dataset(self, train_data, eval_data):
        mlflow.log_input(dataset=train_data, context="training")
        mlflow.log_input(dataset=eval_data, context="validation")

    def split_train_data(self, dataset):
        return mlflow.data.from_numpy(features=dataset.X_train.numpy(), targets=dataset.y_train.numpy())

    def split_eval_data(self, dataset):
        return mlflow.data.from_numpy(features=dataset.X_val.numpy(), targets=dataset.y_val.numpy())
