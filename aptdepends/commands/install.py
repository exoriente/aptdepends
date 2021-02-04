from typing import List

import typer

from ..exceptions.exceptions import (
    DependenciesUnavailableError,
    PackageNameAlreadyExists,
)
from ..general import application_signature
from ..shell.apt import (
    PackageNameStatus,
    get_available_packages,
    get_package_name_status,
    install_deb,
    uninstall_deb,
)
from ..shell.equivs import (
    configure_control_file,
    create_empty_control_file,
    create_package_file,
)


def install_packages(
    virtual_package_name: str,
    dep_packages: List[str],
):
    package_name_status = get_package_name_status(virtual_package_name)

    abort_if_install_impossible(virtual_package_name, package_name_status)

    replace = check_replacement_needed(package_name_status)
    if replace:
        abort_if_replacement_unwanted(virtual_package_name)

    abort_if_dep_packages_not_available(dep_packages)

    if replace:
        uninstall_deb(virtual_package_name)

    description = make_description(virtual_package_name)

    control_file = create_empty_control_file(virtual_package_name)
    configure_control_file(
        control_file, virtual_package_name, dep_packages, description
    )
    package_file = create_package_file(control_file)
    install_deb(package_file)


def abort_if_install_impossible(
    package_name: str, package_name_status: PackageNameStatus
):
    if (
        package_name_status.name_already_in_use or package_name_status.is_installed
    ) and not package_name_status.is_virtual_package:
        raise PackageNameAlreadyExists(package_name)


def check_replacement_needed(package_name_status: PackageNameStatus) -> bool:
    return package_name_status.is_installed and package_name_status.is_virtual_package


def abort_if_replacement_unwanted(virtual_package_name):
    typer.confirm(
        f'A virtual package with the name "{virtual_package_name}" is already installed. '
        f"Do you want to replace it?",
        default=False,
        err=True,
        abort=True,
    )


def abort_if_dep_packages_not_available(dep_packages: List[str]):
    unavailable_packages = set(dep_packages) - set(get_available_packages())
    if unavailable_packages:
        raise DependenciesUnavailableError(unavailable_packages)


def make_description(package_name: str) -> str:
    return f"Meta-package to install dependencies for {package_name}. {application_signature()}"
