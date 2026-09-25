"""Tasker MCP Server - FastMCP v3 server exposing Tasker automation tools.

Provides 13 tools, 4 resources for generating Tasker XML configurations,
searching the Tasker knowledge base, and working with automation patterns.

Run with: python -m tasker_mcp
"""

import json
from typing import Optional

from fastmcp import FastMCP

from tasker_mcp.knowledge import (
    AUTOMATION_PATTERNS,
    BUILTIN_VARIABLES,
    PROFILE_EVENTS,
    PROFILE_STATES,
    TASKER_ACTIONS,
    get_action_by_code,
    get_pattern_by_id,
    search_actions,
    search_events,
    search_patterns,
    search_states,
    search_variables,
)
from tasker_mcp.xml_engine import (
    AppContext,
    EventContext,
    StateContext,
    TaskerXMLGenerator,
    TimeContext,
)
from tasker_mcp.xml_engine.models import (
    TaskerAction,
    TaskerProfile,
    TaskerProject,
    TaskerTask,
)
from tasker_mcp import live

mcp = FastMCP(
    name="Tasker MCP Server",
    instructions=(
        "Generate valid Tasker XML automation configurations for Android. "
        "Search 373 action codes, 82 events, 50 states, and built-in variables. "
        "Build tasks, profiles, and projects importable directly into Tasker. "
        "ALWAYS look up codes with the search_* tools (never invent them) and "
        "validate output with validate_tasker_xml before returning it. "
        "Optionally, if TASKER_HOST/TASKER_API_KEY are set, run_tasker_task can "
        "trigger an existing task on the phone in real time."
    ),
)

generator = TaskerXMLGenerator()


# ═══════════════════════════════════════════════════════════════════════════════
# TOOLS (13)
# ═══════════════════════════════════════════════════════════════════════════════


@mcp.tool
def search_tasker_actions(query: str, category: Optional[str] = None) -> str:
    """Search Tasker action codes by name or description.

    Args:
        query: Search term (e.g., 'wifi', 'notification', 'variable')
        category: Optional filter by category (App, Flow, Communication, Alert,
                  Network, Variable, File, Media, Display, Audio, Code, System,
                  Scene, Input, Google, Tasker, Plugin, Misc)

    Returns:
        JSON list of matching actions with code, name, category, description, args.
    """
    results = search_actions(query, category)
    return json.dumps(
        [
            {
                "code": a.code,
                "name": a.name,
                "category": a.category,
                "description": a.description,
                "args": a.args,
            }
            for a in results[:25]
        ],
        indent=2,
    )


@mcp.tool
def search_tasker_events(query: str, category: Optional[str] = None) -> str:
    """Search Tasker profile event triggers by name or description.

    Args:
        query: Search term (e.g., 'sms', 'battery', 'shake')
        category: Optional filter (Phone, Communication, Hardware, Battery,
                  File, Date/Time, Sensor, App, Notification, System,
                  Connectivity, Variable, Third Party)

    Returns:
        JSON list of matching events with code, name, category, description, args.
    """
    results = search_events(query, category)
    return json.dumps(
        [
            {
                "code": e.code,
                "name": e.name,
                "category": e.category,
                "description": e.description,
                "args": e.args,
            }
            for e in results[:25]
        ],
        indent=2,
    )


@mcp.tool
def search_tasker_states(query: str, category: Optional[str] = None) -> str:
    """Search Tasker profile state contexts by name or description.

    Args:
        query: Search term (e.g., 'wifi', 'battery', 'bluetooth')
        category: Optional filter (Connectivity, Power, Hardware, Phone,
                  Sensor, App, Plugin)

    Returns:
        JSON list of matching states with code, name, category, description, args.
    """
    results = search_states(query, category)
    return json.dumps(
        [
            {
                "code": s.code,
                "name": s.name,
                "category": s.category,
                "description": s.description,
                "args": s.args,
            }
            for s in results[:25]
        ],
        indent=2,
    )


