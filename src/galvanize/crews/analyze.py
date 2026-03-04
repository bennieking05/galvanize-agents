"""Engagement analysis crew: Engagement Analyzer solo."""

from crewai import Crew, Process, Task

from galvanize.agents import analyzer_agent
from galvanize.config import get_embedder_config


def _analyze_task() -> Task:
    return Task(
        description="""Evaluate this content performance data against Galvanize's success metrics and recommend optimizations.

Performance data:
- Impressions: {impressions}
- Engagement rate: {engagement_rate}%
- DMs/inquiries from this post: {dms}
- Post type: {post_type}
Additional context (optional): {context}

Compare to the 6- and 12-month targets (engagement rate 3–5% then 5–7%; DMs 8–15/month then 25–40). Assess whether this post is on track, which segment it likely reached, and what to do next: double down on this post type, try a different format, or adjust targeting. Be specific.""",
        expected_output="A short assessment: performance vs. targets, segment reach interpretation, and 2–3 concrete recommendations for the next content cycle.",
        agent=analyzer_agent,
    )


def analyze_crew() -> Crew:
    return Crew(
        agents=[analyzer_agent],
        tasks=[_analyze_task()],
        process=Process.sequential,
        verbose=True,
        embedder=get_embedder_config(),
    )


def run_analyze(
    impressions: int,
    engagement_rate: float,
    dms: int,
    post_type: str,
    context: str = "",
) -> str:
    """Run the engagement analyzer and return the assessment and recommendations."""
    crew = analyze_crew()
    inputs = {
        "impressions": str(impressions),
        "engagement_rate": str(engagement_rate),
        "dms": str(dms),
        "post_type": post_type,
        "context": context or "None",
    }
    result = crew.kickoff(inputs=inputs)
    return str(result.raw) if hasattr(result, "raw") else str(result)
