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


def add_patient(
    user_id: str, password: str, name: str, symptoms: str = "",
    preferences: str = "", users_path: str = "users.json", patient_path: str = "patient_data.json"
):
    """
    Adds a new patient to users.json and patient_data.json.
    Raises ValueError if user_id already exists.
    Returns dict with 'user' and 'patient' keys.
    """
    users_fp = _resolve_data_path(users_path)
    patients_fp = _resolve_data_path(patient_path)

    # Load and update users.json
    try:
        users_data = _load_json_abs(users_fp)
    except Exception:
        users_data = {"users": []}
    users_data.setdefault("users", [])
    if any(u["user_id"] == user_id for u in users_data["users"]):
        raise ValueError("Patient User ID already exists")
    if " " in user_id:
        raise ValueError("Please don't use spaces in Patient User ID")

    new_user = {
        "user_id": user_id,
        "password": password,
        "name": name,
        "role": "Patient"
    }
    users_data["users"].append(new_user)
    with open(users_fp, "w", encoding="utf-8") as f:
        json.dump(users_data, f, ensure_ascii=False, indent=2)

    # Load and update patient_data.json
    try:
        patient_data = _load_json_abs(patients_fp)
    except Exception:
        patient_data = {"patient_data": []}
    patient_data.setdefault("patient_data", [])

    new_patient = {
        "user_id": user_id,
        "password": password,
        "name": name,
        "role": "Patient",
        "symptoms": symptoms,
        "personal_notes":[],
        "preferences": preferences,
        "logs": []
    }
    patient_data["patient_data"].append(new_patient)
    with open(patients_fp, "w", encoding="utf-8") as f:
        json.dump(patient_data, f, ensure_ascii=False, indent=2)

    return {"user": new_user, "patient": new_patient}

def add_staff(
    user_id: str, password: str, name: str,
    role: str = "CareStaff", users_path: str = "users.json"
):
    """
    Adds a new staff member to users.json.
    Raises ValueError if user_id already exists.
    Returns the created user dict.
    """
    users_fp = _resolve_data_path(users_path)

    # Load users
    try:
        users_data = _load_json_abs(users_fp)
    except Exception:
        users_data = {"users": []}
    users_data.setdefault("users", [])
    if any(u["user_id"] == user_id for u in users_data["users"]):
        raise ValueError("user_id already exists")

    new_user = {
        "user_id": user_id,
        "password": password,
        "name": name,
        "role": role
    }
    users_data["users"].append(new_user)
    with open(users_fp, "w", encoding="utf-8") as f:
        json.dump(users_data, f, ensure_ascii=False, indent=2)

    return new_user

