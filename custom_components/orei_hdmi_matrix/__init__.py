import json
import logging
import time
import urllib.request
from collections.abc import Mapping

_LOGGER = logging.getLogger(__name__)


class HDMIMatrixAPI:
    """HDMI Matrix API abstration."""

    def __init__(self) -> None:
        """Initialize the API."""
        self._cache: Mapping[str, (int, str)] = {}

    def _hdmi_matrix_cmd(self, host, cmd, use_cache=False):
        cmd["language"] = 0
        cache_key = json.dumps(cmd)

        if use_cache:
            cached = self._cache.get(cache_key, None)
            if cached:
                (ts, data) = cached
                if time.time() - ts < 5:
                    _LOGGER.info(f"Cache Hit: '{cache_key}'")
                    return json.loads(data)
                del self._cache[cache_key]

            _LOGGER.info(f"Cache miss: '{cache_key}'")

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
        return self._hdmi_matrix_cmd(
            host, {"comhead": "get video status"}, use_cache=True
        )

    def get_output_status(self, host):
        """Get the output status."""
        return self._hdmi_matrix_cmd(
            host, {"comhead": "get output status"}, use_cache=True
        )

    def video_switch(self, host, input_id, output_id):
        """Switch video source."""
        return self._hdmi_matrix_cmd(
            host,
            {"comhead": "video switch", "source": [input_id, output_id]},
            use_cache=False,
        )


api = HDMIMatrixAPI()
