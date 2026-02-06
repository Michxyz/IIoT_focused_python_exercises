"""
IIoT Practice: Data Normalization and KPI Pipelines
Focus: map and lambda.
"""

#3. Map over a dict: scale values and flag bad types.
# You have a dictionary of “raw” process signals. You want to normalize them for an
#  IIoT pipeline.
# Input:
 
signals_3: dict = {
    "temperature": 81.234,
    "pressure_bar": 1.72,
    "flow": None,   # bad type 
    "running": False,      # bool is NOT considered numeric here
}

# Goal: Create a new dictionary with the same keys, but transformed values:
#temperature: round to 1 decimal
#pressure_bar: convert to kPa (value * 100) and round to 1 decimal
#any other valid numeric values: round to 1 decimal
#any invalid value (not int/float or is bool): set to "BAD_SIGNAL_TYPE"

#Constraints:
# Use map + lambda over signals.items() and rebuild the dictionary.
# Do not use an explicit for loop for the transformation.
print(f"\nExercise 3: Map over a dict: scale values and flag bad types.")


normalized_signals_3 = dict(
    map(
        lambda kv: (
            #validating all value types:
            kv[0],
            "BAD_SIGNAL_TYPE" if (not isinstance(kv[1], (int, float)) or  isinstance(kv[1], bool)) #First discard bad signals
            else round(kv[1]*100, 1)  if  kv[0] == 'pressure_bar' else  round(kv[1], 1) #Needed nested ternary operator for transformations
        ),
        signals_3.items(),
    )
)
print(f"\n\t Normalized dict : {normalized_signals_3}")




#4. IIoT shift KPI pipeline with map + lambda (no explicit for)
#You have shift reports coming from a production line. 
# Build a small transformation pipeline that produces “dashboard-ready” KPIs.
#Input data with some corrupted entries:
shift_reports: list[dict] = [
    {"tag": "filler_1", "shift": "A", "approved": 12000, "rejected": 300},
    {"tag": "filler_1", "shift": "B", "approved": "7",  "rejected": 50}, # Error: string
    {"tag": "labeler_1", "shift": "A", "approved": 0,    "rejected": True}, # Error: bool
    {"tag": "mixer_1", "shift": "C", "approved": 0, "rejected": 0}, # Edge case: zero division
]
#Output requirements:
""" 
Transform the input into a list[dict] where each output dict contains:
*tag (same as input)
*shift (same as input)
*scrap_pct:
rejected / (approved + rejected) * 100
if approved + rejected == 0, then scrap_pct must be None
*alarm:
"HIGH_SCRAP" if scrap_pct is not None and scrap_pct > 1.0
otherwise None
    extra:
    "INVALID_DATA_TYPE" if type validation is not ok.
"""
#Constraints:
#Use only: map, lambda, list, dict, and basic expressions.
#No explicit for loops for the transformation.
#Keep it readable (prefer 1–2 small helper lambdas if needed).

#Extra: I'm assuming that the counters "approved" & "rejected" are always integers, but if
#they are not, the code will crash. To avoid this, add type validation. 

print(f"\nExercise 4: shift KPI pipeline with map + lambda.\n")

#defining type validation function, helper lambdas and tranform function for map:
type_validation_ok = lambda item: isinstance(item["approved"], int) and not isinstance(item["approved"], bool ) and  isinstance(item["rejected"], int ) and not isinstance(item["rejected"], bool )
total_units = lambda element:  element["approved"] + element["rejected"]
calculated_scrap_pct = lambda total_units, element: round(element["rejected"]/ total_units * 100, 2)

#A named transform function keeps the map pipeline readable (nested lambdas get messy quickly).
def transform(x: dict) -> dict:
    """
    This function transforms raw shift data into KPIs. 
    If input data is invalid (wrong types), it returns a record with status 'INVALID_DATA'.

    Args:
        x (dict): A dictionary containing 'tag', 'shift', 'approved', and 'rejected' data.

    Returns:
        dict: A processed dictionary with 'tag', 'shift', 'scrap_pct', and 'alarm' status.
    """
    # 1. Check for bad data 
    if not type_validation_ok(x):
        return {
            "tag": x["tag"],
            "shift": x["shift"],
            "scrap_pct": None,
            "alarm": "INVALID_DATA_TYPE"
        }
    
    # 2. Proceed with business logic if data is ok     
    tot: int = total_units(x)
    scrap: float | None = None if tot == 0 else calculated_scrap_pct(tot, x)
    return{
        "tag": x["tag"],
        "shift": x["shift"],
        "scrap_pct": scrap,
        "alarm": "HIGH_SCRAP" if (scrap is not None and scrap > 1.0 ) else None,
    }


# Pipeline execution: map applies 'transform' to every element safely
dashboard_ready_shift_report = list(map(transform, shift_reports))

# Displaying results
print(dashboard_ready_shift_report)