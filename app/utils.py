# "Utility" file for functions. We can organise functions better in other files or even classes later on
import json
from app.user import User
from app.patient import Patient
import os
import re
import uuid
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime, timezone

def test_function():
    print("function is working!")


class TestClass:
    """If you are seeing this message in streamlit, it means class imports are working"""
    def __init__(self, field):
        self.field = field


def load_user(user_id, data_file):
    """Loads a user by user_id from the json file and returns a User object using the corresponding data. Should use users.json"""
    with open(data_file, "r") as f:
        data = json.load(f)

    for user_data in data["users"]:
        if user_data["user_id"] == user_id:
            return User(**user_data)          

def load_patient(user_id, data_file):
    """Loads a Patient by user_id from the json file and returns a Patient object using the corresponding data. Should use patient_data.json"""
    with open(data_file, "r") as f:
        data = json.load(f)

    for patient_data in data["patient_data"]:
        if patient_data["user_id"] == user_id:
            return Patient(**patient_data)

def _resolve_data_path(relative_path: str) -> str:
    here = os.path.dirname(__file__)
    return os.path.abspath(os.path.join(here, "..", "data", relative_path))

def _load_json_abs(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def list_patients(data_file: str = "data/patient_data.json") -> List[Dict[str, Any]]:
    """
    Returns a flat list of patient dicts (best-effort fields: user_id, name, age, gender).
    Works whether patient_data.json is {"patient_data":[...]}, {"patients":[...]}, or a list.
    """
    data = _load_json_abs(data_file)
    rows = []
    raw = data
    if isinstance(data, dict):
        for key in ("patient_data", "patients", "items", "rows"):
            if key in data and isinstance(data[key], list):
                raw = data[key]
                break
    if isinstance(raw, list):
        for p in raw:
            if isinstance(p, dict):
                rows.append(p)
    return rows

# ---- Keyword scanning core (single place; used by the UI) --------------------

def _compile_phrase_regex(phrase: str) -> re.Pattern:
    tokens = phrase.strip().split()
    escaped = [re.escape(t) for t in tokens]
    pattern = r"\b" + r"\s+".join(escaped) + r"\b"
    return re.compile(pattern, flags=re.IGNORECASE)

def at_risk_patients(
    keywords_path: str = None,
    logs_path: str = None,
    *,
    weights: Dict[str, int] | None = None,
    thresholds: Tuple[int, int] = (4, 8),
    max_snippets_per_patient: int = 8
) -> List[Dict[str, Any]]:
    """
    Scan logs.json for keywords.json; return per-patient hits sorted by score desc.
    Each result:
      { patient_id, score, risk_level, category_counts, hits[{category, phrase, snippet}], logs_scanned }
    """
    if keywords_path is None:
        keywords_path = _resolve_data_path("keywords.json")
    if logs_path is None:
        logs_path = _resolve_data_path("logs.json")

    if weights is None:
        weights = {
            "emotional_distress": 2,
            "health_concerns": 3,
            "medication_issues": 3,
            "behavioural_flags": 1,
            "confusion_or_cognitive": 3,
            "environmental_or_safety": 4,
            "suicidal_or_crisis": 5,
        }

    keywords_data = _load_json_abs(keywords_path)
    logs_data = _load_json_abs(logs_path)

    compiled: Dict[str, List[Tuple[str, re.Pattern]]] = {}
    for category, phrases in keywords_data.items():
        if isinstance(phrases, list):
            compiled[category] = [(p, _compile_phrase_regex(p)) for p in phrases]

    patients: Dict[str, Dict[str, Any]] = {}

    def extract_patient_id(entry: Dict[str, Any]) -> str:
        for k in ("patient_id", "patientId", "patient", "user_id", "userId", "id"):
            if k in entry and isinstance(entry[k], (str, int)):
                return str(entry[k])
        return "UNKNOWN"

    def extract_text(entry: Dict[str, Any]) -> str:
        for k in ("text","note","notes","message","entry","log","content","observation","summary","complaint","body","comment"):
            if k in entry and isinstance(entry[k], str):
                return entry[k]
        parts: List[str] = []
        for v in entry.values():
            if isinstance(v, str):
                parts.append(v)
            elif isinstance(v, list):
                parts.extend([x for x in v if isinstance(x, str)])
        return " ".join(parts)

    def snippet(text: str, m: re.Match, r: int = 60) -> str:
        s = max(0, m.start() - r); e = min(len(text), m.end() + r)
        return text[s:e].replace("\n", " ").strip()

    def hit(pid: str, cat: str, phrase: str, text: str, m: re.Match, raw_index: int):
        rec = patients.setdefault(pid, {
            "patient_id": pid,
            "score": 0,
            "risk_level": "low",
            "category_counts": {c: 0 for c in compiled.keys()},
            "hits": [],
            "logs_scanned": 0
        })
        rec["category_counts"][cat] += 1
        rec["score"] += max(1, int(weights.get(cat, 1)))
        if len(rec["hits"]) < max_snippets_per_patient:
            rec["hits"].append({"category": cat, "phrase": phrase, "snippet": snippet(text, m), "raw_index": raw_index})

    def process_entry(entry: Dict[str, Any], forced_pid: str | None = None, raw_index: int = -1):
        pid = forced_pid or extract_patient_id(entry)
        text = extract_text(entry)
        if not text:
            return
        for cat, pats in compiled.items():
            for phrase, rx in pats:
                for m in rx.finditer(text):
                    hit(pid, cat, phrase, text, m, raw_index)

    # Walk logs.json (supports lists, {"logs":[...]}, or {pid: [ ... ]})
    if isinstance(logs_data, list):
        for i, e in enumerate(logs_data):
            if isinstance(e, dict):
                process_entry(e, raw_index=i)
    elif isinstance(logs_data, dict):
        if "logs" in logs_data and isinstance(logs_data["logs"], list):
            for i, e in enumerate(logs_data["logs"]):
                if isinstance(e, dict):
                    process_entry(e, raw_index=i)
        else:
            for pid, entries in logs_data.items():
                if isinstance(entries, list):
                    for i, e in enumerate(entries):
                        if isinstance(e, dict):
                            process_entry(e, forced_pid=str(pid), raw_index=i)
                elif isinstance(entries, dict):
                    process_entry(entries, forced_pid=str(pid), raw_index=0)

    medium_min, high_min = thresholds
    for rec in patients.values():
        uniq = {h["raw_index"] for h in rec["hits"] if isinstance(h["raw_index"], int) and h["raw_index"] >= 0}
        rec["logs_scanned"] = max(rec["logs_scanned"], len(uniq))
        s = rec["score"]
        rec["risk_level"] = "high" if s >= high_min else ("medium" if s >= medium_min else "low")

    return sorted(patients.values(), key=lambda r: (-r["score"], r["patient_id"]))

def get_patient_risk(patient_id: str) -> Dict[str, Any] | None:
    """Convenience wrapper: return the single patient’s record (or None)."""
    results = at_risk_patients()
    for r in results:
        if r["patient_id"] == str(patient_id):
            return r
    return None

# --- Nurse Call / Alerts ------------------------------------------------------

_ALERTS_FILE = None

def _resolve_data_path(relative_path: str) -> str:
    """Resolve a path inside ../data relative to this file."""
    here = os.path.dirname(__file__)
    return os.path.abspath(os.path.join(here, "..", "data", relative_path))

def _alerts_path() -> str:
    global _ALERTS_FILE
    if _ALERTS_FILE is None:
        _ALERTS_FILE = _resolve_data_path("alerts.json")
    return _ALERTS_FILE

def _load_alerts() -> Dict[str, Any]:
    """Returns {'alerts': [...]} and creates the file if missing."""
    path = _alerts_path()
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"alerts": []}, f, ensure_ascii=False, indent=2)
        return {"alerts": []}
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        if not isinstance(data, dict) or "alerts" not in data or not isinstance(data["alerts"], list):
            data = {"alerts": []}
    return data

