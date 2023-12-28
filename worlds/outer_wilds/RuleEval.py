import json
from typing import Any

from BaseClasses import CollectionState


def eval_rule(state: CollectionState, p: int, rule: [Any]) -> bool:
    return all(eval_criterion(state, p, criterion) for criterion in rule)


def eval_criterion(state: CollectionState, p: int, criterion: Any) -> bool:
    # just a string means it's an item criterion
    if isinstance(criterion, str):
        return state.has(criterion, p)
    elif isinstance(criterion, dict):
        # we're only using JSON objects / Python dicts here as discriminated unions,
        # so there should always be exactly one key-value pair
        if len(criterion.items()) != 1:
            return False
        key, value = next(iter(criterion.items()))
        if key == "anyOf" and isinstance(value, list):
            return any(eval_criterion(state, p, sub_criterion) for sub_criterion in value)
        elif key == "location" and isinstance(value, str):
            return state.can_reach(value, "Location", p)
        elif key == "region" and isinstance(value, str):
            return state.can_reach(value, "Region", p)
    raise ValueError("Unable to evaluate rule criterion: " + json.dumps(criterion))
