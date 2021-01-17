import json
from pathlib import Path
from typing import Dict, List, Set, Tuple

from aptmarkreason.registry.package_registry import PackageRegistry, ReasonStatus

REGISTRY_PATH = Path.home() / ".config" / "aptmarkreason"
REGISTRY_FILENAME = "package_registry.json"
REGISTRY_FILE = REGISTRY_PATH / REGISTRY_FILENAME


def package_registry_to_json_structure(
    package_registry: PackageRegistry,
) -> Tuple[Dict[str, ReasonStatus], Set[Tuple[str, str]]]:
    return package_registry.status_by_reason, package_registry.package_reasons


def json_structure_to_package_registry(
    json_structure: Tuple[Dict[str, str], List[Tuple[str, str]]]
) -> PackageRegistry:
    return PackageRegistry.create_from_reasons_and_packages(
        new_status_by_reason={
            reason: ReasonStatus(status)
            for reason, status in json_structure[0].values()
        },
        new_package_reasons=set(json_structure[1]),
    )


def save_package_registry(package_registry: PackageRegistry):
    if not REGISTRY_FILE.parent.is_dir():
        REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(REGISTRY_FILE, "w") as file:
        json.dump(package_registry_to_json_structure(package_registry), file)


def load_package_registry() -> PackageRegistry:
    if REGISTRY_FILE.is_file():
        with open(REGISTRY_FILE, "r") as file:
            json_structure = json.load(file)
        return json_structure_to_package_registry(json_structure)
    else:
        return PackageRegistry.new()
