# time_block_functions.py
"""
Functions for dealing with messy time block objects
"""


def fix_start_time(time_block_dict):
    if not ":" in time_block_dict["start_time"] and not (
        "pm" in time_block_dict["start_time"] or "am" in time_block_dict["start_time"]
    ):
        start_time_str = time_block_dict["start_time"]
        if len(start_time_str) < 6:
            start_time_str = start_time_str + ":00"
            am_or_pm = time_block_dict["stop_time"][-2:]
            start_time_str = start_time_str + am_or_pm

        time_block_dict["start_time"] = start_time_str
    return time_block_dict
