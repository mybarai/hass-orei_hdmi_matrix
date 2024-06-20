import json
import logging
import time
import urllib.request
from collections.abc import Mapping
from threading import RLock

_LOGGER = logging.getLogger(__name__)


class HDMIMatrixAPI:
    """HDMI Matrix API abstration."""

    def __init__(self) -> None:
        """Initialize the API."""
        self._lock = RLock()
        self._cache: Mapping[str, (int, str)] = {}

    def _hdmi_matrix_cmd(self, host, cmd, use_cache=False):
        cmd["language"] = 0
        cache_key = cmd["comhead"]

        if use_cache:
            cached = self._cache.get(cache_key, None)
            if cached:
                (ts, data) = cached
                if time.time() - ts < 5:
                    _LOGGER.debug(f"Cache Hit: '{cache_key}'")
                    return json.loads(data)
                del self._cache[cache_key]

            _LOGGER.debug(f"Cache miss: '{cache_key}'")

        resp_data = None
        req = urllib.request.Request(
            f"http://{host}/cgi-bin/instr",
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

        if use_cache:
            self._cache[cache_key] = (time.time(), json.dumps(resp_data))

        return resp_data

    def get_video_status(self, host):
        """Get the video status."""
        with self._lock:
            return self._hdmi_matrix_cmd(
                host, {"comhead": "get video status"}, use_cache=True
            )

    def get_output_status(self, host):
        """Get the output status."""
        with self._lock:
            return self._hdmi_matrix_cmd(
                host, {"comhead": "get output status"}, use_cache=True
            )

    def get_input_status(self, host):
        """Get the input status."""
        with self._lock:
            return self._hdmi_matrix_cmd(
                host, {"comhead": "get input status"}, use_cache=True
            )

    def video_switch(self, host, input_id, output_id):
        """Switch video source."""
        with self._lock:
            return self._hdmi_matrix_cmd(
                host,
                {"comhead": "video switch", "source": [input_id, output_id]},
                use_cache=False,
            )

    def tx_stream(self, host, output_id, on_state):
        """Tx Stream switch."""
        with self._lock:
            return self._hdmi_matrix_cmd(
                host,
                {"comhead": "tx stream", "out": [output_id, int(on_state)]},
                use_cache=False,
            )

    def set_arc(self, host, output_id, on_state):
        """Set ARC on output."""
        with self._lock:
            return self._hdmi_matrix_cmd(
                host,
                {"comhead": "set arc", "arc": [output_id, int(on_state)]},
                use_cache=False,
            )

    def video_scaler(self, host, output_id, scaler_mode):
        """Set video scaler."""
        with self._lock:
            return self._hdmi_matrix_cmd(
                host,
                {"comhead": "video scaler", "scaler": [output_id, scaler_mode]},
                use_cache=False,
            )

    def set_input_edid(self, host, input_id, edid_id):
        """Set input EDID."""
        with self._lock:
            return self._hdmi_matrix_cmd(
                host,
                {"comhead": "set edid", "edid": [input_id, edid_id]},
                use_cache=False,
            )
