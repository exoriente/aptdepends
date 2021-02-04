from dataclasses import dataclass
from enum import Enum
from typing import Dict, NamedTuple, Set

from ..basic_types import Package, Packages, Reason, Reasons

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

    @staticmethod
    def empty() -> "PackageRegistry":
        return PackageRegistry(status_by_reason=dict(), package_reasons=set())


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
    # return {reason: ReasonStatus.ACTIVE} | status_by_reason  # todo: use as as soon as mypy support 3.9
    if reason in status_by_reason:
        return status_by_reason
    else:
        return dict(**status_by_reason, reason=ReasonStatus.ACTIVE)


def add_package_reason(
    package_reasons: PackageReasons, package_reason: PackageReason
) -> PackageReasons:
    return package_reasons | {package_reason}
