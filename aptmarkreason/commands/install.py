from typing import List

import typer
from apt.apt import get_system_status
from exceptions import PackageNotFoundError
from exceptions.output import output_exception
from registry.package_registry import PackageRegistry, add_package_with_reason


def mark_package_manual(package: str):
    pass


def perform_installation(package: str):
    pass


def install_package(
    typer_app: typer.Typer, package_registry: PackageRegistry, reason: str, package: str
) -> PackageRegistry:
    try:
        system_status = get_system_status()
        if package not in system_status.installed_manual:
            if package in system_status.installed_auto:
                mark_package_manual(package)
            elif package not in system_status.available:
                raise PackageNotFoundError(package)
            else:
                perform_installation(package)
    except Exception as error:
        output_exception(error)
        raise typer.Exit(code=1) from error
    else:
        add_package_with_reason(package_registry, package, reason)

    return package_registry


def install_packages(
    typer_app: typer.Typer,
    package_registry: PackageRegistry,
    reason: str,
    packages: List[str],
) -> PackageRegistry:
    for package in packages:
        package_registry = install_package(typer_app, package_registry, reason, package)
    return package_registry
