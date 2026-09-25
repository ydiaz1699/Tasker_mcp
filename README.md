# Tasker MCP Server

MCP (Model Context Protocol) server for generating valid **Tasker XML** automation configurations for Android. Provides a complete knowledge base of 373 action codes, 82 events, 50 states, and 99 built-in variables, plus an XML engine that produces files directly importable into Tasker.

## Architecture

```
tasker-mcp-server/
├── src/tasker_mcp/
│   ├── __init__.py              # Package (v0.1.0)
│   ├── __main__.py              # Entry point: python -m tasker_mcp
│   ├── server.py                # FastMCP v3 server (13 tools, 4 resources)
│   ├── knowledge/               # Complete Tasker reference data
│   │   ├── actions.py           # 373 action codes (18 categories)
│   │   ├── events.py            # 82 profile event codes
│   │   ├── states.py            # 50 profile state codes
│   │   ├── variables.py         # 99 built-in variables (%BATT, %WIFI, etc.)
│   │   └── patterns.py          # 10 common automation patterns
│   ├── xml_engine/              # XML generation engine
│   │   ├── models.py            # Pydantic models (Task, Profile, Project, Contexts)
│   │   ├── generator.py         # TaskerXMLGenerator (ElementTree)
│   │   └── builder.py           # Fluent API (quick_task, quick_project)
│   └── agent/                   # Agent integrations
│       └── tasker_agent.py      # TaskerAgent + Strands SDK factory
├── examples/                    # Generated XML examples
├── pyproject.toml               # Hatchling build config
├── mcp_config.json              # Kiro/generic MCP config
└── claude_desktop_config.json   # Claude Desktop config
```

## Installation

```bash
# Clone and setup
git clone <repo-url> && cd Tasker_mcp
python -m venv .venv

# Windows
.\.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

# Install dependencies
pip install -e .
```

### Requirements

- Python >= 3.11
- fastmcp >= 2.0
- pydantic >= 2.0

## Usage

### 1. MCP Server (stdio)

Run the server directly for MCP clients:

```bash
python -m tasker_mcp
```

### 2. Kiro IDE

Add to `.kiro/settings/mcp.json`:

```json
{
  "mcpServers": {
    "tasker-mcp": {
      "command": "python",
      "args": ["-m", "tasker_mcp"],
      "disabled": false
    }
  }
}
```

### 3. Claude Desktop

Copy `claude_desktop_config.json` to your Claude Desktop config directory and update the paths.

### 4. Strands SDK (Agent)

```python
from strands import Agent
from strands.tools.mcp import MCPClient
from tasker_mcp.agent import create_tasker_agent

config = create_tasker_agent()
mcp_client = MCPClient(config["transport"])

with mcp_client:
    agent = Agent(tools=mcp_client.list_tools())
    response = agent("Create a battery saver task that disables WiFi and Bluetooth")
```

### 5. Programmatic (No MCP)

```python
from tasker_mcp.agent import TaskerAgent

agent = TaskerAgent()

# Search the knowledge base
actions = agent.search_actions("wifi")
events = agent.search_events("sms")

# Generate XML directly
xml = agent.generate_task("My Task", [
    {"code": 548, "args": {"arg0": "Hello!"}},
    {"code": 425, "int_args": {"arg0": 1}},  # WiFi ON
])

# Fluent builder
xml = (
    agent.quick_task("Morning Routine")
    .flash("Good morning!")
    .wifi(True)
    .brightness(200)
    .media_volume(10)
    .build()
)

# Save to file
agent.save_task("My Task", actions_list, "output/my_task.tsk.xml")
```

## Tools (14)

| Tool | Description |
|------|-------------|
| `search_tasker_actions` | Search 373 action codes by name/description, filter by category |
| `search_tasker_events` | Search 82 profile event triggers |
| `search_tasker_states` | Search 50 profile state contexts |
| `search_tasker_variables` | Search 99 built-in variables (%BATT, %WIFI, etc.) |
| `generate_task_xml` | Generate .tsk.xml from action list |
| `generate_profile_xml` | Generate .prf.xml with trigger + entry/exit tasks |
| `generate_project_xml` | Generate .prj.xml with multiple profiles |
| `generate_quick_automation` | Generate XML from natural language description |
| `validate_tasker_xml` | Validate Tasker XML structure and action codes |
| `get_action_info` | Get detailed info for a specific action code |
| `list_action_categories` | List all 18 action categories with counts |
| `list_common_patterns` | List 10 pre-built automation patterns |
| `get_pattern_details` | Get full details of a specific pattern |
| `run_tasker_task` | (Optional, opt-in) Trigger an existing Tasker task live on the phone via `POST /run_task`. Needs `TASKER_HOST`/`TASKER_API_KEY`. |