@mcp.tool
def search_tasker_variables(query: str, category: Optional[str] = None) -> str:
    """Search Tasker built-in variables by name or description.

    Args:
        query: Search term (e.g., 'battery', 'wifi', 'time', 'sms')
        category: Optional filter (Battery, Bluetooth, Call, Date/Time,
                  Display, Location, Network, Phone, SMS, Clipboard,
                  Music, Notification, System, Tasker, Profile)

    Returns:
        JSON list of matching variables with name, description, category.
    """
    results = search_variables(query, category)
    return json.dumps(
        [
            {
                "name": v.name,
                "description": v.description,
                "category": v.category,
                "dynamic": v.dynamic,
            }
            for v in results[:25]
        ],
        indent=2,
    )


@mcp.tool
def generate_task_xml(
    task_name: str,
    actions_json: str,
    priority: int = 100,
    collision: int = 0,
) -> str:
    """Generate a Tasker .tsk.xml file from a list of actions.

    Args:
        task_name: Name for the task.
        actions_json: JSON array of actions. Each action is an object with:
            - code (int): Action code number
            - args (dict, optional): String arguments as {"arg0": "value", ...}
            - int_args (dict, optional): Integer arguments as {"arg0": 1, ...}
            - label (str, optional): Action label
        priority: Task priority (default 100).
        collision: Collision handling: 0=Abort New, 1=Abort Existing, 2=Run Both.

    Returns:
        Valid Tasker XML string (.tsk.xml format).

    Example actions_json:
        [{"code": 548, "args": {"arg0": "Hello!"}},
         {"code": 425, "int_args": {"arg0": 1}}]
    """
    actions_data = json.loads(actions_json)
    actions = []
    for a in actions_data:
        actions.append(
            TaskerAction(
                code=a["code"],
                args=a.get("args", {}),
                int_args=a.get("int_args", {}),
                label=a.get("label"),
            )
        )

    task = TaskerTask(
        id=1,
        name=task_name,
        priority=priority,
        collision=collision,
        actions=actions,
    )
    return generator.generate_task(task)


@mcp.tool
def generate_profile_xml(
    name: str,
    trigger_type: str,
    trigger_config: str,
    entry_task_name: str,
    entry_actions: str,
    exit_task_name: Optional[str] = None,
    exit_actions: Optional[str] = None,
) -> str:
    """Generate a Tasker .prf.xml file with profile trigger and tasks.

    Args:
        name: Profile name.
        trigger_type: One of 'event', 'state', 'time', 'app'.
        trigger_config: JSON config for the trigger. Depends on trigger_type:
            - event: {"code": 7, "args": {"arg0": "*"}}
            - state: {"code": 140, "int_args": {"arg0": 0, "arg1": 20}}
            - time: {"from_hour": 8, "from_minute": 0, "to_hour": 17, "to_minute": 0}
            - app: {"label": "YouTube", "package": "com.google.android.youtube"}
        entry_task_name: Name for the entry task.
        entry_actions: JSON array of actions for entry task (same format as generate_task_xml).
        exit_task_name: Optional name for exit task.
        exit_actions: Optional JSON array of actions for exit task.

    Returns:
        Valid Tasker XML string (.prf.xml format).
    """
    config = json.loads(trigger_config)

    # Build entry task
    entry_acts = [
        TaskerAction(code=a["code"], args=a.get("args", {}), int_args=a.get("int_args", {}))
        for a in json.loads(entry_actions)
    ]
    entry_task = TaskerTask(id=1, name=entry_task_name, actions=entry_acts)

    # Build exit task if provided
    exit_task = None
    if exit_task_name and exit_actions:
        exit_acts = [
            TaskerAction(code=a["code"], args=a.get("args", {}), int_args=a.get("int_args", {}))
            for a in json.loads(exit_actions)
        ]
        exit_task = TaskerTask(id=2, name=exit_task_name, actions=exit_acts)

    # Build profile
    profile = TaskerProfile(
        id=1,
        name=name,
        entry_task_id=1,
        exit_task_id=2 if exit_task else None,
    )

    # Add context based on trigger_type
    if trigger_type == "event":
        profile.event_contexts.append(
            EventContext(code=config["code"], args=config.get("args", {}), int_args=config.get("int_args", {}))
        )
    elif trigger_type == "state":
        profile.state_contexts.append(
            StateContext(code=config["code"], args=config.get("args", {}), int_args=config.get("int_args", {}))
        )
    elif trigger_type == "time":
        profile.time_contexts.append(TimeContext(**config))
    elif trigger_type == "app":
        profile.app_contexts.append(AppContext(**config))

    tasks = [entry_task]
    if exit_task:
        tasks.append(exit_task)

    return generator.generate_profile(profile, tasks)


