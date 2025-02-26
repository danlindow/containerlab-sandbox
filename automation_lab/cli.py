import typer
from automation_lab.utils import init_nornir
from automation_lab.tasks import orchestrate_config_sync
from nornir_utils.plugins.functions import print_result
import logging
from pathlib import Path
from nornir.core.task import Result, Task

app = typer.Typer()

# Set up logging to console and file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler()
    ]
)

@app.command()
def sync_configs(hosts_inventory: Path, device_name: str = "all"):
    """
    Renders and deploys the templated configurations to the devices
    """
    logging.info(f"found hosts inventory: {hosts_inventory}")
    nr = init_nornir(hosts_inventory)
    if device_name != "all":
        nr = nr.filter(name=device_name)
    result = nr.run(orchestrate_config_sync)
    typer.echo(print_result(result))


def run():
    app()
