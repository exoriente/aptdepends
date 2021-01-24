from typing import Iterable


class ApplicationError(Exception):
    ...


class PackageNameAlreadyExists(ApplicationError):
    def __init__(self, package: str):
        super().__init__(f'A package with the name "{package}" already exists.')


class PackageNotFoundError(ApplicationError):
    def __init__(self, package: str):
        super().__init__(f'Can\'t find package "{package}"')


class PackageCheckFailureError(ApplicationError):
    def __init__(self, package: str, stderr: str):
        super().__init__(
            f'Unable to check status of package "{package}". '
            f"Error when checking with apt-cache:\n{stderr}"
        )


class DependenciesUnavailableError(ApplicationError):
    def __init__(self, unavailable_dep_packages: Iterable[str]):
        super().__init__(
            f"The following dependency packages do not exist in the current apt cache: "
            f'    {", ".join(unavailable_dep_packages)}'
        )
