"""Complete Tasker Profile Event codes knowledge base.

Source: Tasker v5.15.5-beta (5303) - 82 event codes.
Reference: https://github.com/Taskomater/Tasker-XML-Info
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TaskerEvent:
    """Represents a Tasker profile event trigger."""

    code: int
    name: str
    category: str
    description: str
    args: list[str] = field(default_factory=list)


# fmt: off
PROFILE_EVENTS: dict[int, TaskerEvent] = {
    # ─── Phone Category ───
    2: TaskerEvent(2, "Phone Offhook", "Phone", "Phone has gone off hook (call active/dialling/hold)", ["Number"]),
    4: TaskerEvent(4, "Phone Idle", "Phone", "Phone is not doing anything (call just finished)", []),
    6: TaskerEvent(6, "Phone Ringing", "Phone", "There is an incoming phone call", ["Caller", "Number"]),
    2003: TaskerEvent(2003, "Missed Call", "Phone", "A call has been missed", ["Caller", "Number"]),

    # ─── SMS/Communication Category ───
    7: TaskerEvent(7, "Received Text", "Communication", "A text message has been received", ["Sender", "Content", "Type"]),
    8: TaskerEvent(8, "Received Data SMS", "Communication", "A data SMS has been received", ["Port", "Sender", "Data"]),
    2005: TaskerEvent(2005, "SMS Success", "Communication", "SMS sent to specified number succeeded", ["Number"]),
    2010: TaskerEvent(2010, "SMS Failure", "Communication", "SMS sent to specified number failed", ["Number"]),

    # ─── Hardware/Device Category ───
    134: TaskerEvent(134, "Card Mounted", "Hardware", "An inserted card has been registered and is ready", ["Title", "Frequency"]),
    135: TaskerEvent(135, "Card Unmounted", "Hardware", "A card has been unregistered for removal", ["Title"]),
    136: TaskerEvent(136, "Card Removed", "Hardware", "A card has been physically removed", []),
    208: TaskerEvent(208, "Display On", "Hardware", "The display has just come on", []),
    210: TaskerEvent(210, "Display Off", "Hardware", "The display has just turned off", []),
    215: TaskerEvent(215, "Button: Camera", "Hardware", "Camera hardware button pressed and held", []),
    216: TaskerEvent(216, "Button: Long Search", "Hardware", "Search button has been long-pressed", []),
    411: TaskerEvent(411, "Device Boot", "Hardware", "Phone has just finished turning on", []),
    413: TaskerEvent(413, "Device Shutdown", "Hardware", "Phone is about to shutdown", []),
    422: TaskerEvent(422, "Device Storage Low", "Hardware", "Device storage is low", []),
    1000: TaskerEvent(1000, "Display Unlocked", "Hardware", "Display has just been unlocked", []),
    2079: TaskerEvent(2079, "Volume Long Press", "Hardware", "Volume button long-pressed", ["Direction"]),

    # ─── Battery Category ───
    203: TaskerEvent(203, "Battery Changed", "Battery", "The battery level has changed", ["From", "To"]),
    205: TaskerEvent(205, "Battery Full", "Battery", "Battery is fully charged", []),
    206: TaskerEvent(206, "Battery Overheating", "Battery", "Battery is overheating", []),

    # ─── File Category ───
    220: TaskerEvent(220, "File Moved", "File", "A file has been moved", ["File"]),
    222: TaskerEvent(222, "File Modified", "File", "A file has been modified", ["File"]),
    224: TaskerEvent(224, "File Closed", "File", "A file has been closed", ["File"]),
    226: TaskerEvent(226, "File Opened", "File", "A file has been opened", ["File"]),
    228: TaskerEvent(228, "File Deleted", "File", "A file has been deleted", ["File"]),
    230: TaskerEvent(230, "File Attribute Change", "File", "A file attribute has changed", ["File"]),

    # ─── Date/Time Category ───
    300: TaskerEvent(300, "Date Set", "Date/Time", "The date has been changed", []),
    302: TaskerEvent(302, "Time/Date Set", "Date/Time", "The time or date has been changed", []),
    303: TaskerEvent(303, "Timer Change", "Date/Time", "A Task Timer widget status has changed", ["Task"]),
    304: TaskerEvent(304, "Timezone Set", "Date/Time", "The timezone has been changed", []),
    305: TaskerEvent(305, "Alarm Clock", "Date/Time", "An alarm clock is about to go off", ["Label"]),
    306: TaskerEvent(306, "Alarm Done", "Date/Time", "An alarm has been dismissed or snoozed", ["Label"]),
    2084: TaskerEvent(2084, "Alarm Changed", "Date/Time", "An alarm has been changed", []),

    # ─── Sensor/Gesture Category ───
    307: TaskerEvent(307, "Monitor Start", "System", "Tasker Monitor Service has just started", []),
    309: TaskerEvent(309, "Steps Taken", "Sensor", "Specified number of steps taken", ["Steps"]),
    2083: TaskerEvent(2083, "Significant Motion", "Sensor", "Significant motion detected", []),
    2088: TaskerEvent(2088, "Any Sensor", "Sensor", "Any sensor event", ["Sensor", "Value"]),
    3000: TaskerEvent(3000, "Gesture", "Sensor", "Phone waved in a particular way", ["Name"]),
    3001: TaskerEvent(3001, "Shake", "Sensor", "Device is being physically shaken", ["Axis", "Sensitivity", "Duration"]),
    2096: TaskerEvent(2096, "Sleeping", "Sensor", "Device determines user is sleeping", []),

    # ─── App/Package Category ───
    450: TaskerEvent(450, "New Package", "App", "A new package has been added", ["Name", "Package"]),
    451: TaskerEvent(451, "Package Removed", "App", "A package has been removed", ["Package"]),
    453: TaskerEvent(453, "Package Updated", "App", "A package has been updated", ["Name", "Package"]),
    460: TaskerEvent(460, "Wallpaper Changed", "App", "System wallpaper was changed", []),
    463: TaskerEvent(463, "New Window", "App", "A new window has appeared", ["Label", "App"]),
    2077: TaskerEvent(2077, "Secondary App Opened", "App", "A secondary app was opened", ["App"]),
    2078: TaskerEvent(2078, "App Changed", "App", "Active app has changed", ["App"]),

    # ─── Notification Category ───
    461: TaskerEvent(461, "Notification", "Notification", "A notification has been sent to status bar", ["Owner App", "Title", "Text", "Other Text", "New Only"]),
    462: TaskerEvent(462, "Button Widget Clicked", "Notification", "A button widget has been clicked", ["Label", "Click Length", "New Button State"]),
    464: TaskerEvent(464, "Notification Removed", "Notification", "A notification has been removed", ["Owner App", "Title", "Text"]),
    2000: TaskerEvent(2000, "Notification Click", "Notification", "A notification has been clicked", ["Owner App", "Title"]),
    2050: TaskerEvent(2050, "Quick Setting Clicked", "Notification", "Custom Quick Setting tile clicked", ["Label"]),

    # ─── Intent/System Category ───
    599: TaskerEvent(599, "Intent Received", "System", "A broadcast intent has been received", ["Action", "Cat", "Data", "Mime Type", "Extra", "Package", "Class", "Priority"]),
    201: TaskerEvent(201, "Assistance Request", "System", "User requested assistance in an app", ["App"]),
    429: TaskerEvent(429, "Locale Changed", "System", "System locale has changed", []),
    2075: TaskerEvent(2075, "Custom Setting", "System", "A custom system setting changed", ["Type", "Name", "Value"]),
    2085: TaskerEvent(2085, "Logcat Entry", "System", "A logcat entry matched", ["Component", "Filter", "Level"]),
    2091: TaskerEvent(2091, "Command", "System", "A command was received from another app", ["Command", "Caller", "Regex"]),
    2092: TaskerEvent(2092, "Power Menu Shown", "System", "Power menu was shown", []),
    2093: TaskerEvent(2093, "Assistant Action", "System", "Assistant action triggered", []),
    2094: TaskerEvent(2094, "Call Screened", "System", "A call was screened", ["Number"]),
    2095: TaskerEvent(2095, "Tick", "System", "Periodic tick event", ["Interval"]),

    # ─── Bluetooth/Connectivity Category ───
    2076: TaskerEvent(2076, "NFC Tag", "Connectivity", "An NFC tag was detected", ["ID", "Content"]),
    2080: TaskerEvent(2080, "BT Connection", "Connectivity", "Bluetooth connection event", ["Name", "Address", "Type"]),
    2081: TaskerEvent(2081, "Music Track Changed", "Connectivity", "Music track has changed", ["Title", "Artist", "Album", "App"]),

    # ─── Variable Category ───
    3050: TaskerEvent(3050, "Variable Set", "Variable", "A user variable has had its value set", ["Variable", "Value", "Operator"]),
    3060: TaskerEvent(3060, "Variable Cleared", "Variable", "A user variable has been cleared", ["Variable"]),
    3071: TaskerEvent(3071, "Zoom Click", "Variable", "A Zoom element has been clicked", ["Widget", "Name"]),

    # ─── Third Party Category ───
    424: TaskerEvent(424, "Screebl / TSC", "Third Party", "Screebl orientation event", []),
    425: TaskerEvent(425, "K9 Email Received", "Third Party", "K9 email received", ["Subject", "From"]),
    426: TaskerEvent(426, "Widget Locker", "Third Party", "WidgetLocker event", []),
    427: TaskerEvent(427, "OpenWatch", "Third Party", "OpenWatch event", []),
    428: TaskerEvent(428, "Kaloer Clock", "Third Party", "Kaloer Clock event", []),
    444: TaskerEvent(444, "Pomodroido", "Third Party", "Pomodroido event", []),
    445: TaskerEvent(445, "Radardroid", "Third Party", "Radardroid event", []),
    446: TaskerEvent(446, "Gentle Alarm", "Third Party", "Gentle Alarm event", []),
    447: TaskerEvent(447, "Reddit Notify", "Third Party", "Reddit notification", ["Number", "Message"]),
    448: TaskerEvent(448, "Notify My Android", "Third Party", "Notify My Android event", []),

    # ─── Plugin Category ───
    # Note: Plugin event shares XML code 1000 with Display Unlocked.
    # Tasker differentiates them internally. We use 10001 as internal key.
    10001: TaskerEvent(1000, "Plugin", "Plugin", "Locale-compatible event plugin trigger", ["Plugin", "Configuration"]),
}
# fmt: on


def get_event_by_code(code: int) -> Optional[TaskerEvent]:
    """Get a Tasker event by its numeric code."""
    return PROFILE_EVENTS.get(code)


def get_event_by_name(name: str) -> Optional[TaskerEvent]:
    """Get a Tasker event by its exact name (case-insensitive)."""
    name_lower = name.lower()
    for event in PROFILE_EVENTS.values():
        if event.name.lower() == name_lower:
            return event
    return None


def search_events(
    query: str, category: Optional[str] = None
) -> list[TaskerEvent]:
    """Search events by name/description, optionally filtered by category."""
    query_lower = query.lower()
    results = []
    for event in PROFILE_EVENTS.values():
        if category and event.category.lower() != category.lower():
            continue
        if (
            query_lower in event.name.lower()
            or query_lower in event.description.lower()
        ):
            results.append(event)
    return results
