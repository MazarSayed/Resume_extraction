from datetime import datetime


def create_timestamp() -> str:
    """Generate a timestamp string in YYYYMMDD_HHMMSS format."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def normalize_filename(filename: str) -> str:
    """Normalize filename: lowercase and replace spaces with underscores."""
    return filename.lower().replace(" ", "_")
