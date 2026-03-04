"""Content Strategist agent: plans content calendars from the strategy matrix and implementation priorities."""

from crewai import Agent
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource

from galvanize.config import get_knowledge_dir, get_llm


def _load_knowledge(*parts: str) -> str:
    path = get_knowledge_dir()
    for part in parts:
        path = path / part
    return path.read_text(encoding="utf-8")


def _strategist_knowledge() -> StringKnowledgeSource:
    content = "\n\n---\n\n".join([
        _load_knowledge("strategy_matrix.md"),
        _load_knowledge("consumption_habits.md"),
        _load_knowledge("implementation.md"),
    ])
    return StringKnowledgeSource(content=content)


strategist_agent = Agent(
    role="Content Strategist",
    goal="Plan weekly and monthly LinkedIn content calendars for Galvanize Sustainable Capital that align with the cross-segment strategy matrix, consumption habits, and implementation priorities for NMTC/HTC advisory.",
    backstory="You are an expert content strategist for community development finance. You know which post types drive follows, engagement, and conversions for each audience segment (developers, investors, CDEs, community leaders). You plan content that fills the market's information gap with clarity and positions Galvanize as the go-to source.",
    llm=get_llm(),
    allow_delegation=False,
    verbose=True,
    knowledge_sources=[_strategist_knowledge()],
)
