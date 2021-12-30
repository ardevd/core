"""Sensor platform for the Bobcat Miner."""
from datetime import timedelta

from bobcatpy import Bobcat

from homeassistant.components.sensor import SensorEntity

from .const import CONFIG_HOST, DOMAIN

SCAN_INTERVAL = timedelta(minutes=10)

SENSORS = {
    "syncgap": "mdi:cloud-sync",
}


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Sensor setup based on config entry created in the integrations UI."""

    config = hass.data[DOMAIN][config_entry.entry_id]
    miner = Bobcat(config[CONFIG_HOST])
    entities = []
    entities.append(BobcatMinerSensor(miner))

    async_add_entities(entities, True)


class BobcatMinerSensor(SensorEntity):
    """Sensor representing a bobcat miner."""

    _attr_native_unit_of_measurement = "blocks"

    def __init__(self, bobcat):
        """Initialize miner sensor."""
        super().__init__()

        self.bobcat = bobcat
        self._attr_unique_id = "bobcatminer"
        self._attr_name = "Bobcat Miner"
        self._available = True
        self._state = None

    @property
    def available(self):
        """Return sensor availability."""
        return self._available

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self._state

    def get_sync_status(self):
        """Get miner sync status."""
        return self.bobcat.sync_status()

    def update(self):
        """State of the sensor."""
        sync_status = self.bobcat.sync_status()

        self._state = sync_status["gap"]
        self._available = True
