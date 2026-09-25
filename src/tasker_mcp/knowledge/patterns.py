"""Common Tasker Automation Patterns.

Pre-built automation patterns that serve as templates for common use cases.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class AutomationPattern:
    """Represents a common Tasker automation pattern/template."""

    id: str
    name: str
    description: str
    category: str
    profile_type: str  # event, state, time
    trigger_codes: list[int] = field(default_factory=list)
    action_codes: list[int] = field(default_factory=list)
    variables_used: list[str] = field(default_factory=list)
    example_description: str = ""


# fmt: off
AUTOMATION_PATTERNS: dict[str, AutomationPattern] = {
    "battery_saver": AutomationPattern(
        id="battery_saver",
        name="Battery Saver",
        description="Automatically enable power-saving measures when battery is low",
        category="Power",
        profile_type="state",
        trigger_codes=[140],  # Battery Level state
        action_codes=[425, 433, 294, 810, 333],  # WiFi Off, Mobile Data Off, BT Off, Brightness Low, Airplane
        variables_used=["%BATT", "%SCREEN"],
        example_description="When battery drops below 20%, disable WiFi, reduce brightness to 50, and disable Bluetooth. Restore when charging.",
    ),
    "silent_at_work": AutomationPattern(
        id="silent_at_work",
        name="Silent at Work",
        description="Automatically mute phone when arriving at work location or during work hours",
        category="Location/Time",
        profile_type="state",
        trigger_codes=[170, 160],  # Wifi Near, Wifi Connected
        action_codes=[310, 304, 305, 312],  # Vibrate Mode, Ringer Volume, Notification Volume, DND
        variables_used=["%WIFI", "%TIME", "%LOC"],
        example_description="When connected to work WiFi network, set phone to vibrate mode and enable Do Not Disturb. Restore on disconnect.",
    ),

    "wifi_at_home": AutomationPattern(
        id="wifi_at_home",
        name="WiFi at Home",
        description="Automatically enable WiFi when arriving home and disable when leaving",
        category="Location",
        profile_type="state",
        trigger_codes=[7],  # Cell Near state
        action_codes=[425],  # WiFi
        variables_used=["%WIFII", "%CELLID"],
        example_description="When near home cell tower(s), enable WiFi. When leaving, disable WiFi to save battery.",
    ),
    "morning_routine": AutomationPattern(
        id="morning_routine",
        name="Morning Routine",
        description="Execute a series of actions at a specified morning time",
        category="Time",
        profile_type="time",
        trigger_codes=[],  # Time context (no event code, uses time range)
        action_codes=[810, 304, 305, 425, 559, 548],  # Brightness, Ringer Vol, Notif Vol, WiFi, Say, Flash
        variables_used=["%TIME", "%DATE", "%BATT"],
        example_description="At 7:00 AM on weekdays: set brightness to 80%, ringer volume high, enable WiFi, and announce today's weather.",
    ),
    "auto_reply_sms": AutomationPattern(
        id="auto_reply_sms",
        name="Auto Reply SMS",
        description="Automatically reply to incoming SMS when busy or driving",
        category="Communication",
        profile_type="event",
        trigger_codes=[7],  # Received Text event
        action_codes=[41, 548],  # Send SMS, Flash
        variables_used=["%SMSRF", "%SMSRB", "%SMSRN"],
        example_description="When SMS received while in a call or driving: auto-reply with 'I'm busy right now, will call back soon.' Flash notification.",
    ),
    "shake_flashlight": AutomationPattern(
        id="shake_flashlight",
        name="Shake Flashlight",
        description="Toggle flashlight/torch by shaking the device",
        category="Gesture",
        profile_type="event",
        trigger_codes=[3001],  # Shake event
        action_codes=[511],  # Torch
        variables_used=["%SCREEN"],
        example_description="When device is shaken (while screen is off), toggle the camera flashlight. Use vibrate to confirm.",
    ),

    "notification_on_connect": AutomationPattern(
        id="notification_on_connect",
        name="Notification on BT Connect",
        description="Show notification or perform action when a Bluetooth device connects",
        category="Connectivity",
        profile_type="state",
        trigger_codes=[3],  # BT Connected state
        action_codes=[523, 548, 307],  # Notify, Flash, Media Volume
        variables_used=["%BLUE", "%BTSTATUS"],
        example_description="When Bluetooth headphones connect: set media volume to 10, show notification with device name. On disconnect, reduce volume.",
    ),
    "http_request_pattern": AutomationPattern(
        id="http_request_pattern",
        name="HTTP Request Pattern",
        description="Make HTTP requests to APIs and process the response",
        category="Network",
        profile_type="event",
        trigger_codes=[],  # Can be triggered by various events
        action_codes=[339, 547, 548, 129],  # HTTP Request, Variable Set, Flash, JavaScriptlet
        variables_used=["%HTTPD", "%HTTPR", "%WIFI"],
        example_description="Make HTTP GET request to a weather API, parse JSON response with JavaScriptlet, flash current temperature.",
    ),
    "geofence_action": AutomationPattern(
        id="geofence_action",
        name="Geofence Action",
        description="Trigger actions when entering or leaving a geographic area",
        category="Location",
        profile_type="state",
        trigger_codes=[7, 170],  # Cell Near, Wifi Near
        action_codes=[547, 548, 523, 425, 310],  # Variable Set, Flash, Notify, WiFi, Vibrate Mode
        variables_used=["%LOC", "%LOCACC", "%CELLID", "%WIFII"],
        example_description="When entering home geofence (Cell Near + WiFi Near): enable WiFi, set ringer to normal, notify arrival. Reverse on exit.",
    ),
    "app_launch_action": AutomationPattern(
        id="app_launch_action",
        name="App Launch Action",
        description="Perform specific actions when a particular app is launched",
        category="App",
        profile_type="state",
        trigger_codes=[],  # Application context (no event code)
        action_codes=[822, 810, 312, 307, 308],  # AutoRotate, Brightness, DND, Media Volume, System Volume
        variables_used=["%WIN", "%LAPP", "%SCREEN"],
        example_description="When YouTube launches: enable auto-rotate, max brightness, max media volume. Restore all when exiting.",
    ),
}
# fmt: on


def get_pattern_by_id(pattern_id: str) -> Optional[AutomationPattern]:
    """Get an automation pattern by its ID."""
    return AUTOMATION_PATTERNS.get(pattern_id)


def search_patterns(query: str) -> list[AutomationPattern]:
    """Search patterns by name, description, or category."""
    query_lower = query.lower()
    results = []
    for pattern in AUTOMATION_PATTERNS.values():
        if (
            query_lower in pattern.name.lower()
            or query_lower in pattern.description.lower()
            or query_lower in pattern.category.lower()
            or query_lower in pattern.example_description.lower()
        ):
            results.append(pattern)
    return results
