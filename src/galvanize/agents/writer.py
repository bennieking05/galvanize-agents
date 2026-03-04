"""Segment Content Writer agent: generates LinkedIn-ready content for each audience segment."""

from crewai import Agent
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource

from galvanize.config import get_knowledge_dir, get_llm


def _load_knowledge(*parts: str) -> str:
    path = get_knowledge_dir()
    for part in parts:
        path = path / part
    return path.read_text(encoding="utf-8")


def _writer_knowledge() -> StringKnowledgeSource:
    content = "\n\n---\n\n".join([
        _load_knowledge("segments", "developers.md"),
        _load_knowledge("segments", "investors.md"),
        _load_knowledge("segments", "cdes.md"),
        _load_knowledge("segments", "community_leaders.md"),
        _load_knowledge("consumption_habits.md"),
    ])
    return StringKnowledgeSource(content=content)


writer_agent = Agent(
    role="Segment Content Writer",
    goal="Write LinkedIn-ready posts for Galvanize Sustainable Capital that match each audience segment's emotional triggers, follow/engage/buy triggers, and preferred formats—plain language, no jargon, clarity over complexity.",
    backstory="You are a senior B2B content writer specializing in community development and tax credit finance. You write for developers, investors, CDEs, and community leaders. You know their frustrations and speak to them directly. You produce educational carousels, impact spotlights, policy updates, case study frameworks, common-mistakes posts, and contrarian takes that build trust and drive DMs.",
    llm=get_llm(),
    allow_delegation=False,
    verbose=True,
    knowledge_sources=[_writer_knowledge()],
)
