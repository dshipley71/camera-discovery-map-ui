from camera_discovery_map_ui.status import normalize_status


def test_status_mapping_live_dead_unknown():
    assert normalize_status("active_live_verified") == "live"
    assert normalize_status("active_live_dynamic") == "live"
    assert normalize_status("restricted_http") == "dead"
    assert normalize_status("offline_http") == "dead"
    assert normalize_status("not_validated") == "unknown"
    assert normalize_status(None) == "unknown"
    assert normalize_status("unexpected_new_status") == "unknown"
