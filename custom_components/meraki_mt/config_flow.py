import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import aiohttp_client
from homeassistant.helpers.selector import selector

from .const import DOMAIN, CONF_API_KEY, CONF_ORG_ID, CONF_NETWORK_ID
from .meraki_mt import MerakiMT

class MerakiMTConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    MINOR_VERSION = 3
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            try:
                await self._test_connection(user_input)
            except Exception:
                errors["base"] = "cannot_connect"
            if not errors:
                return self.async_create_entry(title="Meraki MT", data=user_input)

        data_schema = vol.Schema({
            vol.Required(CONF_API_KEY): str,
            vol.Required(CONF_ORG_ID): str,
            vol.Optional(CONF_NETWORK_ID): str,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "api_key": self.hass.config_entries.async_get_entry_title(),
                "organization_id": self.hass.config_entries.async_get_entry_title(),
                "network_id": self.hass.config_entries.async_get_entry_title()
            }
        )

    async def _test_connection(self, config):
        session = aiohttp_client.async_get_clientsession(self.hass)
        api = MerakiMT(config, session)
        await api.get_latest_readings()

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return MerakiMTOptionsFlowHandler(config_entry)

class MerakiMTOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        return self.async_show_form(step_id="init")
