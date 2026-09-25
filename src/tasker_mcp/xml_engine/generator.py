"""Tasker XML Generator - Produces valid Tasker-importable XML files.

Generates XML compatible with Tasker's import format using xml.etree.ElementTree.
Output files use extensions: .tsk.xml, .prf.xml, .prj.xml

Reference: https://github.com/Taskomater/Tasker-XML-Info
"""

import xml.etree.ElementTree as ET
from xml.dom import minidom

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


class TaskerXMLGenerator:
    """Generates valid Tasker XML from model objects."""

    def __init__(self, tasker_version: str = "6.3.13"):
        self.tasker_version = tasker_version

    def _prettify(self, element: ET.Element) -> str:
        """Return a pretty-printed XML string with proper declaration."""
        rough = ET.tostring(element, encoding="unicode", xml_declaration=False)
        dom = minidom.parseString(rough)
        pretty = dom.toprettyxml(indent="\t", encoding=None)
        # Remove the minidom XML declaration, we'll add our own
        lines = pretty.split("\n")
        if lines[0].startswith("<?xml"):
            lines = lines[1:]
        return "\n".join(lines).strip()

    def _make_root(self) -> ET.Element:
        """Create the TaskerData root element."""
        root = ET.Element("TaskerData")
        root.set("sr", "")
        root.set("dvi", "1")
        root.set("tv", self.tasker_version)
        return root

    def _build_action(self, parent: ET.Element, action: TaskerAction, index: int) -> None:
        """Build an Action XML node."""
        act_el = ET.SubElement(parent, "Action")
        act_el.set("sr", f"act{index}")
        act_el.set("ve", "7")

        code_el = ET.SubElement(act_el, "code")
        code_el.text = str(action.code)

        # Optional label
        if action.label:
            label_el = ET.SubElement(act_el, "label")
            label_el.text = action.label

        # String arguments
        for arg_key, arg_val in sorted(action.args.items()):
            str_el = ET.SubElement(act_el, "Str")
            str_el.set("sr", arg_key)
            str_el.set("ve", "3")
            str_el.text = str(arg_val)

        # Integer arguments
        for arg_key, arg_val in sorted(action.int_args.items()):
            int_el = ET.SubElement(act_el, "Int")
            int_el.set("sr", arg_key)
            int_el.set("val", str(arg_val))

        # Condition
        if action.condition_var:
            cond_el = ET.SubElement(act_el, "ConditionList")
            cond_el.set("sr", "if")
            condition = ET.SubElement(cond_el, "Condition")
            condition.set("sr", "c0")
            cv = ET.SubElement(condition, "lhs")
            cv.text = action.condition_var
            if action.condition_op:
                cop = ET.SubElement(condition, "op")
                cop.text = action.condition_op
            if action.condition_val:
                cval = ET.SubElement(condition, "rhs")
                cval.text = action.condition_val

    def _build_task(self, parent: ET.Element, task: TaskerTask) -> None:
        """Build a Task XML node."""
        task_el = ET.SubElement(parent, "Task")
        task_el.set("sr", f"task{task.id}")

        id_el = ET.SubElement(task_el, "id")
        id_el.text = str(task.id)

        if task.name:
            nme_el = ET.SubElement(task_el, "nme")
            nme_el.text = task.name

        if task.priority != 100:
            pri_el = ET.SubElement(task_el, "pri")
            pri_el.text = str(task.priority)

        if task.collision != 0:
            rty_el = ET.SubElement(task_el, "rty")
            rty_el.text = str(task.collision)

        if task.keep_awake:
            stay_el = ET.SubElement(task_el, "stayawake")
            stay_el.text = "true"

        for i, action in enumerate(task.actions):
            self._build_action(task_el, action, i)

    def _build_time_context(self, parent: ET.Element, ctx: TimeContext, index: int) -> None:
        """Build a Time context XML node."""
        time_el = ET.SubElement(parent, "Time")
        time_el.set("sr", f"con{index}")

        fh = ET.SubElement(time_el, "fh")
        fh.text = str(ctx.from_hour)
        fm = ET.SubElement(time_el, "fm")
        fm.text = str(ctx.from_minute)
        th = ET.SubElement(time_el, "th")
        th.text = str(ctx.to_hour)
        tm = ET.SubElement(time_el, "tm")
        tm.text = str(ctx.to_minute)

        if ctx.repeat:
            rep = ET.SubElement(time_el, "rep")
            rep.text = str(ctx.repeat_minutes) if ctx.repeat_minutes else "1"

    def _build_event_context(self, parent: ET.Element, ctx: EventContext, index: int) -> None:
        """Build an Event context XML node."""
        event_el = ET.SubElement(parent, "Event")
        event_el.set("sr", f"con{index}")
        event_el.set("ve", "2")

        code_el = ET.SubElement(event_el, "code")
        code_el.text = str(ctx.code)

        for arg_key, arg_val in sorted(ctx.args.items()):
            str_el = ET.SubElement(event_el, "Str")
            str_el.set("sr", arg_key)
            str_el.set("ve", "3")
            str_el.text = str(arg_val)

        for arg_key, arg_val in sorted(ctx.int_args.items()):
            int_el = ET.SubElement(event_el, "Int")
            int_el.set("sr", arg_key)
            int_el.set("val", str(arg_val))

    def _build_state_context(self, parent: ET.Element, ctx: StateContext, index: int) -> None:
        """Build a State context XML node."""
        state_el = ET.SubElement(parent, "State")
        state_el.set("sr", f"con{index}")
        state_el.set("ve", "2")

        code_el = ET.SubElement(state_el, "code")
        code_el.text = str(ctx.code)

        if ctx.invert:
            inv_el = ET.SubElement(state_el, "pin")
            inv_el.text = "true"

        for arg_key, arg_val in sorted(ctx.args.items()):
            str_el = ET.SubElement(state_el, "Str")
            str_el.set("sr", arg_key)
            str_el.set("ve", "3")
            str_el.text = str(arg_val)

        for arg_key, arg_val in sorted(ctx.int_args.items()):
            int_el = ET.SubElement(state_el, "Int")
            int_el.set("sr", arg_key)
            int_el.set("val", str(arg_val))

    def _build_app_context(self, parent: ET.Element, ctx: AppContext, index: int) -> None:
        """Build an App context XML node."""
        app_el = ET.SubElement(parent, "App")
        app_el.set("sr", f"con{index}")

        label_el = ET.SubElement(app_el, "label")
        label_el.text = ctx.label
        pkg_el = ET.SubElement(app_el, "pkg")
        pkg_el.text = ctx.package
        if ctx.activity:
            cls_el = ET.SubElement(app_el, "class")
            cls_el.text = ctx.activity

    def _build_profile(self, parent: ET.Element, profile: TaskerProfile) -> None:
        """Build a Profile XML node."""
        prof_el = ET.SubElement(parent, "Profile")
        prof_el.set("sr", f"prof{profile.id}")
        prof_el.set("ve", "2")

        id_el = ET.SubElement(prof_el, "id")
        id_el.text = str(profile.id)

        if profile.entry_task_id is not None:
            mid0 = ET.SubElement(prof_el, "mid0")
            mid0.text = str(profile.entry_task_id)

        if profile.exit_task_id is not None:
            mid1 = ET.SubElement(prof_el, "mid1")
            mid1.text = str(profile.exit_task_id)

        if profile.name:
            nme_el = ET.SubElement(prof_el, "nme")
            nme_el.text = profile.name

        # Build context nodes
        ctx_index = 0
        for time_ctx in profile.time_contexts:
            self._build_time_context(prof_el, time_ctx, ctx_index)
            ctx_index += 1
        for event_ctx in profile.event_contexts:
            self._build_event_context(prof_el, event_ctx, ctx_index)
            ctx_index += 1
        for state_ctx in profile.state_contexts:
            self._build_state_context(prof_el, state_ctx, ctx_index)
            ctx_index += 1
        for app_ctx in profile.app_contexts:
            self._build_app_context(prof_el, app_ctx, ctx_index)
            ctx_index += 1

    def generate_task(self, task: TaskerTask) -> str:
        """Generate a .tsk.xml file content for a single task.

        Returns valid XML string importable by Tasker.
        """
        root = self._make_root()
        self._build_task(root, task)
        return self._prettify(root)

    def generate_profile(
        self, profile: TaskerProfile, tasks: list[TaskerTask]
    ) -> str:
        """Generate a .prf.xml file content for a profile with its tasks.

        Returns valid XML string importable by Tasker.
        """
        root = self._make_root()
        self._build_profile(root, profile)
        for task in tasks:
            self._build_task(root, task)
        return self._prettify(root)

    def generate_project(self, project: TaskerProject) -> str:
        """Generate a .prj.xml file content for a complete project.

        Returns valid XML string importable by Tasker.
        """
        root = self._make_root()

        # Display metrics
        dmetric = ET.SubElement(root, "dmetric")
        dmetric.text = project.display_metrics

        # Profiles
        for profile in project.profiles:
            self._build_profile(root, profile)

        # Project node
        proj_el = ET.SubElement(root, "Project")
        proj_el.set("sr", "proj0")
        proj_el.set("ve", "2")

        name_el = ET.SubElement(proj_el, "name")
        name_el.text = project.name

        if project.profiles:
            pids_el = ET.SubElement(proj_el, "pids")
            pids_el.text = ",".join(str(p.id) for p in project.profiles)

        if project.tasks:
            tids_el = ET.SubElement(proj_el, "tids")
            tids_el.text = ",".join(str(t.id) for t in project.tasks if t.name)

        # Tasks
        for task in project.tasks:
            self._build_task(root, task)

        return self._prettify(root)
