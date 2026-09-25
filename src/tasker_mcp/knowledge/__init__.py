"""Tasker Knowledge Base - Complete reference data for Tasker automation."""

from tasker_mcp.knowledge.actions import (
    TASKER_ACTIONS,
    TaskerAction,
    get_action_by_code,
    get_action_by_name,
    search_actions,
)
from tasker_mcp.knowledge.events import (
    PROFILE_EVENTS,
    TaskerEvent,
    get_event_by_code,
    get_event_by_name,
    search_events,
)
from tasker_mcp.knowledge.patterns import (
    AUTOMATION_PATTERNS,
    AutomationPattern,
    get_pattern_by_id,
    search_patterns,
)
from tasker_mcp.knowledge.states import (
    PROFILE_STATES,
    TaskerState,
    get_state_by_code,
    get_state_by_name,
    search_states,
)
from tasker_mcp.knowledge.variables import (
    BUILTIN_VARIABLES,
    TaskerVariable,
    get_variable_by_name,
    search_variables,
)

__all__ = [
    # Actions
    "TaskerAction",
    "TASKER_ACTIONS",
    "get_action_by_code",
    "get_action_by_name",
    "search_actions",
    # Events
    "TaskerEvent",
    "PROFILE_EVENTS",
    "get_event_by_code",
    "get_event_by_name",
    "search_events",
    # States
    "TaskerState",
    "PROFILE_STATES",
    "get_state_by_code",
    "get_state_by_name",
    "search_states",
    # Variables
    "TaskerVariable",
    "BUILTIN_VARIABLES",
    "get_variable_by_name",
    "search_variables",
    # Patterns
    "AutomationPattern",
    "AUTOMATION_PATTERNS",
    "get_pattern_by_id",
    "search_patterns",
]
