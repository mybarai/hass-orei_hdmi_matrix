from media_player import HDMIMatrixAPI

if __name__ == "__main__":
    api = HDMIMatrixAPI("192.168.1.131")
    resp = api.get_video_status()
    for field in ["comhead", "allsource", "allinputname", "alloutputname"]:
        assert (
            field in resp
        ), f"Field '{field}' not found in 'get_video_status' response"
    assert "get video status" in resp["comhead"]

    resp = api.get_output_status()
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

    resp = api.video_switch(1, 2)
    for field in ["comhead", "result"]:
        assert field in resp, f"Field '{field}' not found in 'video_switch' response"
    assert "video switch" in resp["comhead"]
    assert resp["result"] == 1

    print("All tests passed")
