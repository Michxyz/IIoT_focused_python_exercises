# Python exercises with IIoT focus (public)

Selected Python exercises inspired by Industrial IoT (IIoT) patterns: MQTT/UNS-style naming, alarm routing, signal validation, and KPI calculations.

## Featured Exercises

- **ex_funcs_iiot.py**
  - Function-based exercises: alarm routing, report generation, clean function design with realistic plant logic.
  - Using `map` and `lambda` to transform process variables in a single pass, including unit conversion (Bar to kPa) and data type validation.

- **ex_map_lambda_kpi.py**
A robust data pipeline that:
- Validates sensor data types (preventing `bool` or `str` errors).
- Calculates **Scrap Rate** percentage.
- Triggers **HIGH_SCRAP** alarms for values over 1.0%.
- Handles edge cases like zero production to avoid `ZeroDivisionError`.

## Run

python ex_funcs_iiot.py
python ex_map_lambda_kpi.py


### Why this repo

This repository is meant as a learning log and a small portfolio showcase. The focus is not on building a large package, but on writing clear, practical code with an IIoT mindset.

### Notes

Python 3.10+ recommended
No external dependencies
