# ----------------Actionable Event Router-----------------

#Filter out non-actionable IIoT events and transform the remaining ones into a unified 
# structure ready for storage/dashboarding. Practice map + filter + lambda pipelines.

print(f"\nExercise: lambda + map + filter -> Actionable Event Router.\n")
#input data:
events: list[dict] = [
    {"ts": 1700000001, "topic": "site1/line1/cell1/temp",  "value": "21.2"},
    {"ts": 1700000002, "topic": "site1/line1/cell1/temp",  "value": None},
    {"ts": 1700000003, "topic": "site1/line1/cell1/alarm", "value": {"code": "HI_TEMP",   "sev": 3}},
    {"ts": 1690000000, "topic": "site1/line1/cell1/temp",  "value": "22.0"},  # stale
    {"ts": 1700000004, "topic": "site1/line1/cell1/alarm", "value": {"code": "INFO_ONLY", "sev": 1}},
]
now_ts: int = 1700000100

# Rules:
# - Drop stale events: discard if (now_ts - ts) > 300
# - Telemetry is actionable if value is convertible to float
# - Alarms are actionable if value is a dict and sev >= 2
""" 
Transform each accepted event into this unified dict:
{
  "ts": <int>,
  "type": "telemetry" or "alarm",
  "key": <topic string>,
  "value": <float for telemetry OR alarm code string>,
  "severity": <int for alarms OR None for telemetry>
}
"""

#Defining  helpers funcs:

def to_float_or_none(val: object) -> float | None:
    """Return float(val) if possible; otherwise return None.
    """
    if isinstance(val, str):
        val = val.strip()
    try:
        return float(val)
    except (TypeError, ValueError):
        return None
    

def is_stale_event(event: dict, now_ts: int, max_diff: int = 300) -> bool:
    """Return True if the event timestamp is older than max_diff seconds."""
    return (now_ts - event["ts"]) > max_diff 


def is_actionable(event: dict) -> bool:
    """Return True for actionable telemetry (float-convertible) or alarms (sev >= 2)."""
    topic: str = event.get("topic", "") 
    #if "topic" is missing, return "" instead of None. This because None  crahs the .endswith(). 
    value = event. get("value")

    # Alarm events
    if topic.endswith("/alarm"):
        if not isinstance(value, dict):
            return False
        sev = value.get("sev", 0)
        return sev >= 2

    # Telemetry events
    if to_float_or_none(value) is None:
        return False
    return True


#Remove stale events and keep the good ones:
good_events  = list(filter(lambda e: not is_stale_event(e, now_ts), events))
print(f"Good events:\n {good_events}")

#From the good events, keep only actionable:
actionable_events = list(filter(lambda e: is_actionable(e), good_events))
print(f"Actionable events:\n{actionable_events}")

#Using map() to transform each actionable event into the unified dict:
transformed_events = list(map(lambda x: {
    "ts": x["ts"],
    "type": "alarm" if (x["topic"].endswith("/alarm")) else "telemetry", 
    "key": x["topic"],
    "value": x["value"]["code"] if (x["topic"].endswith("/alarm")) else float(x["value"]),
    "severity": x["value"]["sev"] if (x["topic"].endswith("/alarm")) else None

}, actionable_events))

print(f"Transformed events:\n {transformed_events}")