class ApplicationError(Exception):
    ...


class PackageNotFoundError(Exception):
    def __init__(self, package: str):
        super().__init__(f'Can\'t find package "{package}"')
