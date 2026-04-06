"""Base entity for the Kubernetes integration."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import KubernetesCoordinator, ResourceKey


class KubernetesEntity(CoordinatorEntity[KubernetesCoordinator]):
    """Base class for Kubernetes entities."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: KubernetesCoordinator,
        resource_key: ResourceKey,
    ) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        self._resource_key = resource_key
        self._namespace, self._kind, self._resource_name = resource_key

    @property
    def _entry_id(self) -> str:
        return self.coordinator.entry.entry_id

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info for this resource."""
        return DeviceInfo(
            identifiers={
                (DOMAIN, f"{self._entry_id}_{self._namespace}/{self._kind}/{self._resource_name}")
            },
            name=self._resource_name,
            manufacturer="Kubernetes",
            model=self._kind,
            sw_version=self._namespace,
        )

    @property
    def resource_data(self) -> dict | None:
        """Get the current data for this resource."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get(self._resource_key)

    @property
    def available(self) -> bool:
        """Return True if the resource exists in the latest data."""
        return super().available and self.resource_data is not None
