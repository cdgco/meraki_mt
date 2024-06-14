from homeassistant.components.sensor import SensorEntity
from homeassistant.const import TEMP_CELSIUS, TEMP_FAHRENHEIT, PERCENTAGE

from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    sensors = []

    for sensor_data in coordinator.data:
        if sensor_data["battery"] is not None:
            sensors.append(MerakiMTBatterySensor(coordinator, sensor_data))
        if sensor_data["temperature_celsius"] is not None or sensor_data["temperature_fahrenheit"] is not None:
            sensors.append(MerakiMTTemperatureSensor(coordinator, sensor_data))
        if sensor_data["humidity"] is not None:
            sensors.append(MerakiMTHumiditySensor(coordinator, sensor_data))

    async_add_entities(sensors)

class MerakiMTSensorBase(SensorEntity):
    def __init__(self, coordinator, sensor_data):
        self.coordinator = coordinator
        self.sensor_data = sensor_data

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.sensor_data["id"])},
            "name": f"Meraki Sensor {self.sensor_data['id']}",
            "manufacturer": "Cisco Meraki",
        }

class MerakiMTBatterySensor(MerakiMTSensorBase):
    def __init__(self, coordinator, sensor_data):
        super().__init__(coordinator, sensor_data)
        self._name = f"MT {sensor_data['id']} Battery"
        self._unique_id = f"{sensor_data['id']}_battery"

    @property
    def name(self):
        return self._name

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def state(self):
        return self.sensor_data["battery"]

    @property
    def extra_state_attributes(self):
        return {
            "network_name": self.sensor_data["network_name"],
        }

    @property
    def unit_of_measurement(self):
        return PERCENTAGE

    @property
    def should_poll(self):
        return True

    async def async_update(self):
        await self.coordinator.async_request_refresh()

class MerakiMTTemperatureSensor(MerakiMTSensorBase):
    def __init__(self, coordinator, sensor_data):
        super().__init__(coordinator, sensor_data)
        self._name = f"MT {sensor_data['id']} Temperature"
        self._unique_id = f"{sensor_data['id']}_temperature"

    @property
    def name(self):
        return self._name

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def state(self):
        return self.sensor_data["temperature_celsius"]

    @property
    def extra_state_attributes(self):
        return {
            "network_name": self.sensor_data["network_name"],
            "temperature_celsius": self.sensor_data["temperature_celsius"],
            "temperature_fahrenheit": self.sensor_data["temperature_fahrenheit"],
        }

    @property
    def unit_of_measurement(self):
        return TEMP_CELSIUS

    @property
    def should_poll(self):
        return True

    async def async_update(self):
        await self.coordinator.async_request_refresh()

class MerakiMTHumiditySensor(MerakiMTSensorBase):
    def __init__(self, coordinator, sensor_data):
        super().__init__(coordinator, sensor_data)
        self._name = f"MT {sensor_data['id']} Humidity"
        self._unique_id = f"{sensor_data['id']}_humidity"

    @property
    def name(self):
        return self._name

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def state(self):
        return self.sensor_data["humidity"]

    @property
    def extra_state_attributes(self):
        return {
            "network_name": self.sensor_data["network_name"],
        }

    @property
    def unit_of_measurement(self):
        return PERCENTAGE

    @property
    def should_poll(self):
        return True

    async def async_update(self):
        await self.coordinator.async_request_refresh()
