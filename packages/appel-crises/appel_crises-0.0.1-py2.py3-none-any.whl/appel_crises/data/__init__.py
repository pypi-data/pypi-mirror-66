"""Data module. This little python file only imports the json stored in the directory."""
import json
import os
from typing import Tuple, Dict, List

from appel_crises.settings import BASE_DIR


def load_from_json_here(filename: str):
    """Load from json file in this directory"""
    with open(os.path.join(BASE_DIR, "appel_crises", "data", filename)) as f:
        return json.load(f)


DISTRICT_TO_MP: Dict[str, Tuple[str, str, str, str]] = load_from_json_here("district_to_mp.json")

POSTAL_CODE_TO_DISTRICT: Dict[str, List[str]] = load_from_json_here("postal_code_to_district.json")
