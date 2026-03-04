"""Engagement Analyzer agent: evaluates content performance against success metrics and recommends optimizations."""

from crewai import Agent
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource

from galvanize.config import get_knowledge_dir, get_llm


def _load_knowledge(*parts: str) -> str:
    path = get_knowledge_dir()
    for part in parts:
        path = path / part
    return path.read_text(encoding="utf-8")


def _analyzer_knowledge() -> StringKnowledgeSource:
    content = "\n\n---\n\n".join([
        _load_knowledge("implementation.md"),
        _load_knowledge("strategy_matrix.md"),
        _load_knowledge("consumption_habits.md"),
    ])
    return StringKnowledgeSource(content=content)


analyzer_agent = Agent(
    role="Engagement Analyzer",
    goal="Evaluate LinkedIn content performance against Galvanize's success metrics (followers, engagement rate, DMs, gated downloads, advisory leads) and recommend specific optimizations for the next content cycle.",
    backstory="You are a content and social analytics expert for B2B professional services. You know what good looks like for NMTC/HTC advisory: 3–5% engagement near-term, 5–7% at 12 months, and a clear path from content to DMs and advisory engagements. You tie performance back to segment reach and post type, and suggest concrete next steps.",
    llm=get_llm(),
    allow_delegation=False,
    verbose=True,
    knowledge_sources=[_analyzer_knowledge()],
)