@mcp.tool
def generate_project_xml(project_name: str, profiles_json: str) -> str:
    """Generate a Tasker .prj.xml file with multiple profiles and tasks.

    Args:
        project_name: Name for the project.
        profiles_json: JSON array of profile objects. Each profile has:
            - name (str): Profile name
            - trigger_type (str): 'event', 'state', 'time', or 'app'
            - trigger_config (dict): Trigger configuration
            - entry_task (dict): {"name": str, "actions": [...]}
            - exit_task (dict, optional): {"name": str, "actions": [...]}

    Returns:
        Valid Tasker XML string (.prj.xml format).
    """
    profiles_data = json.loads(profiles_json)
    profiles = []
    tasks = []
    task_id = 1
    profile_id = 1

    for p in profiles_data:
        # Build entry task
        entry_acts = [
            TaskerAction(code=a["code"], args=a.get("args", {}), int_args=a.get("int_args", {}))
            for a in p["entry_task"]["actions"]
        ]
        entry_task = TaskerTask(id=task_id, name=p["entry_task"]["name"], actions=entry_acts)
        tasks.append(entry_task)
        entry_id = task_id
        task_id += 1

        # Build exit task if provided
        exit_id = None
        if p.get("exit_task"):
            exit_acts = [
                TaskerAction(code=a["code"], args=a.get("args", {}), int_args=a.get("int_args", {}))
                for a in p["exit_task"]["actions"]
            ]
            exit_task = TaskerTask(id=task_id, name=p["exit_task"]["name"], actions=exit_acts)
            tasks.append(exit_task)
            exit_id = task_id
            task_id += 1

        # Build profile
        profile = TaskerProfile(
            id=profile_id,
            name=p["name"],
            entry_task_id=entry_id,
            exit_task_id=exit_id,
        )

        config = p["trigger_config"]
        trigger_type = p["trigger_type"]
        if trigger_type == "event":
            profile.event_contexts.append(
                EventContext(code=config["code"], args=config.get("args", {}), int_args=config.get("int_args", {}))
            )
        elif trigger_type == "state":
            profile.state_contexts.append(
                StateContext(code=config["code"], args=config.get("args", {}), int_args=config.get("int_args", {}))
            )
        elif trigger_type == "time":
            profile.time_contexts.append(TimeContext(**config))
        elif trigger_type == "app":
            profile.app_contexts.append(AppContext(**config))

        profiles.append(profile)
        profile_id += 1

    project = TaskerProject(name=project_name, profiles=profiles, tasks=tasks)
    return generator.generate_project(project)


