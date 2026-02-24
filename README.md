# Python exercises with IIoT focus (public)

Selected Python exercises inspired by Industrial IoT (IIoT) patterns: MQTT/UNS-style naming, alarm routing, signal validation, and KPI calculations.
The goal of this repo is **clarity + realistic plant logic**, not building a big framework.

## Featured Exercises (progressive difficulty)

### 1) `ex_funcs_iiot.py`
Function-based exercises with an IIoT mindset:
- Type hints (basic), runtime checks, dicts, `**kwargs`
- MQTT/UNS-style topic building
- Report generation with dynamic keys (`approved_*`, `rejected_*`)
- Scrap rate calculation
- Alarm routing logic with practical runtime checks

### 2) `ex_mqtt_topic_normalizer.py`
**MQTT Topic Normalizer** (dirty input → clean UNS-style topic):
- Split topics into segments
- Normalize segments (strip/lower/space → `_`)
- Remove invalid segments (e.g. empty segments caused by `//`)
- Validate the final structure (`site/line/cell/tag`) and allowed tags

✅ This exercise uses a full **pipeline** approach with `map` + `lambda` + `filter` for progressive improvement in data processing style.

### 3) `ex_actionable_event_router.py`
**Actionable Event Router** (events → unified structure):
- Drop stale events (time-based filtering)
- Keep only actionable events:
  - telemetry: value convertible to `float`
  - alarms: dict payload with `sev >= 2`
- Transform accepted events into a unified dict (ready for storage / dashboards)

✅ Also built using **pipelines** (`map` + `filter` + `lambda`) to keep the logic explicit and easy to reason about.

### 4) `ex_map_lambda_kpi.py`
A more robust data pipeline that:
- Uses `map` + `lambda` to transform process variables (including unit conversion and type validation)
- Validates sensor values (avoids issues like `bool` behaving like `int`)
- Calculates scrap percentage and triggers alarms (e.g., HIGH_SCRAP)
- Handles edge cases such as zero production (avoids `ZeroDivisionError`)


## How to run

Python 3.10+ recommended. No external dependencies.

python ex_funcs_iiot.py
python ex_mqtt_topic_normalizer.py
python ex_actionable_event_router.py
python ex_map_lambda_kpi.py



### Why this repo

This repository is a learning log and a small portfolio showcase focused on:
- clean Python fundamentals
- realistic IIoT data handling
- Consistent naming (MQTT / UNS-like conventions)
- Practical validation and robustness for “messy real-world data”

### Notes

These are standalone exercises/scripts (not a package).
The emphasis is on readable, practical code that scales in complexity over time.
