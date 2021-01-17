from collections import namedtuple
from typing import Set, Dict

Package = str
Reason = str
Packages = Set[Package]
Reasons = Set[Reason]
PackagesByReason = Dict[Package, Reasons]
ReasonsByPackage = Dict[Reason, Packages]


class PackageReason(namedtuple):
    package: Package
    reason: Reason


class PackageRegistry(Set[PackageReason]):
    def by_reason(self) -> PackagesByReason:
        packages_by_reason = dict()
        for package, reason in self:
            if package in packages_by_reason:
                packages_by_reason[reason].add(package)
            else:
                packages_by_reason[reason] = {package}
        return packages_by_reason

    def by_package(self) -> ReasonsByPackage:
        reasons_by_package = dict()
        for package, reason in self:
            if package in reasons_by_package:
                reasons_by_package[package].add(reason)
            else:
                reasons_by_package[package] = {reason}
        return reasons_by_package