@mcp.tool
def generate_quick_automation(
    description: str, output_format: str = "task"
) -> str:
    """Generate a quick Tasker automation from a natural language description.

    Matches against known patterns and generates appropriate XML.

    Args:
        description: Natural language description of desired automation
                     (e.g., 'save battery when low', 'silent at work',
                      'flash hello world', 'toggle wifi')
        output_format: Output type - 'task', 'profile', or 'project' (default: 'task')

    Returns:
        Generated Tasker XML based on matched pattern or simple action mapping.
    """
    desc_lower = description.lower()

    # Try to match a known pattern
    matched_patterns = search_patterns(description)
    if matched_patterns:
        pattern = matched_patterns[0]
        # Generate based on pattern
        actions = []
        for code in pattern.action_codes[:5]:
            action_info = get_action_by_code(code)
            if action_info:
                if code in (425, 294, 433, 333):  # Toggle actions
                    actions.append(TaskerAction(code=code, int_args={"arg0": 0}))
                elif code in (810,):  # Brightness
                    actions.append(TaskerAction(code=code, int_args={"arg0": 50}))
                elif code in (304, 305, 307, 308):  # Volume
                    actions.append(TaskerAction(code=code, int_args={"arg0": 5}))
                elif code == 548:  # Flash
                    actions.append(TaskerAction(code=548, args={"arg0": f"{pattern.name} activated"}))
                elif code == 310:  # Vibrate mode
                    actions.append(TaskerAction(code=310, int_args={"arg0": 1}))
                elif code == 312:  # DND
                    actions.append(TaskerAction(code=312, int_args={"arg0": 1}))
                else:
                    actions.append(TaskerAction(code=code))

        task = TaskerTask(id=1, name=pattern.name, actions=actions)

        if output_format == "task":
            return generator.generate_task(task)
        elif output_format == "profile":
            profile = TaskerProfile(id=1, name=pattern.name, entry_task_id=1)
            if pattern.trigger_codes:
                if pattern.profile_type == "event":
                    profile.event_contexts.append(EventContext(code=pattern.trigger_codes[0]))
                elif pattern.profile_type == "state":
                    profile.state_contexts.append(StateContext(code=pattern.trigger_codes[0]))
            return generator.generate_profile(profile, [task])
        else:
            project = TaskerProject(name=pattern.name, tasks=[task])
            return generator.generate_project(project)

    # Simple keyword-to-action mapping for common requests
    simple_actions = []
    if "flash" in desc_lower or "message" in desc_lower:
        msg = description.replace("flash ", "").replace("message ", "").strip() or "Hello!"
        simple_actions.append(TaskerAction(code=548, args={"arg0": msg}))
    if "wifi on" in desc_lower or "enable wifi" in desc_lower:
        simple_actions.append(TaskerAction(code=425, int_args={"arg0": 1}))
    elif "wifi off" in desc_lower or "disable wifi" in desc_lower:
        simple_actions.append(TaskerAction(code=425, int_args={"arg0": 0}))
    if "bluetooth on" in desc_lower:
        simple_actions.append(TaskerAction(code=294, int_args={"arg0": 1}))
    elif "bluetooth off" in desc_lower:
        simple_actions.append(TaskerAction(code=294, int_args={"arg0": 0}))
    if "vibrate" in desc_lower:
        simple_actions.append(TaskerAction(code=61, int_args={"arg0": 500}))
    if "torch" in desc_lower or "flashlight" in desc_lower:
        simple_actions.append(TaskerAction(code=511, int_args={"arg0": 1}))
    if "silent" in desc_lower or "mute" in desc_lower:
        simple_actions.append(TaskerAction(code=310, int_args={"arg0": 2}))
    if "brightness" in desc_lower:
        simple_actions.append(TaskerAction(code=810, int_args={"arg0": 128}))

    if not simple_actions:
        simple_actions.append(TaskerAction(code=548, args={"arg0": description}))

    task = TaskerTask(id=1, name=description[:30], actions=simple_actions)
    return generator.generate_task(task)


