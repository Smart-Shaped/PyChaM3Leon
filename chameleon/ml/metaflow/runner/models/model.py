from abc import ABC, abstractmethod
from jinja2 import Environment, FileSystemLoader


class TemplateRenderingModel(ABC):
    
    def __init__(self, input: dict, template_path: str, template_filename: str):
        
        """
        :param input: A dictionary containing the configuration data to be processed.
        :param template_path: path to the template folder
        :param template_filename: name of the template file to render
        :return: None
        """

        env = Environment(loader=FileSystemLoader(template_path), trim_blocks=True, lstrip_blocks=True)
        self.template = env.get_template(template_filename)
        self.data = self.process_config(input)
    
    @abstractmethod
    def process_config(self, input: dict) -> dict:
        pass
    
    def render(self) -> str:
        
        """
        Render the template using the processed configuration data.

        :return: The rendered template as a string
        """
        
        return self.template.render(**self.data)
    
class TemplateAggregationModel(TemplateRenderingModel):
    
    def __init__(self, input: dict, template_path: str, template_filename: str) -> None:

        """
        Initialize the TemplateAggregationModel instance.

        :param input: A dictionary containing the configuration data to be processed.
        :param template_path: The path to the template folder.
        :param template_filename: The name of the template file to render.
        :return: None
        """

        self.process_data_models()
        super().__init__(input=input, template_path=template_path, template_filename=template_filename)
        
    @abstractmethod
    def process_data_models(self):
        pass
