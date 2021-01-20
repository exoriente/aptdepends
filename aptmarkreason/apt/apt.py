from dataclasses import dataclass

from basic_types import Packages
from shell.shell import make_call_to_shell


@dataclass(frozen=True)
class SystemStatus:
    available: Packages
    installed_auto: Packages
    installed_manual: Packages


def get_system_status() -> SystemStatus:
    return SystemStatus(
        available=get_available_packages(),
        installed_auto=get_auto_installed_packages(),
        installed_manual=get_manual_installed_packages(),
    )


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
