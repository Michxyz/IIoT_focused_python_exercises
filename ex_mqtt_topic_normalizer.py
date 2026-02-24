#---------------------------MQTT Topic Normalizer-------------------

#Normalize raw MQTT topic strings into a consistent UNS-style format, then filter out invalid topics.
# Rules:
# 1) A valid topic must have exactly 4 segments: site/line/cell/tag
# 2) Normalization:
#    - lowercase everything
#    - trim whitespace around segments
#    - replace internal spaces with "_"
#    - remove empty segments (e.g., caused by "//")
# 3) Allowed tags: {"temp", "pressure", "flow", "level"}

print(f"\nExercise: lambda + map + filter -> MQTT Topic Normalizer.\n")
#input data:
allowed_tags: set[str] = {"temp", "pressure", "flow", "level"}

topics: list[str] = [
  "Factory 1/Line A/Cell 2/Temp",
  "factory_1/line_a/cell_2/temp",
  "Factory1/LineA/Cell2/Temp",
  "Factory 1/Line A//Temp",
  "Factory 1/Line A/Cell 2/Pressure"
]

#With step 1 I separate/split each string (the topic), in segments (list of strings).
#Later, each segment will be cleaned with a func.
#Split generates a list -> [['segment_a','segment_b','segment_c'], ['segment_n']  ]
step_1_split: list[list[str]] = list(map(lambda a: a.split("/"), topics))
print(f"Split the list of topics by '/': \n{step_1_split}")


def clean_segments(segment: list[str]) -> list[str]:
    """This func is prepared to receive each  topic segments from 'step_1_split' with the map call.
    Then the map inside this func will clean each  topic's segment:
        *strip spaces around
        *lowercases
        *replace internal whitespace with '_'
        *finally filter out the empty segments (eg: '')
    """
    cleaned: list[str] = list(map(lambda x: x.strip().lower().replace(" ", "_"), segment))
    non_empty: list[str] = list(filter(None, cleaned))
    return non_empty

step_2_cleaned: list[list[str]] = list(map(clean_segments, step_1_split))
print(f"\nThe cleaned list of lists:\n {step_2_cleaned}\n")

#The next step is filter out the topics that have less or more than 4 segments AND whose tag 
#is not in the allowed_tags var. 
valid_segments: list[list[str]] = list(filter(
    lambda topic: len(topic) == 4 and topic[-1] in allowed_tags, step_2_cleaned ))

print(f"\nThe valid segments are:\n{valid_segments}\n")

# The last step is joining again all segments with '/' to rebuild the topics.
joined_topics: list[str]  = list(map(lambda segment:  "/".join(segment), valid_segments))
print(f"Last step, the joined topics:\n{joined_topics }\n")