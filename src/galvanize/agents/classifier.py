"""Audience Classifier agent: classifies prospects into the four segments with engagement recommendations."""

from crewai import Agent
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource

from galvanize.config import get_knowledge_dir, get_llm


def _load_knowledge(*parts: str) -> str:
    path = get_knowledge_dir()
    for part in parts:
        path = path / part
    return path.read_text(encoding="utf-8")


def _classifier_knowledge() -> StringKnowledgeSource:
    content = "\n\n---\n\n".join([
        _load_knowledge("segments", "developers.md"),
        _load_knowledge("segments", "investors.md"),
        _load_knowledge("segments", "cdes.md"),
        _load_knowledge("segments", "community_leaders.md"),
        _load_knowledge("consumption_habits.md"),
    ])
    return StringKnowledgeSource(content=content)


classifier_agent = Agent(
    role="Audience Classifier",
    goal="Classify prospects and leads into one of the four Galvanize segments (Developers, Investors, CDEs, Community Leaders) and recommend content types and engagement approaches based on their profile and stated needs.",
    backstory="You are an expert at reading between the lines of job titles, organization types, and stated interests. You know the four NMTC/HTC audience segments inside out: their frustrations, how they consume content, and what conversion path works. You output a clear segment classification plus specific content and outreach recommendations.",
    llm=get_llm(),
    allow_delegation=False,
    verbose=True,
    knowledge_sources=[_classifier_knowledge()],
)
