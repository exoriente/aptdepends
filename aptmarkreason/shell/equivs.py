import re
from pathlib import Path
from tempfile import gettempdir
from typing import Iterable, List

from ..exceptions.exceptions import UnexpectedShellResult
from ..shell.shell import make_call_to_shell


def create_empty_control_file(package_name: str) -> Path:
    control_file_path = Path(gettempdir()) / (package_name + ".ctl")
    command = f"equivs-control {control_file_path}"
    make_call_to_shell(command.split())
    return control_file_path


def configure_control_file(
    control_file_path: Path,
    package_name: str,
    dependencies: List[str],
    description: str,
):
    with open(control_file_path, "r") as control_file:
        lines: Iterable[str] = control_file.readlines()

    name_line = f"Package: {package_name}"
    dependency_line = "Depends: " + ",".join(dependencies)
    description_line = f"Description: {description}"

    lines = replace_in_lines(lines, "Package:", name_line)
    lines = replace_in_lines(lines, "# Depends:", dependency_line)
    lines = replace_in_lines(lines, "Description:", description_line)
    lines = delete_lines_after(lines, "Description:")

    with open(control_file_path, "w") as control_file:
        control_file.writelines(lines)


def replace_in_lines(lines: Iterable[str], prefix: str, new_line: str) -> Iterable[str]:
    new_lines = list()
    for line in lines:
        if line.startswith(prefix):
            new_lines.append(new_line + "\n")
        else:
            new_lines.append(line)
    return new_lines


def delete_lines_after(lines: Iterable[str], prefix: str) -> Iterable[str]:
    new_lines = list()
    for line in lines:
        new_lines.append(line)
        if line.startswith(prefix):
            break
    return new_lines


def create_package_file(control_file_path: Path) -> Path:
    deb_path = control_file_path.parent
    command = f"equivs-build {control_file_path.resolve()}"
    result, stdout, stderr = make_call_to_shell(command.split(), cwd=deb_path)

    for line in stdout:
        match = re.match(r"^dpkg-deb: building package '.*' in '\.\./(.*)'\.$", line)
        if match:
            deb_file_name = match.group(1)
            break
    else:
        raise UnexpectedShellResult(f'Command "{command}" did not yield a deb package')

    return deb_path / deb_file_name
