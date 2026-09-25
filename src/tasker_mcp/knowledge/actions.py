"""Complete Tasker Action codes knowledge base.

Source: Tasker v5.15.5-beta (5303) - 373 action codes.
Reference: https://github.com/Taskomater/Tasker-XML-Info
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TaskerAction:
    """Represents a Tasker task action."""

    code: int
    name: str
    category: str
    description: str
    args: list[str] = field(default_factory=list)


# fmt: off
TASKER_ACTIONS: dict[int, TaskerAction] = {
    # ─── App Category ───
    15: TaskerAction(15, "Lock", "App", "Show a lock screen requiring a code to continue", ["Code", "Allow Cancel", "Remember Till Off"]),
    16: TaskerAction(16, "System Lock", "App", "Turn off the display and engage the keyguard", []),
    18: TaskerAction(18, "Kill App", "App", "Stop the specified application", ["App", "Use Root"]),
    20: TaskerAction(20, "Launch App", "App", "Launch the specified application", ["App", "Data", "Exclude From Recent Apps", "Always Use New Copy"]),
    22: TaskerAction(22, "Load Last App", "App", "Launch the previous foreground application", []),
    25: TaskerAction(25, "Go Home", "App", "Go to the current system Home Screen", ["Page"]),
    100: TaskerAction(100, "Search", "App", "Perform a search for the specified text", ["Text"]),
    104: TaskerAction(104, "Browse URL", "App", "Open the specified URL in the default browser", ["URL"]),
    335: TaskerAction(335, "App Info", "App", "Show app info screen", ["App"]),
    370: TaskerAction(370, "Shortcut", "App", "Launch a shortcut", ["Name"]),
    815: TaskerAction(815, "List Apps", "App", "List installed packages/apps/components", ["Type", "Store Results In"]),
    900: TaskerAction(900, "Browse Files", "App", "Run File Magic file manager", ["Dir", "Match", "Show Hidden"]),
    909: TaskerAction(909, "Contacts", "App", "Show contacts from the Android contacts app", ["Type"]),
    910: TaskerAction(910, "Call Log", "App", "Show the Call Log tab", []),

    # ─── Flow Category ───
    30: TaskerAction(30, "Wait", "Flow", "Stop executing the current task for the specified time", ["Hours", "Minutes", "Seconds"]),
    35: TaskerAction(35, "Wait Until", "Flow", "Stop executing until the condition is met", ["Condition", "Max Wait"]),
    37: TaskerAction(37, "If", "Flow", "Conditional execution of following actions", ["Condition"]),
    38: TaskerAction(38, "End If", "Flow", "End a conditional If block", []),
    39: TaskerAction(39, "For", "Flow", "Loop through a set of values", ["Variable", "Items"]),
    40: TaskerAction(40, "End For", "Flow", "End a For loop block", []),
    43: TaskerAction(43, "Else", "Flow", "Alternate branch in If block", []),
    126: TaskerAction(126, "Return", "Flow", "Return a value to the parent task", ["Value", "Stop"]),
    130: TaskerAction(130, "Perform Task", "Flow", "Run the selected Tasker task", ["Task", "Priority", "%par1", "%par2", "Return Value Variable", "Stop"]),
    135: TaskerAction(135, "Goto", "Flow", "Go to a different place in the current task", ["Type", "Number", "Label"]),
    137: TaskerAction(137, "Stop", "Flow", "Stop execution of one or more tasks", ["Task", "With Error"]),
    300: TaskerAction(300, "Anchor", "Flow", "Provides a fixed named point in a task", ["Label"]),
    365: TaskerAction(365, "Tasker Function", "Flow", "Execute a Tasker function", ["Function", "Args"]),

    # ─── Communication Category ───
    41: TaskerAction(41, "Send SMS", "Communication", "Send an SMS without user interaction", ["Number", "Message", "Store In Messaging App"]),
    42: TaskerAction(42, "Send Data SMS", "Communication", "Send a binary data SMS", ["Number", "Port", "Data"]),
    90: TaskerAction(90, "Call", "Communication", "Bring up the dialer with the specified number", ["Number", "Auto Dial"]),
    95: TaskerAction(95, "Call Block", "Communication", "Block outgoing calls to matched numbers", ["Number", "Info"]),
    97: TaskerAction(97, "Call Divert", "Communication", "Divert outgoing calls from a number to another", ["From", "To", "Info"]),
    99: TaskerAction(99, "Call Revert", "Communication", "Stop blocking or diverting calls", ["Number", "Info"]),
    111: TaskerAction(111, "Compose MMS", "Communication", "Launch an app to compose an MMS", ["Recipient", "Subject", "Message"]),
    125: TaskerAction(125, "Compose Email", "Communication", "Launch an app to compose an email", ["Recipient(s)", "Subject", "Message"]),
    250: TaskerAction(250, "Compose SMS", "Communication", "Launch an app to compose an SMS", ["Recipient", "Message"]),
    252: TaskerAction(252, "Set SMS App", "Communication", "Set the default SMS app", ["App"]),
    381: TaskerAction(381, "Contact Via App", "Communication", "Contact via a specific app", ["Contact", "App"]),
    731: TaskerAction(731, "Take Call", "Communication", "Silence the ringer and pick up the phone", []),
    733: TaskerAction(733, "End Call", "Communication", "End the current call", []),
    734: TaskerAction(734, "Silence Ringer", "Communication", "Stop the ring sound during incoming call", []),

    # ─── Alert Category ───
    61: TaskerAction(61, "Vibrate", "Alert", "Activate the device vibrator", ["Time"]),
    62: TaskerAction(62, "Vibrate Pattern", "Alert", "Activate the device vibrator in a pattern", ["Pattern", "Repeat"]),
    171: TaskerAction(171, "Beep", "Alert", "Generate a fixed-frequency audio tone", ["Frequency", "Duration", "Amplitude", "Stream"]),
    172: TaskerAction(172, "Morse", "Alert", "Play morse code representing given text", ["Text", "Frequency", "Amplitude", "Stream"]),
    177: TaskerAction(177, "Haptic Feedback", "Alert", "Change global system haptic feedback setting", ["Set"]),
    192: TaskerAction(192, "Play Ringtone", "Alert", "Play an alarm, notification or ringer ringtone", ["Type", "Sound", "Stream"]),
    523: TaskerAction(523, "Notify", "Alert", "Show a notification on the top bar", ["Title", "Text", "Icon", "Number", "Permanent", "Actions"]),
    525: TaskerAction(525, "Notify LED", "Alert", "Show notification and flash an LED", ["Title", "Text", "Colour", "Rate", "Number", "Permanent"]),
    536: TaskerAction(536, "Notify Vibrate", "Alert", "Show notification and vibrate", ["Title", "Text", "Pattern", "Number", "Permanent"]),
    538: TaskerAction(538, "Notify Sound", "Alert", "Show notification and play a sound", ["Title", "Text", "Sound File", "Number", "Permanent"]),
    548: TaskerAction(548, "Flash", "Alert", "Flash a message up briefly", ["Text", "Long"]),
    550: TaskerAction(550, "Popup", "Alert", "Show a popup box with a message", ["Title", "Text", "Timeout", "Show Over Keyguard"]),
    551: TaskerAction(551, "Menu", "Alert", "Show a selection dialog", ["Items", "Layout", "Timeout"]),
    552: TaskerAction(552, "Popup Task Buttons", "Alert", "Show a popup with 1-3 task buttons", ["Title", "Text", "Task 1", "Task 2", "Task 3"]),
    559: TaskerAction(559, "Say", "Alert", "Synthesize text into speech", ["Text", "Engine:Voice", "Stream", "Pitch", "Speed", "Continue Task Immediately"]),
    699: TaskerAction(699, "Say To File", "Alert", "Synthesize text to a WAV file", ["Text", "File", "Engine:Voice", "Pitch", "Speed"]),
    697: TaskerAction(697, "Shut Up", "Alert", "Stop speech from a previous Say action", []),
    334: TaskerAction(334, "Say WaveNet", "Alert", "Synthesize text using WaveNet", ["Text", "Voice", "Speed", "Pitch"]),
    779: TaskerAction(779, "Notify Cancel", "Alert", "Cancel a notification in the status bar", ["Title", "Warn Not Exist"]),
    543: TaskerAction(543, "Start System Timer", "Alert", "Start a system countdown timer", ["Seconds", "Message", "Show UI"]),
    566: TaskerAction(566, "Set Alarm", "Alert", "Set a new alarm in the default alarm clock", ["Hours", "Minutes", "Message", "Confirm"]),
    165: TaskerAction(165, "Cancel Alarm", "Alert", "Cancel a currently active or future system alarm", ["Label"]),
    166: TaskerAction(166, "Show Alarms", "Alert", "Bring up a screen showing configured alarms", []),

    # ─── Network Category ───
    113: TaskerAction(113, "WiFi Tether", "Network", "Turn on sharing of Internet via wifi", []),
    114: TaskerAction(114, "USB Tether", "Network", "Turn on sharing of Internet via USB", []),
    116: TaskerAction(116, "HTTP Post", "Network", "Send an HTTP POST request", ["Server:Port", "Path", "Data", "Cookies", "Content-Type", "File", "Timeout"]),
    117: TaskerAction(117, "HTTP Head", "Network", "Send an HTTP HEAD request", ["Server:Port", "Path", "Attributes", "Cookies", "Timeout"]),
    118: TaskerAction(118, "HTTP Get", "Network", "Send an HTTP GET request", ["Server:Port", "Path", "Attributes", "Cookies", "Content-Type", "File", "Timeout"]),
    173: TaskerAction(173, "Network Access", "Network", "Deny network access to all or selected apps", ["Mode", "Apps"]),
    294: TaskerAction(294, "Bluetooth", "Network", "Enable or disable Bluetooth radio", ["Set"]),
    295: TaskerAction(295, "Bluetooth ID", "Network", "Set the name of local bluetooth device", ["Name"]),
    296: TaskerAction(296, "Bluetooth Voice", "Network", "Switch to/from Bluetooth headset for voice", ["Set"]),
    317: TaskerAction(317, "NFC", "Network", "Enable or disable NFC", ["Set"]),
    320: TaskerAction(320, "Ping", "Network", "Ping a network host", ["Host", "Times"]),
    323: TaskerAction(323, "Airplane Radios", "Network", "Specify which radios disabled in Airplane Mode", ["Radios"]),
    330: TaskerAction(330, "NFC Tag", "Network", "Write data to an NFC tag", ["Data"]),
    331: TaskerAction(331, "Auto-Sync", "Network", "Whether auto-syncing of data is enabled", ["Set"]),
    332: TaskerAction(332, "GPS", "Network", "Whether the GPS receiver is enabled", ["Set"]),
    333: TaskerAction(333, "Airplane Mode", "Network", "Whether airplane mode is enabled", ["Set"]),
    339: TaskerAction(339, "HTTP Request", "Network", "Make an HTTP request", ["Method", "URL", "Headers", "Body", "File", "Timeout", "Trust Any Certificate"]),
    340: TaskerAction(340, "Bluetooth Connection", "Network", "Connect/disconnect a BT device", ["Device", "Action"]),
    341: TaskerAction(341, "Test Net", "Network", "Test a network attribute", ["Type", "Data", "Store Result In"]),
    351: TaskerAction(351, "HTTP Auth", "Network", "Set HTTP authentication credentials", ["Server:Port", "Username", "Password"]),
    358: TaskerAction(358, "Bluetooth Info", "Network", "Get info about a Bluetooth device", ["Device", "Store Result In"]),
    375: TaskerAction(375, "ADB Wifi", "Network", "Enable/disable ADB over Wifi", ["Set"]),
    398: TaskerAction(398, "Connect To WiFi", "Network", "Connect to a specific WiFi network", ["SSID", "Password"]),
    425: TaskerAction(425, "WiFi", "Network", "Whether the WiFi radio is enabled or disabled", ["Set"]),
    426: TaskerAction(426, "WiFi Net", "Network", "Change wifi network connection status", ["Command", "SSID", "MAC", "Reassociate", "Force"]),
    427: TaskerAction(427, "WiFi Sleep", "Network", "The policy for when Wifi should go to sleep", ["Policy"]),
    433: TaskerAction(433, "Mobile Data", "Network", "Set mobile data status", ["Set"]),
    439: TaskerAction(439, "WiMax", "Network", "Whether WiMax radio is enabled or disabled", ["Set"]),
    735: TaskerAction(735, "Mobile Data 2G/3G", "Network", "Set mobile data mode to 2G or 3G", ["Mode"]),
    363: TaskerAction(363, "Mobile Network Type", "Network", "Set the mobile network type", ["Type"]),
    905: TaskerAction(905, "Location Mode", "Network", "Set the device location mode", ["Mode"]),

    # ─── Variable Category ───
    354: TaskerAction(354, "Array Set", "Variable", "Set array values from a preset list", ["Variable", "Values", "Splitter"]),
    355: TaskerAction(355, "Array Push", "Variable", "Add a new element to a variable array", ["Variable", "Position", "Value", "Fill Spaces"]),
    356: TaskerAction(356, "Array Pop", "Variable", "Remove an element from an array", ["Variable", "Position", "To Var"]),
    357: TaskerAction(357, "Array Clear", "Variable", "Remove all elements of an array variable", ["Variable"]),
    369: TaskerAction(369, "Array Process", "Variable", "Perform an operation on array elements", ["Variable", "Type"]),
    389: TaskerAction(389, "Multiple Variables Set", "Variable", "Set multiple variables at once", ["Variables"]),
    392: TaskerAction(392, "Set Variable Structure Type", "Variable", "Set variable structure type", ["Variable", "Type"]),
    393: TaskerAction(393, "Arrays Merge", "Variable", "Merge two arrays", ["Array 1", "Array 2", "Type"]),
    394: TaskerAction(394, "Parse/Format DateTime", "Variable", "Parse or format date/time values", ["Input", "Input Format", "Output Format", "Store Result In"]),
    396: TaskerAction(396, "Simple Match/Regex", "Variable", "Perform simple match or regex on text", ["Text", "Pattern", "Store Result In"]),
    399: TaskerAction(399, "Variable Map", "Variable", "Map variable values", ["Variable", "Mappings"]),
    545: TaskerAction(545, "Variable Randomize", "Variable", "Set variable to random integer", ["Name", "Min", "Max"]),
    547: TaskerAction(547, "Variable Set", "Variable", "Set the variable to a value", ["Name", "To", "Recurse Variables", "Do Maths", "Append"]),
    549: TaskerAction(549, "Variable Clear", "Variable", "Remove the stored value for a variable", ["Name", "Pattern Matching"]),
    590: TaskerAction(590, "Variable Split", "Variable", "Split variable value into sub-variables", ["Name", "Splitter", "Delete Base"]),
    592: TaskerAction(592, "Variable Join", "Variable", "Join array values into a single variable", ["Name", "Joiner", "Delete Array"]),
    595: TaskerAction(595, "Variable Query", "Variable", "Ask user for a value via popup dialog", ["Variable", "Title", "Default", "Input Type"]),
    596: TaskerAction(596, "Variable Convert", "Variable", "Convert variable value between units", ["Variable", "Function", "Store Result In"]),
    597: TaskerAction(597, "Variable Section", "Variable", "Select a particular section of a variable", ["Variable", "From", "Length", "Adapt To Fit"]),
    598: TaskerAction(598, "Variable Search Replace", "Variable", "Find/replace parts matching a regex", ["Variable", "Search", "Ignore Case", "Multi-Line", "One Match Only", "Store Matches In", "Replace Matches", "Replace With"]),
    888: TaskerAction(888, "Variable Add", "Variable", "Increase the value of a variable", ["Name", "Value", "Wrap Around"]),
    890: TaskerAction(890, "Variable Subtract", "Variable", "Decrease the value of a variable", ["Name", "Value", "Wrap Around"]),
    345: TaskerAction(345, "Test Variable", "Variable", "Test a variable attribute", ["Type", "Data", "Store Result In"]),

    # ─── File Category ───
    400: TaskerAction(400, "Move", "File", "Move an SD card file or directory", ["From", "To"]),
    404: TaskerAction(404, "Copy File", "File", "Copy an SD card file to a new directory", ["From", "To"]),
    405: TaskerAction(405, "Copy Dir", "File", "Recursively copy a directory", ["From", "To"]),
    406: TaskerAction(406, "Delete File", "File", "Delete an SD card file", ["File", "Shred Level"]),
    408: TaskerAction(408, "Delete Directory", "File", "Delete an SD card directory", ["Dir", "Recurse"]),
    409: TaskerAction(409, "Create Directory", "File", "Create an SD card directory", ["Dir", "Create All"]),
    410: TaskerAction(410, "Write File", "File", "Write text to a file", ["File", "Text", "Append", "Add Newline"]),
    412: TaskerAction(412, "List Files", "File", "List files in a directory", ["Dir", "Match", "Store Results In", "Sort", "Use Root"]),
    415: TaskerAction(415, "Read Line", "File", "Read a line from a text file", ["File", "Line", "Variable"]),
    416: TaskerAction(416, "Read Paragraph", "File", "Read a paragraph from a text file", ["File", "Paragraph", "Variable"]),
    417: TaskerAction(417, "Read File", "File", "Read a text file into a variable", ["File", "Variable"]),
    420: TaskerAction(420, "Zip", "File", "Compress files to a zip archive", ["File(s)", "Output Path", "Level", "Delete Orig"]),
    422: TaskerAction(422, "UnZip", "File", "Decompress a zip archive", ["File", "Delete Zip"]),
    475: TaskerAction(475, "GZip", "File", "Compress a file to gzip archive", ["File", "Delete Orig"]),
    476: TaskerAction(476, "GUnzip", "File", "Decompress a gzip archive", ["File", "Delete Zip"]),
    775: TaskerAction(775, "Write Binary", "File", "Write base64 data to binary file", ["File", "Variable"]),
    776: TaskerAction(776, "Read Binary", "File", "Read binary data into base64 variable", ["File", "Variable"]),
    342: TaskerAction(342, "Test File", "File", "Test an attribute of a file", ["Type", "Data", "Store Result In"]),
    376: TaskerAction(376, "Share File", "File", "Share a file with another app", ["File", "Mime Type", "Show Chooser", "Chooser Title"]),

    # ─── Media Category ───
    101: TaskerAction(101, "Take Photo", "Media", "Take a photo", ["Camera", "Filename", "Discreet", "Insert In Gallery", "Resolution"]),
    185: TaskerAction(185, "Filter Image", "Media", "Apply filter to image in image store", ["Filter", "Value"]),
    187: TaskerAction(187, "Save Image", "Media", "Write image store to a file", ["File", "Quality"]),
    188: TaskerAction(188, "Load Image", "Media", "Load an image into the image store", ["File", "Max Width Or Height", "Respect EXIF"]),
    189: TaskerAction(189, "Crop Image", "Media", "Crop image in the image store", ["Left", "Top", "Right", "Bottom"]),
    190: TaskerAction(190, "Flip Image", "Media", "Flip image in the image store", ["Direction"]),
    191: TaskerAction(191, "Rotate Image", "Media", "Rotate image in the image store", ["Degrees"]),
    193: TaskerAction(193, "Resize Image", "Media", "Resize and scale image in image store", ["Width", "Height"]),
    343: TaskerAction(343, "Test Media", "Media", "Test some aspect of media", ["Type", "Data", "Store Result In"]),
    374: TaskerAction(374, "Screen Capture", "Media", "Capture the screen", ["File", "Quality"]),
    443: TaskerAction(443, "Media Control", "Media", "Send a command to a media player", ["Command", "Simulate Media Button", "App"]),
    445: TaskerAction(445, "Music Play", "Media", "Play a sound file from SD card", ["File", "Start", "Loop", "Stream"]),
    447: TaskerAction(447, "Music Play Dir", "Media", "Play music files from a directory", ["Dir", "Audio Only", "Random"]),
    449: TaskerAction(449, "Music Stop", "Media", "Stop playback of a sound file", ["Clear Dir"]),
    451: TaskerAction(451, "Music Skip", "Media", "Jump forward in a sound file", ["Seconds"]),
    453: TaskerAction(453, "Music Back", "Media", "Jump backwards in a sound file", ["Seconds"]),
    455: TaskerAction(455, "Record Audio", "Media", "Record from microphone to file", ["File", "Source", "Format", "Max Filesize"]),
    457: TaskerAction(457, "Default Ringtone", "Media", "Set the default ringtone", ["Type", "Sound"]),
    459: TaskerAction(459, "Scan Media", "Media", "Force system to scan SD card for media", ["File"]),
    490: TaskerAction(490, "Media Button Events", "Media", "Grab media button events for Tasker", ["Grab"]),
    657: TaskerAction(657, "Record Audio Stop", "Media", "Stop a sound recording", []),
    176: TaskerAction(176, "Take Screenshot", "Media", "Take a screenshot of the display", ["File"]),

    # ─── Display Category ───
    150: TaskerAction(150, "Keyguard", "Display", "Whether the keyguard is enabled or disabled", ["Set"]),
    244: TaskerAction(244, "Toggle Split Screen", "Display", "Toggle split screen mode for current app", []),
    316: TaskerAction(316, "Display Size", "Display", "Set the display size/density", ["Size"]),
    318: TaskerAction(318, "Force Rotation", "Display", "Force display rotation", ["Mode"]),
    329: TaskerAction(329, "Navigation Bar", "Display", "Show/hide the navigation bar", ["Set"]),
    361: TaskerAction(361, "Dark Mode", "Display", "Enable or disable dark mode", ["Set"]),
    512: TaskerAction(512, "Status Bar", "Display", "Expand or collapse the system status bar", ["Set"]),
    513: TaskerAction(513, "Close System Dialogs", "Display", "Close system dialogs like Recent Apps", []),
    806: TaskerAction(806, "Turn On", "Display", "Turn on the display", []),
    808: TaskerAction(808, "Auto Brightness", "Display", "Enable/disable automatic brightness", ["Set"]),
    810: TaskerAction(810, "Display Brightness", "Display", "Set screen brightness level 0-255", ["Level", "Disable Safeguard", "Ignore Current Level", "Immediate Effect"]),
    812: TaskerAction(812, "Display Timeout", "Display", "Set time before screen powers off", ["Secs", "Mins", "Hours"]),
    820: TaskerAction(820, "Stay On", "Display", "Prevent screen off while power supply present", ["Mode"]),
    822: TaskerAction(822, "Display AutoRotate", "Display", "Whether rotating device rotates screen", ["Set"]),
    906: TaskerAction(906, "Immersive Mode", "Display", "Enable/disable immersive mode", ["Mode"]),
    907: TaskerAction(907, "Status Bar Icons", "Display", "Show/hide status bar icons", ["Set"]),
    348: TaskerAction(348, "Test Display", "Display", "Test an attribute of the display", ["Type", "Store Result In"]),
    511: TaskerAction(511, "Torch", "Display", "Hold the camera flashlight on", ["Set"]),

    # ─── Audio Category ───
    136: TaskerAction(136, "Sound Effects", "Audio", "Whether to enable/disable system sounds", ["Set"]),
    156: TaskerAction(156, "MIDI Play", "Audio", "Play notes on a MIDI instrument via USB", ["Notes", "Instrument", "Duration"]),
    254: TaskerAction(254, "Speakerphone", "Audio", "Whether speakerphone is on or off", ["Set"]),
    256: TaskerAction(256, "Vibrate On Ringer", "Audio", "Whether to vibrate on incoming call", ["Set"]),
    258: TaskerAction(258, "Vibrate On Notify", "Audio", "Whether to vibrate with notification", ["Set"]),
    259: TaskerAction(259, "Notification Pulse", "Audio", "Whether to pulse LED for notifications", ["Set"]),
    301: TaskerAction(301, "Mic Mute", "Audio", "Mute the device microphone", ["Set"]),
    303: TaskerAction(303, "Alarm Volume", "Audio", "Set alarm volume level", ["Level", "Display", "Sound"]),
    304: TaskerAction(304, "Ringer Volume", "Audio", "Set phone ringer volume level", ["Level", "Display", "Sound"]),
    305: TaskerAction(305, "Notification Volume", "Audio", "Set notification volume level", ["Level", "Display", "Sound"]),
    306: TaskerAction(306, "In-Call Volume", "Audio", "Set volume during calls", ["Level", "Display", "Sound"]),
    307: TaskerAction(307, "Media Volume", "Audio", "Set media playback volume level", ["Level", "Display", "Sound"]),
    308: TaskerAction(308, "System Volume", "Audio", "Set system sounds volume level", ["Level", "Display", "Sound"]),
    309: TaskerAction(309, "DTMF Volume", "Audio", "Set DTMF volume level", ["Level", "Display", "Sound"]),
    310: TaskerAction(310, "Vibrate Mode", "Audio", "Set vibrate/silent mode", ["Mode"]),
    311: TaskerAction(311, "BT Voice Volume", "Audio", "Set in-call volume on bluetooth", ["Level", "Display", "Sound"]),
    312: TaskerAction(312, "Do Not Disturb", "Audio", "Set Do Not Disturb mode", ["Mode"]),
    313: TaskerAction(313, "Sound Mode", "Audio", "Set the sound/silent/vibrate mode", ["Mode"]),
    387: TaskerAction(387, "Accessibility Volume", "Audio", "Set accessibility volume", ["Level", "Display", "Sound"]),

    # ─── Code Category ───
    112: TaskerAction(112, "Run SL4A Script", "Code", "Run a Scripting Layer for Android script", ["Script", "Passed Variables"]),
    123: TaskerAction(123, "Run Shell", "Code", "Run a system shell command under linux", ["Command", "Timeout", "Use Root", "Store Output In", "Store Errors In", "Continue On Error"]),
    129: TaskerAction(129, "JavaScriptlet", "Code", "Run a piece of JavaScript and wait", ["Code", "Libraries", "Auto Exit", "Timeout"]),
    131: TaskerAction(131, "JavaScript", "Code", "Run JavaScript from a file and wait", ["File", "Libraries", "Auto Exit", "Timeout"]),
    664: TaskerAction(664, "Java Function", "Code", "Execute a native Java function", ["Class Or Object", "Function", "Param 1", "Param 2", "Return", "Return Type"]),
    665: TaskerAction(665, "Java Object", "Code", "Manipulate a Java object", ["Action", "Object", "Class"]),
    667: TaskerAction(667, "SQL Query", "Code", "Query an SQL database in file or URI", ["Mode", "File/URI", "Table", "Columns", "Query/Selection", "Selection Args", "Order", "Output Column Divider", "Variable"]),
    877: TaskerAction(877, "Send Intent", "Code", "Broadcast an ordered Intent", ["Action", "Cat", "Data", "Mime Type", "Extra", "Package", "Class", "Target"]),
    385: TaskerAction(385, "Command", "Code", "Send a command to Tasker from another app", ["Command", "Caller", "Regex"]),

    # ─── System Category ───
    59: TaskerAction(59, "Reboot", "System", "Reboot or shutdown the device", ["Type"]),
    105: TaskerAction(105, "Set Clipboard", "System", "Copy text to the system clipboard", ["Text", "Add"]),
    109: TaskerAction(109, "Set Wallpaper", "System", "Set system wallpaper from an image file", ["File", "Scale", "Crop"]),
    124: TaskerAction(124, "Remount", "System", "Remount a filesystem read-write or read-only", ["Path", "Writeable"]),
    153: TaskerAction(153, "Import Data", "System", "Dynamically load a task into configuration", ["Data", "Type"]),
    175: TaskerAction(175, "Power Mode", "System", "Set the system power mode", ["Mode"]),
    245: TaskerAction(245, "Back Button", "System", "Simulate pressing the back button", []),
    246: TaskerAction(246, "Long Power Button", "System", "Simulate long press of power button", []),
    247: TaskerAction(247, "Show Recents", "System", "Show recent apps", []),
    248: TaskerAction(248, "Turn Off", "System", "Turn off the device", []),
    249: TaskerAction(249, "System Screenshot", "System", "Take a system screenshot", []),
    251: TaskerAction(251, "Battery Info", "System", "Show battery info settings screen", []),
    314: TaskerAction(314, "Authentication Dialog", "System", "Show an authentication dialog", ["Title", "Subtitle", "Description"]),
    319: TaskerAction(319, "Ask Permissions", "System", "Ask for runtime permissions", ["Permissions"]),
    322: TaskerAction(322, "Data Backup", "System", "Backup Tasker data", []),
    328: TaskerAction(328, "Keyboard", "System", "Show/hide the soft keyboard", ["Set"]),
    344: TaskerAction(344, "Test App", "System", "Test some aspect of an application", ["Type", "Data", "Store Result In"]),
    346: TaskerAction(346, "Test Phone", "System", "Test something phone related", ["Type", "Data", "Store Result In"]),
    347: TaskerAction(347, "Test Tasker", "System", "Test some aspect of Tasker configuration", ["Type", "Data", "Store Result In"]),
    349: TaskerAction(349, "Test System", "System", "Test an operating system attribute", ["Type", "Store Result In"]),
    364: TaskerAction(364, "Test Next Alarm", "System", "Test next alarm info", ["Store Result In"]),
    372: TaskerAction(372, "Sensor Info", "System", "Get sensor information", ["Sensor", "Store Result In"]),
    373: TaskerAction(373, "Test Sensor", "System", "Test a sensor value", ["Sensor", "Store Result In"]),
    383: TaskerAction(383, "Settings Panel", "System", "Open a system settings panel", ["Panel"]),
    384: TaskerAction(384, "Power Menu Action", "System", "Perform a power menu action", ["Action"]),
    386: TaskerAction(386, "Call Screening", "System", "Set up call screening", ["Action"]),
    440: TaskerAction(440, "Set Timezone", "System", "Set the device timezone", ["Timezone"]),
    804: TaskerAction(804, "Input Method Select", "System", "Show Input Method picker dialog", []),
    915: TaskerAction(915, "CPU", "System", "Control CPU frequency/governor", ["Frequency", "Governor"]),
    987: TaskerAction(987, "Soft Keyboard", "System", "Show/hide the soft keyboard", ["Set"]),
    988: TaskerAction(988, "Car Mode", "System", "Enable or disable Car Mode", ["Set", "Go Home"]),
    989: TaskerAction(989, "Night Mode", "System", "Change Night Mode setting", ["Set"]),
    999: TaskerAction(999, "Set Light", "System", "Change brightness of a light", ["Light", "Level"]),
    362: TaskerAction(362, "Set Assistant", "System", "Set the device assistant app", ["App"]),

    # ─── Scene Category ───
    46: TaskerAction(46, "Create Scene", "Scene", "Create a scene without displaying it", ["Name"]),
    47: TaskerAction(47, "Show Scene", "Scene", "Display a scene", ["Name", "Display As", "Horizontal Position", "Vertical Position", "Animation", "Continue Task Immediately", "Allow Outside"]),
    48: TaskerAction(48, "Hide Scene", "Scene", "Hide a scene currently displayed", ["Name", "Animation"]),
    49: TaskerAction(49, "Destroy Scene", "Scene", "Destroy a previously created scene", ["Name"]),
    50: TaskerAction(50, "Element Value", "Scene", "Set value of a scene element", ["Scene", "Element", "Value"]),
    51: TaskerAction(51, "Element Text", "Scene", "Set text of a scene element", ["Scene", "Element", "Text", "Selection"]),
    53: TaskerAction(53, "Element Web Control", "Scene", "Manipulate a WebView element", ["Scene", "Element", "Command"]),
    54: TaskerAction(54, "Element Text Colour", "Scene", "Set text colour of element", ["Scene", "Element", "Colour"]),
    55: TaskerAction(55, "Element Back Colour", "Scene", "Set background colour of element", ["Scene", "Element", "Colour", "End Colour"]),
    56: TaskerAction(56, "Element Border", "Scene", "Set border of an element", ["Scene", "Element", "Width", "Colour"]),
    57: TaskerAction(57, "Element Position", "Scene", "Move a scene element", ["Scene", "Element", "X", "Y", "Animation Time"]),
    58: TaskerAction(58, "Element Size", "Scene", "Change size of an element", ["Scene", "Element", "Width", "Height"]),
    60: TaskerAction(60, "Element Add GeoMarker", "Scene", "Add a marker to a Map element", ["Scene", "Element", "Lat", "Lon", "Label", "Spot Radius"]),
    63: TaskerAction(63, "Element Delete GeoMarker", "Scene", "Delete a marker from Map element", ["Scene", "Element", "Lat", "Lon"]),
    64: TaskerAction(64, "Element Map Control", "Scene", "Control a Map scene element", ["Scene", "Element", "Command"]),
    65: TaskerAction(65, "Element Visibility", "Scene", "Hide or show a scene element", ["Scene", "Element", "Set", "Animation Time"]),
    66: TaskerAction(66, "Element Image", "Scene", "Set image of an Image element", ["Scene", "Element", "Image"]),
    67: TaskerAction(67, "Element Depth", "Scene", "Set depth of element in scene", ["Scene", "Element", "Depth"]),
    68: TaskerAction(68, "Element Focus", "Scene", "Give/remove input focus to element", ["Scene", "Element", "Set"]),
    69: TaskerAction(69, "Element Create", "Scene", "Create new element dynamically", ["Scene", "Element Type", "Position", "Size"]),
    71: TaskerAction(71, "Element Text Size", "Scene", "Set text size of element", ["Scene", "Element", "Size"]),
    73: TaskerAction(73, "Element Destroy", "Scene", "Destroy and remove an element", ["Scene", "Element"]),
    194: TaskerAction(194, "Test Scene", "Scene", "Test an attribute of a scene", ["Scene", "Type", "Store Result In"]),
    195: TaskerAction(195, "Test Element", "Scene", "Test a property of a scene element", ["Scene", "Element", "Type", "Store Result In"]),
    612: TaskerAction(612, "Element Video Control", "Scene", "Control a Video element", ["Scene", "Element", "Command", "Source"]),

    # ─── Input Category ───
    360: TaskerAction(360, "Input Dialog", "Input", "Show an input dialog", ["Title", "Text", "Default", "Input Type", "Timeout"]),
    377: TaskerAction(377, "Text Dialog", "Input", "Show a text dialog", ["Title", "Text", "Button 1", "Button 2", "Button 3"]),
    378: TaskerAction(378, "List Dialog", "Input", "Show a list dialog", ["Title", "Items", "Selection Mode", "Multi-Select Initial"]),
    390: TaskerAction(390, "Pick Input Dialog", "Input", "Show a pick input dialog", ["Title", "Items", "Default"]),
    595: TaskerAction(595, "Variable Query", "Input", "Ask user for a value via popup dialog", ["Variable", "Title", "Default", "Input Type"]),
    701: TaskerAction(701, "Dpad", "Input", "Simulate use of Dpad or trackball", ["Direction", "Times"]),
    702: TaskerAction(702, "Type", "Input", "Simulate typing of text (root)", ["Text"]),
    703: TaskerAction(703, "Button", "Input", "Simulate pressing hardware button (root)", ["Button"]),
    903: TaskerAction(903, "Get Voice", "Input", "Use speech recognizer to convert speech to text", ["Language Model", "Timeout"]),
    904: TaskerAction(904, "Voice Command", "Input", "Run default voice command app", []),
    368: TaskerAction(368, "Pick Location", "Input", "Pick a location on a map", ["Store Result In"]),

    # ─── Google Category ───
    321: TaskerAction(321, "GD Upload", "Google", "Upload a file to Google Drive", ["File", "Folder"]),
    324: TaskerAction(324, "GD List", "Google", "List Google Drive items", ["Folder", "Store Result In"]),
    325: TaskerAction(325, "GD Trash", "Google", "Trash a Google Drive item", ["File"]),
    326: TaskerAction(326, "GD Download", "Google", "Download from Google Drive", ["File", "Destination"]),
    327: TaskerAction(327, "GD Sign In", "Google", "Sign into Google Drive", []),
    119: TaskerAction(119, "Open Map", "Google", "Launch Google Maps", ["Mode", "Address", "Lat", "Lon", "Zoom", "Label"]),
    567: TaskerAction(567, "Calendar Insert", "Google", "Insert entry into a calendar", ["Calendar", "Title", "Location", "Description", "In", "For", "Available"]),
    397: TaskerAction(397, "Get Material You Colors", "Google", "Get Material You color palette", ["Store Result In"]),

    # ─── Tasker Category ───
    133: TaskerAction(133, "Set Tasker Pref", "Tasker", "Dynamically set a Tasker preference", ["Preference", "Value"]),
    134: TaskerAction(134, "Query Action", "Tasker", "Get details of an action then run it", ["Action"]),
    138: TaskerAction(138, "Set Tasker Icon", "Tasker", "Set Tasker notification icon", ["Icon"]),
    139: TaskerAction(139, "Disable", "Tasker", "Permanently turn off Tasker monitor", []),
    140: TaskerAction(140, "Change Icon Set", "Tasker", "Change widget Task icons", ["New", "Old"]),
    142: TaskerAction(142, "Edit Task", "Tasker", "Open Task Edit screen in Tasker UI", ["Task", "Action"]),
    143: TaskerAction(143, "Edit Scene", "Tasker", "Open Scene Edit screen in Tasker UI", ["Scene", "Element"]),
    147: TaskerAction(147, "Show Prefs", "Tasker", "Show Tasker preferences", []),
    148: TaskerAction(148, "Show Runlog", "Tasker", "Show Tasker run log", []),
    152: TaskerAction(152, "Set Widget Icon", "Tasker", "Change widget task icon", ["Name", "Icon"]),
    155: TaskerAction(155, "Set Widget Label", "Tasker", "Change widget task label", ["Name", "Label"]),
    157: TaskerAction(157, "Quick Setting Add", "Tasker", "Add custom Quick Settings tile (Cyanogen)", ["Label", "Icon", "Status", "Items"]),
    158: TaskerAction(158, "Quick Setting Remove", "Tasker", "Remove a Quick Settings tile", ["Label"]),
    159: TaskerAction(159, "Profile Status", "Tasker", "Enable or disable a named profile", ["Name", "Set"]),
    161: TaskerAction(161, "Setup App Shortcuts", "Tasker", "Configure app shortcuts on long-click", ["Task 1", "Task 2", "Task 3", "Task 4"]),
    162: TaskerAction(162, "Setup Quick Setting", "Tasker", "Configure a Quick Settings tile", ["Number", "Task", "Label", "Icon", "Status", "Long Click Task", "Double Click Task"]),
    395: TaskerAction(395, "JD Status", "Tasker", "Juice Defender status control", ["Set"]),
    544: TaskerAction(544, "Timer Widget Control", "Tasker", "Control a Task Timer widget", ["Task", "Command"]),
    546: TaskerAction(546, "Timer Widget Set", "Tasker", "Set the period of a Timer widget", ["Task", "Hours", "Minutes", "Seconds"]),

    # ─── Plugin Category ───
    1000: TaskerAction(1000, "Plugin", "Plugin", "Run the specified action plugin", ["Plugin", "Timeout"]),

    # ─── Misc Category ───
    102: TaskerAction(102, "Open File", "Misc", "Open a file on the SD card", ["File", "Mime Type"]),
    366: TaskerAction(366, "Get Location v2", "Misc", "Get a location fix (v2)", ["Source", "Timeout", "Continue Task Immediately", "Keep Tracking"]),
    367: TaskerAction(367, "Camera", "Misc", "Control camera", ["Command"]),
    371: TaskerAction(371, "Astrid", "Misc", "Interact with Astrid task manager", []),
    442: TaskerAction(442, "SleepBot", "Misc", "Interact with SleepBot app", []),
    444: TaskerAction(444, "TeslaLED", "Misc", "Use camera flash as torch via TeslaLED", ["Set"]),
    450: TaskerAction(450, "APN Droid", "Misc", "Enable/disable mobile data via APNDroid", ["Set"]),
    456: TaskerAction(456, "JD APN", "Misc", "Juice Defender APN control", ["Set"]),
    458: TaskerAction(458, "WidgetLocker", "Misc", "Control WidgetLocker", ["Command"]),
    553: TaskerAction(553, "SMS Backup+", "Misc", "Trigger SMS Backup+", ["Action"]),
    555: TaskerAction(555, "BeyondPod", "Misc", "Control BeyondPod podcast app", ["Command"]),
    556: TaskerAction(556, "GrazeRSS", "Misc", "Control GrazeRSS reader", ["Command"]),
    558: TaskerAction(558, "Android Notifier", "Misc", "Send notification via Android Notifier", ["Type"]),
    568: TaskerAction(568, "DailyRoads Voyager", "Misc", "Control DailyRoads Voyager app", ["Command"]),
    599: TaskerAction(599, "Due Today", "Misc", "Interact with Due Today app", []),
    643: TaskerAction(643, "OfficeTalk", "Misc", "Control OfficeTalk app", []),
    732: TaskerAction(732, "Radio", "Misc", "Set phone radio status", ["Set"]),
    911: TaskerAction(911, "Gentle Alarm", "Misc", "Enable/disable Gentle Alarm", ["Name", "Set"]),
    941: TaskerAction(941, "HTML Popup", "Misc", "Show a popup with HTML content", ["HTML", "Timeout", "Width", "Height"]),
    901: TaskerAction(901, "Stop Location", "Misc", "Stop tracking a location source", []),
    902: TaskerAction(902, "Get Location", "Misc", "Get a location fix", ["Source", "Timeout", "Continue Task Immediately", "Keep Tracking"]),

    # ─── Settings Category (mapped to System) ───
    197: TaskerAction(197, "Developer Settings", "System", "Open Developer Settings", []),
    198: TaskerAction(198, "Device Info Settings", "System", "Open Device Info Settings", []),
    199: TaskerAction(199, "Add Account Settings", "System", "Open Add Account Settings", []),
    200: TaskerAction(200, "All Settings", "System", "Open All Settings", []),
    201: TaskerAction(201, "Airplane Mode Settings", "System", "Open Airplane Mode Settings", []),
    202: TaskerAction(202, "APN Settings", "System", "Open APN Settings", []),
    203: TaskerAction(203, "Date Settings", "System", "Open Date Settings", []),
    204: TaskerAction(204, "Internal Storage Settings", "System", "Open Internal Storage Settings", []),
    206: TaskerAction(206, "WIFI Settings", "System", "Open WIFI Settings", []),
    208: TaskerAction(208, "Location Settings", "System", "Open Location Settings", []),
    210: TaskerAction(210, "InputMethod Settings", "System", "Open InputMethod Settings", []),
    211: TaskerAction(211, "Sync Settings", "System", "Open Sync Settings", []),
    212: TaskerAction(212, "WIFI IP Settings", "System", "Open WIFI IP Settings", []),
    214: TaskerAction(214, "Wireless Settings", "System", "Open Wireless Settings", []),
    216: TaskerAction(216, "App Settings", "System", "Open App Settings", []),
    218: TaskerAction(218, "Bluetooth Settings", "System", "Open Bluetooth Settings", []),
    219: TaskerAction(219, "Quick Settings", "System", "Open Quick Settings", []),
    220: TaskerAction(220, "Mobile Data Settings", "System", "Open Mobile Data Settings", []),
    222: TaskerAction(222, "Display Settings", "System", "Open Display Settings", []),
    224: TaskerAction(224, "Locale Settings", "System", "Open Locale Settings", []),
    226: TaskerAction(226, "App Manage Settings", "System", "Open App Manager Settings", []),
    227: TaskerAction(227, "Memory Card Settings", "System", "Open Memory Card Settings", []),
    228: TaskerAction(228, "Network Operator Settings", "System", "Open Network Operator Settings", []),
    229: TaskerAction(229, "Quick Launch Settings", "System", "Open Quick Launch Settings", []),
    230: TaskerAction(230, "Security Settings", "System", "Open Security Settings", []),
    231: TaskerAction(231, "Search Settings", "System", "Open Search Settings", []),
    232: TaskerAction(232, "Sound Settings", "System", "Open Sound Settings", []),
    234: TaskerAction(234, "Dictionary Settings", "System", "Open Dictionary Settings", []),
    235: TaskerAction(235, "Custom Setting", "System", "Read/write a custom system setting", ["Type", "Name", "Value"]),
    236: TaskerAction(236, "Accessibility Settings", "System", "Open Accessibility Settings", []),
    237: TaskerAction(237, "Notification Listener Settings", "System", "Open Notification Listener Settings", []),
    238: TaskerAction(238, "Privacy Settings", "System", "Open Privacy Settings", []),
    239: TaskerAction(239, "Print Settings", "System", "Open Print Settings", []),
    257: TaskerAction(257, "Power Usage Settings", "System", "Open Power Usage Settings", []),
    337: TaskerAction(337, "Notification Settings", "System", "Open Notification Settings", []),
    338: TaskerAction(338, "Notification Category Info", "System", "Get notification category info", ["App", "Store Result In"]),
    956: TaskerAction(956, "NFC Settings", "System", "Open NFC Settings", []),
    957: TaskerAction(957, "Android Beam Settings", "System", "Open Android Beam Settings", []),
    958: TaskerAction(958, "NFC Payment Settings", "System", "Open NFC Payment Settings", []),
    959: TaskerAction(959, "Dream Settings", "System", "Open Dream/Daydream Settings", []),

    # ─── Zoom (Scene Widget) Category ───
    721: TaskerAction(721, "Zoom Visibility", "Scene", "Show/hide a Zoom element", ["Widget", "Element", "Set"]),
    740: TaskerAction(740, "Zoom Text", "Scene", "Set text of Zoom element", ["Widget", "Element", "Text"]),
    741: TaskerAction(741, "Zoom Text Size", "Scene", "Set text size of Zoom element", ["Widget", "Element", "Size"]),
    742: TaskerAction(742, "Zoom Text Colour", "Scene", "Set text colour of Zoom element", ["Widget", "Element", "Colour"]),
    760: TaskerAction(760, "Zoom Alpha", "Scene", "Set alpha level of Zoom element", ["Widget", "Element", "Alpha"]),
    761: TaskerAction(761, "Zoom Image", "Scene", "Set image of Zoom element", ["Widget", "Element", "Image"]),
    762: TaskerAction(762, "Zoom Colour", "Scene", "Set colour of Zoom element", ["Widget", "Element", "Colour", "End Colour"]),
    793: TaskerAction(793, "Zoom State", "Scene", "Set state of Zoom Switcher element", ["Widget", "Element", "State"]),
    794: TaskerAction(794, "Zoom Position", "Scene", "Set position of Zoom element", ["Widget", "Element", "X", "Y"]),
    795: TaskerAction(795, "Zoom Size", "Scene", "Set size of Zoom element", ["Widget", "Element", "Width", "Height"]),
}
# fmt: on


def get_action_by_code(code: int) -> Optional[TaskerAction]:
    """Get a Tasker action by its numeric code."""
    return TASKER_ACTIONS.get(code)


def get_action_by_name(name: str) -> Optional[TaskerAction]:
    """Get a Tasker action by its exact name (case-insensitive)."""
    name_lower = name.lower()
    for action in TASKER_ACTIONS.values():
        if action.name.lower() == name_lower:
            return action
    return None


def search_actions(
    query: str, category: Optional[str] = None
) -> list[TaskerAction]:
    """Search actions by name/description, optionally filtered by category."""
    query_lower = query.lower()
    results = []
    for action in TASKER_ACTIONS.values():
        if category and action.category.lower() != category.lower():
            continue
        if (
            query_lower in action.name.lower()
            or query_lower in action.description.lower()
        ):
            results.append(action)
    return results
