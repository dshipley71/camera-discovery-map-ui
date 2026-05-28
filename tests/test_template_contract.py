from importlib.resources import files


def _template_text() -> str:
    return files("camera_discovery_map_ui").joinpath("templates/map_template.html").read_text(encoding="utf-8")


def test_template_references_bundle_and_summarization_contract():
    text = _template_text()
    assert "camera_map_bundle.json" in text
    assert "Summarize Video" in text
    assert "15" in text and "300" in text
    assert "hls.js" in text.lower() or "hls.min.js" in text.lower()


def test_template_has_no_active_old_geography_overlay_contract():
    text = _template_text()
    forbidden = ["Tier 1", "Tier 2", "Tier 3", "TIER1_CITIES", "TIER2_CITIES", "TIER3_CITIES", "Coverage Tier"]
    for item in forbidden:
        assert item not in text


def test_summarization_docs_include_model_provider_and_interval():
    docs = (files("camera_discovery_map_ui").joinpath("../..") if False else None)
    text = open("docs/summarization_contract.md", encoding="utf-8").read()
    assert "summarizer.provider" in text
    assert "summarizer.model" in text
    assert "sample_window_seconds" in text
    assert "15s" in text and "300s" in text