def remove_patient(user_id: str, users_path: str = "users.json", patient_path: str = "patient_data.json") -> bool:
    """
    Removes a patient from users.json and patient_data.json.
    Returns True if the patient was found and removed, False otherwise.
    """
    users_fp = _resolve_data_path(users_path)
    patients_fp = _resolve_data_path(patient_path)

    # Remove from users.json 
    try:
        users_data = _load_json_abs(users_fp)
        original_users = users_data.get("users", [])
        updated_users = [u for u in original_users if u.get("user_id") != user_id]
        
        if len(original_users) == len(updated_users):
            return False  # No such user found

        users_data["users"] = updated_users
        with open(users_fp, "w", encoding="utf-8") as f:
            json.dump(users_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        raise RuntimeError(f"Error removing from users.json: {e}")

    # Remove from patient_data.json 
    try:
        patient_data = _load_json_abs(patients_fp)
        original_patients = patient_data.get("patient_data", [])
        updated_patients = [p for p in original_patients if p.get("user_id") != user_id]

        patient_data["patient_data"] = updated_patients
        with open(patients_fp, "w", encoding="utf-8") as f:
            json.dump(patient_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        raise RuntimeError(f"Error removing from patient_data.json: {e}")

    return True

  

def remove_staff(
    user_id: str,
    users_path: str = "users.json"
) -> dict:
    """
    Removes a staff user from users.json by user_id.
    Only removes users with role 'CareStaff' or 'Admin'.
    Returns dict with 'removed_user' if successful.
    Raises ValueError if user_id not found or not a staff member.
    """
    users_fp = _resolve_data_path(users_path)

    try:
        users_data = _load_json_abs(users_fp)
    except Exception:
        raise ValueError("users.json could not be loaded")

    users_data.setdefault("users", [])
    removed_user = None
    updated_users = []

    for user in users_data["users"]:
        if user["user_id"] == user_id:
            if user["role"] in ("CareStaff", "Admin"):
                removed_user = user
                continue
            else:
                raise ValueError(f"user_id '{user_id}' exists but is not a staff member.")
        updated_users.append(user)

    if not removed_user:
        raise ValueError(f"Staff user_id '{user_id}' not found.")

    users_data["users"] = updated_users
    with open(users_fp, "w", encoding="utf-8") as f:
        json.dump(users_data, f, ensure_ascii=False, indent=2)

    return {"removed_user": removed_user}



# ---- Keyword scanning core (single place; used by the UI) --------------------

def _compile_phrase_regex(phrase: str) -> re.Pattern:
    tokens = phrase.strip().split()
    escaped = [re.escape(t) for t in tokens]
    pattern = r"\b" + r"\s+".join(escaped) + r"\b"
    return re.compile(pattern, flags=re.IGNORECASE)

def _coerce_logs_to_strings(logs_obj: Any) -> List[str]:
    """
    Accepts a patient's logs field which may be a list of dicts like
    [{"Log 1": "..."}, {"Log 2": "..."}] or a list of strings.
    Returns a flat list of log strings.
    """
    out: List[str] = []
    if isinstance(logs_obj, list):
        for item in logs_obj:
            if isinstance(item, dict):
                # join all string values from {"Log N": "..."} shape
                vals = [v for v in item.values() if isinstance(v, str)]
                if vals:
                    out.append(" ".join(vals))
            elif isinstance(item, str):
                out.append(item)
    elif isinstance(logs_obj, dict):
        # fallback: join any string values
        vals = [v for v in logs_obj.values() if isinstance(v, str)]
        if vals:
            out.append(" ".join(vals))
    elif isinstance(logs_obj, str):
        out.append(logs_obj)
    return out

def at_risk_patients(
    keywords_path: str = None,
    logs_path: str = None,
    *,
    weights: Dict[str, int] | None = None,
    thresholds: Tuple[int, int] = (4, 8),
    max_snippets_per_patient: int = 8
) -> List[Dict[str, Any]]:
    """
    Scan logs for keywords.
    Supports these sources:
      1) data/logs.json   -> list or {"logs":[...]} or { "<pid>": [ ... ] }
      2) data/patient_data.json -> {"patient_data":[{ user_id, logs:[...] }, ...]}
    Returns per-patient hits sorted by score desc.
    """
    if keywords_path is None:
        keywords_path = _resolve_data_path("keywords.json")
    if logs_path is None:
        # default to patient_data.json (where you actually store the logs)
        logs_path = _resolve_data_path("patient_data.json")

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

    def snippet(text: str, m: re.Match, r: int = 60) -> str:
        s = max(0, m.start() - r); e = min(len(text), m.end() + r)
        return text[s:e].replace("\n", " ").strip()

    def ensure_rec(pid: str) -> Dict[str, Any]:
        return patients.setdefault(pid, {
            "patient_id": pid,
            "score": 0,
            "risk_level": "low",
            "category_counts": {c: 0 for c in compiled.keys()},
            "hits": [],
            "logs_scanned": 0
        })

    def add_hit(pid: str, cat: str, phrase: str, text: str, m: re.Match, raw_index: int):
        rec = ensure_rec(pid)
        rec["category_counts"][cat] += 1
        rec["score"] += max(1, int(weights.get(cat, 1)))
        if len(rec["hits"]) < max_snippets_per_patient:
            rec["hits"].append({
                "category": cat,
                "phrase": phrase,
                "snippet": snippet(text, m),
                "raw_index": raw_index
            })

    # --- Walk source variants ---

    def process_text(pid: str, text: str, raw_index: int):
        if not text:
            return
        for cat, pats in compiled.items():
            for phrase, rx in pats:
                for m in rx.finditer(text):
                    add_hit(pid, cat, phrase, text, m, raw_index)

    if isinstance(logs_data, dict) and any(k in logs_data for k in ("patient_data", "patients")):
        # patient_data.json shape
        patient_list = logs_data.get("patient_data") or logs_data.get("patients") or []
        for p in patient_list:
            if not isinstance(p, dict):
                continue
            pid = str(p.get("user_id") or p.get("id") or p.get("patient_id") or "UNKNOWN")
            texts = _coerce_logs_to_strings(p.get("logs", []))
            for i, t in enumerate(texts):
                process_text(pid, t, i)
                ensure_rec(pid)["logs_scanned"] += 1
    else:
        # logs.json shapes
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

        if isinstance(logs_data, list):
            for i, e in enumerate(logs_data):
                if isinstance(e, dict):
                    process_text(extract_patient_id(e), extract_text(e), i)
                    ensure_rec(extract_patient_id(e))["logs_scanned"] += 1
        elif isinstance(logs_data, dict):
            if "logs" in logs_data and isinstance(logs_data["logs"], list):
                for i, e in enumerate(logs_data["logs"]):
                    if isinstance(e, dict):
                        process_text(extract_patient_id(e), extract_text(e), i)
                        ensure_rec(extract_patient_id(e))["logs_scanned"] += 1
            else:
                for pid, entries in logs_data.items():
                    if isinstance(entries, list):
                        for i, e in enumerate(entries):
                            if isinstance(e, dict):
                                process_text(str(pid), extract_text(e), i)
                                ensure_rec(str(pid))["logs_scanned"] += 1
                    elif isinstance(entries, dict):
                        process_text(str(pid), extract_text(entries), 0)
                        ensure_rec(str(pid))["logs_scanned"] += 1

    # Risk levels
    medium_min, high_min = thresholds
    for rec in patients.values():
        s = rec["score"]
        rec["risk_level"] = "high" if s >= high_min else ("medium" if s >= medium_min else "low")

    return sorted(patients.values(), key=lambda r: (-r["score"], r["patient_id"]))

def get_patient_risk(patient_id: str) -> Dict[str, Any] | None:
    """
    Convenience wrapper: scan patient_data.json (per-patient logs).
    Falls back to logs.json if you later add a centralized log sink.
    """
    # 1) scan per-patient logs
    res_pd = at_risk_patients(logs_path=_resolve_data_path("patient_data.json"))
    # 2) optionally also scan centralized logs.json and keep the higher score
    res_logs = []
    try:
        res_logs = at_risk_patients(logs_path=_resolve_data_path("logs.json"))
    except Exception:
        pass

    best: Dict[str, Any] | None = None
    for r in res_pd + res_logs:
        if r["patient_id"] == str(patient_id):
            if best is None or r["score"] > best["score"]:
                best = r
    return best


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



# --- Recording Patient data Functions-----------------------
def load_all_patients():
    """Loads a Patient by user_id from the json file and returns a Patient object using the corresponding data. Should use patient_data.json"""
    with open("data/patient_data.json", "r") as f:
        data = json.load(f)

        patients = [Patient(**p) for p in data["patient_data"]]

        return patients



def save_patient_data(patients):
    """Saves all patient objects back to the JSON file."""
    data = {"patient_data": [p.__dict__ for p in patients]}
    with open("data/patient_data.json", "w") as f:
        json.dump(data, f, indent=4)


def submit_patient_log(patient_id, log_info):
    if log_info == "":
        return False
    patient_data = load_all_patients()
    for p in patient_data:
        if p.user_id == patient_id:
            log_num = len(p.logs) + 1
            log = {f"Log {log_num}":  log_info}
            p.logs.append(log)
            save_patient_data(patient_data)
            return True
    
    else:
        return False
            

def update_patient_preferences(patient_id, patient_preference):
    if patient_preference == "":
        return False
    patient_data = load_all_patients()
    for p in patient_data:
        if p.user_id == patient_id:
            if p.preferences != "":
                previous_preferences = p.preferences
                p.preferences = f"{previous_preferences}, {patient_preference}"
            else:
                p.preferences = f"{patient_preference}"
            save_patient_data(patient_data)
            return True
    
    else:
        return False

    


def update_patient_symptoms(patient_id, symptoms): 
    if symptoms == "":
        return False 
    patient_data = load_all_patients()
    for p in patient_data:
        if p.user_id == patient_id:
            p.symptoms = f"{symptoms}"
            save_patient_data(patient_data)
            return True 
        
    else:
        return False
    

def update_patient_personal_note(patient_id, personal_note):
    if personal_note == "":
        return False 
    patient_data = load_all_patients()
    for p in patient_data:
        if p.user_id == patient_id:
            note_num = len(p.personal_notes) + 1
            note = {f"Note {note_num}":  personal_note}
            p.personal_notes.append(note)
            save_patient_data(patient_data)
            return True
    
    else:
        return False


