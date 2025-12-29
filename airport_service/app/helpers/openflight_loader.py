from core.settings      import openflights_settings
from helpers.exceptions import OpenFlightDownloadError, OpenFlightParseError
from pathlib            import Path

import requests
import csv


class OpenFlightLoader:

    def __init__(self):
        self.url = openflights_settings.OPENFLIGHTS_URL
        self.path = Path(openflights_settings.OPENFLIGHTS_PATH)
    
    def ensure_file(self) -> Path:
        if self.path.exists():
            return self.path
        self.path.parent.mkdir(parents = True, exist_ok = True)

        try:
            response = requests.get(self.url, timeout = 30)
            response.raise_for_status()
        except Exception as e:
            raise OpenFlightDownloadError(e) 
    
        self.path.write_bytes(response.content)
        return self.path

    def load_rows(self) -> list[list[str]]:
        path = self.ensure_file()

        try:
            with path.open(encoding = "utf-8") as f:
                reader = csv.reader(f)
                return list(reader)
        except Exception as e:
            raise OpenFlightParseError(e) 
    
