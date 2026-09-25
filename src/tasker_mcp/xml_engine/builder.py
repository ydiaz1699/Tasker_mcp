"""Fluent Builder API for Tasker XML generation.

Provides an intuitive chainable interface for building Tasker tasks and projects.

Usage:
    xml = quick_task("My Task").flash("Hello!").wifi(True).variable_set("%x", "5").build()
    xml = quick_project("My Project").add_task(task).build()
"""

from typing import Optional

from tasker_mcp.xml_engine.generator import TaskerXMLGenerator
from tasker_mcp.xml_engine.models import (
    AppContext,
    EventContext,
    StateContext,
    TaskerAction,
    TaskerProfile,
    TaskerProject,
    TaskerTask,
    TimeContext,
)


class TaskBuilder:
    """Fluent builder for constructing Tasker tasks with chained actions."""

    def __init__(self, name: str, task_id: int = 1):
        self._task = TaskerTask(id=task_id, name=name)
        self._generator = TaskerXMLGenerator()

    def _add_action(
        self,
        code: int,
        args: Optional[dict[str, str]] = None,
        int_args: Optional[dict[str, int]] = None,
        label: Optional[str] = None,
    ) -> "TaskBuilder":
        """Add an action to the task."""
        self._task.actions.append(
            TaskerAction(
                code=code,
                args=args or {},
                int_args=int_args or {},
                label=label,
            )
        )
        return self

    # ─── Alert Actions ───

    def flash(self, text: str, long: bool = False) -> "TaskBuilder":
        """Flash a message (code 548)."""
        int_args = {"arg1": 1} if long else {}
        return self._add_action(548, args={"arg0": text}, int_args=int_args)

    def vibrate(self, ms: int = 500) -> "TaskBuilder":
        """Vibrate for specified milliseconds (code 61)."""
        return self._add_action(61, int_args={"arg0": ms})

    def beep(self, frequency: int = 5000, duration: int = 500) -> "TaskBuilder":
        """Beep with frequency and duration (code 171)."""
        return self._add_action(171, int_args={"arg0": frequency, "arg1": duration})

    def notify(self, title: str, text: str, permanent: bool = False) -> "TaskBuilder":
        """Show a notification (code 523)."""
        int_args = {"arg2": 1} if permanent else {}
        return self._add_action(523, args={"arg0": title, "arg1": text}, int_args=int_args)

    def notify_cancel(self, title: str) -> "TaskBuilder":
        """Cancel a notification (code 779)."""
        return self._add_action(779, args={"arg0": title})

    def say(self, text: str, engine: str = "default:default") -> "TaskBuilder":
        """Text-to-speech (code 559)."""
        return self._add_action(559, args={"arg0": text, "arg1": engine})

    def popup(self, title: str, text: str, timeout: int = 5) -> "TaskBuilder":
        """Show a popup (code 550)."""
        return self._add_action(550, args={"arg0": title, "arg1": text}, int_args={"arg2": timeout})

    # ─── Variable Actions ───

    def variable_set(self, name: str, value: str, do_maths: bool = False, append: bool = False) -> "TaskBuilder":
        """Set a variable (code 547)."""
        int_args: dict[str, int] = {}
        if do_maths:
            int_args["arg2"] = 1
        if append:
            int_args["arg3"] = 1
        return self._add_action(547, args={"arg0": name, "arg1": value}, int_args=int_args)

    def variable_clear(self, name: str) -> "TaskBuilder":
        """Clear a variable (code 549)."""
        return self._add_action(549, args={"arg0": name})

    def variable_add(self, name: str, value: int = 1, wrap: int = 0) -> "TaskBuilder":
        """Increment a variable (code 888)."""
        return self._add_action(888, args={"arg0": name}, int_args={"arg1": value, "arg2": wrap})

    def variable_split(self, name: str, splitter: str = ",") -> "TaskBuilder":
        """Split a variable into array (code 590)."""
        return self._add_action(590, args={"arg0": name, "arg1": splitter})

    # ─── Network Actions ───

    def wifi(self, enable: bool) -> "TaskBuilder":
        """Enable/disable WiFi (code 425)."""
        return self._add_action(425, int_args={"arg0": 1 if enable else 0})

    def bluetooth(self, enable: bool) -> "TaskBuilder":
        """Enable/disable Bluetooth (code 294)."""
        return self._add_action(294, int_args={"arg0": 1 if enable else 0})

    def mobile_data(self, enable: bool) -> "TaskBuilder":
        """Enable/disable Mobile Data (code 433)."""
        return self._add_action(433, int_args={"arg0": 1 if enable else 0})

    def airplane_mode(self, enable: bool) -> "TaskBuilder":
        """Enable/disable Airplane Mode (code 333)."""
        return self._add_action(333, int_args={"arg0": 1 if enable else 0})

    def http_request(self, method: str, url: str, headers: str = "", body: str = "", timeout: int = 30) -> "TaskBuilder":
        """Make an HTTP request (code 339)."""
        return self._add_action(
            339,
            args={"arg0": method, "arg1": url, "arg2": headers, "arg3": body},
            int_args={"arg4": timeout},
        )

    # ─── Audio Actions ───

    def ringer_volume(self, level: int) -> "TaskBuilder":
        """Set ringer volume (code 304)."""
        return self._add_action(304, int_args={"arg0": level})

    def media_volume(self, level: int) -> "TaskBuilder":
        """Set media volume (code 307)."""
        return self._add_action(307, int_args={"arg0": level})

    def notification_volume(self, level: int) -> "TaskBuilder":
        """Set notification volume (code 305)."""
        return self._add_action(305, int_args={"arg0": level})

    def vibrate_mode(self, mode: str = "vibrate") -> "TaskBuilder":
        """Set vibrate/silent mode (code 310). Modes: vibrate, silent, normal."""
        mode_map = {"vibrate": 1, "silent": 2, "normal": 0}
        return self._add_action(310, int_args={"arg0": mode_map.get(mode, 1)})

    def do_not_disturb(self, mode: str = "all") -> "TaskBuilder":
        """Set DND mode (code 312). Modes: all, priority, alarms, none."""
        mode_map = {"none": 0, "all": 1, "priority": 2, "alarms": 3}
        return self._add_action(312, int_args={"arg0": mode_map.get(mode, 1)})

    # ─── Display Actions ───

    def brightness(self, level: int) -> "TaskBuilder":
        """Set display brightness 0-255 (code 810)."""
        return self._add_action(810, int_args={"arg0": level})

    def display_timeout(self, seconds: int) -> "TaskBuilder":
        """Set display timeout in seconds (code 812)."""
        return self._add_action(812, int_args={"arg0": seconds})

    def auto_rotate(self, enable: bool) -> "TaskBuilder":
        """Enable/disable auto-rotate (code 822)."""
        return self._add_action(822, int_args={"arg0": 1 if enable else 0})

    def torch(self, enable: bool = True) -> "TaskBuilder":
        """Toggle torch/flashlight (code 511)."""
        return self._add_action(511, int_args={"arg0": 1 if enable else 0})

    def dark_mode(self, enable: bool) -> "TaskBuilder":
        """Enable/disable dark mode (code 361)."""
        return self._add_action(361, int_args={"arg0": 1 if enable else 0})

    # ─── App Actions ───

    def launch_app(self, package: str, data: str = "") -> "TaskBuilder":
        """Launch an application (code 20)."""
        args = {"arg0": package}
        if data:
            args["arg1"] = data
        return self._add_action(20, args=args)

    def kill_app(self, package: str) -> "TaskBuilder":
        """Kill an application (code 18)."""
        return self._add_action(18, args={"arg0": package})

    def go_home(self) -> "TaskBuilder":
        """Go to home screen (code 25)."""
        return self._add_action(25)

    def browse_url(self, url: str) -> "TaskBuilder":
        """Open URL in browser (code 104)."""
        return self._add_action(104, args={"arg0": url})

    # ─── Communication Actions ───

    def send_sms(self, number: str, message: str) -> "TaskBuilder":
        """Send an SMS (code 41)."""
        return self._add_action(41, args={"arg0": number, "arg1": message})

    def call(self, number: str) -> "TaskBuilder":
        """Open dialer with number (code 90)."""
        return self._add_action(90, args={"arg0": number})

    # ─── Flow Control Actions ───

    def wait(self, seconds: int = 0, minutes: int = 0, hours: int = 0) -> "TaskBuilder":
        """Wait for a duration (code 30)."""
        return self._add_action(30, int_args={"arg0": hours, "arg1": minutes, "arg2": seconds})

    def if_condition(self, variable: str, op: str, value: str) -> "TaskBuilder":
        """Start an If block (code 37)."""
        action = TaskerAction(
            code=37,
            condition_var=variable,
            condition_op=op,
            condition_val=value,
        )
        self._task.actions.append(action)
        return self

    def else_action(self) -> "TaskBuilder":
        """Else in If block (code 43)."""
        return self._add_action(43)

    def end_if(self) -> "TaskBuilder":
        """End If block (code 38)."""
        return self._add_action(38)

    def for_each(self, variable: str, items: str) -> "TaskBuilder":
        """Start a For loop (code 39)."""
        return self._add_action(39, args={"arg0": variable, "arg1": items})

    def end_for(self) -> "TaskBuilder":
        """End For loop (code 40)."""
        return self._add_action(40)

    def stop(self) -> "TaskBuilder":
        """Stop the task (code 137)."""
        return self._add_action(137)

    def perform_task(self, task_name: str, priority: int = 0, par1: str = "", par2: str = "") -> "TaskBuilder":
        """Perform another task (code 130)."""
        args: dict[str, str] = {"arg0": task_name}
        if par1:
            args["arg1"] = par1
        if par2:
            args["arg2"] = par2
        int_args = {"arg3": priority} if priority else {}
        return self._add_action(130, args=args, int_args=int_args)

    # ─── Code Actions ───

    def run_shell(self, command: str, use_root: bool = False, store_output: str = "") -> "TaskBuilder":
        """Run a shell command (code 123)."""
        args: dict[str, str] = {"arg0": command}
        if store_output:
            args["arg1"] = store_output
        int_args: dict[str, int] = {}
        if use_root:
            int_args["arg2"] = 1
        return self._add_action(123, args=args, int_args=int_args)

    def javascript(self, code: str) -> "TaskBuilder":
        """Run JavaScriptlet (code 129)."""
        return self._add_action(129, args={"arg0": code})

    def send_intent(self, action: str, package: str = "", extra: str = "") -> "TaskBuilder":
        """Send an Intent broadcast (code 877)."""
        args: dict[str, str] = {"arg0": action}
        if package:
            args["arg5"] = package
        if extra:
            args["arg4"] = extra
        return self._add_action(877, args=args)

    # ─── File Actions ───

    def write_file(self, path: str, text: str, append: bool = False) -> "TaskBuilder":
        """Write to a file (code 410)."""
        int_args = {"arg2": 1} if append else {}
        return self._add_action(410, args={"arg0": path, "arg1": text}, int_args=int_args)

    def read_file(self, path: str, variable: str) -> "TaskBuilder":
        """Read a file into a variable (code 417)."""
        return self._add_action(417, args={"arg0": path, "arg1": variable})

    # ─── System Actions ───

    def set_clipboard(self, text: str) -> "TaskBuilder":
        """Set clipboard contents (code 105)."""
        return self._add_action(105, args={"arg0": text})

    def set_alarm(self, hours: int, minutes: int, message: str = "") -> "TaskBuilder":
        """Set an alarm (code 566)."""
        args: dict[str, str] = {}
        if message:
            args["arg2"] = message
        return self._add_action(566, args=args, int_args={"arg0": hours, "arg1": minutes})

    def location_get(self, source: str = "GPS", timeout: int = 60) -> "TaskBuilder":
        """Get location fix (code 902)."""
        return self._add_action(902, args={"arg0": source}, int_args={"arg1": timeout})

    # ─── Generic Action ───

    def action(self, code: int, args: Optional[dict[str, str]] = None, int_args: Optional[dict[str, int]] = None, label: Optional[str] = None) -> "TaskBuilder":
        """Add any action by code with custom arguments."""
        return self._add_action(code, args=args, int_args=int_args, label=label)

    # ─── Build Methods ───

    def get_task(self) -> TaskerTask:
        """Return the built TaskerTask model."""
        return self._task

    def build(self) -> str:
        """Generate the final .tsk.xml string."""
        return self._generator.generate_task(self._task)

    def build_to_file(self, filepath: str) -> str:
        """Generate XML and write to a .tsk.xml file."""
        xml_content = self.build()
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(xml_content)
        return xml_content


