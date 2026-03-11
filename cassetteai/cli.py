import uvicorn
from config import HOST, PORT

# I am the command line entry point for the main app.
# Instead of typing the full uvicorn command every time, I can just run:
#
#   py -3.11 cli.py
#
# This is equivalent to:
#   uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
#
# For production, drop the reload flag. It is only useful during development
# because it restarts the server automatically when I change a file.

if __name__ == "__main__":
    uvicorn.run(
        "api.main:app",
        host=HOST,
        port=PORT,
        reload=True,
    )
