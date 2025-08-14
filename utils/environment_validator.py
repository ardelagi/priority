
import os

REQUIRED_VARS = ["DISCORD_TOKEN", "MONGODB_URI"]

def validate_environment() -> None:
    missing = [k for k in REQUIRED_VARS if not os.getenv(k)]
    if missing:
        raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")
