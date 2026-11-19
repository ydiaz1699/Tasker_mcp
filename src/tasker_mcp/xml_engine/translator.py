"""Tasker XML Translation & Localization Engine.

Enables safe extraction, translation, and verification of user-facing
strings in Tasker projects, profiles, and tasks without breaking internal logic
(task names, variable names, HTTP calls, or code tags).
"""

import re
import xml.etree.ElementTree as ET
from typing import Any, Optional


# Actions that contain user-facing strings (Alerts, Dialogs, Voice, etc.)
USER_FACING_ACTIONS: dict[int, dict[str, str]] = {
    548: {"arg0": "Flash Text", "arg3": "Flash Title"},
    523: {"arg1": "Notification Title", "arg2": "Notification Text"},
    559: {"arg0": "Say Text", "arg1": "TTS Engine/Locale"},
    360: {"arg1": "Input Dialog Title", "arg2": "Input Dialog Text"},
    538: {"arg1": "Text Dialog Title", "arg2": "Text Dialog Text"},
    539: {"arg1": "List Dialog Title", "arg2": "List Dialog Text"},
    377: {"arg1": "Set Clipboard Text"},
    41: {"arg1": "Send SMS Message"},
}


class TaskerXMLTranslator:
    """Manages extraction, application, and safety verification of translations in Tasker XML."""

    @staticmethod
    def extract_strings(xml_content: str) -> list[dict[str, Any]]:
        """Extract all translatable user-facing strings from a Tasker XML.

        Identifies dialog titles, notification messages, flash alerts, TTS texts,
        share descriptions, and project variable default values.

        Returns:
            List of translatable items with unique ID, context, and original text.
        """
        root = ET.fromstring(xml_content)
        items: list[dict[str, Any]] = []

        # 1. Project level metadata and Share description
        project = root.find("Project")
        if project is not None:
            proj_name = project.findtext("name", "Project")
            share_d = project.find(".//Share/d")
            if share_d is not None and share_d.text and share_d.text.strip():
                items.append({
                    "id": "proj:Share:d",
                    "location": f"Project '{proj_name}' > Share Description",
                    "field": "description",
                    "original": share_d.text,
                    "type": "description",
                })

            # ProfileVariables (Project Variables)
            for pv in project.findall("ProfileVariable"):
                pvid = pv.findtext("pvid", "0")
                pvn = pv.findtext("pvn", "%var")
                pvd = pv.find("pvd")
                if pvd is not None and pvd.text and pvd.text.strip():
                    items.append({
                        "id": f"proj:pv:{pvn}:pvd",
                        "location": f"Project Variable '{pvn}' > Description",
                        "field": "pvd",
                        "original": pvd.text,
                        "type": "variable_description",
                    })
                pvv = pv.find("pvv")
                if pvv is not None and pvv.text and pvv.text.strip():
                    # Check if pvv is a human text (not just numbers/codes)
                    if any(c.isalpha() for c in pvv.text) and not pvv.text.startswith("%"):
                        items.append({
                            "id": f"proj:pv:{pvn}:pvv",
                            "location": f"Project Variable '{pvn}' > Default Value",
                            "field": "pvv",
                            "original": pvv.text,
                            "type": "variable_default_value",
                        })

        # 2. Tasks and Actions
        for task in root.findall("Task"):
            task_id = task.findtext("id", "0")
            task_name = task.findtext("nme", f"Task_{task_id}")
            actions = task.findall("Action")

            for act_idx, action in enumerate(actions):
                code_elem = action.find("code")
                if code_elem is None or not code_elem.text:
                    continue
                try:
                    code = int(code_elem.text)
                except ValueError:
                    continue

                # Check known user-facing action fields
                if code in USER_FACING_ACTIONS:
                    field_specs = USER_FACING_ACTIONS[code]
                    for str_el in action.findall("Str"):
                        sr = str_el.get("sr")
                        text = str_el.text
                        if sr in field_specs and text and text.strip():
                            # For code 559 (Say), arg1 is TTS engine locale
                            is_tts_engine = (code == 559 and sr == "arg1")
                            items.append({
                                "id": f"task:{task_id}:act:{act_idx}:{sr}",
                                "location": f"Task '{task_name}' > Action #{act_idx} (Code {code})",
                                "field": sr,
                                "field_name": field_specs[sr],
                                "original": text,
                                "type": "tts_engine" if is_tts_engine else "user_text",
                            })

                # Check Variable Set (code 547) for user messages/prompts
                elif code == 547:
                    var_name = ""
                    var_val = ""
                    for s in action.findall("Str"):
                        if s.get("sr") == "arg0":
                            var_name = s.text or ""
                        elif s.get("sr") == "arg1":
                            var_val = s.text or ""

                    # If the value contains spaces and letters, and is not a pure formula/variable
                    if var_val and any(c.isalpha() for c in var_val) and " " in var_val and not var_val.startswith("%"):
                        items.append({
                            "id": f"task:{task_id}:act:{act_idx}:arg1",
                            "location": f"Task '{task_name}' > Action #{act_idx} (Variable Set {var_name})",
                            "field": "arg1",
                            "field_name": f"Value for {var_name}",
                            "original": var_val,
                            "type": "variable_message",
                        })

        return items

    @staticmethod
    def apply_translations(
        xml_content: str,
        translations: dict[str, str],
        tts_locale: Optional[str] = None,
    ) -> str:
        """Apply a mapping of translations to the Tasker XML string.

        Args:
            xml_content: The original Tasker XML string.
            translations: Mapping of {id_or_original_text: translated_text}.
            tts_locale: Optional TTS engine locale (e.g., 'com.google.android.tts:spa-MEX').
                        If given, updates all Say (code 559) actions to use this locale.

        Returns:
            Updated valid Tasker XML string.
        """
        root = ET.fromstring(xml_content)

        # 1. Project Share description
        project = root.find("Project")
        if project is not None:
            share_d = project.find(".//Share/d")
            if share_d is not None and share_d.text:
                new_text = translations.get("proj:Share:d") or translations.get(share_d.text)
                if new_text:
                    share_d.text = new_text

            # ProfileVariables
            for pv in project.findall("ProfileVariable"):
                pvn = pv.findtext("pvn", "")
                pvd = pv.find("pvd")
                if pvd is not None and pvd.text:
                    key = f"proj:pv:{pvn}:pvd"
                    new_val = translations.get(key) or translations.get(pvd.text)
                    if new_val:
                        pvd.text = new_val

                pvv = pv.find("pvv")
                if pvv is not None and pvv.text:
                    key = f"proj:pv:{pvn}:pvv"
                    new_val = translations.get(key) or translations.get(pvv.text)
                    if new_val:
                        pvv.text = new_val

        # 2. Tasks and Actions
        for task in root.findall("Task"):
            task_id = task.findtext("id", "0")
            for act_idx, action in enumerate(task.findall("Action")):
                code_elem = action.find("code")
                if code_elem is None or not code_elem.text:
                    continue
                try:
                    code = int(code_elem.text)
                except ValueError:
                    continue

                for str_el in action.findall("Str"):
                    sr = str_el.get("sr")
                    text = str_el.text
                    if not sr or not text:
                        continue

                    # Update TTS engine if provided
                    if code == 559 and sr == "arg1" and tts_locale:
                        str_el.text = tts_locale
                        continue

                    # Lookup by locator ID or original text
                    loc_id = f"task:{task_id}:act:{act_idx}:{sr}"
                    new_text = translations.get(loc_id) or translations.get(text)
                    if new_text:
                        str_el.text = new_text

        return ET.tostring(root, encoding="utf-8").decode("utf-8")

    @staticmethod
    def compare_xmls(orig_xml: str, trans_xml: str) -> dict[str, Any]:
        """Perform a safety audit comparing an original and translated Tasker XML.

        Verifies that task names, variable references, and action codes were preserved,
        and lists all user-facing changes vs any unintended logic regressions.
        """
        root_orig = ET.fromstring(orig_xml)
        root_trans = ET.fromstring(trans_xml)

        tasks_orig = {t.findtext("nme", f"Task_{t.findtext('id', i)}"): t for i, t in enumerate(root_orig.findall("Task"))}
        tasks_trans = {t.findtext("nme", f"Task_{t.findtext('id', i)}"): t for i, t in enumerate(root_trans.findall("Task"))}

        report: dict[str, Any] = {
            "is_safe": True,
            "tasks_count_orig": len(tasks_orig),
            "tasks_count_trans": len(tasks_trans),
            "renamed_tasks": [],
            "action_differences": [],
            "condition_changes": [],
            "translated_strings": [],
            "warnings": [],
        }

        # Check if tasks were renamed (which breaks Perform Task calls)
        missing_tasks = set(tasks_orig.keys()) - set(tasks_trans.keys())
        added_tasks = set(tasks_trans.keys()) - set(tasks_orig.keys())
        if missing_tasks or added_tasks:
            report["is_safe"] = False
            report["renamed_tasks"] = {"missing": list(missing_tasks), "added": list(added_tasks)}
            report["warnings"].append(
                "Task names were modified! In Tasker, 'Perform Task' references tasks by name. "
                "Renaming tasks can cause runtime failures."
            )

        # Inspect common tasks
        common_tasks = set(tasks_orig.keys()) & set(tasks_trans.keys())
        for tname in common_tasks:
            acts_orig = tasks_orig[tname].findall("Action")
            acts_trans = tasks_trans[tname].findall("Action")

            if len(acts_orig) != len(acts_trans):
                report["warnings"].append(f"Task '{tname}' has different action counts ({len(acts_orig)} vs {len(acts_trans)}).")
                continue

            for idx, (a_o, a_t) in enumerate(zip(acts_orig, acts_trans)):
                c_o = a_o.findtext("code", "")
                c_t = a_t.findtext("code", "")

                if c_o != c_t:
                    report["is_safe"] = False
                    report["warnings"].append(f"Action code mismatch in '{tname}' action #{idx}: {c_o} vs {c_t}")
                    continue

                # Compare string fields
                strs_o = {s.get("sr"): s.text for s in a_o.findall("Str")}
                strs_t = {s.get("sr"): s.text for s in a_t.findall("Str")}

                for k in set(strs_o.keys()) | set(strs_t.keys()):
                    vo = strs_o.get(k)
                    vt = strs_t.get(k)
                    if vo != vt:
                        report["translated_strings"].append({
                            "task": tname,
                            "action_idx": idx,
                            "code": c_o,
                            "field": k,
                            "original": vo,
                            "translated": vt,
                        })

                # Check conditions
                conds_o = [(c.findtext("lhs"), c.findtext("op"), c.findtext("rhs")) for c in a_o.findall(".//Condition")]
                conds_t = [(c.findtext("lhs"), c.findtext("op"), c.findtext("rhs")) for c in a_t.findall(".//Condition")]
                if conds_o != conds_t:
                    report["condition_changes"].append({
                        "task": tname,
                        "action_idx": idx,
                        "orig_condition": conds_o,
                        "trans_condition": conds_t,
                    })

        return report
