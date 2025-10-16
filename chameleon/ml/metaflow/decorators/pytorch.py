from metaflow import user_step_decorator


@user_step_decorator
def trainer_fit(step_name, flow, inputs=None, attributes=None):
    
    if flow.model is not None and flow.datamodule is not None:
        try:
            yield
            flow.trainer.fit(model=flow.model, datamodule=flow.datamodule)
        except Exception as e:
            print(f"Error during training: {e}")
