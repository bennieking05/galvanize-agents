"""Policy & Market Monitor agent: finds and synthesizes NMTC/HTC regulatory and market developments."""

from crewai import Agent
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource

from galvanize.config import get_knowledge_dir, get_llm
from galvanize.tools.web_search import get_web_search_tool


def _load_knowledge(*parts: str) -> str:
    path = get_knowledge_dir()
    for part in parts:
        path = path / part
    return path.read_text(encoding="utf-8")


def _policy_monitor_knowledge() -> StringKnowledgeSource:
    content = "\n\n---\n\n".join([
        _load_knowledge("market_context.md"),
        _load_knowledge("segments", "investors.md"),
        _load_knowledge("segments", "cdes.md"),
    ])
    return StringKnowledgeSource(content=content)


def get_policy_monitor_agent():
    """Build the Policy Monitor agent with web search tool when SERPER_API_KEY is set."""
    search_tool = get_web_search_tool()
    tools = [search_tool] if search_tool else []
    return Agent(
        role="Policy & Market Monitor",
        goal="Search for and synthesize NMTC/HTC regulatory changes, CDFI Fund updates, market data, and legislative developments; produce briefings and content angles for investors and CDEs.",
        backstory="You are a policy and market analyst focused on community development tax credits. You track the CDFI Fund, IRS guidance, allocation rounds, and competitive dynamics. You know what investors and CDEs care about: counterparty risk, compliance, pricing, and program permanency. You use web search to find the latest news and distill it into actionable briefings when the tool is available; otherwise you rely on your knowledge of the market.",
        llm=get_llm(),
        tools=tools,
        allow_delegation=False,
        verbose=True,
        knowledge_sources=[_policy_monitor_knowledge()],
    )


# Lazy singleton for crews that import the agent by name
policy_monitor_agent = None


def _get_policy_monitor_agent():
    global policy_monitor_agent
    if policy_monitor_agent is None:
        policy_monitor_agent = get_policy_monitor_agent()
    return policy_monitor_agent
