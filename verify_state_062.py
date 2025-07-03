#!/usr/bin/env python3
"""
Re-create the Round-Robin team with autogen-agentchat 0.6.2 and
*await* load_state() to ensure the migrated JSON is valid.

Usage:
    ./venv_062/bin/python verify_state_062.py [migrated_state.json]
"""
from __future__ import annotations
import asyncio, json, sys

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient


async def main(path: str = "migrated_state.json") -> None:
    model_client = OpenAIChatCompletionClient(model="gpt-4o-2024-08-06")

    primary = AssistantAgent("primary", model_client=model_client)
    critic  = AssistantAgent("critic",  model_client=model_client)

    team = RoundRobinGroupChat(
        [primary, critic], termination_condition=TextMentionTermination("APPROVE")
    )

    state = json.load(open(path))
    await team.load_state(state)          # <- async instance method
    print("🎉 AutoGen-0.6.2 accepted the migrated state")

    await model_client.close()


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else "migrated_state.json"))
