from .model import TemplateRenderingModel, TemplateAggregationModel


class MetaflowTemplate(TemplateAggregationModel):
    
    template_filename = "metaflow_template.py.jinja"
    
    def __init__(self, input: dict, template_path: str) -> None:
        
        """
        :param input: A dictionary containing the configuration data to be processed.
        :param template_path: path to the template folder
        :return: None
        """
        
        try:
            self.imports = Imports(input["imports"], template_path=template_path)
        except KeyError:
            self.imports = Imports([], template_path=template_path)
        self.workflow_class = WorkflowClass(input["class"], template_path=template_path)
        
        super().__init__(input, template_path=template_path, template_filename=self.template_filename)
        
    def process_data_models(self):
        
        """
        Process the data models.
        
        This method processes the data models and calls the render methods of the
        imports and workflow_class to generate the metaflow template.
        
        :return: None
        """
        
        self.imports.set_add_parameters(self.workflow_class.add_parameters)
        self.imports.set_add_include_files(self.workflow_class.add_include_files)
        self.imports.set_add_configs(self.workflow_class.add_configs)
        
    def process_config(self, input: dict) -> dict:
        
        """
        Process the configuration input and return it.

        This method processes the configuration input by calling the render methods
        of the imports and workflow_class to generate the final configuration data.

        :param input: A dictionary containing the configuration data to be processed.
        :return: A dictionary with the processed configuration data.
        """

        input["imports"] = self.imports.render()
        input["workflow_class"] = self.workflow_class.render()
        
        return input

class Imports(TemplateRenderingModel):
    
    template_filename = "imports.py.jinja"
    
    def __init__(self, imports: list, template_path: str):
        
        """
        :param imports: list of imports to render
        :param template_path: path to the template folder
        :return: none
        """

        dict_imports = {"imports": imports}
        
        super().__init__(input=dict_imports, template_path=template_path, template_filename=self.template_filename)
    
    def process_config(self, input: dict) -> dict:
        
        """
        Process the configuration input and return it.

        :param input: A dictionary containing the configuration data to be processed.
        :return: A dictionary with the processed configuration data.
        """

        return input
    
    def set_add_parameters(self, add_parameters: bool):
        
        """
        Set the add_parameters flag in the data dict.
        
        :param add_parameters: the value to set the add_parameters flag to
        :type add_parameters: bool
        """
        
        self.data["add_parameters"] = add_parameters
        
    def set_add_include_files(self, add_include_files: bool):
        
        """
        Set the add_include_files flag in the data dict.

        :param add_include_files: the value to set the add_include_files flag to
        :type add_include_files: bool
        """
        
        self.data["add_include_files"] = add_include_files
        
    def set_add_configs(self, add_configs: bool):
        
        """
        Set the add_configs flag in the data dict.

        :param add_configs: the value to set the add_configs flag to
        :type add_configs: bool
        """
        
        self.data["add_configs"] = add_configs

class WorkflowClass(TemplateAggregationModel):
    
    template_filename = "workflow_class.py.jinja"
    
    def __init__(self, input: dict, template_path: str):
        
        """
        Initialize the WorkflowClass instance with the given configuration.

        :param input: A dictionary containing the configuration data to be processed.
        :param template_path: The path to the template folder.
        :return: None
        """
        
        try:
            self.parameters = Parameters(input["parameters"], template_path=template_path)
        except KeyError:
            self.parameters = Parameters([], template_path=template_path)
        try:
            self.include_files = IncludeFiles(input["include_files"], template_path=template_path)
        except KeyError:
            self.include_files = IncludeFiles([], template_path=template_path)
        try:
            self.configs = Configs(input["configs"], template_path=template_path)
        except KeyError:
            self.configs = Configs([], template_path=template_path)
        try:
            self.constructor = Constructor(input["constructor"], template_path=template_path)
        except KeyError:
            self.constructor = Constructor([], template_path=template_path)
        self.steps = Steps(input["steps"], template_path=template_path)
        
        super().__init__(input=input, template_path=template_path, template_filename=self.template_filename)
        self.process_data_models()
        
    def process_data_models(self):
        
        """
        Process the data models.
        
        This method processes the data models and calls the render methods of the
        parameters, include_files, constructor, and steps to generate the workflow
        class.
        
        :return: None
        """
        
        self.add_parameters = self.parameters.data != {"parameters": []}
        self.add_include_files = self.include_files.data != {"include_files": []}
        self.add_configs = self.configs.data != {"configs": []}
        
    def process_config(self, input: dict) -> dict:
        
        """
        Process the configuration input and return it.

        This method processes the configuration input by rendering parameters, 
        include files, configs, and steps, then updates the input dictionary 
        with these rendered components.

        :param input: A dictionary containing the configuration data to be processed.
        :return: A dictionary with the processed configuration data.
        """

        input["parameters"] = self.parameters.render()
        input["include_files"] = self.include_files.render()
        input["configs"] = self.configs.render()
        input["constructor"] = None
        input["steps"] = self.steps.render()
        
        return input

