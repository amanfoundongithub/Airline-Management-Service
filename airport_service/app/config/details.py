import os 
import requests

# Load environment variables to get the flight details
OPENFLIGHTS_URL  = os.getenv("OPENFLIGHTS_URL")
OPENFLIGHTS_PATH = os.getenv("OPENFLIGHTS_PATH")


def load_iata_data() -> None:
    
    # Check if file is downloaded or not
    if not os.path.exists(OPENFLIGHTS_PATH):
        print("File not found. Starting download...") 

        # Start download 
        r = requests.get(OPENFLIGHTS_URL, timeout = 30)
        r.raise_for_status() 

        # Write if not found
        with open(OPENFLIGHTS_PATH, "wb") as f:
            f.write(r.content)

