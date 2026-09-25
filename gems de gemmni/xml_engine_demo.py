"""Demo: Tasker XML Engine usage examples.

Run from project root:
    .\.venv\Scripts\python.exe examples/xml_engine_demo.py
"""
import sys
sys.path.insert(0, "src")

from tasker_mcp.xml_engine.builder import quick_task, quick_project
from tasker_mcp.xml_engine.models import StateContext, EventContext, TimeContext

# ─── Example 1: Simple task with fluent builder ───
print("=== Example 1: Simple Task ===")
xml = (
    quick_task("Morning Routine")
    .flash("Good morning!")
    .wifi(True)
    .brightness(200)
    .media_volume(8)
    .variable_set("%MORNING", "done")
    .build()
)
print(xml)
print()

# ─── Example 2: Battery saver project ───
print("=== Example 2: Battery Saver Project ===")
entry = (
    quick_task("Save Power", task_id=1)
    .flash("Battery low! Saving power...")
    .wifi(False)
    .bluetooth(False)
    .brightness(30)
    .get_task()
)
exit_task = (
    quick_task("Restore Power", task_id=2)
    .flash("Battery OK! Restoring settings...")
    .wifi(True)
    .bluetooth(True)
    .brightness(150)
    .get_task()
)
xml = (
    quick_project("Battery Saver")
    .add_profile(
        name="Low Battery",
        entry_task=entry,
        exit_task=exit_task,
        state_context=StateContext(code=140, int_args={"arg0": 0, "arg1": 20}),
    )
    .build()
)
print(xml)
print()

# ─── Example 3: Auto-reply SMS ───
print("=== Example 3: Auto Reply SMS ===")
reply_task = (
    quick_task("Auto Reply", task_id=10)
    .send_sms("%SMSRF", "I'm busy right now, will get back to you soon.")
    .flash("Auto-replied to %SMSRN")
    .get_task()
)
xml = (
    quick_project("SMS Auto Reply")
    .add_profile(
        name="Reply When Busy",
        entry_task=reply_task,
        event_context=EventContext(code=7, args={"arg0": "*"}),
    )
    .build()
)
print(xml)
