import json
import os
import pytest
from schema import Schema, Or, Optional
import unittest

from ..shared_static_logic.items import items_data
from ..shared_static_logic.locations import locations_data
from ..shared_static_logic.connections import connections_data


IN_GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"

# Unfortunately Python schemas don't support recursion, so we can only test the "top-level" keys for locations/connections.
# Fortunately the transpilation from "requires" objects to Rule Builder rules at runtime does a lot of the nested validation implicitly.

# The { "option": ... } usage in items.py is just simple enough that we can get away with this hack:
str_option_schema_1 = Or(str, Schema({ "option": str, str: str }))
str_option_schema_2 = Or(str, Schema({ "option": str, str: str_option_schema_1 }))
int_option_schema_1 = Or(int, Schema({ "option": str, str: int }))

items_data_schema = Schema([
    {
        Optional("category"): str,
        "code": Or(int, None),  # noqa, turns out Or(None) is broken
        "name": str,
        Optional("count"): int_option_schema_1,
        "type": str_option_schema_2,
    }
])

locations_data_top_level_schema = Schema([
    {
        Optional("category"): str,
        "address": Or(int, None),  # noqa
        "name": str,
        "region": str,
        Optional("requires"): [object],
        Optional("medium_requires"): [object],
        Optional("ls_requires"): [object],
    }
])

connections_data_top_level_schema = Schema([
    {
        Optional("category"): str,
        "from": str,
        "to": str,
        Optional("requires"): [object],
        Optional("medium_requires"): [object],
        Optional("ls_requires"): [object],
    },
])

class TestLogicFiles(unittest.TestCase):
    def test_items_data(self):
        items_data_schema.validate(items_data)

    def test_locations_data(self):
        locations_data_top_level_schema.validate(locations_data)

    def test_connections_data(self):
        connections_data_top_level_schema.validate(connections_data)

    @pytest.mark.skipif(IN_GITHUB_ACTIONS,
                        reason="We only want to test this locally before a release. "
                               "On individual PRs it would force too many conflicts.")
    def test_generated_files_up_to_date(self) -> None:
        expected_items_data = json.dumps(items_data)
        expected_locations_data = json.dumps(locations_data)
        expected_connections_data = json.dumps(connections_data)

        items_path = os.path.join(os.path.dirname(__file__), "..", "shared_static_logic", "items.jsonc")
        locations_path = os.path.join(os.path.dirname(__file__), "..", "shared_static_logic", "locations.jsonc")
        connections_path = os.path.join(os.path.dirname(__file__), "..", "shared_static_logic", "connections.jsonc")

        with open(items_path, 'r') as items_file:
            actual_items_data = items_file.read()
        with open(locations_path, 'r') as locations_file:
            actual_locations_data = locations_file.read()
        with open(connections_path, 'r') as connections_file:
            actual_connections_data = connections_file.read()

        self.assertEqual(
            expected_items_data,
            actual_items_data,
            "items.jsonc does not match items.py. Please regenerate these files.")
        self.assertEqual(
            expected_locations_data,
            actual_locations_data,
            "locations.jsonc does not match locations.py. Please regenerate these files.")
        self.assertEqual(
            expected_connections_data,
            actual_connections_data,
            "connections.jsonc does not match connections.py. Please regenerate these files.")