class Configs(TemplateRenderingModel):
    
    template_filename = "configs.py.jinja"
    
    def __init__(self, configs: list, template_path: str):
        
        dict_configs = {"configs": configs}
        
        super().__init__(input=dict_configs, template_path=template_path, template_filename=self.template_filename)
    
    def process_config(self, input: dict) -> dict:
        
        """
        Process the configuration input to format config objects.

        This method iterates over the list of configs in the input dictionary and 
        transforms each config's object into a list of strings with key-value pairs 
        formatted as "key=value".

        :param input: A dictionary containing the configuration data to be processed.
        :return: A dictionary with the processed configuration data.
        """

        for config in input["configs"]:
            config["object"] = [f"{key}={value}" for key, value in config["object"].items()]
        
        return input

class Parameters(TemplateRenderingModel):
    
    template_filename = "parameters.py.jinja"
    
    def __init__(self, parameters: list, template_path: str):

        """
        Initialize the Parameters instance with the given configuration.

        :param parameters: A list of parameters configurations data to render
        :param template_path: The path to the template folder
        """
        
        dict_parameters = {"parameters": parameters}
        
        super().__init__(input=dict_parameters, template_path=template_path, template_filename=self.template_filename)
    
    def process_config(self, input: dict) -> dict:
        
        """
        Process the configuration input to format parameter objects.

        This method iterates over the list of parameters in the input dictionary and 
        transforms each parameter's object into a list of strings with key-value pairs 
        formatted as "key=value".

        :param input: A dictionary containing the configuration data to be processed.
        :return: A dictionary with the processed configuration data.
        """
        
        for parameter in input["parameters"]:
            parameter["object"] = [f"{key}={value}" for key, value in parameter["object"].items()]
        
        return input
    
class IncludeFiles(TemplateRenderingModel):
    
    template_filename = "include_files.py.jinja"
    
    def __init__(self, include_files: list, template_path: str):

        """
        Initialize the IncludeFiles instance with the given configuration.

        :param include_files: A list of IncludeFile objects configurations to render
        :param template_path: The path to the template folder
        """
        
        dict_include_files = {"include_files": include_files}
        
        super().__init__(input=dict_include_files, template_path=template_path, template_filename=self.template_filename)
    
    def process_config(self, input: dict) -> dict:
        
        """
        Process the configuration input to format include file objects.
        This method iterates over the list of include files in the input dictionary and
        transforms each include file's object into a list of strings with key-value pairs
        formatted as "key=value".

        :param input: A dictionary containing the configuration data to be processed.
        :return: A dictionary with the processed configuration data.
        """
        
        for include_file in input["include_files"]:
            include_file["object"] = [f"{key}={value}" for key, value in include_file["object"].items()]

        return input
    
class Constructor(TemplateRenderingModel):
    
    template_filename = "constructor.py.jinja"
    
    def __init__(self, constructor: list, template_path: str):

        """
        :param constructor: list of parameters to be used in the constructor
        :param template_path: path to the template folder
        :return: None
        """
        
        dict_constructor = {"constructor": constructor}
        
        super().__init__(input=dict_constructor, template_path=template_path, template_filename=self.template_filename)
    
    def process_config(self, input: dict) -> dict:

        """
        Process the configuration input and return it.

        :param input: A dictionary containing the configuration data to be processed.
        :return: A dictionary with the processed configuration data.
        """
        
        return input
    
class Steps(TemplateRenderingModel):
    
    template_filename = "steps.py.jinja"
    
    def __init__(self, steps: list, template_path: str):

        """
        Initialize the Steps instance with the given configuration.

        :param steps: A list of steps configurations data to render
        :param template_path: The path to the template folder
        :return: None
        """
        
        dict_steps = {"steps": steps}
        
        super().__init__(input=dict_steps, template_path=template_path, template_filename=self.template_filename)
    
    def process_config(self, input: dict) -> dict:
        
        """
        Process the configuration input to prepare the steps for rendering.

        This method adjusts the configuration of steps by setting up the 'next' attribute
        for the last step to point to 'end'. If a step's 'next' attribute is a list, 
        it marks the step with 'multiple_next'. Additionally, it identifies and marks 
        join steps, which are steps that multiple other steps transition into.

        :param input: A dictionary containing the steps configuration data.
        :return: A dictionary with the processed steps configuration data.
        """
        
        steps = input["steps"]

        nexts = [step.get("next", "") for step in steps]

        for step in steps:
            
            # check if next is a list and set multiple_next as true
            if isinstance(step.get("next", ""), list):
                step["multiple_next"] = True
                step["next"] = [f"self.{next_step}" for next_step in step["next"]]
            
            # define join steps
            next_occurrences = nexts.count(step["name"])
            if next_occurrences > 1:
                step["join_step"] = True
                
            # fix decorators parameters
            if "decorators" in step.keys():
                for decorator in step["decorators"]:
                    if "parameters" in decorator.keys():
                        decorator["parameters"] = [f"{key}={value}" for key, value in decorator["parameters"].items()]
                
        return input
    