# PyChaM3Leon

ChaM3Leon is a Python library of helpers, templates and workflow components to build reproducible MLOps pipelines using Metaflow, MLflow and Apache Spark. It provides templating for Metaflow flows, utilities for MLflow integration, and Spark session helpers to simplify building data engineering and machine learning workflows.

## Features

- Metaflow templates and flow constructors (Jinja2 templates bundled in the package)
- MLflow helper utilities for experiment and run management
- Spark session helpers and mutators for reproducible environments
- Additional integration with various data sources like MinIO and PostgreSQL

## Installation

Install from PyPI (when published):

```powershell
pip install pycham3leon
```

Or install from the repository for development:

```powershell
pip install --no-cache-dir git+https://github.com/Smart-Shaped/PyChaM3Leon.git@public
```

Note: the package targets Python 3.9–3.12.

## License

This project is licensed under the Apache-2.0 License — see the `LICENSE` file for details.

## Publication

Article link — [ChaM3Leon announcement](https://www.smartshaped.com/blog/cham3leon-new-python-library)

## Contact

Smart-Shaped Srl — [AI & Big Data service](https://www.smartshaped.com/servizio/ai-and-big-data)

## Changelog

See `CHANGELOG.md` (not present yet) — consider adding a changelog for releases and notable changes.

## Templating JSON example

The package includes Jinja2-based templates to generate Metaflow workflows. Below is a minimal example of the JSON structure you can use as input for the templating engine. Save this as a JSON file (for example `flow_config.json`) and pass its content to the templating/constructor utilities in your code.

Example `flow_config.json`:

```json
{
  "imports": [
    "mlflow",
    {
      "from": "chameleon.ml.metaflow.decorators.data_sources",
      "elements": [
        "data_source"
      ]
    }
  ],
  "class": {
    "name": "ExampleWorkflow",
    "parameters": [
      {
        "variable_name": "input_path",
        "object": {
          "type": "str",
          "default": "\"s3://my-bucket/data/\"",
          "help": "\"Path to input data\""
        }
      }
    ],
    "steps": [
      {
        "name": "start",
        "decorators": [
          {
            "name": "data_source",
            "parameters": {
              "source_type": "source_type_value",
              "conn_id": "conn_id_value"
            }
          }
        ]
      },
      {
        "name": "train"
      },
      {
        "name": "end"
      }
    ]
  }
}
```

Notes:

- The exact fields required depend on which templating function you use from `chameleon.ml.runner.templates` — use the bundled templates under `chameleon/ml/runner/templates` as canonical examples.
- Keep parameter names, step names and action identifiers consistent with the template placeholders you intend to fill.

If you'd like, I can add a small example script that loads this JSON and renders one of the bundled templates — tell me which template to target and I will add it under `examples/`.
