#IIOT-oriented python practice - functions 

#5. Define a function `format_value(tag, value, unit)` that returns a formatted string
#  such as “PT1001: 4.8 bar”. Return the string and print it.
print(f"Exercise 5: Sensor value formatter\n")

def format_value(tag: str, value: float | int, unit: str) -> str:
    """This func just return a formatted string with certain sensor's info

    Args:
        tag (str): The sensor tag
        value (float, int): process value
        unit (str): unit for the PV

    Returns:
        str: the important sensor's info, like LIT123: 345.12 mm
    """
    if not isinstance(value, (int, float)):
        raise TypeError("The value has to be integer or float.")
    
    formatted_string = (f"{tag.upper()}: {value} {unit.lower()}")
    return formatted_string

pt123 = format_value('pit123', 456.09, 'mBar')
print(pt123)

#6. Create a function `avg_temp(values)` that takes a list of temperature readings and 
# returns the average. Use it on `[72.4, 73.1, 71.9, 72.6]`
print(f"Exercise 6: Average Temperature Calculator\n")

def avg_temp(values: list) -> float:
    """The func return the average of a list of temp. readings.

    Args:
        values (list): a list of temp readings. 

    Raises:
        TypeError: If in the func. call the arg is not a list a TypeError is raised. 

    """
    if not isinstance(values, list):
        raise TypeError("The argument in the func call has to contain a LIST")
    
    return sum(values) / len(values)

average_temp_value = avg_temp([72.4, 73.1, 71.9, 72.6])

print(f"The average temperatur value is: {average_temp_value}\n")

#7.  Write build_topic(factory, line, machine, variable) that returns a full MQTT topic string
#  like factory/line1/machineA/temperature.
print(f"Exercise 7: MQTT Topic Builder\n")

def build_topic(factory: str, line: str, machine: str, variable: str) -> str:
    """
    Build a hierarchical MQTT topic following common IIoT / UNS conventions.

    This function constructs an MQTT topic string using four logical levels:
    factory, production line, machine, and process variable. The resulting
    topic can be used to publish or subscribe to process data in an IIoT system.

    Args:
        factory (str): Name of the factory or site (e.g. "gsk").
        line (str): Production line identifier (e.g. "vial_line").
        machine (str): Machine or station name (e.g. "cutting_machine").
        variable (str): Process variable or data point
            (e.g. "rejected_vials", "temperature").

    Returns:
        str: A formatted MQTT topic string following the pattern:
            factory/line/machine/variable
    """

    return (
        #MQTT  does NOT allow spaces in topics.
        #The topics should be
        #without spaces
        #snake_case o kebab-case and consistent
        f"{factory.lower()}/"
        f"{line.replace(' ','_').lower()}/"
        f"{machine.replace(' ','_').lower()}/"
        f"{variable.replace(' ', '_').lower()}" 
    )

mqtt_topic_1 = build_topic('gsk', 'vial line','cutting machine', 'rejected vials' )
print(f"MQTT topic 1 for vial line is: {mqtt_topic_1}")
mqtt_topic_2 = build_topic('gsk', 'packing line','label machine', 'approved vials' )
print(f"MQTT topic 2 for packing  line is: {mqtt_topic_2}\n")

#8. Define a function `process_report(**kwargs)` that accepts arbitrary keyword arguments
#  (e.g. `temp=78.3, pressure=2.5`) and prints a short process summary.
print(f"Exercise 8: Process Report Generator\n")

def process_report(**kwargs) -> str:
    """
This function return a proces report for a current shift.  
If approved_* and rejected_* counters are present, the function
calculates the loss percentage independently of the item type (vials, syringes, ampoules, etc.)
If these counters are not an integer or float, the code generates a warnig in the report and
the loss is not calculated. 

    :param kwargs: any type of key-value pair representing the proces variables and values
    :return: Return a string with the process summary
    """
    summary = "Process report:\n"

    # Print all provided process variables
    for k, v in kwargs.items():
        summary += f"\t{k}: {v}\n"
    
    # Detect approved_* and rejected_* dynamically
    approved_key = None
    rejected_key = None

    for key in kwargs:
        if key.startswith("approved_"):
            approved_key = key
        elif key.startswith("rejected_"):
            rejected_key = key
        if approved_key and rejected_key:
            break

    # Calculate loss if both counters exist
    if approved_key and rejected_key:
        approved = kwargs[approved_key]
        rejected = kwargs[rejected_key]

        if isinstance(approved, (int, float)) and isinstance(rejected, (int, float)):
            total = approved + rejected
            if total > 0:
                loss_percent = (rejected / total) * 100
                summary += f"\tloss_percent: {loss_percent:.4f}%\n"
            else:
                summary += "warning: total produced is 0, cannot compute loss_percent\n"
        else:
            summary += "warning: approved_* and rejected_* must be numeric to compute loss_percent\n"

    return summary