> **Diseñar vs ejecutar:** las tools `search_*`/`generate_*`/`validate_*` diseñan y
> generan XML **offline** (no tocan el teléfono). `run_tasker_task` **ejecuta en vivo**
> una tarea ya existente en el móvil y es opcional (desactivada si no configuras las
> env vars). Cómo el LLM evita errores de códigos/argumentos y cómo se integra con el
> MCP externo `dceluis/tasker-mcp`: ver [`docs/integracion-dceluis.md`](docs/integracion-dceluis.md).

## Resources (4)

| URI | Description |
|-----|-------------|
| `tasker://reference/action-codes` | Complete 373 action codes by category |
| `tasker://reference/event-codes` | Complete 82 event codes by category |
| `tasker://reference/state-codes` | Complete 50 state codes by category |
| `tasker://reference/variables` | All built-in variables by category |

## Action Categories (18)

App, Flow, Communication, Alert, Network, Variable, File, Media, Display, Audio, Code, System, Scene, Input, Google, Tasker, Plugin, Misc

## Automation Patterns (10)

| Pattern | Description |
|---------|-------------|
| `battery_saver` | Disable radios and reduce brightness when battery low |
| `silent_at_work` | Vibrate mode when connected to work WiFi |
| `wifi_at_home` | Auto-enable WiFi near home cell towers |
| `morning_routine` | Timed actions for starting the day |
| `auto_reply_sms` | Auto-reply to SMS when busy/driving |
| `shake_flashlight` | Toggle torch by shaking the device |
| `notification_on_connect` | Actions when BT device connects |
| `http_request_pattern` | HTTP API calls with response parsing |
| `geofence_action` | Location-based triggers and actions |
| `app_launch_action` | Custom settings per app in foreground |

## Examples

The `examples/` directory contains 5 ready-to-import XML files:

1. **01_hello_world.tsk.xml** - Simple task: flash, vibrate, say, variable set
2. **02_battery_saver.prf.xml** - Profile: low battery state triggers power saving
3. **03_morning_routine.tsk.xml** - Task: WiFi, brightness, volumes, HTTP, TTS
4. **04_smart_doorbell.prf.xml** - Profile: BT connect event triggers notification + photo
5. **05_full_project.prj.xml** - Full project: 3 profiles (work/night/SMS), 5 tasks

### Importing into Tasker

1. Copy the `.xml` file to your Android device
2. In Tasker, long-press the relevant tab (TASKS/PROFILES)
3. Select "Import Task" / "Import Profile" / "Import Project"
4. Navigate to and select the file

## XML Format Reference

Tasker XML files follow this structure (from [Taskomater/Tasker-XML-Info](https://github.com/Taskomater/Tasker-XML-Info)):

```xml
<TaskerData sr="" dvi="1" tv="6.3.13">
  <Task sr="task1">
    <id>1</id>
    <nme>Task Name</nme>
    <Action sr="act0" ve="7">
      <code>548</code>
      <Str sr="arg0" ve="3">Hello World</Str>
    </Action>
  </Task>
</TaskerData>
```

File extensions:
- `.tsk.xml` - Single task
- `.prf.xml` - Profile with tasks  
- `.prj.xml` - Project (profiles + tasks)

## Development

```bash
# Run server in development
python -m tasker_mcp

# Test imports
python -c "from tasker_mcp.knowledge import TASKER_ACTIONS; print(len(TASKER_ACTIONS))"

# Generate example XML
python examples/xml_engine_demo.py
```

## Data Sources

- Action/Event/State codes: [Taskomater/Tasker-XML-Info](https://github.com/Taskomater/Tasker-XML-Info) (Tasker v5.15.5-beta)
- Action descriptions: [tasker.joaoapps.com](https://tasker.joaoapps.com/userguide/en/help/ah_index.html)
- Variables: [Tasker Variables Reference](https://tasker.joaoapps.com/userguide/en/variables.html)

## License

MIT
