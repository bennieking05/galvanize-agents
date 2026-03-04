"""Web search tool for the Policy Monitor agent. Uses Serper when SERPER_API_KEY is set."""

import os

# Prefer crewai_tools SerperDevTool when API key is available
try:
    from crewai_tools import SerperDevTool

    if os.environ.get("SERPER_API_KEY"):
        web_search_tool = SerperDevTool(n_results=8)
    else:
        web_search_tool = None
except Exception:
    web_search_tool = None


def get_web_search_tool():
    """Return the web search tool if configured, else None (Policy Monitor runs without live search)."""
    if web_search_tool is not None:
        return web_search_tool
    if os.environ.get("SERPER_API_KEY"):
        try:
            from crewai_tools import SerperDevTool
            return SerperDevTool(n_results=8)
        except Exception:
            pass
    return None
