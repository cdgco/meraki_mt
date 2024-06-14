from homeassistant.components.sensor import SensorEntity
from homeassistant.const import TEMP_CELSIUS, PERCENTAGE

from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    sensors = []

    for sensor_data in coordinator.data:
        sensors.append(MerakiSensor(coordinator, sensor_data))

    async_add_entities(sensors)

class MerakiSensor(SensorEntity):
    def __init__(self, coordinator, sensor_data):
        self.coordinator = coordinator
        self.sensor_data = sensor_data
        self._name = sensor_data["id"]
        self._unique_id = sensor_data["id"]

    @property
    def name(self):
        return self._name

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def state(self):
        return {
            "battery": self.sensor_data["battery"],
            "temperature": self.sensor_data["temperature"],
            "humidity": self.sensor_data["humidity"]
        }

    @property
    def extra_state_attributes(self):
        return {
            "network_name": self.sensor_data["network_name"],
            "battery": self.sensor_data["battery"],
            "temperature": self.sensor_data["temperature"],
            "humidity": self.sensor_data["humidity"],
        }

    @property
    def unit_of_measurement(self):
        if self.sensor_data["temperature"] is not None:
            return TEMP_CELSIUS
        elif self.sensor_data["humidity"] is not None:
            return PERCENTAGE
        return None

    @property
    def should_poll(self):
        return True

    async def async_update(self):
        await self.coordinator.async_request_refresh()