class ProjectBuilder:
    """Fluent builder for constructing Tasker projects."""

    def __init__(self, name: str):
        self._project = TaskerProject(name=name)
        self._generator = TaskerXMLGenerator()
        self._next_task_id = 1
        self._next_profile_id = 1

    def add_task(self, task: TaskerTask) -> "ProjectBuilder":
        """Add a pre-built task to the project."""
        self._project.tasks.append(task)
        return self

    def add_task_builder(self, builder: TaskBuilder) -> "ProjectBuilder":
        """Add a task from a TaskBuilder."""
        self._project.tasks.append(builder.get_task())
        return self

    def add_profile(
        self,
        name: str,
        entry_task: TaskerTask,
        exit_task: Optional[TaskerTask] = None,
        time_context: Optional[TimeContext] = None,
        event_context: Optional[EventContext] = None,
        state_context: Optional[StateContext] = None,
        app_context: Optional[AppContext] = None,
    ) -> "ProjectBuilder":
        """Add a profile with its contexts and linked tasks."""
        profile = TaskerProfile(
            id=self._next_profile_id,
            name=name,
            entry_task_id=entry_task.id,
            exit_task_id=exit_task.id if exit_task else None,
        )

        if time_context:
            profile.time_contexts.append(time_context)
        if event_context:
            profile.event_contexts.append(event_context)
        if state_context:
            profile.state_contexts.append(state_context)
        if app_context:
            profile.app_contexts.append(app_context)

        self._project.profiles.append(profile)
        self._next_profile_id += 1

        # Add tasks to project if not already there
        if entry_task not in self._project.tasks:
            self._project.tasks.append(entry_task)
        if exit_task and exit_task not in self._project.tasks:
            self._project.tasks.append(exit_task)

        return self

    def get_project(self) -> TaskerProject:
        """Return the built TaskerProject model."""
        return self._project

    def build(self) -> str:
        """Generate the final .prj.xml string."""
        return self._generator.generate_project(self._project)

    def build_to_file(self, filepath: str) -> str:
        """Generate XML and write to a .prj.xml file."""
        xml_content = self.build()
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(xml_content)
        return xml_content


def quick_task(name: str, task_id: int = 1) -> TaskBuilder:
    """Create a new TaskBuilder with the given name.

    Usage:
        xml = quick_task("My Task").flash("Hello!").wifi(True).build()
    """
    return TaskBuilder(name=name, task_id=task_id)


def quick_project(name: str) -> ProjectBuilder:
    """Create a new ProjectBuilder with the given name.

    Usage:
        proj = quick_project("My Project").add_task(task).build()
    """
    return ProjectBuilder(name=name)
