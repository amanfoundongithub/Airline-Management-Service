from dotenv import load_dotenv
from pathlib import Path

def pytest_configure():
    env_path = Path(__file__).resolve().parent.parent / "src" / ".env"
    load_dotenv(env_path)
