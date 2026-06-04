from __future__ import annotations

from dataclasses import asdict, dataclass
import json


@dataclass(frozen=True)
class FrameworkDefinition:
    id: str
    name: str
    package_name: str
    docs_url: str
    best_for: str
    tradeoff: str


@dataclass(frozen=True)
class ScenarioDefinition:
    id: str
    name: str
    domain: str
    summary: str
    default_input: str
    rubric: list[dict[str, str]]


FRAMEWORKS: list[FrameworkDefinition] = [
    FrameworkDefinition(
        id="langchain",
        name="LangChain",
        package_name="langchain",
        docs_url="https://reference.langchain.com/v0.3/python/langchain/agents.html",
        best_for="Broad LLM applications with rich integrations.",
        tradeoff="Fast-moving APIs require version-aware examples.",
    ),
    FrameworkDefinition(
        id="langgraph",
        name="LangGraph",
        package_name="langgraph",
        docs_url="https://docs.langchain.com/oss/python/langgraph",
        best_for="Stateful graph orchestration and durable workflows.",
        tradeoff="Best when the team is comfortable thinking in state transitions.",
    ),
    FrameworkDefinition(
        id="crewai",
        name="CrewAI",
        package_name="crewai",
        docs_url="https://docs.crewai.com/",
        best_for="Role-based collaboration with approachable multi-agent primitives.",
        tradeoff="Less explicit than graph-driven orchestration.",
    ),
    FrameworkDefinition(
        id="agno",
        name="Agno",
        package_name="agno",
        docs_url="https://docs.agno.com/agents",
        best_for="Agent systems with memory, teams and platform expansion.",
        tradeoff="Shines most when you embrace the broader Agno shape.",
    ),
    FrameworkDefinition(
        id="smolagents",
        name="SmolAgents",
        package_name="smolagents",
        docs_url="https://huggingface.co/docs/smolagents/en/index",
        best_for="Small, fast code-agent experimentation.",
        tradeoff="Code-oriented execution needs explicit guardrails.",
    ),
    FrameworkDefinition(
        id="autogen",
        name="Microsoft AutoGen",
        package_name="autogen-agentchat",
        docs_url="https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/agents.html",
        best_for="Conversational multi-agent systems and team interactions.",
        tradeoff="Carries more runtime concepts to explain.",
    ),
    FrameworkDefinition(
        id="openai-agents",
        name="OpenAI Agents SDK",
        package_name="openai-agents",
        docs_url="https://openai.github.io/openai-agents-python/agents/",
        best_for="Lean tool-and-handoff workflows with tracing support.",
        tradeoff="Needs careful explanation so orchestration is not confused with raw API usage.",
    ),
    FrameworkDefinition(
        id="pydanticai",
        name="PydanticAI",
        package_name="pydantic-ai",
        docs_url="https://ai.pydantic.dev/",
        best_for="Typed contracts, validation and structured output.",
        tradeoff="Feels most natural when the team values strict schemas.",
    ),
]

DEFAULT_SCENARIO = ScenarioDefinition(
    id="sql-lineage-triage",
    name="SQL Lineage Triage",
    domain="Data/SQL governance",
    summary="Analyze a SQL change, identify impact, contract risk and promotion recommendation.",
    default_input=(
        "Mudanca proposta: adicionar total_spent e last_order_at ao mart "
        "analytics.customer_360 usando raw.orders e raw.customers. "
        "A tabela alimenta dashboards executivos e um contrato de consumo para CRM."
    ),
    rubric=[
        {"id": "lineage_clarity", "label": "Lineage clarity", "description": "Find source, target and consumers."},
        {"id": "risk_detection", "label": "Risk detection", "description": "Detect contract and downstream risks."},
        {"id": "actionability", "label": "Actionability", "description": "Produce a clear promotion recommendation."},
        {"id": "traceability", "label": "Traceability", "description": "Explain why the answer was reached."},
        {"id": "framework_fit", "label": "Framework fit", "description": "Show what the framework is good at."},
    ],
)


def list_frameworks() -> list[dict[str, str]]:
    return [asdict(framework) for framework in FRAMEWORKS]


def build_prompt(framework_id: str, user_input: str | None = None) -> str:
    framework = next(item for item in FRAMEWORKS if item.id == framework_id)
    scenario_input = user_input or DEFAULT_SCENARIO.default_input
    return (
        f"Framework under comparison: {framework.name}\n"
        f"Scenario: {DEFAULT_SCENARIO.name}\n"
        f"Domain: {DEFAULT_SCENARIO.domain}\n"
        f"Rubric: {json.dumps(DEFAULT_SCENARIO.rubric, ensure_ascii=False)}\n\n"
        "System task:\n"
        "You are an Agentix data governance analyst. Be didactic and concrete. "
        "Return sections: lineage, risks, recommendation, next_steps. "
        "Recommendation must be exactly one of approve, review, block.\n\n"
        f"Task input:\n{scenario_input}\n"
    )
