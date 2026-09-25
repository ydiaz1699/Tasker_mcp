"""Pydantic models for Tasker XML structure.

These models represent the structure of Tasker XML files as documented at:
https://github.com/Taskomater/Tasker-XML-Info

Tasker XML export types:
- .tsk.xml  — Single task
- .prf.xml  — Profile with tasks
- .prj.xml  — Project with profiles, tasks, scenes
- .xml      — Full data backup
"""

from typing import Optional

from pydantic import BaseModel, Field


class TaskerAction(BaseModel):
    """A single action within a Tasker task.

    XML structure:
    <Action sr="actN" ve="7">
        <code>CODE</code>
        <Str sr="arg0" ve="3">value</Str>
        <Str sr="arg1" ve="3">value</Str>
        <Int sr="arg0" val="N"/>
        ...
    </Action>
    """

    code: int = Field(..., description="Action code from Tasker action codes")
    label: Optional[str] = Field(None, description="Optional label for the action")
    args: dict[str, str] = Field(
        default_factory=dict,
        description="Action arguments as key-value pairs (argN -> value)",
    )
    int_args: dict[str, int] = Field(
        default_factory=dict,
        description="Integer arguments (argN -> value)",
    )

    # Conditional execution
    condition_var: Optional[str] = Field(None, description="If condition variable")
    condition_op: Optional[str] = Field(None, description="If condition operator")
    condition_val: Optional[str] = Field(None, description="If condition value")


class TaskerTask(BaseModel):
    """A Tasker task containing one or more actions.

    XML structure:
    <Task sr="taskN">
        <id>N</id>
        <nme>Task Name</nme>
        <pri>100</pri>
        <Action sr="act0" ve="7">...</Action>
        <Action sr="act1" ve="7">...</Action>
    </Task>
    """

    id: int = Field(..., description="Unique task ID")
    name: Optional[str] = Field(None, description="Task name (nme tag)")
    priority: int = Field(100, description="Task priority")
    collision: int = Field(
        0, description="Collision handling: 0=Abort New, 1=Abort Existing, 2=Run Both"
    )
    keep_awake: bool = Field(False, description="Keep device awake during task")
    actions: list[TaskerAction] = Field(
        default_factory=list, description="List of actions in the task"
    )


class TimeContext(BaseModel):
    """Time context for a profile trigger.

    Triggers the profile during a time range.
    """

    from_hour: int = Field(0, ge=0, le=23)
    from_minute: int = Field(0, ge=0, le=59)
    to_hour: int = Field(23, ge=0, le=23)
    to_minute: int = Field(59, ge=0, le=59)
    repeat: bool = Field(False, description="Repeat during the time range")
    repeat_minutes: int = Field(0, description="Minutes between repeats")


class EventContext(BaseModel):
    """Event context for a profile trigger.

    XML structure:
    <Event sr="conN" ve="2">
        <code>CODE</code>
        <Str sr="arg0" ve="3">value</Str>
        ...
    </Event>
    """

    code: int = Field(..., description="Event code from Tasker event codes")
    args: dict[str, str] = Field(
        default_factory=dict, description="Event arguments"
    )
    int_args: dict[str, int] = Field(
        default_factory=dict, description="Integer event arguments"
    )


class StateContext(BaseModel):
    """State context for a profile trigger.

    XML structure:
    <State sr="conN" ve="2">
        <code>CODE</code>
        <Str sr="arg0" ve="3">value</Str>
        ...
    </State>
    """

    code: int = Field(..., description="State code from Tasker state codes")
    args: dict[str, str] = Field(
        default_factory=dict, description="State arguments"
    )
    int_args: dict[str, int] = Field(
        default_factory=dict, description="Integer state arguments"
    )
    invert: bool = Field(False, description="Invert the state (NOT condition)")


class AppContext(BaseModel):
    """Application context for a profile trigger.

    Triggers when the specified app is in the foreground.

    XML structure:
    <App sr="conN">
        <label>App Label</label>
        <pkg>com.package.name</pkg>
        <class>com.package.name.Activity</class>
    </App>
    """

    label: str = Field(..., description="Application label/name")
    package: str = Field(..., description="Application package name")
    activity: Optional[str] = Field(None, description="Specific activity class")


class TaskerProfile(BaseModel):
    """A Tasker profile with contexts and linked tasks.

    XML structure:
    <Profile sr="profN" ve="2">
        <id>N</id>
        <nme>Profile Name</nme>
        <mid0>entry_task_id</mid0>
        <mid1>exit_task_id</mid1>
        <Time sr="con0">...</Time>
        <Event sr="con0" ve="2">...</Event>
        <State sr="con0" ve="2">...</State>
        <App sr="con0">...</App>
    </Profile>
    """

    id: int = Field(..., description="Unique profile ID")
    name: Optional[str] = Field(None, description="Profile name")
    entry_task_id: Optional[int] = Field(None, description="Entry task ID (mid0)")
    exit_task_id: Optional[int] = Field(None, description="Exit task ID (mid1)")
    enabled: bool = Field(True, description="Whether profile is enabled")

    # Context triggers (at least one required)
    time_contexts: list[TimeContext] = Field(default_factory=list)
    event_contexts: list[EventContext] = Field(default_factory=list)
    state_contexts: list[StateContext] = Field(default_factory=list)
    app_contexts: list[AppContext] = Field(default_factory=list)


class TaskerProject(BaseModel):
    """A complete Tasker project containing profiles and tasks.

    XML structure:
    <TaskerData sr="" dvi="1" tv="6.3.13">
        <dmetric>1080.0,1920.0</dmetric>
        <Profile>...</Profile>
        <Project sr="proj0" ve="2">
            <name>Project Name</name>
            <pids>1,2</pids>
            <tids>1,2,3</tids>
        </Project>
        <Task>...</Task>
    </TaskerData>
    """

    name: str = Field(..., description="Project name")
    profiles: list[TaskerProfile] = Field(default_factory=list)
    tasks: list[TaskerTask] = Field(default_factory=list)
    display_metrics: str = Field(
        "1080.0,1920.0", description="Display metrics (width,height)"
    )
    tasker_version: str = Field("6.3.13", description="Tasker version for XML tv attribute")
