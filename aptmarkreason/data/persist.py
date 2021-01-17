import json
from pathlib import Path

from aptmarkreason.data.data import PackageRegistry

REGISTRY_PATH = Path.home() / ".config" / "aptmarkreason"
REGISTRY_FILENAME = "package_registry.json"
REGISTRY_FILE = REGISTRY_PATH / REGISTRY_FILENAME


def save_package_registry(package_registry: PackageRegistry):
    if not REGISTRY_FILE.parent.is_dir():
        REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(REGISTRY_FILE, "w") as file:
        json.dump(package_registry, file)


def load_package_registry() -> PackageRegistry:
    if REGISTRY_FILE.is_file():
        with open(REGISTRY_FILE, "r") as file:
            package_registry = json.load(file)
        return package_registry
    else:
        return PackageRegistry()
