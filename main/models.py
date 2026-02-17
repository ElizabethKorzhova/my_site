"""Load data for main application of my_site project from JSON.
DATA is the dictionary that contains all information needed for main application."""

import json
from pathlib import Path
from django.conf import settings

file_path = Path(settings.BASE_DIR) / "main" / "test_data.json"
with open(file_path) as file:
    DATA: dict[str, str] = json.load(file)