@mcp.tool
def validate_tasker_xml(xml_content: str) -> str:
    """Validate a Tasker XML string for structural correctness.

    Checks that the XML is well-formed and has the expected Tasker structure
    (TaskerData root, proper Task/Profile/Action nodes).

    Args:
        xml_content: XML string to validate.

    Returns:
        JSON with validation result: {"valid": bool, "errors": [...], "info": {...}}
    """
    import xml.etree.ElementTree as ET

    errors = []
    info = {}

    # Check well-formedness
    try:
        root = ET.fromstring(xml_content)
    except ET.ParseError as e:
        return json.dumps({"valid": False, "errors": [f"XML parse error: {e}"], "info": {}})

    # Check root element
    if root.tag != "TaskerData":
        errors.append(f"Root element should be 'TaskerData', got '{root.tag}'")

    if not root.get("sr") == "":
        errors.append("TaskerData missing sr='' attribute")

    if not root.get("tv"):
        errors.append("TaskerData missing 'tv' (Tasker version) attribute")

    # Count elements
    tasks = root.findall("Task")
    profiles = root.findall("Profile")
    projects = root.findall("Project")

    info["tasks"] = len(tasks)
    info["profiles"] = len(profiles)
    info["projects"] = len(projects)

    # Validate tasks
    for task in tasks:
        task_id = task.find("id")
        if task_id is None:
            errors.append(f"Task missing <id> element")
        actions = task.findall("Action")
        info.setdefault("total_actions", 0)
        info["total_actions"] += len(actions)
        for action in actions:
            code = action.find("code")
            if code is None:
                errors.append("Action missing <code> element")
            elif code.text and int(code.text) not in TASKER_ACTIONS:
                errors.append(f"Unknown action code: {code.text}")

    # Validate profiles
    for profile in profiles:
        pid = profile.find("id")
        if pid is None:
            errors.append("Profile missing <id> element")
        mid0 = profile.find("mid0")
        if mid0 is None:
            errors.append(f"Profile missing <mid0> (entry task) element")

    return json.dumps({"valid": len(errors) == 0, "errors": errors, "info": info}, indent=2)


@mcp.tool
def get_action_info(code: int) -> str:
    """Get detailed information about a specific Tasker action by its code number.

    Args:
        code: The numeric action code (e.g., 548 for Flash, 425 for WiFi).

    Returns:
        JSON with action details or error message.
    """
    action = get_action_by_code(code)
    if action is None:
        return json.dumps({"error": f"No action found with code {code}"})
    return json.dumps(
        {
            "code": action.code,
            "name": action.name,
            "category": action.category,
            "description": action.description,
            "args": action.args,
        },
        indent=2,
    )


@mcp.tool
def list_action_categories() -> str:
    """List all Tasker action categories with the count of actions in each.

    Returns:
        JSON object mapping category names to action counts and example actions.
    """
    categories: dict[str, list] = {}
    for action in TASKER_ACTIONS.values():
        categories.setdefault(action.category, []).append(action.name)

    result = {}
    for cat, names in sorted(categories.items()):
        result[cat] = {
            "count": len(names),
            "examples": names[:5],
        }
    return json.dumps(result, indent=2)


@mcp.tool
def list_common_patterns() -> str:
    """List all available common automation patterns with brief descriptions.

    Returns:
        JSON array of patterns with id, name, description, and category.
    """
    return json.dumps(
        [
            {
                "id": p.id,
                "name": p.name,
                "description": p.description,
                "category": p.category,
            }
            for p in AUTOMATION_PATTERNS.values()
        ],
        indent=2,
    )


@mcp.tool
def get_pattern_details(pattern_name: str) -> str:
    """Get full details of a specific automation pattern including trigger codes and actions.

    Args:
        pattern_name: Pattern ID (e.g., 'battery_saver', 'silent_at_work',
                      'wifi_at_home', 'morning_routine', 'auto_reply_sms',
                      'shake_flashlight', 'notification_on_connect',
                      'http_request_pattern', 'geofence_action', 'app_launch_action')

    Returns:
        JSON with full pattern details including action codes and example.
    """
    pattern = get_pattern_by_id(pattern_name)
    if pattern is None:
        # Try searching
        results = search_patterns(pattern_name)
        if results:
            pattern = results[0]
        else:
            return json.dumps({"error": f"Pattern '{pattern_name}' not found"})

    # Resolve action names
    action_details = []
    for code in pattern.trigger_codes:
        action_details.append({"code": code, "type": "trigger"})
    for code in pattern.action_codes:
        info = get_action_by_code(code)
        action_details.append({
            "code": code,
            "name": info.name if info else "Unknown",
            "type": "action",
        })

    return json.dumps(
        {
            "id": pattern.id,
            "name": pattern.name,
            "description": pattern.description,
            "category": pattern.category,
            "profile_type": pattern.profile_type,
            "trigger_codes": pattern.trigger_codes,
            "action_codes": pattern.action_codes,
            "action_details": action_details,
            "variables_used": pattern.variables_used,
            "example": pattern.example_description,
        },
        indent=2,
    )


