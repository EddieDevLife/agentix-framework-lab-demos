from __future__ import annotations

import asyncio
import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from .scenario import DEFAULT_SCENARIO, build_prompt


OUTPUT_ROOT = Path("outputs")
DEFAULT_MODEL = "gpt-4o-mini"


def run_demo(framework_id: str, user_input: str | None = None, model: str | None = None) -> dict[str, Any]:
    load_dotenv()
    prompt = build_prompt(framework_id, user_input)
    result = asyncio.run(_run(framework_id, prompt, model))
    _save_result(framework_id, result)
    return result


async def _run(framework_id: str, prompt: str, model: str | None = None) -> dict[str, Any]:
    run_id = f"{framework_id}-{uuid.uuid4()}"
    started_at = datetime.now(timezone.utc).isoformat()
    selected_model = model or os.getenv("OPENAI_MODEL") or DEFAULT_MODEL

    if not os.getenv("OPENAI_API_KEY"):
        return {
            "run_id": run_id,
            "framework_id": framework_id,
            "scenario_id": DEFAULT_SCENARIO.id,
            "status": "setup_required",
            "started_at": started_at,
            "message": "Set OPENAI_API_KEY before running live demos.",
        }

    try:
        output = await _execute_framework(framework_id, prompt, selected_model)
        return {
            "run_id": run_id,
            "framework_id": framework_id,
            "scenario_id": DEFAULT_SCENARIO.id,
            "status": "completed",
            "started_at": started_at,
            "model": selected_model,
            "output": output,
        }
    except Exception as exc:
        return {
            "run_id": run_id,
            "framework_id": framework_id,
            "scenario_id": DEFAULT_SCENARIO.id,
            "status": "failed",
            "started_at": started_at,
            "model": selected_model,
            "error": str(exc),
        }


async def _execute_framework(framework_id: str, prompt: str, model: str) -> str:
    if framework_id == "openai-agents":
        return await _run_openai_agents(prompt, model)
    if framework_id == "crewai":
        return await asyncio.to_thread(_run_crewai, prompt, model)
    if framework_id == "pydanticai":
        return await asyncio.to_thread(_run_pydanticai, prompt, model)
    if framework_id == "langgraph":
        return await asyncio.to_thread(_run_langgraph, prompt, model)
    if framework_id == "langchain":
        return await asyncio.to_thread(_run_langchain, prompt, model)
    if framework_id == "agno":
        return await asyncio.to_thread(_run_agno, prompt, model)
    if framework_id == "smolagents":
        return await asyncio.to_thread(_run_smolagents, prompt, model)
    if framework_id == "autogen":
        return await _run_autogen(prompt, model)
    raise ValueError(f"Unsupported framework: {framework_id}")


async def _run_openai_agents(prompt: str, model: str) -> str:
    from openai import AsyncOpenAI
    from agents import Agent, Runner
    from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel

    _configure_agents_tracing()
    client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=_openai_base_url())
    agent = Agent(
        name="Agentix SQL Governance Analyst",
        instructions="You are an Agentix data governance analyst.",
        model=OpenAIChatCompletionsModel(model=model, openai_client=client),
    )
    result = await Runner.run(agent, prompt)
    return str(result.final_output)


def _run_crewai(prompt: str, model: str) -> str:
    from crewai import Agent, Crew, LLM, Process, Task

    _configure_openrouter_api_key()
    analyst = Agent(
        role="SQL Governance Analyst",
        goal="Evaluate SQL lineage changes and recommend promotion decisions.",
        backstory="You are a precise Agentix governance analyst.",
        verbose=False,
        allow_delegation=False,
        llm=LLM(model=model, api_key=os.getenv("OPENAI_API_KEY"), base_url=_openai_base_url()),
    )
    task = Task(
        description=prompt,
        expected_output="A concise governance recommendation with lineage, risks and next steps.",
        agent=analyst,
    )
    result = Crew(agents=[analyst], tasks=[task], process=Process.sequential, verbose=False).kickoff()
    return str(result)


def _run_pydanticai(prompt: str, model: str) -> str:
    from pydantic_ai import Agent
    from pydantic_ai.models.openai import OpenAIChatModel
    from pydantic_ai.providers.openai import OpenAIProvider

    provider = OpenAIProvider(api_key=os.getenv("OPENAI_API_KEY"), base_url=_openai_base_url())
    agent = Agent(OpenAIChatModel(model_name=model, provider=provider))
    result = agent.run_sync(prompt)
    return str(getattr(result, "output", result))


