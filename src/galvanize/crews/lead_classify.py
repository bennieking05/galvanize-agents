"""Lead classification crew: Audience Classifier solo."""

from crewai import Crew, Process, Task

from galvanize.agents import classifier_agent
from galvanize.config import get_embedder_config


def _classify_task() -> Task:
    return Task(
        description="""Classify this prospect/lead into one of the four Galvanize audience segments and recommend how to engage them.

Prospect description: {description}

Segments: (1) Developers & Project Sponsors, (2) Tax Credit Investors & Syndicators, (3) CDEs, (4) Community Leaders & Nonprofit Executives.

Output: (1) Primary segment and confidence; (2) key frustrations they likely feel; (3) 2–3 content types or post themes that would resonate; (4) suggested engagement approach (e.g., DM with resource, invite to webinar, send market brief). Be specific and actionable.""",
        expected_output="A structured classification: primary segment, key frustrations, recommended content types, and a concrete next step for engagement.",
        agent=classifier_agent,
    )


def lead_classify_crew() -> Crew:
    return Crew(
        agents=[classifier_agent],
        tasks=[_classify_task()],
        process=Process.sequential,
        verbose=True,
        embedder=get_embedder_config(),
    )


def run_lead_classify(description: str) -> str:
    """Run the lead classifier and return the classification and recommendations."""
    crew = lead_classify_crew()
    result = crew.kickoff(inputs={"description": description})
    return str(result.raw) if hasattr(result, "raw") else str(result)
