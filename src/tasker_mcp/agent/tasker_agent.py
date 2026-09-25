"""Tasker Agent - Standalone agent and Strands SDK factory.

Provides two usage modes:
1. TaskerAgent: Standalone class that calls server tools directly (no MCP needed)
2. create_tasker_agent(): Factory for Strands SDK with MCPClient via stdio
"""

import json
import sys
from pathlib import Path
from typing import Any, Optional

from tasker_mcp.knowledge import (
    get_action_by_code,
    get_pattern_by_id,
    search_actions,
    search_events,
    search_patterns,
    search_states,
    search_variables,
)
from tasker_mcp.xml_engine import TaskerXMLGenerator
from tasker_mcp.xml_engine.builder import quick_project, quick_task
from tasker_mcp.xml_engine.models import (
    EventContext,
    StateContext,
    TaskerAction,
    TaskerProfile,
    TaskerProject,
    TaskerTask,
    TimeContext,
)


class TaskerAgent:
    """Standalone Tasker automation agent.

    Calls the knowledge base and XML engine directly without requiring
    an MCP connection. Useful for scripting, testing, and embedding.

    Usage:
        agent = TaskerAgent()
        xml = agent.generate_task("My Task", [
            {"code": 548, "args": {"arg0": "Hello!"}},
            {"code": 425, "int_args": {"arg0": 1}},
        ])
        agent.save_task("My Task", [...], "output/my_task.tsk.xml")
    """

    def __init__(self):
        self._generator = TaskerXMLGenerator()

    # ─── Search Methods ───

    def search_actions(self, query: str, category: Optional[str] = None) -> list[dict]:
        """Search Tasker actions by name/description."""
        results = search_actions(query, category)
        return [
            {"code": a.code, "name": a.name, "category": a.category, "description": a.description}
            for a in results
        ]

    def search_events(self, query: str, category: Optional[str] = None) -> list[dict]:
        """Search Tasker profile events."""
        results = search_events(query, category)
        return [
            {"code": e.code, "name": e.name, "category": e.category, "description": e.description}
            for e in results
        ]

    def search_states(self, query: str, category: Optional[str] = None) -> list[dict]:
        """Search Tasker profile states."""
        results = search_states(query, category)
        return [
            {"code": s.code, "name": s.name, "category": s.category, "description": s.description}
            for s in results
        ]

    def search_variables(self, query: str, category: Optional[str] = None) -> list[dict]:
        """Search Tasker built-in variables."""
        results = search_variables(query, category)
        return [
            {"name": v.name, "description": v.description, "category": v.category}
            for v in results
        ]

    def get_action_info(self, code: int) -> Optional[dict]:
        """Get detailed info about an action by code."""
        action = get_action_by_code(code)
        if action is None:
            return None
        return {
            "code": action.code,
            "name": action.name,
            "category": action.category,
            "description": action.description,
            "args": action.args,
        }

    def get_pattern(self, pattern_id: str) -> Optional[dict]:
        """Get a common automation pattern by ID."""
        pattern = get_pattern_by_id(pattern_id)
        if pattern is None:
            return None
        return {
            "id": pattern.id,
            "name": pattern.name,
            "description": pattern.description,
            "category": pattern.category,
            "profile_type": pattern.profile_type,
            "action_codes": pattern.action_codes,
            "variables_used": pattern.variables_used,
            "example": pattern.example_description,
        }

    # ─── Generation Methods ───

    def generate_task(self, name: str, actions: list[dict], priority: int = 100) -> str:
        """Generate a .tsk.xml from a list of action dicts.

        Args:
            name: Task name.
            actions: List of action dicts with 'code', optional 'args', 'int_args'.
            priority: Task priority (default 100).

        Returns:
            Valid Tasker XML string.
        """
        task_actions = [
            TaskerAction(
                code=a["code"],
                args=a.get("args", {}),
                int_args=a.get("int_args", {}),
                label=a.get("label"),
            )
            for a in actions
        ]
        task = TaskerTask(id=1, name=name, priority=priority, actions=task_actions)
        return self._generator.generate_task(task)

    def generate_profile(
        self,
        name: str,
        trigger_type: str,
        trigger_config: dict,
        entry_task_name: str,
        entry_actions: list[dict],
        exit_task_name: Optional[str] = None,
        exit_actions: Optional[list[dict]] = None,
    ) -> str:
        """Generate a .prf.xml with profile trigger and tasks.

        Args:
            name: Profile name.
            trigger_type: 'event', 'state', or 'time'.
            trigger_config: Trigger configuration dict.
            entry_task_name: Entry task name.
            entry_actions: List of action dicts for entry task.
            exit_task_name: Optional exit task name.
            exit_actions: Optional list of action dicts for exit task.

        Returns:
            Valid Tasker XML string.
        """
        entry_acts = [
            TaskerAction(code=a["code"], args=a.get("args", {}), int_args=a.get("int_args", {}))
            for a in entry_actions
        ]
        entry_task = TaskerTask(id=1, name=entry_task_name, actions=entry_acts)

        exit_task = None
        if exit_task_name and exit_actions:
            exit_acts = [
                TaskerAction(code=a["code"], args=a.get("args", {}), int_args=a.get("int_args", {}))
                for a in exit_actions
            ]
            exit_task = TaskerTask(id=2, name=exit_task_name, actions=exit_acts)

        profile = TaskerProfile(
            id=1, name=name, entry_task_id=1, exit_task_id=2 if exit_task else None
        )

        if trigger_type == "event":
            profile.event_contexts.append(
                EventContext(code=trigger_config["code"], args=trigger_config.get("args", {}), int_args=trigger_config.get("int_args", {}))
            )
        elif trigger_type == "state":
            profile.state_contexts.append(
                StateContext(code=trigger_config["code"], args=trigger_config.get("args", {}), int_args=trigger_config.get("int_args", {}))
            )
        elif trigger_type == "time":
            profile.time_contexts.append(TimeContext(**trigger_config))

        tasks = [entry_task]
        if exit_task:
            tasks.append(exit_task)
        return self._generator.generate_profile(profile, tasks)

    def generate_project(self, name: str, profiles_config: list[dict]) -> str:
        """Generate a .prj.xml from a list of profile configurations.

        Args:
            name: Project name.
            profiles_config: List of profile config dicts, each with:
                - name, trigger_type, trigger_config, entry_task, exit_task (optional)

        Returns:
            Valid Tasker XML string.
        """
        from tasker_mcp.server import generate_project_xml
        return generate_project_xml(name, json.dumps(profiles_config))

    # ─── Fluent Builders ───

    def quick_task(self, name: str, task_id: int = 1):
        """Get a fluent TaskBuilder instance."""
        return quick_task(name, task_id)

    def quick_project(self, name: str):
        """Get a fluent ProjectBuilder instance."""
        return quick_project(name)

    # ─── File Output ───

    def save_task(self, name: str, actions: list[dict], filepath: str) -> str:
        """Generate and save a task XML to a file."""
        xml = self.generate_task(name, actions)
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        Path(filepath).write_text(xml, encoding="utf-8")
        return xml

    def save_profile(self, filepath: str, **kwargs) -> str:
        """Generate and save a profile XML to a file."""
        xml = self.generate_profile(**kwargs)
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        Path(filepath).write_text(xml, encoding="utf-8")
        return xml

    # ─── Validation ───

    def validate_xml(self, xml_content: str) -> dict:
        """Validate Tasker XML structure. Returns dict with valid, errors, info."""
        from tasker_mcp.server import validate_tasker_xml
        return json.loads(validate_tasker_xml(xml_content))


