#!/usr/bin/env python3
"""Translate a 0.4.7 team-state JSON into the 0.6.2 layout."""
from __future__ import annotations
import json, pathlib, sys
from typing import Any, Mapping

_MANAGER_TYPE_TO_NAME = {
    "RoundRobinManagerState": "RoundRobinGroupChatManager",
    "SelectorManagerState":   "SelectorGroupChatManager",
    "SwarmManagerState":      "SwarmGroupChatManager",
    "MagenticOneOrchestratorState": "MagenticOneOrchestrator",
    "BaseGroupChatManagerState":    "GroupChatManager",
}


def migrate_state(src: Mapping[str, Any]) -> dict[str, Any]:
    if "agent_states" not in src:
        raise ValueError("input does not look like an AutoGen 0.4.x team state")

    new_agent_states: dict[str, Any] = {}
    for key, val in src["agent_states"].items():
        kind = key.split("/", 1)[0]            # strip trailing team-uuid
        if kind == "group_chat_manager":       # map to concrete manager name
            mgr_typ = val.get("type", "")
            kind = _MANAGER_TYPE_TO_NAME.get(mgr_typ, "GroupChatManager")
        new_agent_states[kind] = val

    return {"agent_states": new_agent_states}  # drop top-level team_id


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: python migrate_state.py <old.json> <new.json>")
    old = json.load(open(sys.argv[1]))
    new = migrate_state(old)
    pathlib.Path(sys.argv[2]).write_text(json.dumps(new, indent=2))
    print(f"✅ migrated state written to {sys.argv[2]}")
