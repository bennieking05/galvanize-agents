"""Content Planning crew: Strategist plans the calendar, Writer produces drafts."""

from crewai import Crew, Process, Task

from galvanize.agents import strategist_agent, writer_agent
from galvanize.config import get_embedder_config


def _plan_task() -> Task:
    return Task(
        description="""Create a content plan for Galvanize Sustainable Capital's LinkedIn for the given time period and target segments.

Time period: {period}
Target segments: {segments}
Additional context (optional): {context}

Use the strategy matrix and consumption habits to choose post types, timing, and expected engagement (follow/engage/buy) for each segment. Output a structured plan: for each planned post, list post type, target segment(s), suggested topic or angle, and best day/time to publish.""",
        expected_output="A structured content plan: list of posts with post type, target segment(s), topic/angle, and recommended publish timing. Clear and actionable for the writer.",
        agent=strategist_agent,
    )


def _write_task(plan_task: Task) -> Task:
    return Task(
        description="""Using the content plan from the Content Strategist (provided in the previous step's output), write LinkedIn-ready draft posts for Galvanize.

For each post in the plan, produce one full draft suitable for LinkedIn: hook, body (plain language, no jargon), and CTA. Match tone and format to the target segment (developers, investors, CDEs, or community leaders) and their follow/engage/buy triggers. Keep each post concise and scannable.""",
        expected_output="A set of full LinkedIn post drafts, one per planned item, with clear labels for post type and target segment. Each draft is ready for light editing and posting.",
        agent=writer_agent,
        context=[plan_task],
    )


def content_planning_crew() -> Crew:
    plan_task = _plan_task()
    write_task = _write_task(plan_task)
    return Crew(
        agents=[strategist_agent, writer_agent],
        tasks=[plan_task, write_task],
        process=Process.sequential,
        verbose=True,
        embedder=get_embedder_config(),
    )


def run_plan_only(period: str, segments: str, context: str = "") -> str:
    """Run only the Strategist to produce a content plan (no drafts)."""
    crew = Crew(
        agents=[strategist_agent],
        tasks=[_plan_task()],
        process=Process.sequential,
        verbose=True,
        embedder=get_embedder_config(),
    )
    inputs = {"period": period, "segments": segments, "context": context or "None"}
    result = crew.kickoff(inputs=inputs)
    return str(result.raw) if hasattr(result, "raw") else str(result)


def run_content_planning(period: str, segments: str, context: str = "") -> str:
    """Run the full content planning crew and return the final output (drafts)."""
    crew = content_planning_crew()
    inputs = {
        "period": period,
        "segments": segments,
        "context": context or "None",
    }
    result = crew.kickoff(inputs=inputs)
    return str(result.raw) if hasattr(result, "raw") else str(result)
