"""Basic tests for crew instantiation and wiring."""

import os

import pytest


@pytest.mark.skipif(
    not os.environ.get("GOOGLE_API_KEY"),
    reason="GOOGLE_API_KEY required for agent/crew imports (get_llm)",
)
def test_import_crews():
    """Crews can be imported without error when API key is set."""
    from galvanize.crews import (
        content_planning_crew,
        market_intel_crew,
        lead_classify_crew,
        analyze_crew,
    )
    assert content_planning_crew is not None
    assert market_intel_crew is not None
    assert lead_classify_crew is not None
    assert analyze_crew is not None


def test_knowledge_dir_exists():
    """Knowledge base directory and key files exist."""
    from galvanize.config import get_knowledge_dir

    root = get_knowledge_dir()
    assert root.exists()
    assert (root / "strategy_matrix.md").exists()
    assert (root / "segments" / "developers.md").exists()
