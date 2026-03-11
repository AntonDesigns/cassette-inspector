# Engineer identity module — Windows username resolution + dropdown fallback.
# Reads the logged-in Windows username and matches it against the ENGINEERS list.
# Does not know about the API, the database, or the camera.
import os

def resolve_engineer(engineers: list) -> str | None:
    windows_user = os.environ.get("USERNAME", "").lower().strip()
    for eng in engineers:
        if eng.get("windows_user", "").lower() == windows_user:
            return eng["name"]
    return None
