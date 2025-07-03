#!/usr/bin/env python3
"""
Create the *documentation* Round-Robin team (primary + critic) with
autogen-agentchat 0.4.7 and dump its state to JSON.

Usage:
    ./venv_047/bin/python generate_state_047.py [output_json]
Default output file: old_state.json
"""
from __future__ import annotations
import asyncio, json, pathlib, sys

# --- tutorial imports --------------------------------------------------------
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient

# --------------------------------------------------------------------------- #
async def main(out_path: str = "old_state.json") -> None:
    # Model client – never contacted because we don't run the team.
    model_client = OpenAIChatCompletionClient(model="gpt-4o-2024-08-06")

    # Primary & critic agents.
    primary = AssistantAgent(
        "primary",
        model_client=model_client,
        system_message="You are a helpful AI assistant.",
    )
    critic = AssistantAgent(
        "critic",
        model_client=model_client,
        system_message="Provide constructive feedback. Respond with 'APPROVE' when your feedbacks are addressed.",
    )

    # Stop when critic says APPROVE.
    termination = TextMentionTermination("APPROVE")

    # Team.
    team = RoundRobinGroupChat([primary, critic], termination_condition=termination)

    # Run the team to initialize it.
    # This is not strictly necessary, but it ensures that the team is ready
    # to be saved, and that the agents have been initialized properly.
    _ = await team.run(
        task="Write a poem about winter.",
    )

    # --- async save ----------------------------------------------------------
    state = await team.save_state()
    pathlib.Path(out_path).write_text(json.dumps(state, indent=2))
    print(f"✅ 0.4.7 state written to {out_path}")


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else "old_state.json"))