def _run_langgraph(prompt: str, model: str) -> str:
    from langchain_openai import ChatOpenAI
    from langgraph.prebuilt import create_react_agent

    agent = create_react_agent(
        ChatOpenAI(model=model, api_key=os.getenv("OPENAI_API_KEY"), base_url=_openai_base_url()),
        tools=[],
        prompt="You are an Agentix data governance analyst.",
    )
    result = agent.invoke({"messages": [{"role": "user", "content": prompt}]})
    messages = result.get("messages") if isinstance(result, dict) else None
    if messages:
        return str(messages[-1].content)
    return str(result)


def _run_langchain(prompt: str, model: str) -> str:
    from langchain.agents import create_agent
    from langchain_openai import ChatOpenAI

    agent = create_agent(
        model=ChatOpenAI(model=model, api_key=os.getenv("OPENAI_API_KEY"), base_url=_openai_base_url()),
        tools=[],
        system_prompt="You are an Agentix data governance analyst.",
    )
    result = agent.invoke({"messages": [{"role": "user", "content": prompt}]})
    messages = result.get("messages") if isinstance(result, dict) else None
    if messages:
        return str(messages[-1].content)
    return str(result)


def _run_agno(prompt: str, model: str) -> str:
    from agno.agent import Agent
    from agno.models.openai import OpenAIChat

    agent = Agent(
        model=OpenAIChat(id=model, api_key=os.getenv("OPENAI_API_KEY"), base_url=_openai_base_url()),
        instructions="You are an Agentix data governance analyst.",
        markdown=False,
    )
    result = agent.run(prompt)
    return str(getattr(result, "content", result))


def _run_smolagents(prompt: str, model: str) -> str:
    from smolagents import CodeAgent, OpenAIServerModel

    agent = CodeAgent(
        tools=[],
        model=OpenAIServerModel(model_id=model, api_base=_openai_base_url(), api_key=os.getenv("OPENAI_API_KEY")),
        max_steps=3,
        verbosity_level=0,
    )
    return str(agent.run(prompt))


async def _run_autogen(prompt: str, model: str) -> str:
    from autogen_agentchat.agents import AssistantAgent
    from autogen_core.models import ModelFamily
    from autogen_ext.models.openai import OpenAIChatCompletionClient

    _configure_openrouter_api_key()
    client = OpenAIChatCompletionClient(
        model=model,
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=_openai_base_url(),
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": True,
            "family": ModelFamily.GPT_4O,
            "structured_output": True,
            "multiple_system_messages": True,
        },
    )
    agent = AssistantAgent(
        name="agentix_sql_governance_analyst",
        model_client=client,
        system_message="You are an Agentix data governance analyst.",
    )
    try:
        result = await agent.run(task=prompt)
        messages = getattr(result, "messages", None)
        if messages:
            return str(getattr(messages[-1], "content", messages[-1]))
        return str(result)
    finally:
        close = getattr(client, "close", None)
        if close:
            await close()


def _openai_base_url() -> str | None:
    return os.getenv("OPENAI_BASE_URL") or os.getenv("OPENAI_API_BASE") or None


def _configure_openrouter_api_key() -> None:
    api_key = os.getenv("OPENAI_API_KEY") or ""
    base_url = _openai_base_url() or ""
    if api_key.startswith("sk-or-") and "openrouter.ai" in base_url and not os.getenv("OPENROUTER_API_KEY"):
        os.environ["OPENROUTER_API_KEY"] = api_key


def _configure_agents_tracing() -> None:
    base_url = _openai_base_url() or ""
    if "openrouter.ai" in base_url and not os.getenv("OPENAI_AGENTS_DISABLE_TRACING"):
        os.environ["OPENAI_AGENTS_DISABLE_TRACING"] = "1"


def _save_result(framework_id: str, result: dict[str, Any]) -> None:
    output_dir = OUTPUT_ROOT / framework_id
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{result['run_id']}.json"
    path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")


def print_result(result: dict[str, Any]) -> None:
    json.dump(result, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
