"""CLI for Galvanize agents: plan, create, market-update, classify, analyze."""

import typer

from galvanize.crews import (
    run_analyze,
    run_content_planning,
    run_lead_classify,
    run_market_intel,
    run_plan_only,
)

app = typer.Typer(
    name="galvanize",
    help="Galvanize Sustainable Capital — NMTC/HTC content strategy agents.",
)


@app.command()
def plan(
    period: str = typer.Option("next week", "--period", "-p", help="Time period to plan (e.g. 'next week', 'March 2026')"),
    segments: str = typer.Option("all", "--segments", "-s", help="Target segments: developers, investors, cdes, community, or all"),
    context: str = typer.Option("", "--context", "-c", help="Optional context or topics to emphasize"),
):
    """Generate a content plan for the given period and segments (Strategist only)."""
    typer.echo(f"Planning content for {period}, segments: {segments}...")
    output = run_plan_only(period=period, segments=segments, context=context)
    typer.echo(output)


@app.command()
def create(
    period: str = typer.Option("next week", "--period", "-p", help="Time period for the content batch"),
    segments: str = typer.Option("all", "--segments", "-s", help="Target segments: developers, investors, cdes, community, or all"),
    posts: int = typer.Option(5, "--posts", "-n", help="Approximate number of posts to plan and draft"),
    context: str = typer.Option("", "--context", "-c", help="Optional context for the strategist"),
):
    """Generate a full content batch: plan + LinkedIn drafts (Strategist -> Writer)."""
    typer.echo(f"Creating content batch for {period}, segments: {segments}, ~{posts} posts...")
    output = run_content_planning(
        period=period,
        segments=segments,
        context=context or f"Request approximately {posts} posts.",
    )
    typer.echo(output)


@app.command("market-update")
def market_update(
    topic: str = typer.Argument(..., help="Topic for the policy/market update (e.g. 'NMTC allocation round results')"),
):
    """Generate a timely policy or market update post (Monitor -> Writer)."""
    typer.echo(f"Researching and drafting market update: {topic}...")
    output = run_market_intel(topic=topic)
    typer.echo(output)


@app.command()
def classify(
    description: str = typer.Argument(..., help="Prospect description (title, org, stated needs)"),
):
    """Classify a lead into a segment and get engagement recommendations."""
    typer.echo("Classifying prospect...")
    output = run_lead_classify(description=description)
    typer.echo(output)


@app.command()
def analyze(
    impressions: int = typer.Option(..., "--impressions", "-i", help="Post impressions"),
    engagement_rate: float = typer.Option(..., "--engagement-rate", "-e", help="Engagement rate (e.g. 4.2 for 4.2%%)"),
    dms: int = typer.Option(0, "--dms", "-d", help="DMs or inquiries from this post"),
    post_type: str = typer.Option("post", "--post-type", "-t", help="Post type (e.g. 'educational carousel')"),
    context: str = typer.Option("", "--context", "-c", help="Optional extra context"),
):
    """Analyze post performance and get recommendations."""
    typer.echo("Analyzing performance...")
    output = run_analyze(
        impressions=impressions,
        engagement_rate=engagement_rate,
        dms=dms,
        post_type=post_type,
        context=context,
    )
    typer.echo(output)


if __name__ == "__main__":
    app()
