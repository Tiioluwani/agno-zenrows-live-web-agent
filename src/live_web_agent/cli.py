from __future__ import annotations

import argparse
import json
import os

from dotenv import load_dotenv

from .agents import build_agents
from .config import Settings
from .web import fetch_direct
from .workflow import run_workflow


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Agno and Zenrows workflow")
    parser.add_argument("--url", default=os.getenv("TARGET_URL"))
    parser.add_argument("--skip-direct", action="store_true")
    return parser.parse_args()


def main() -> None:
    load_dotenv()
    args = parse_args()
    if not args.url:
        raise SystemExit("Pass --url or set TARGET_URL")

    if not args.skip_direct:
        print("Direct request comparison:")
        print(json.dumps(fetch_direct(args.url), indent=2, ensure_ascii=False))

    settings = Settings.from_env()
    fetch_agent, processing_agent = build_agents(settings)
    result = run_workflow(args.url, fetch_agent, processing_agent)
    print("\nTwo-agent result:")
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()

