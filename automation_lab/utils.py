from pathlib import Path
from nornir import InitNornir
from nornir.core import Nornir
import yaml
from dataclasses import dataclass

def init_nornir(simple_inventory_path: Path) -> Nornir:
    return InitNornir(
        runner={
            "plugin": "threaded",
            "options": {
                "num_workers": 100,
            },
        },
        logging={
            "enabled": False
        },
        inventory={
            "plugin": "SimpleInventory",
            "options": {
                "host_file": simple_inventory_path.resolve(),
                "defaults_file": "inventory/defaults.yaml"
            }
        }
)

@dataclass
class SourceOfTruthData:
    hostname: str
    device_data: dict
    global_data: dict

def fetch_source_of_truth_data(hostname) -> SourceOfTruthData:
    """
    acts as a static source of truth provider of data
    """
    with open('inventory/source_of_truth.yaml', "r") as f:
        source_of_truth_data = yaml.safe_load(f)
        return SourceOfTruthData(
            hostname=hostname,
            device_data=source_of_truth_data.get("hosts").get(hostname),
            global_data=source_of_truth_data.get('globals')
        )