def create_tasker_agent() -> dict[str, Any]:
    """Factory for creating a Tasker agent via Strands SDK with MCPClient.

    Returns a configuration dict for use with Strands Agent SDK.
    The agent connects to the Tasker MCP Server via stdio transport.

    Usage with Strands SDK:
        from strands import Agent
        from strands.tools.mcp import MCPClient

        config = create_tasker_agent()
        mcp_client = MCPClient(config["transport"])

        with mcp_client:
            agent = Agent(tools=mcp_client.list_tools())
            response = agent(
                "Create a Tasker task that flashes 'Hello' and enables WiFi"
            )

    Returns:
        Dict with 'transport' config for MCPClient stdio connection.
    """
    # Find the python executable in the venv or system
    python_exe = sys.executable

    return {
        "name": "tasker-mcp-server",
        "transport": {
            "type": "stdio",
            "command": python_exe,
            "args": ["-m", "tasker_mcp"],
        },
        "description": (
            "Tasker MCP Server - Generate valid Tasker XML automation "
            "configurations for Android. 373 actions, 82 events, 50 states."
        ),
        "tools": [
            "search_tasker_actions",
            "search_tasker_events",
            "search_tasker_states",
            "search_tasker_variables",
            "generate_task_xml",
            "generate_profile_xml",
            "generate_project_xml",
            "generate_quick_automation",
            "validate_tasker_xml",
            "get_action_info",
            "list_action_categories",
            "list_common_patterns",
            "get_pattern_details",
        ],
        "resources": [
            "tasker://reference/action-codes",
            "tasker://reference/event-codes",
            "tasker://reference/state-codes",
            "tasker://reference/variables",
        ],
    }
