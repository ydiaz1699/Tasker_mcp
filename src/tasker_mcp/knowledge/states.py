"""Complete Tasker Profile State codes knowledge base.

Source: Tasker v5.15.5-beta (5303) - 50 state codes.
Reference: https://github.com/Taskomater/Tasker-XML-Info
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TaskerState:
    """Represents a Tasker profile state context."""

    code: int
    name: str
    category: str
    description: str
    args: list[str] = field(default_factory=list)


# fmt: off
PROFILE_STATES: dict[int, TaskerState] = {
    # ─── Connectivity Category ───
    2: TaskerState(2, "BT Status", "Connectivity", "Bluetooth adapter is on or off", ["Status"]),
    3: TaskerState(3, "BT Connected", "Connectivity", "A Bluetooth device is connected", ["Name", "Address", "Type"]),
    4: TaskerState(4, "BT Near", "Connectivity", "A Bluetooth device is nearby", ["Name", "Address", "Standard", "Low-Energy", "Non-Paired", "Toggle BT"]),
    110: TaskerState(110, "Mobile Network", "Connectivity", "Device has mobile data connectivity", ["Type", "Active"]),
    136: TaskerState(136, "VPN Connected", "Connectivity", "A VPN network is connected", ["Active"]),
    160: TaskerState(160, "Wifi Connected", "Connectivity", "Connected to a Wifi Access Point", ["SSID", "MAC", "IP", "Active"]),
    161: TaskerState(161, "Ethernet Connect", "Connectivity", "Connected via ethernet interface", ["Active"]),
    170: TaskerState(170, "Wifi Near", "Connectivity", "Near a Wifi Access Point", ["SSID", "MAC", "Capabilities", "Min Signal Level", "Channel", "Toggle Wifi"]),
    195: TaskerState(195, "NFC Status", "Connectivity", "Whether NFC adapter is enabled or not", ["Status"]),

    # ─── Power Category ───
    10: TaskerState(10, "Power", "Power", "Device is connected to a power source", ["Source"]),
    12: TaskerState(12, "HDMI Plugged", "Power", "HDMI cable is plugged in", []),
    14: TaskerState(14, "Power Save Mode", "Power", "Power Save/Battery Saver mode is enabled", []),
    16: TaskerState(16, "Device Idle", "Power", "Device is in idle/doze mode", []),
    140: TaskerState(140, "Battery Level", "Power", "Battery level is within specified range", ["From", "To"]),
    141: TaskerState(141, "Battery Temperature", "Power", "Battery temperature in specified range (Celsius)", ["From", "To"]),
    150: TaskerState(150, "USB Connected", "Power", "A USB device is connected", ["Class"]),

    # ─── Hardware Category ───
    30: TaskerState(30, "Headset Plugged", "Hardware", "A headset is plugged in", ["Type"]),
    50: TaskerState(50, "Keyboard Out", "Hardware", "The physical keyboard is showing", []),
    80: TaskerState(80, "Docked", "Hardware", "A car or desk dock is connected", ["Type"]),
    120: TaskerState(120, "Orientation", "Hardware", "Device is in specified orientation", ["Orientation"]),
    122: TaskerState(122, "Display Orientation", "Hardware", "Screen is in portrait or landscape", ["Orientation"]),
    123: TaskerState(123, "Display State", "Hardware", "Whether display is on or off", ["State"]),
    125: TaskerState(125, "Proximity Sensor", "Hardware", "Object is nearby the proximity sensor", []),
    148: TaskerState(148, "Pen Out", "Hardware", "Hardware pen is not in its port (Samsung SPen)", []),
    149: TaskerState(149, "Pen Menu", "Hardware", "Pen menu is showing (Samsung SPen)", []),

    # ─── Phone Category ───
    40: TaskerState(40, "Call", "Phone", "A phone call is active", ["Type", "Number"]),
    7: TaskerState(7, "Cell Near", "Phone", "Device is near specified cell tower(s)", ["Cells", "Ignore Cells"]),
    107: TaskerState(107, "Missed Call", "Phone", "Call log has one or more missed calls", ["Caller"]),
    145: TaskerState(145, "Signal Strength", "Phone", "Signal level is within specified range", ["From", "To"]),
    147: TaskerState(147, "Unread Text", "Phone", "There is an unread SMS/MMS", ["Sender", "Content", "Type"]),

    # ─── Sensor Category ───
    103: TaskerState(103, "Light Level", "Sensor", "Ambient light level as percentage", ["From", "To"]),
    104: TaskerState(104, "Pressure", "Sensor", "Atmospheric pressure in millibars", ["From", "To"]),
    106: TaskerState(106, "Magnetic Field", "Sensor", "Magnetic field strength in micro-Tesla", ["From", "To"]),
    180: TaskerState(180, "Temperature", "Sensor", "Ambient temperature in Celsius", ["From", "To"]),
    182: TaskerState(182, "Heart Rate", "Sensor", "Heart rate in BPM within range", ["From", "To"]),
    185: TaskerState(185, "Humidity", "Sensor", "Relative ambient air humidity in percent", ["From", "To"]),
    190: TaskerState(190, "Any Sensor", "Sensor", "Any sensor value", ["Sensor", "Value"]),
    192: TaskerState(192, "Sleeping", "Sensor", "Device determines user is sleeping", []),

    # ─── App/System Category ───
    5: TaskerState(5, "Calendar Entry", "App", "A calendar entry is active", ["Calendar", "Title", "Location", "Description"]),
    100: TaskerState(100, "Airplane Mode", "App", "Airplane Mode is enabled", []),
    105: TaskerState(105, "Media Button", "App", "A media button is pressed", ["Button", "Held", "Stop Event", "Grab"]),
    135: TaskerState(135, "Auto-Sync", "App", "Auto-sync is enabled", []),
    142: TaskerState(142, "Profile Active", "App", "A Tasker profile is active", ["Name"]),
    143: TaskerState(143, "Task Running", "App", "A Tasker task is running", ["Name"]),
    154: TaskerState(154, "Active User", "App", "The specified user ID is active", ["ID"]),
    165: TaskerState(165, "Variable Value", "App", "A variable matches specified condition", ["Variable", "Operator", "Value"]),
    175: TaskerState(175, "Dreaming", "App", "Display is in Android Daydream mode", []),
    186: TaskerState(186, "Custom Setting", "App", "A custom system setting has a value", ["Type", "Name", "Operator", "Value"]),
    188: TaskerState(188, "Dark Mode", "App", "Dark mode is enabled or disabled", ["Mode"]),

    # ─── Plugin Category ───
    1000: TaskerState(1000, "Plugin", "Plugin", "Locale-compatible condition plugin state", ["Plugin", "Configuration"]),
}
# fmt: on


def get_state_by_code(code: int) -> Optional[TaskerState]:
    """Get a Tasker state by its numeric code."""
    return PROFILE_STATES.get(code)


def get_state_by_name(name: str) -> Optional[TaskerState]:
    """Get a Tasker state by its exact name (case-insensitive)."""
    name_lower = name.lower()
    for state in PROFILE_STATES.values():
        if state.name.lower() == name_lower:
            return state
    return None


def search_states(
    query: str, category: Optional[str] = None
) -> list[TaskerState]:
    """Search states by name/description, optionally filtered by category."""
    query_lower = query.lower()
    results = []
    for state in PROFILE_STATES.values():
        if category and state.category.lower() != category.lower():
            continue
        if (
            query_lower in state.name.lower()
            or query_lower in state.description.lower()
        ):
            results.append(state)
    return results
