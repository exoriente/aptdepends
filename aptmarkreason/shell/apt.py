from dataclasses import dataclass

from basic_types import Packages
from general import application_signature
from exceptions.exceptions import PackageCheckFailureError
from shell.shell import make_call_to_shell


@dataclass(frozen=True)
class PackageNameStatus:
    name_already_in_use: bool
    is_installed: bool
    is_virtual_package: bool


def get_available_packages() -> Packages:
    command = "apt-cache pkgnames"
    result, stdout, stderr = make_call_to_shell(command.split())
    return set(stdout)


def get_auto_installed_packages() -> Packages:
    command = "apt-mark showauto"
    result, stdout, stderr = make_call_to_shell(command.split())
    return set(stdout)


def get_manual_installed_packages() -> Packages:
    command = "apt-mark showmanual"
    result, stdout, stderr = make_call_to_shell(command.split())
    return set(stdout)


def get_package_name_status(package_name: str) -> PackageNameStatus:
    command = f"apt-cache show {package_name}"
    result, stdout, stderr = make_call_to_shell(command.split())

    if result == 0:
        name_already_in_use = True
        is_installed = "Status: install ok installed" in stdout

        description = next(filter(lambda x: x.startswith("Description:"), stdout))
        if description and application_signature() in description:
            is_virtual_package = True
        else:
            is_virtual_package = False
    elif "E: No packages found" in stderr:
        name_already_in_use = False
        is_installed = False
        is_virtual_package = False
    else:
        raise PackageCheckFailureError(package_name, "\n".join(stderr))

    return PackageNameStatus(
        name_already_in_use=name_already_in_use,
        is_installed=is_installed,
        is_virtual_package=is_virtual_package,
    )
