import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import aiohttp_client

from .const import DOMAIN, CONF_API_KEY, CONF_ORG_ID, CONF_NETWORK_ID
from .meraki_api import MerakiAPI

class MerakiSensorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema({
                    vol.Required(CONF_API_KEY): str,
                    vol.Required(CONF_ORG_ID): str,
                    vol.Optional(CONF_NETWORK_ID): str,
                })
            )

        errors = {}
        try:
            await self._test_connection(user_input)
        except Exception:
            errors["base"] = "cannot_connect"
        if errors:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema({
                    vol.Required(CONF_API_KEY): str,
                    vol.Required(CONF_ORG_ID): str,
                    vol.Optional(CONF_NETWORK_ID): str,
                }),
                errors=errors
            )

        return self.async_create_entry(title="Meraki Sensor", data=user_input)

    async def _test_connection(self, config):
        session = aiohttp_client.async_get_clientsession(self.hass)
        api = MerakiAPI(config, session)
        await api.get_latest_readings()

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return MerakiSensorOptionsFlowHandler(config_entry)

class MerakiSensorOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        return self.async_show_form(step_id="init")
