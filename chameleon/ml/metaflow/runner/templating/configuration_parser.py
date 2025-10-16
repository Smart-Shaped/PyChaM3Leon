import os
import json
from pathlib import Path
from io import StringIO
from chameleon.ml.metaflow.runner.models.metaflow_template import MetaflowTemplate


def read_config_file(path: str) -> dict:
    
    """
    Read a JSON configuration file and return its content as a dictionary.

    :param path: path to the configuration file
    :return: dictionary containing the configuration data
    """
    
    with open(path, "r") as f:
        return json.load(f)
    
def write_rendered_file(path: str, content: str):
    
    """
    Write a rendered template to a file at the given path.

    :param path: The path to the file to write
    :param content: The rendered template content to write
    :return: None
    """
    
    with open(path, "w") as f:
        f.write(content)

def generate_workflow(config_path: str, workflow_dir: str) -> str:
    
    """
    Generate a workflow file from a configuration file and return its path.

    This function reads a configuration file, processes its contents, and uses 
    a template to generate a workflow Python file. The workflow file is saved 
    in a specified directory or a default workflows directory if none is provided. 
    The function returns the path to the generated workflow file.

    :param config_path: The path to the configuration file.
    :param workflow_dir: The directory where the workflow file will be saved. 
                         If empty, a default directory is used.
    :return: The path to the generated workflow file.
    """

    runner_dir = str(Path(__file__).resolve().parents[1])
    
    template_path = os.path.join(runner_dir, 'templates')
    if workflow_dir == '':
        workflow_dir = os.path.join(runner_dir, 'workflows')
    
    os.makedirs(workflow_dir, exist_ok=True)
    
    config = read_config_file(config_path)
    
    template = MetaflowTemplate(config, template_path)
    
    class_name = config["class"]["name"]
    rendered_path = os.path.join(workflow_dir, f"{class_name}.py")
    write_rendered_file(rendered_path, template.render())
    
    return rendered_path
