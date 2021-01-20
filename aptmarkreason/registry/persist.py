import json
from pathlib import Path
from typing import Dict, List, Set, Tuple

from registry.package_registry import (
    PackageReason,
    PackageReasons,
    PackageRegistry,
    ReasonStatus,
    StatusByReason,
)

REGISTRY_PATH = Path.home() / ".config" / "aptmarkreason"
REGISTRY_FILENAME = "package_registry.json"
REGISTRY_FILE = REGISTRY_PATH / REGISTRY_FILENAME


def package_registry_to_json_structure(
    package_registry: PackageRegistry,
) -> Tuple[StatusByReason, PackageReasons]:
    return package_registry.status_by_reason, package_registry.package_reasons


def json_structure_to_package_registry(
    json_structure: Tuple[Dict[str, str], List[Tuple[str, str]]]
) -> PackageRegistry:
    return PackageRegistry(
        status_by_reason={
            reason: ReasonStatus(status) for reason, status in json_structure[0].items()
        },
        package_reasons=set(map(lambda x: PackageReason(*x), json_structure[1])),
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
        return PackageRegistry.empty()