process_report_mornig_shift = process_report(temp=78.3, pressure=2.5, flow=40.34, 
                                             approved_vials=923405, rejected_vials='453f')
print(f"The morning report is: {process_report_mornig_shift}")


#8.1 Exercise 8.1  — IIoT Alarm Router with **kwargs
print(f"Exercise 8.1: IIoT Alarm Router with **kwargs\n")

def alarm_router(tag: str, **signals) -> dict:
    """Route IIoT process signals into alarm codes based on configurable rules.

    The function validates a small set of known signals and generates alarms when
    thresholds or conditions are met. Invalid types for known signals are reported
    in `bad_signal_type` and the corresponding alarm rule is skipped.

    Args:
        tag (str): Equipment or machine identifier (e.g., "machineA", "filler_1").
        **signals: Arbitrary process signals as keyword arguments. Supported keys:
            - temperature (int|float): Triggers "HIGH_TEMP" if > 80.
            - pressure (int|float): Triggers "LOW_PRESSURE" if < 1.8.
            - running (bool): Triggers "MACHINE_STOPPED" if False.
            - approved (int|float): Used for scrap calculation when paired with `rejected`.
            - rejected (int|float): Used for scrap calculation when paired with `approved`.

    Returns:
        dict: A dictionary with:
            - tag (str): The input tag.
            - alarms (list[str]): Triggered alarm codes.
            - summary (str): One-line summary including tag, alarm count, and valid signals.
            - bad_signal_type (list[str]): Names of supported signals with invalid types.
    """


    bad_signal_type: list[str] = [] #Using type hints
    alarms: list[str] = []
    parts: list[str] = [] 
    temp_value = None 
    press_value = None
    approved_value = None
    rejected_value = None
    running_status = None

    #1 Validation by signals:
    for k, v in signals.items():
        #Finding the signals of interes: temperature in this situation
        if k == 'temperature':
            #En now, if it exists, validating by the expected type.
            if isinstance (v, (int, float)) and not isinstance(v, bool):
                temp_value = v 
            else:
                bad_signal_type.append(k)   

        elif k == 'pressure':
            if isinstance (v, (int, float)) and not isinstance(v, bool):
                press_value = v
            else:
                bad_signal_type.append(k)

        elif k == 'approved':
            if isinstance (v, (int, float)) and not isinstance(v, bool):
                approved_value = v 
            else:
                bad_signal_type.append(k)   

        elif k ==  'rejected':
            if isinstance (v, (int, float)) and not isinstance(v, bool):
                rejected_value =  v
            else:
                bad_signal_type.append(k)

        elif k == 'running':
            if isinstance(v, bool):
                running_status = v
            else:
                bad_signal_type.append(k)

    #2 Rules of alarms:
    if temp_value is not None and temp_value > 80:
        #If the temp_value is not  None, it means it exists and passes the type validation
        alarms.append("HIGH_TEMP")

    if press_value is not None and press_value < 1.8:
        alarms.append("LOW_PRESSURE")

    if running_status is False:
        alarms.append('MACHINE_STOPPED')
    
    #3 Calculating the scrap% and generating alarm:
    if approved_value is not None and rejected_value is not None:
        #validation of approved and rejected passed
        total = approved_value + rejected_value 
        if total > 0: #Avoid dividing by 0
            scrap = rejected_value / (total ) * 100
            if scrap > 1.0:
                alarms.append('HIGH_SCRAP')

    #4 Generating the output dict and the sumamry:

    if temp_value is not None:
        parts.append(f"temperature={temp_value}")
    if press_value is not None:
        parts.append(f"pressure={press_value}")
    if running_status is not None:
        parts.append(f"running={running_status}")

    out_dict = {
        'tag': tag,
        'alarms': alarms,
        'summary': f'{tag} | alarms={len(alarms)} | ' + " ".join(parts)
    }

    #Adding bad_signal_type to the out_dict only if exist bad singal types
    if bad_signal_type:
        out_dict["bad_signal_type"] = bad_signal_type
    
    return out_dict



result = alarm_router(
    "filler_1",
    temperature=85.2,
    pressure=1.2,
    running=True,
    approved=12000,
    rejected=300
)

print(f"result ex 8.1:\n{result}")