def _save_alerts(data: Dict[str, Any]) -> None:
    with open(_alerts_path(), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def create_help_alert(
    patient_id: str,
    patient_name: str,
    *,
    room: Optional[str] = None,
    priority: str = "normal",
    source: str = "patient_dashboard"
) -> Dict[str, Any]:
    """
    Create a new nurse-call alert and persist it to alerts.json.
    Returns the created alert dict.
    """
    now = datetime.now(timezone.utc).isoformat()
    alert = {
        "id": str(uuid.uuid4()),
        "timestamp": now,
        "status": "open",                # open -> acknowledged -> resolved
        "priority": priority,
        "source": source,
        "patient_id": str(patient_id),
        "patient_name": patient_name,
        "room": room or "",
        "ack_by": None,
        "ack_time": None,
        "resolved_by": None,
        "resolved_time": None,
        "notes": "",
        "kind": "nurse_call"
    }
    data = _load_alerts()
    data["alerts"].append(alert)
    _save_alerts(data)
    return alert

def list_alerts(status: Optional[str] = None) -> List[Dict[str, Any]]:
    """List alerts (optionally filter by status), newest first."""
    alerts = _load_alerts()["alerts"]
    if status:
        alerts = [a for a in alerts if a.get("status") == status]
    return sorted(alerts, key=lambda a: a.get("timestamp", ""), reverse=True)

def acknowledge_alert(alert_id: str, staff_id: Optional[str] = None, staff_name: str = "") -> bool:
    """Mark an alert as acknowledged. Returns True if updated."""
    data = _load_alerts()
    for a in data["alerts"]:
        if a.get("id") == alert_id and a.get("status") == "open":
            a["status"] = "acknowledged"
            a["ack_by"] = staff_name or staff_id or ""
            a["ack_time"] = datetime.now(timezone.utc).isoformat()
            _save_alerts(data)
            return True
    return False

def resolve_alert(alert_id: str, staff_id: Optional[str] = None, staff_name: str = "", notes: str = "") -> bool:
    """Mark an alert as resolved. Returns True if updated."""
    data = _load_alerts()
    for a in data["alerts"]:
        if a.get("id") == alert_id and a.get("status") in ("open", "acknowledged"):
            a["status"] = "resolved"
            a["resolved_by"] = staff_name or staff_id or ""
            a["resolved_time"] = datetime.now(timezone.utc).isoformat()
            if notes:
                a["notes"] = notes
            _save_alerts(data)
            return True
    return False

# --- Staff Alert (call staff to a room) --------------------------------------
def list_staff(data_file: str = None) -> List[Dict[str, Any]]:
    """
    Returns a flat list of staff dicts with best-effort fields: user_id, name, role, on_duty.
    Looks in ../data/staff_data.json by default. If file missing/invalid, returns [].
    """
    if data_file is None:
        data_file = _resolve_data_path("staff_data.json")
    try:
        with open(data_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return []
    except Exception:
        return []

    rows = []
    raw = data
    if isinstance(data, dict):
        for key in ("staff", "on_duty", "items", "rows"):
            if key in data and isinstance(data[key], list):
                raw = data[key]
                break
    if isinstance(raw, list):
        for s in raw:
            if isinstance(s, dict):
                rows.append(s)
    return rows

def create_staff_alert(
    *,
    raised_by_id: str,
    raised_by_name: str,
    room: str,
    message: str = "",
    priority: str = "urgent",
    target_staff_ids: Optional[List[str]] = None,
    target_roles: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Create an alert to call on-duty staff to a room.
    Stores in alerts.json with kind='staff_alert'.
    If target_staff_ids/target_roles are empty, treat as broadcast to all on-duty staff.
    """
    now = datetime.now(timezone.utc).isoformat()
    alert = {
        "id": str(uuid.uuid4()),
        "kind": "staff_alert",           # <— distinguishes from patient nurse-call
        "timestamp": now,
        "status": "open",                # open -> acknowledged -> resolved
        "priority": priority,
        "source": "carestaff_dashboard",
        "room": room,
        "message": message,
        "raised_by_id": str(raised_by_id),
        "raised_by_name": raised_by_name,
        "to_staff_ids": target_staff_ids or [],
        "to_roles": target_roles or [],
        # kept for compatibility with your table (may be empty for staff alerts)
        "patient_id": "",
        "patient_name": "",
        "ack_by": None,
        "ack_time": None,
        "resolved_by": None,
        "resolved_time": None,
        "notes": ""
    }
    data = _load_alerts()
    data["alerts"].append(alert)
    _save_alerts(data)
    return alert
