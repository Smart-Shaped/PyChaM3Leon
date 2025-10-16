from metaflow import Runner


def run_workflow(rendered_path: str):
    
    """
    Run a rendered Metaflow workflow.

    This function will run a Metaflow workflow from a rendered template at the given path.

    :param rendered_path: The path to the rendered Metaflow workflow template.
    :return: None
    """
    
    with Runner(rendered_path).run() as running:
        if running.status == 'failed':
            print(f'❌ {running.run} failed:')
        elif running.status == 'successful':
            print(f'✅ {running.run} succeeded:')
