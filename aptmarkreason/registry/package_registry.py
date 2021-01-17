from dataclasses import dataclass
from enum import Enum
from typing import Dict, NamedTuple, Set

Package = str
Reason = str
Packages = Set[Package]
Reasons = Set[Reason]
PackagesByReason = Dict[Package, Reasons]
ReasonsByPackage = Dict[Reason, Packages]


class ReasonStatus(Enum):
    ACTIVE = "active"
    DEACTIVATED = "deactivated"

    def __str__(self):
        return self.value


StatusByReason = Dict[Reason, ReasonStatus]


class PackageReason(NamedTuple):
    package: Package
    reason: Reason


PackageReasons = Set[PackageReason]


@dataclass(frozen=True)
class PackageRegistry:
    status_by_reason: StatusByReason
    package_reasons: PackageReasons

    def by_reason(self) -> PackagesByReason:
        packages_by_reason: PackagesByReason = dict()
        for package, reason in self.package_reasons:
            if package in packages_by_reason:
                packages_by_reason[reason].add(package)
            else:
                packages_by_reason[reason] = {package}
        return packages_by_reason

    def by_package(self) -> ReasonsByPackage:
        reasons_by_package: ReasonsByPackage = dict()
        for package, reason in self.package_reasons:
            if package in reasons_by_package:
                reasons_by_package[package].add(reason)
            else:
                reasons_by_package[package] = {reason}
        return reasons_by_package


def add_package_with_reason(
    package_registry: PackageRegistry, package: Package, reason: Reason
) -> PackageRegistry:
    return PackageRegistry(
        status_by_reason=add_reason(package_registry.status_by_reason, reason),
        package_reasons=add_package_reason(
            package_registry.package_reasons, PackageReason(package, reason)
        ),
    )


def add_reason(status_by_reason: StatusByReason, reason: Reason) -> StatusByReason:
    return {reason: ReasonStatus.ACTIVE} | status_by_reason


def add_package_reason(
    package_reasons: PackageReasons, package_reason: PackageReason
) -> PackageReasons:
    return package_reasons | {package_reason}
