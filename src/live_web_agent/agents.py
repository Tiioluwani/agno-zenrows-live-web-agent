from __future__ import annotations

from agno.agent import Agent
from agno.models.openai import OpenAIChat

from .config import Settings
from .schemas import FetchedPage, MarketSnapshot
from .web import fetch_with_zenrows


def build_agents(settings: Settings) -> tuple[Agent, Agent]:
    model = OpenAIChat(id=settings.openai_model, api_key=settings.openai_api_key)

    def fetch_with_zenrows_tool(url: str) -> dict[str, object]:
        """Fetch a public page through Zenrows and return compact page text."""
        try:
            return fetch_with_zenrows(url, api_key=settings.zenrows_api_key)
        except Exception:
            # Request exceptions can include the complete query string. Do not let
            # Zenrows credentials enter Agno logs or the model's tool result.
            raise RuntimeError("Zenrows request failed") from None

    # Agno and the model should see the public tool name, never its credential.
    fetch_with_zenrows_tool.__name__ = "fetch_with_zenrows"

    fetch_agent = Agent(
        name="Web data agent",
        model=model,
        tools=[fetch_with_zenrows_tool],
        output_schema=FetchedPage,
        instructions=[
            "Always call fetch_with_zenrows for the supplied URL.",
            "Return only the fetched page data. Do not invent missing content.",
        ],
    )
    processing_agent = Agent(
        name="Market intelligence agent",
        model=model,
        output_schema=MarketSnapshot,
        instructions=[
            "Extract only values supported by the supplied page data.",
            "Use null for missing fields and quote short evidence snippets.",
        ],
    )
    return fetch_agent, processing_agent