@mcp.tool
def run_tasker_task(task_name: str, arguments_json: Optional[str] = None) -> str:
    """Trigger a task that ALREADY EXISTS in Tasker on the phone (live execution).

    This is optional and OFF by default. It only works if the environment variables
    TASKER_HOST and TASKER_API_KEY are set (and optionally TASKER_PORT, default 1821).
    It sends POST http://<host>:<port>/run_task to Tasker's HTTP server.

    Use this to EXECUTE an automation in real time. To DESIGN/GENERATE a new
    automation as importable XML, use generate_task_xml / generate_profile_xml /
    generate_project_xml instead (those work offline and don't need the phone).

    Args:
        task_name: Exact Tasker task name as it appears on the phone.
        arguments_json: Optional JSON object of arguments, e.g. '{"text": "hi"}'.

    Returns:
        Tasker's response body, or a clear "ERROR: ..." message if not configured
        or unreachable (never raises, so the MCP session stays alive).
    """
    if not live.is_configured():
        return (
            "ERROR: live execution is disabled. Set TASKER_HOST and TASKER_API_KEY "
            "(and optionally TASKER_PORT) to enable run_tasker_task. This repo's main "
            "job is to GENERATE validated Tasker XML offline; live execution is opt-in."
        )
    try:
        args = json.loads(arguments_json) if arguments_json else {}
        if not isinstance(args, dict):
            return "ERROR: arguments_json must be a JSON object, e.g. '{\"text\": \"hi\"}'."
    except json.JSONDecodeError as e:
        return f"ERROR: arguments_json is not valid JSON: {e}"

    try:
        return live.run_task(task_name, args)
    except live.TaskerLiveError as e:
        return f"ERROR: {e}"


# ═══════════════════════════════════════════════════════════════════════════════
# RESOURCES (4)
# ═══════════════════════════════════════════════════════════════════════════════


@mcp.resource("tasker://reference/action-codes")
def resource_action_codes() -> str:
    """Complete reference of all 373 Tasker action codes organized by category."""
    categories: dict[str, list] = {}
    for action in TASKER_ACTIONS.values():
        categories.setdefault(action.category, []).append(
            {"code": action.code, "name": action.name, "description": action.description}
        )
    return json.dumps(categories, indent=2)


@mcp.resource("tasker://reference/event-codes")
def resource_event_codes() -> str:
    """Complete reference of all 82 Tasker profile event codes."""
    categories: dict[str, list] = {}
    for event in PROFILE_EVENTS.values():
        categories.setdefault(event.category, []).append(
            {"code": event.code, "name": event.name, "description": event.description}
        )
    return json.dumps(categories, indent=2)


@mcp.resource("tasker://reference/state-codes")
def resource_state_codes() -> str:
    """Complete reference of all 50 Tasker profile state codes."""
    categories: dict[str, list] = {}
    for state in PROFILE_STATES.values():
        categories.setdefault(state.category, []).append(
            {"code": state.code, "name": state.name, "description": state.description}
        )
    return json.dumps(categories, indent=2)


@mcp.resource("tasker://reference/variables")
def resource_variables() -> str:
    """Complete reference of all Tasker built-in variables."""
    categories: dict[str, list] = {}
    for var in BUILTIN_VARIABLES.values():
        categories.setdefault(var.category, []).append(
            {"name": var.name, "description": var.description, "dynamic": var.dynamic}
        )
    return json.dumps(categories, indent=2)


# ═══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════


def main():
    """Run the Tasker MCP Server."""
    mcp.run()


if __name__ == "__main__":
    main()
