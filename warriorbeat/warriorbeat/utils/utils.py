"""
    warriorbeat/api/utils/utils.py
    Various helper functions
"""


def deep_merge_lists(original, incoming):
    """
    Deep merge two lists. Modifies original.
    Reursively call deep merge on each correlated element of list. 
    If item type in both elements are
     a. dict: call deep_merge_dicts on both values.
     b. list: Calls deep_merge_lists on both values.
     c. any other type: Value is overridden.
     d. conflicting types: Value is overridden.

    If length of incoming list is more that of original then extra values are appended.

    See: https://stackoverflow.com/a/50773244
    """
    common_length = min(len(original), len(incoming))
    for idx in range(common_length):
        if isinstance(original[idx], dict) and isinstance(incoming[idx], dict):
            deep_merge_dicts(original[idx], incoming[idx])

        elif isinstance(original[idx], list) and isinstance(incoming[idx], list):
            deep_merge_lists(original[idx], incoming[idx])

        else:
            original[idx] = incoming[idx]

    for idx in range(common_length, len(incoming)):
        original.append(incoming[idx])


def deep_merge_dicts(original, incoming):
    """
    Deep merge two dictionaries. Modfies original.
    For key conflicts if both values are:
     a. dict: Recursivley call deep_merge_dicts on both values.
     b. list: Calls deep_merge_lists on both values.
     c. any other type: Value is overridden.
     d. conflicting types: Value is overridden.

    See: https://stackoverflow.com/a/50773244
    """
    for key in incoming:
        if key in original:
            if isinstance(original[key], dict) and isinstance(incoming[key], dict):
                deep_merge_dicts(original[key], incoming[key])

            elif isinstance(original[key], list) and isinstance(incoming[key], list):
                deep_merge_lists(original[key], incoming[key])

            else:
                original[key] = incoming[key]
        else:
            original[key] = incoming[key]
