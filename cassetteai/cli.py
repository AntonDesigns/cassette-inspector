"""
cassetteai CLI entry point.
Usage: cassetteai serve
"""
import argparse
import sys


def main():
    parser = argparse.ArgumentParser(
        prog="cassetteai",
        description="Cassette Inspector — AI-powered semiconductor cassette inspection"
    )
    subparsers = parser.add_subparsers(dest="command")

    serve_parser = subparsers.add_parser("serve", help="Start the web server")
    serve_parser.add_argument("--host", default="0.0.0.0", help="Host to bind to (default: 0.0.0.0)")
    serve_parser.add_argument("--port", type=int, default=8000, help="Port to listen on (default: 8000)")
    serve_parser.add_argument("--reload", action="store_true", help="Enable auto-reload for development")

    args = parser.parse_args()

    if args.command == "serve":
        import uvicorn
        uvicorn.run(
            "cassetteai.api.main:app",
            host=args.host,
            port=args.port,
            reload=args.reload,
        )
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
