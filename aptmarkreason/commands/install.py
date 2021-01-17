from typing import List

from typer import Typer

from aptmarkreason.registry.package_registry import (
    PackageRegistry,
    add_package_with_reason,
)


def is_package_installed(package: str) -> bool:
    return True


def is_package_marked_manual(package: str) -> bool:
    return True


def mark_package_manual(package: str):
    pass


def perform_installation(package: str):
    pass


def install_package(
    typer: Typer, package_registry: PackageRegistry, reason: str, package: str
) -> PackageRegistry:
    try:
        if is_package_installed(package):
            if not is_package_marked_manual(package):
                mark_package_manual(package)
        else:
            perform_installation(package)
    except Exception as error:
        raise error from error
    else:
        add_package_with_reason(package_registry, package, reason)

    return package_registry


def install_packages(
    typer: Typer, package_registry: PackageRegistry, reason: str, packages: List[str]
) -> PackageRegistry:
    for package in packages:
        package_registry = install_package(typer, package_registry, reason, package)
    return package_registry
