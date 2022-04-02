"""Config flow for Hello World integration."""
import logging

import voluptuous as vol

from homeassistant import config_entries
import homeassistant.helpers.config_validation as cv
from homeassistant.core import callback
from homeassistant.config_entries import ConfigFlow, OptionsFlow, ConfigEntry

from .const import DOMAIN  # pylint:disable=unused-import

_LOGGER = logging.getLogger(__name__)

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def get_media_players(self):
        all_media_player = dict()
        all_entities = await self.hass.async_add_executor_job(self.hass.states.all)
        for e in all_entities:
            if e.entity_id.startswith("media_player."):
                all_media_player.update({e.entity_id: e.name})
        return all_media_player

    async def get_media_player_types(self):
        media_player_types: dict = {
            "chromecast": "谷歌Nest Entity",
            "entity": "其他HA内置 Entity",
            "web": "网页播放器",
            "windows": "Windows应用",
            "mpd": "MPD播放器",
            "vlc": "VLC播放器"
        }
        return media_player_types

    async def async_step_user(self, user_input=None):        
        errors = {}
        if DOMAIN in self.hass.data:
            return self.async_abort(reason="single_instance_allowed")

        media_players = await self.get_media_players()
        media_player_types = await self.get_media_player_types()

        # 如果输入内容不为空，则进行验证
        if user_input is not None:
            user_input['api_url'] = user_input['api_url'].strip('/')
            return self.async_create_entry(title=DOMAIN, data=user_input)
        
        # 显示表单
        DATA_SCHEMA = vol.Schema({
            vol.Required("api_url", default="https://netease-cloud-music-api-7k8q.vercel.app"): str,
            vol.Required("media_player_type"): vol.In(media_player_types),
            vol.Optional("media_player"): vol.In(media_players),
            vol.Optional("mpd_host"): str,
            vol.Optional("is_voice", default=True): bool,
        })
        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(entry: ConfigEntry):
        return OptionsFlowHandler(entry)


class OptionsFlowHandler(OptionsFlow):
    def __init__(self, config_entry: ConfigEntry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        return await self.async_step_user(user_input)

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is None:
            options = self.config_entry.options
            errors = {}
            DATA_SCHEMA = vol.Schema({
                vol.Optional("find_api_url", default=options.get('find_api_url', '')): str,
                vol.Optional("user", default=options.get('user', '')): str,
                vol.Optional("password", default=options.get('password', '')): str,
                vol.Optional("tts_before_message", default=options.get('tts_before_message', '')): str,
                vol.Optional("tts_after_message", default=options.get('tts_after_message', '')): str,
                vol.Optional("is_notify", default=options.get('is_notify', True)): bool,
                vol.Optional("tts_mode", default=options.get('tts_mode', 4)): int,
                vol.Optional("is_skip_invalid_music_url", default=options.get('is_skip_invalid_music_url', True)): bool,
            })
            return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA, errors=errors)
        # 选项更新
            user_input['find_api_url'] = user_input['find_api_url'].strip('/')
        return self.async_create_entry(title=DOMAIN, data=user_input)