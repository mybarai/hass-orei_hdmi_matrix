"""Platform to control OREI HDMI Matrix."""

from __future__ import annotations

import json
import logging
import urllib.request

import voluptuous as vol

from homeassistant.components.media_player import (
    PLATFORM_SCHEMA,
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
)
from homeassistant.components.media_player.const import DOMAIN
from homeassistant.const import (
    ATTR_ENTITY_ID,
    CONF_HOST,
    CONF_NAME,
    CONF_TYPE,
    STATE_OFF,
    STATE_ON,
)
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

_LOGGER = logging.getLogger(__name__)

SUPPORT_HDMIMATRIX = MediaPlayerEntityFeature.SELECT_SOURCE

MEDIA_PLAYER_SCHEMA = vol.Schema(
    {
        ATTR_ENTITY_ID: cv.comp_entity_ids,
    }
)


ZONE_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME): cv.string,
    }
)

SOURCE_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME): cv.string,
    }
)

DATA_HDMIMATRIX = "hdmi_matrix"

SERVICE_SETZONE = "hdmi_matrix_set_zone"
ATTR_SOURCE = "source"

SERVICE_SETZONE_SCHEMA = MEDIA_PLAYER_SCHEMA.extend(
    {vol.Required(ATTR_SOURCE): cv.string}
)

CONF_SOURCES = "allinputname"
CONF_ZONES = "alloutputname"

# Valid zone ids: 1-8
ZONE_IDS = vol.All(vol.Coerce(int), vol.Range(min=1, max=8))

# Valid source ids: 1-8
SOURCE_IDS = vol.All(vol.Coerce(int), vol.Range(min=1, max=8))

PLATFORM_SCHEMA = vol.All(
    cv.has_at_least_one_key(CONF_HOST),
    PLATFORM_SCHEMA.extend(
        {
            vol.Exclusive(CONF_HOST, CONF_TYPE): cv.string,
        }
    ),
)


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the HDMI Matrix platform."""

    if DATA_HDMIMATRIX not in hass.data:
        hass.data[DATA_HDMIMATRIX] = {}

    data = None
    connection = None
    host = config.get(CONF_HOST)
    if host is not None:
        api = HDMIMatrixAPI(host)
        data = api.get_video_status()
        if data is not None:
            connection = host

    if data is None or connection is None:
        _LOGGER.error(f"Failed to setup platform, unable to contact host at: {host}")
        return

    sources = dict(
        zip(range(1, len(data[CONF_SOURCES]) + 1), data[CONF_SOURCES], strict=False)
    )

    devices = []
    for zone_id, name in zip(
        range(1, len(data[CONF_ZONES]) + 1), data[CONF_ZONES], strict=False
    ):
        _LOGGER.info("Adding zone %d - %s", zone_id, name)
        unique_id = f"{connection}-{zone_id}"
        device = HDMIMatrixZone(connection, sources, zone_id, name)
        hass.data[DATA_HDMIMATRIX][unique_id] = device
        devices.append(device)

    add_entities(devices, True)

    def service_handle(service):
        """Handle for services."""
        entity_ids = service.data.get(ATTR_ENTITY_ID)
        source = service.data.get(ATTR_SOURCE)
        if entity_ids:
            devices = [
                device
                for device in hass.data[DATA_HDMIMATRIX].values()
                if device.entity_id in entity_ids
            ]
        else:
            devices = hass.data[DATA_HDMIMATRIX].values()

        for device in devices:
            if service.service == SERVICE_SETZONE:
                device.select_source(source)

    hass.services.register(
        DOMAIN, SERVICE_SETZONE, service_handle, schema=SERVICE_SETZONE_SCHEMA
    )


class HDMIMatrixAPI:
    """HDMI Matrix API abstration"""

    def __init__(self, host):
        """Initialize the API"""

        self._host = host

    def _hdmi_matrix_cmd(self, cmd):
        cmd["language"] = 0

        resp_data = None
        req = urllib.request.Request(
            f"http://{self._host}/cgi-bin/instr",
            data=json.dumps(cmd).encode("utf-8"),
            headers={"Accept": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=5) as r:
                if r.getcode() == 200:
                    resp_data = json.load(r)
        except Exception as e:
            _LOGGER.error(f"Error connecting to the HDMI Matrix: {e}")

        return resp_data

    def get_video_status(self):
        """Get the video status"""

        return self._hdmi_matrix_cmd({"comhead": "get video status"})

    def get_output_status(self):
        """Get the output status"""

        return self._hdmi_matrix_cmd({"comhead": "get output status"})

    def video_switch(self, input_id, output_id):
        """Switch video source"""

        return self._hdmi_matrix_cmd(
            {"comhead": "video switch", "source": [input_id, output_id]}
        )


# TODO: Make this a member of a parent class that aggregates the update() call for all zones.
#       Rationale: the API returns status for all inputs/outputs and is not fast, so zones should not be performing their own updates.
class HDMIMatrixZone(MediaPlayerEntity):
    """Representation of a HDMI matrix zone."""

    def __init__(self, hdmi_host, sources, zone_id, zone_name):
        """Initialize new zone."""
        self._api = HDMIMatrixAPI(hdmi_host)
        # dict source_id -> source name
        self._source_id_name = sources
        # dict source name -> source_id
        self._source_name_id = {v: k for k, v in sources.items()}
        # ordered list of all source names
        self._source_names = sorted(
            self._source_name_id.keys(), key=lambda v: self._source_name_id[v]
        )
        self._zone_id = zone_id
        self._name = f"OREI HDMI Matrix Zone - {zone_name}"
        self._state = None
        self._source = None

    def update(self):
        """Retrieve latest state."""

        data = self._api.get_video_status()
        if data is None:
            self._state = STATE_OFF
            return

        if "allsource" in data:
            state = data["allsource"][self._zone_id - 1]
        else:
            _LOGGER.error("Failed to find 'allsource' in video status output")
            return

        idx = state
        self._state = STATE_ON
        if idx in self._source_id_name:
            self._source = self._source_id_name[idx]
        else:
            self._source = None

    @property
    def name(self):
        """Return the name of the zone."""
        return self._name

    @property
    def state(self):
        """Return the state of the zone."""
        return self._state

    @property
    def supported_features(self):
        """Return flag of media commands that are supported."""
        return SUPPORT_HDMIMATRIX

    @property
    def media_title(self):
        """Return the current source as media title."""
        return self._source

    @property
    def source(self):
        """Return the current input source of the device."""
        return self._source

    @property
    def source_list(self):
        """List of available input sources."""
        return self._source_names

    def select_source(self, source):
        """Set input source."""
        if source not in self._source_name_id:
            return
        idx = self._source_name_id[source]
        _LOGGER.debug("Setting zone %d source to %s", self._zone_id, idx)

        self._api.video_switch(idx, self._zone_id)
