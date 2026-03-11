import os

# I handle Windows username resolution here and nothing else.
# I have no knowledge of the API, the database, or the camera.
#
# At startup the main app calls me with the ENGINEERS list from config.py.
# I read the Windows domain username from the environment, find the matching
# engineer entry, and return their display name.
#
# If I cannot find a match, I return None. The dashboard then shows a
# dropdown so the engineer can pick their name manually. No passwords,
# no friction, no hardcoded names anywhere in the HTML or JS.


def resolve_engineer(engineers: list) -> str | None:
    # Read the Windows domain username. On a Trymax domain machine this
    # is always set. On a dev machine it may be a personal username that
    # does not match anyone in the list, which is fine.
    windows_username = os.environ.get("USERNAME", "").lower().strip()

    if not windows_username:
        return None

    for engineer in engineers:
        if engineer.get("windows_user", "").lower() == windows_username:
            return engineer["name"]

    # No match found. The caller shows the dropdown fallback.
    return None
