from __future__ import annotations

from enum import Enum

from typing import Final

DATA_HDMIMATRIX: Final = "hdmi_matrix"

SERVICE_SET_ZONE: Final = "hdmi_matrix_set_zone"

SERVICE_SET_SCALER: Final = "hdmi_matrix_set_scaler"

SERVICE_SET_TX_STREAM: Final = "hdmi_matrix_set_tx_stream"

SERVICE_SET_ARC: Final = "hdmi_matrix_set_arc"

SERVICE_SET_INPUT_EDID: Final = "hdmi_matrix_set_input_edid"

ATTR_SOURCE: Final = "source"

CONF_ALL_SOURCE: Final = "allsource"

CONF_SOURCES: Final = "allinputname"

CONF_ZONES: Final = "alloutputname"

CONF_OUT: Final = "allout"

CONF_SCALER: Final = "allscaler"

CONF_ARC: Final = "allarc"

CONF_CONNECT: Final = "allconnect"

CONF_HDCP: Final = "allhdcp"

CONF_EDID: Final = "edid"

CONF_INNAME: Final = "inname"

CONF_INPUT_ACTIVE: Final = "inactive"

ATTR_SCALER_MODE: Final = "scaler_mode"

SCALER_TYPES: Final[dict[int, str]] = {
    0: "Bypass",
    1: "4K -> 1080P",
    3: "AUTO",
}

ATTR_STREAM: Final = "stream"

ATTR_ARC: Final = "arc"

ATTR_CONNECT: Final = "connected"

ATTR_HDCP: Final = "hdcp"

ATTR_INPUT_EDID: Final = "input_edid"

ATTR_INPUT_ACTIVE: Final = "input_active"


class ScalerModes(Enum):
    """Enum for setting the scaler mode."""

    BYPASS = 0
    SCALE_4K_1080P = 1
    AUTO = 3


class EDIDModes(Enum):
    """Enum for setting the EDID."""

    # 1080P,Stereo Audio 2.0
    EDID_1080P_STEREO_AUDIO_2_0 = 1
    # 1080P,Dolby/DTS 5.1
    EDID_1080P_DOLBY_DTS_5_1 = 2
    # 1080P,HD Audio 7.1
    EDID_1080P_HD_AUDIO_7_1 = 3
    # 1080I,Stereo Audio 2.0
    EDID_1080I_STEREO_AUDIO_2_0 = 4
    # 1080I,Dolby/DTS 5.1
    EDID_1080I_DOLBY_DTS_5_1 = 5
    # 1080I,HD Audio 7.1
    EDID_1080I_HD_AUDIO_7_1 = 6
    # 3D,Stereo Audio 2.0
    EDID_3D_STEREO_AUDIO_2_0 = 7
    # 3D,Dolby/DTS 5.1
    EDID_3D_DOLBY_DTS_5_1 = 8
    # 3D,HD Audio 7.1
    EDID_3D_HD_AUDIO_7_1 = 9
    # 4K2K30_444,Stereo Audio 2.0
    EDID_4K2K30_444_STEREO_AUDIO_2_0 = 10
    # 4K2K30_444,Dolby/DTS 5.1
    EDID_4K2K30_444_DOLBY_DTS_5_1 = 11
    # 4K2K30_444,HD Audio 7.1
    EDID_4K2K30_444_HD_AUDIO_7_1 = 12
    # 4K2K60_420,Stereo Audio 2.0
    EDID_4K2K60_420_STEREO_AUDIO_2_0 = 13
    # 4K2K60_420,Dolby/DTS 5.1
    EDID_4K2K60_420_DOLBY_DTS_5_1 = 14
    # 4K2K60_420,HD Audio 7.1
    EDID_4K2K60_420_HD_AUDIO_7_1 = 15
    # 4K2K60_444,Stereo Audio 2.0
    EDID_4K2K60_444_STEREO_AUDIO_2_0 = 16
    # 4K2K60_444,Dolby/DTS 5.1
    EDID_4K2K60_444_DOLBY_DTS_5_1 = 17
    # 4K2K60_444,HD Audio 7.1
    EDID_4K2K60_444_HD_AUDIO_7_1 = 18
    # 4K2K60_444,Stereo Audio 2.0 HDR
    EDID_4K2K60_444_STEREO_AUDIO_2_0_HDR = 19
    # 4K2K60_444,Dolby/DTS 5.1 HDR
    EDID_4K2K60_444_DOLBY_DTS_5_1_HDR = 20
    # 4K2K60_444,HD Audio 7.1 HDR
    EDID_4K2K60_444_HD_AUDIO_7_1_HDR = 21
    # User Define1
    EDID_USER_DEFINE_1 = 22
    # User Define2
    EDID_USER_DEFINE_2 = 23
    # COPY_FROM_OUT_1
    EDID_COPY_FROM_OUT_1 = 24
    # COPY_FROM_OUT_2
    EDID_COPY_FROM_OUT_2 = 25
    # COPY_FROM_OUT_3
    EDID_COPY_FROM_OUT_3 = 26
    # COPY_FROM_OUT_4
    EDID_COPY_FROM_OUT_4 = 27
    # COPY_FROM_OUT_5
    EDID_COPY_FROM_OUT_5 = 28
    # COPY_FROM_OUT_6
    EDID_COPY_FROM_OUT_6 = 29
    # COPY_FROM_OUT_7
    EDID_COPY_FROM_OUT_7 = 30
    # COPY_FROM_OUT_8
    EDID_COPY_FROM_OUT_8 = 31
