from typing import Any

from nornir.core.task import Result, Task
from nornir_napalm.plugins.tasks import napalm_configure
from jinja2 import Environment, FileSystemLoader
from automation_lab.utils import fetch_source_of_truth_data, SourceOfTruthData

def orchestrate_config_sync(task: Task, **kwargs: Any) -> Result:
    """
    Orchestrates the configuration sync tasks to the device
    """
    # fetch data from source-of-truth
    source_of_truth_data = fetch_source_of_truth_data(task.host.name)
    # render configuration
    configuration_artifact = task.run(render_configuration, template_data=source_of_truth_data)
    # deploy to the device
    config_diff = task.run(napalm_configure, configuration=configuration_artifact.result, replace=True, dry_run=False)
    return Result(task.host, result=config_diff)


def render_configuration(task: Task, template_data: SourceOfTruthData, template_name: str = "base.j2", **kwargs: Any) -> Result:
    """
    Renders the configuration for the device
    """
    env = Environment(loader=FileSystemLoader('templates/'))
    template = env.get_template(template_name)
    rendered_config = template.render(data=template_data)
    return Result(host=task.host, result=rendered_config)
