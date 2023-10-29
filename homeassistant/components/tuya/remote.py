"""Support for Tuya Remote."""
from __future__ import annotations

from typing import Any

from tuya_iot import TuyaDevice, TuyaDeviceManager

from homeassistant.components.remote import (
    RemoteEntity,
)

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import HomeAssistantTuyaData
from .base import EnumTypeData, IntegerTypeData, TuyaEntity
from .const import DOMAIN, TUYA_DISCOVERY_NEW, DPCode, DPType

import logging
_LOGGER = logging.getLogger(__name__)

import types


TUYA_SUPPORT_TYPE = {
    ## Programmable Remote
    # No specification on Tuya portal
    "qt"  
}

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up tuya IR remote dynamically through tuya discovery."""
    hass_data: HomeAssistantTuyaData = hass.data[DOMAIN][entry.entry_id]

    @callback
    def async_discover_device(device_ids: list[str]) -> None:
        """Discover and add a discovered tuya IR remote."""
        entities: list[TuyaRemoteEntity] = []
        _LOGGER.debug('BBBBBB async_discover_device(): ' + " ".join(device_ids))
        for device_id in device_ids:
            device = hass_data.device_manager.device_map[device_id]
#            if device and (device.category in TUYA_SUPPORT_TYPE or device.category.startswith("infrared_")):
            if device and device.category.startswith("infrared_"):
                entities.append(TuyaRemoteEntity(device, hass_data.device_manager))
                _LOGGER.debug('BBBBBB: entities.append: device_id: ' + device_id)
        async_add_entities(entities)

    async_discover_device([*hass_data.device_manager.device_map])

    entry.async_on_unload(
        async_dispatcher_connect(hass, TUYA_DISCOVERY_NEW, async_discover_device)
    )


class TuyaRemoteEntity(TuyaEntity, RemoteEntity):
    """Tuya Remote Device."""

    def __init__(
        self,
        device: TuyaDevice,
        device_manager: TuyaDeviceManager,
    ) -> None:
        """Init Tuya Remote Device."""
        super().__init__(device, device_manager)

        _LOGGER.debug('AAAAAA0: ' + " ".join(device.__dir__()))
        _LOGGER.debug('AAAAAA0.5: ' + " ".join(device.__dict__.__dir__()))
        _LOGGER.debug('AAAAAA0.6: ' + " ".join(device.__dict__.keys.__dir__()))
        _LOGGER.debug('AAAAAA0.7: ' + " ".join(device.__dict__.values.__dir__()))
        _LOGGER.debug('AAAAAA1: ' + " ".join(device.function.__dir__()))
        _LOGGER.debug('AAAAAA2: ' + " ".join(device.function.keys.__dir__()))
        _LOGGER.debug('AAAAAA3: ' + type(device.function.keys).__name__)
        _LOGGER.debug('AAAAAA4: ' + " ".join(device.function.values.__dir__()))
        _LOGGER.debug('AAAAAA5: ' + type(device.function.values).__name__)






