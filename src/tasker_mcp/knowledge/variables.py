"""Complete Tasker Built-in Variables knowledge base.

Reference: https://tasker.joaoapps.com/userguide/en/variables.html
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class TaskerVariable:
    """Represents a Tasker built-in variable."""

    name: str
    description: str
    category: str
    dynamic: bool = False
    monitored: bool = False


# fmt: off
BUILTIN_VARIABLES: dict[str, TaskerVariable] = {
    # ─── Battery ───
    "%BATT": TaskerVariable("%BATT", "Current device battery level from 0-100", "Battery", dynamic=True),
    "%BATTERY_PERCENT": TaskerVariable("%BATTERY_PERCENT", "Same as %BATT, battery percentage", "Battery", dynamic=True),
    "%UPS": TaskerVariable("%UPS", "Current device uptime in seconds", "Battery"),

    # ─── Bluetooth ───
    "%BLUE": TaskerVariable("%BLUE", "Bluetooth status: on or off", "Bluetooth", dynamic=True),
    "%BTSTATUS": TaskerVariable("%BTSTATUS", "Bluetooth status: on/off/connected", "Bluetooth", dynamic=True),

    # ─── Calendar ───
    "%CALTITLE": TaskerVariable("%CALTITLE", "Title of the current calendar event (or shortest if multiple)", "Calendar"),
    "%CALDESCR": TaskerVariable("%CALDESCR", "Description of the current calendar event", "Calendar"),
    "%CALLOC": TaskerVariable("%CALLOC", "Location of the current calendar event", "Calendar"),

    # ─── Call ───
    "%CALS": TaskerVariable("%CALS", "Call status: incoming/outgoing/ongoing", "Call"),
    "%CALL": TaskerVariable("%CALL", "Whether currently in a call: true/false", "Call", dynamic=True),
    "%CNAME": TaskerVariable("%CNAME", "Name of current/last caller", "Call"),
    "%CNUM": TaskerVariable("%CNUM", "Number of current/last caller", "Call"),
    "%CDATE": TaskerVariable("%CDATE", "Date of current incoming call", "Call", dynamic=True, monitored=True),
    "%CTIME": TaskerVariable("%CTIME", "Time of current incoming call", "Call", dynamic=True, monitored=True),
    "%CONAME": TaskerVariable("%CONAME", "Caller name of current outgoing call", "Call", dynamic=True, monitored=True),
    "%CONUM": TaskerVariable("%CONUM", "Caller number of current outgoing call", "Call", dynamic=True, monitored=True),
    "%CODATE": TaskerVariable("%CODATE", "Date of last outgoing call", "Call"),
    "%COTIME": TaskerVariable("%COTIME", "Time of last outgoing call", "Call"),
    "%CODUR": TaskerVariable("%CODUR", "Duration in seconds of last outgoing call", "Call"),
    "%CINUM": TaskerVariable("%CINUM", "Number of last incoming call", "Call"),
    "%CINAME": TaskerVariable("%CINAME", "Name of last incoming caller", "Call"),
    "%CIDATE": TaskerVariable("%CIDATE", "Date of last incoming call", "Call"),
    "%CITIME": TaskerVariable("%CITIME", "Time of last incoming call", "Call"),
    "%CIDUR": TaskerVariable("%CIDUR", "Duration in seconds of last incoming call", "Call"),
    "%SPHONE": TaskerVariable("%SPHONE", "Whether speakerphone is currently on or off", "Call", dynamic=True),

    # ─── Date/Time ───
    "%TIME": TaskerVariable("%TIME", "Current time in HH.MM format", "Date/Time", dynamic=True),
    "%TIMES": TaskerVariable("%TIMES", "Current time in seconds since epoch", "Date/Time"),
    "%TIMEMS": TaskerVariable("%TIMEMS", "Current time in milliseconds since epoch", "Date/Time"),
    "%DATE": TaskerVariable("%DATE", "Current date in user-preferred format", "Date/Time", dynamic=True),
    "%DATEFMT": TaskerVariable("%DATEFMT", "Current date in specified format", "Date/Time"),
    "%DATEF": TaskerVariable("%DATEF", "Current date in DD-MM-YYYY format", "Date/Time"),
    "%DAY": TaskerVariable("%DAY", "Current day of month (1-31)", "Date/Time"),
    "%DAYM": TaskerVariable("%DAYM", "Current day of the month (1-31)", "Date/Time"),
    "%DAYW": TaskerVariable("%DAYW", "Current day of the week (Sunday, Monday, etc.)", "Date/Time"),
    "%DESSION": TaskerVariable("%DESSION", "Undocumented date session var", "Date/Time"),
    "%MESSION": TaskerVariable("%MESSION", "Undocumented month session var", "Date/Time"),
    "%TESSION": TaskerVariable("%TESSION", "Undocumented time session var", "Date/Time"),

    # ─── Display ───
    "%SCREEN": TaskerVariable("%SCREEN", "Whether screen is on or off", "Display", dynamic=True),
    "%BRIGHT": TaskerVariable("%BRIGHT", "Current display brightness 0-255", "Display"),
    "%DTOUT": TaskerVariable("%DTOUT", "Current display timeout in seconds", "Display"),
    "%SYSRES": TaskerVariable("%SYSRES", "System display resolution WxH", "Display"),

    # ─── Email ───
    "%EFROM": TaskerVariable("%EFROM", "Sender of last received email", "Email", dynamic=True),
    "%ECC": TaskerVariable("%ECC", "Cc recipients of last received email", "Email", dynamic=True),
    "%ESUBJ": TaskerVariable("%ESUBJ", "Subject of last received email", "Email", dynamic=True),
    "%EDATE": TaskerVariable("%EDATE", "Date of last received email", "Email", dynamic=True),
    "%ETIME": TaskerVariable("%ETIME", "Time of last received email", "Email", dynamic=True),

    # ─── Hardware & Sensors ───
    "%CPUFREQ": TaskerVariable("%CPUFREQ", "Current frequency CPU 0 is running at (MHz)", "Hardware"),
    "%CPUGOV": TaskerVariable("%CPUGOV", "Current governor controlling CPU 0 frequency", "Hardware"),
    "%MEMF": TaskerVariable("%MEMF", "System free memory remaining in MB", "Hardware", dynamic=True),
    "%LIGHT": TaskerVariable("%LIGHT", "Ambient light level in lux", "Sensors", dynamic=True, monitored=True),
    "%PRESSURE": TaskerVariable("%PRESSURE", "Current air pressure in millibars", "Sensors", dynamic=True, monitored=True),
    "%TEMP": TaskerVariable("%TEMP", "Ambient temperature in degrees Celsius", "Sensors", dynamic=True, monitored=True),
    "%HUMIDITY": TaskerVariable("%HUMIDITY", "Relative ambient air humidity percentage", "Sensors", dynamic=True, monitored=True),
    "%MFIELD": TaskerVariable("%MFIELD", "Magnetic field strength in micro-Teslas", "Sensors", dynamic=True, monitored=True),
    "%HEART": TaskerVariable("%HEART", "Current detected heart rate in bpm", "Sensors", dynamic=True, monitored=True),

    # ─── Location ───
    "%LOC": TaskerVariable("%LOC", "Last known location as lat,lon", "Location", monitored=True),
    "%LOCACC": TaskerVariable("%LOCACC", "Accuracy of last location fix in meters", "Location"),
    "%LOCALT": TaskerVariable("%LOCALT", "Altitude of last fix in meters", "Location"),
    "%LOCSPD": TaskerVariable("%LOCSPD", "Speed at last fix in m/s", "Location"),
    "%LOCTMS": TaskerVariable("%LOCTMS", "Time of last fix in seconds since epoch", "Location"),
    "%LOCN": TaskerVariable("%LOCN", "Last network location as lat,lon", "Location", monitored=True),
    "%LOCNACC": TaskerVariable("%LOCNACC", "Accuracy of last network fix in meters", "Location"),
    "%LOCNTMS": TaskerVariable("%LOCNTMS", "Time of last network fix in epoch seconds", "Location"),
    "%GPS": TaskerVariable("%GPS", "Whether GPS is currently enabled: on/off", "Location", dynamic=True),

    # ─── Network ───
    "%WIFI": TaskerVariable("%WIFI", "Whether WiFi is enabled: on/off", "Network", dynamic=True),
    "%WIFII": TaskerVariable("%WIFII", "WiFi info when connected (SSID, MAC, IP, Speed)", "Network"),
    "%WIFIN": TaskerVariable("%WIFIN", "Nearest WiFi network SSID when scanning", "Network"),
    "%IP": TaskerVariable("%IP", "Current IP address of the device", "Network"),
    "%CELLID": TaskerVariable("%CELLID", "Current cell tower ID", "Network", monitored=True),
    "%CELLSIG": TaskerVariable("%CELLSIG", "Current cell signal strength (dBm)", "Network", dynamic=True),
    "%CELLSRV": TaskerVariable("%CELLSRV", "Cell service status: roaming/searching/service/noservice", "Network"),
    "%ROAM": TaskerVariable("%ROAM", "Whether device is roaming on telephone network: on/off", "Network", dynamic=True),
    "%TETHER": TaskerVariable("%TETHER", "Comma-separated list of enabled tethering forms (wifi, usb, bt)", "Network", dynamic=True),
    "%TETHBT": TaskerVariable("%TETHBT", "Bluetooth tether status: on/off", "Network"),
    "%TETHUSB": TaskerVariable("%TETHUSB", "USB tether status: on/off", "Network"),
    "%TETHWIFI": TaskerVariable("%TETHWIFI", "WiFi tether (hotspot) status: on/off", "Network"),
    "%WIMAX": TaskerVariable("%WIMAX", "Whether WiMAX status is on or off", "Network"),
    "%HTTPR": TaskerVariable("%HTTPR", "HTTP response code from last HTTP action", "Network", dynamic=True),
    "%HTTPD": TaskerVariable("%HTTPD", "HTTP response body data from last HTTP action", "Network", dynamic=True),
    "%HTTPL": TaskerVariable("%HTTPL", "HTTP response content length from last HTTP action", "Network", dynamic=True),

    # ─── Phone ───
    "%PESSION": TaskerVariable("%PESSION", "Phone session variable", "Phone"),
    "%PNUM": TaskerVariable("%PNUM", "Current phone number of the device", "Phone"),
    "%DEVID": TaskerVariable("%DEVID", "Device unique ID", "Phone"),
    "%DEVTID": TaskerVariable("%DEVTID", "Device telephony ID (IMEI for GSM, MEID for CDMA)", "Phone"),
    "%DEVMAN": TaskerVariable("%DEVMAN", "Device manufacturer", "Phone"),
    "%DEVMOD": TaskerVariable("%DEVMOD", "Device model", "Phone"),
    "%DEVPROD": TaskerVariable("%DEVPROD", "Device product name", "Phone"),
    "%SDK": TaskerVariable("%SDK", "Android SDK version number", "Phone"),
    "%SIMNUM": TaskerVariable("%SIMNUM", "SIM card serial number (ICCID)", "Phone"),
    "%SIMSTATE": TaskerVariable("%SIMSTATE", "Current SIM state: unknown/absent/pinrequired/pukrequired/netlocked/ready", "Phone"),

    # ─── SMS ───
    "%SMSRN": TaskerVariable("%SMSRN", "Name of last SMS sender (incoming)", "SMS"),
    "%SMSRF": TaskerVariable("%SMSRF", "Number of last SMS sender (incoming)", "SMS"),
    "%SMSRB": TaskerVariable("%SMSRB", "Body of last received SMS", "SMS"),
    "%SMSRD": TaskerVariable("%SMSRD", "Date of last received SMS", "SMS"),
    "%SMSRT": TaskerVariable("%SMSRT", "Time of last received SMS", "SMS"),
    "%MMSRS": TaskerVariable("%MMSRS", "Subject of last received MMS", "SMS"),

    # ─── Clipboard ───
    "%CLIP": TaskerVariable("%CLIP", "Current system clipboard contents", "Clipboard", dynamic=True),

    # ─── Music ───
    "%MTRACK": TaskerVariable("%MTRACK", "Current music track title", "Music", dynamic=True),
    "%MARTIST": TaskerVariable("%MARTIST", "Current music track artist", "Music"),
    "%MALBUM": TaskerVariable("%MALBUM", "Current music track album", "Music"),

    # ─── Notification ───
    "%NTITLE": TaskerVariable("%NTITLE", "Title of last notification", "Notification", dynamic=True),
    "%NTEXT": TaskerVariable("%NTEXT", "Text of last notification", "Notification"),
    "%NAPP": TaskerVariable("%NAPP", "App that sent last notification", "Notification"),
    "%NPACK": TaskerVariable("%NPACK", "Package name of last notification app", "Notification"),

    # ─── System ───
    "%AIR": TaskerVariable("%AIR", "Airplane mode status: on/off", "System", dynamic=True),
    "%AIRR": TaskerVariable("%AIRR", "Airplane radios that will be disabled", "System"),
    "%INTERRUPT": TaskerVariable("%INTERRUPT", "Current interruption/DND mode", "System", dynamic=True),
    "%LAPP": TaskerVariable("%LAPP", "Label of last used application", "System", dynamic=True),
    "%PACTIVE": TaskerVariable("%PACTIVE", "Comma-separated list of active profiles", "System"),
    "%ROESSION": TaskerVariable("%ROESSION", "Undocumented roam session var", "System"),
    "%MUTED": TaskerVariable("%MUTED", "Whether microphone is currently muted: on/off", "System", dynamic=True),
    "%SILENT": TaskerVariable("%SILENT", "Current silent mode state: off/vibrate/on", "System", dynamic=True),
    "%NIGHT": TaskerVariable("%NIGHT", "Current Android Night Mode: on/off/auto", "System", dynamic=True),
    "%UIMODE": TaskerVariable("%UIMODE", "Current Android UI mode: car/desk/appliance/tv/watch/normal", "System", dynamic=True, monitored=True),
    "%KEYG": TaskerVariable("%KEYG", "Whether Keyguard (lockscreen) is on or off", "System", dynamic=True),
    "%ROOT": TaskerVariable("%ROOT", "Whether root functions are available: yes/no", "System"),
    "%IMETHOD": TaskerVariable("%IMETHOD", "Current active input method name and subtype", "System"),
    "%FOTO": TaskerVariable("%FOTO", "Filesystem path to last photo taken by Tasker or camera", "System", dynamic=True),
    "%SPEECH": TaskerVariable("%SPEECH", "Current utterance from Say or Say File action", "System", dynamic=True),
    "%VOLC": TaskerVariable("%VOLC", "Current call volume", "System"),
    "%VOLM": TaskerVariable("%VOLM", "Current media volume", "System"),
    "%VOLN": TaskerVariable("%VOLN", "Current notification volume", "System"),
    "%VOLR": TaskerVariable("%VOLR", "Current ringer volume", "System"),
    "%VOLS": TaskerVariable("%VOLS", "Current system volume", "System"),
    "%VOLA": TaskerVariable("%VOLA", "Current alarm volume", "System"),
    "%VOLD": TaskerVariable("%VOLD", "Current DTMF volume", "System"),
    "%VOLBT": TaskerVariable("%VOLBT", "Current BT voice volume", "System"),
    "%WIN": TaskerVariable("%WIN", "Current window label (foreground activity)", "System", dynamic=True),

    # ─── Tasker Internal ───
    "%TRUN": TaskerVariable("%TRUN", "Current running task name", "Tasker"),
    "%TNET": TaskerVariable("%TNET", "Task entry task name", "Tasker"),
    "%TPRI": TaskerVariable("%TPRI", "Current task priority", "Tasker"),
    "%TCAL": TaskerVariable("%TCAL", "Caller task name (if run via Perform Task)", "Tasker"),
    "%qtime": TaskerVariable("%qtime", "Task queue time in seconds that task has been running", "Tasker"),
    "%tasker_current_action_number": TaskerVariable("%tasker_current_action_number", "Current action number in the running task (Tasker 6.2+)", "Tasker"),
    "%priority": TaskerVariable("%priority", "Current task priority (local)", "Tasker"),
    "%caller": TaskerVariable("%caller", "Task/profile/scene that started current task", "Tasker"),
    "%err": TaskerVariable("%err", "Error code from last action (0 = no error)", "Tasker"),
    "%errmsg": TaskerVariable("%errmsg", "Error message from last action", "Tasker"),

    # ─── Profile/Event ───
    "%PENABLED": TaskerVariable("%PENABLED", "Whether current profile is enabled", "Profile"),
    "%PNAME": TaskerVariable("%PNAME", "Current profile name", "Profile"),
    "%evtprm1": TaskerVariable("%evtprm1", "First event parameter (local)", "Profile"),
    "%evtprm2": TaskerVariable("%evtprm2", "Second event parameter (local)", "Profile"),
    "%evtprm3": TaskerVariable("%evtprm3", "Third event parameter (local)", "Profile"),
}
# fmt: on


def get_variable_by_name(name: str) -> Optional[TaskerVariable]:
    """Get a Tasker variable by its exact name (e.g., '%BATT')."""
    # Try exact match
    if name in BUILTIN_VARIABLES:
        return BUILTIN_VARIABLES[name]
    # Try with % prefix
    if not name.startswith("%"):
        key = f"%{name}"
        if key in BUILTIN_VARIABLES:
            return BUILTIN_VARIABLES[key]
    return None


def search_variables(
    query: str, category: Optional[str] = None
) -> list[TaskerVariable]:
    """Search variables by name/description, optionally filtered by category."""
    query_lower = query.lower()
    results = []
    for var in BUILTIN_VARIABLES.values():
        if category and var.category.lower() != category.lower():
            continue
        if (
            query_lower in var.name.lower()
            or query_lower in var.description.lower()
        ):
            results.append(var)
    return results
