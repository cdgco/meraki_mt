import aiohttp

class MerakiMT:
    def __init__(self, config, session):
        self.api_key = config["api_key"]
        self.org_id = config["organization_id"]
        self.network_id = config.get("network_id")
        self.session = session

    async def get_latest_readings(self):
        url = f"https://api.meraki.com/api/v1/organizations/{self.org_id}/sensor/readings/latest"
        if self.network_id:
            url += f"?networkIds={self.network_id}"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        async with self.session.get(url, headers=headers) as response:
            response.raise_for_status()
            data = await response.json()
            return self._parse_readings(data)

    def _parse_readings(self, data):
        sensors = []
        for sensor in data:
            sensor_data = {
                "id": sensor["serial"],
                "network_name": sensor["network"]["name"],
                "battery": None,
                "temperature_celsius": None,
                "temperature_fahrenheit": None,
                "humidity": None
            }
            for reading in sensor["readings"]:
                if reading["metric"] == "battery":
                    sensor_data["battery"] = reading["battery"]["percentage"]
                elif reading["metric"] == "humidity":
                    sensor_data["humidity"] = reading["humidity"]["relativePercentage"]
                elif reading["metric"] == "temperature":
                    if reading["temperature"]["fahrenheit"]:
                        sensor_data["temperature_fahrenheit"] = reading["temperature"]["fahrenheit"]
                    if reading["temperature"]["celsius"]:
                        sensor_data["temperature_celsius"] = reading["temperature"]["celsius"]

            sensors.append(sensor_data)
        return sensors
