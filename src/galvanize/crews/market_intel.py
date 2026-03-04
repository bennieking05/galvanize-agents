"""Market Intelligence crew: Policy Monitor researches, Writer drafts the content piece."""

from crewai import Crew, Process, Task

from galvanize.agents import get_policy_monitor_agent, writer_agent
from galvanize.config import get_embedder_config


def _monitor_task() -> Task:
    return Task(
        description="""Research the given topic for NMTC/HTC regulatory, market, or legislative developments.

Topic: {topic}

Search for recent news, CDFI Fund updates, IRS guidance, allocation results, or legislative changes. Synthesize the key developments into a short briefing: what happened, why it matters for investors and CDEs, and 2–3 content angles that would resonate with the audience. If web search is available, use it; otherwise use your knowledge of the market and typical sources.""",
        expected_output="A briefing document with: (1) summary of key developments, (2) why it matters for investors and CDEs, (3) 2–3 suggested content angles with target segment and post type.",
        agent=get_policy_monitor_agent(),
    )


def _write_from_briefing_task(monitor_task: Task) -> Task:
    return Task(
        description="""Using the policy/market briefing from the previous step, write one LinkedIn post (or carousel outline) for Galvanize that targets investors and/or CDEs.

The briefing contains the key developments and suggested angles. Choose the strongest angle and produce a full draft: hook, body (plain language, data or specifics where relevant), and CTA. Match the tone to the segment (investors want data and clarity; CDEs want compliance and allocation intelligence).""",
        expected_output="One complete LinkedIn post draft (or carousel outline with slide-by-slide copy) ready for review, with a note on target segment and suggested publish timing.",
        agent=writer_agent,
        context=[monitor_task],
    )


def market_intel_crew() -> Crew:
    monitor_task = _monitor_task()
    write_task = _write_from_briefing_task(monitor_task)
    return Crew(
        agents=[get_policy_monitor_agent(), writer_agent],
        tasks=[monitor_task, write_task],
        process=Process.sequential,
        verbose=True,
        embedder=get_embedder_config(),
    )


def run_market_intel(topic: str) -> str:
    """Run the market intelligence crew and return the final post draft and briefing."""
    crew = market_intel_crew()
    result = crew.kickoff(inputs={"topic": topic})
    return str(result.raw) if hasattr(result, "raw") else str(result)
