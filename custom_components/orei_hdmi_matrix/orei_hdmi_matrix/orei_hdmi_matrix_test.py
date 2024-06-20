from orei_hdmi_matrix import HDMIMatrixAPI

host = "192.168.1.131"

if __name__ == "__main__":
    api = HDMIMatrixAPI()
    resp = api.get_video_status(host)
    print(resp)
    for field in ["comhead", "allsource", "allinputname", "alloutputname"]:
        assert (
            field in resp
        ), f"Field '{field}' not found in 'get_video_status' response"
    assert "get video status" in resp["comhead"]

    resp = api.get_output_status(host)
    print(resp)
    for field in [
        "comhead",
        "allsource",
        "allscaler",
        "allhdcp",
        "allout",
        "allconnect",
        "allarc",
        "name",
    ]:
        assert (
            field in resp
        ), f"Field '{field}' not found in 'get_output_status' response"
    assert "get output status" in resp["comhead"]

    resp = api.get_input_status(host)
    print(resp)
    for field in ["comhead", "edid", "inactive", "inname", "power"]:
        assert (
            field in resp
        ), f"Field '{field}' not found in 'get_input_status' response"
    assert "get input status" in resp["comhead"]

    # resp = api.video_switch(host, 1, 2)
    # print(resp)
    # for field in ["comhead", "result"]:
    #     assert field in resp, f"Field '{field}' not found in 'video_switch' response"
    # assert "video switch" in resp["comhead"]
    # assert resp["result"] == 1

    print("All tests passed")
