from __future__ import annotations

import argparse
import json

from langchain_guardrails_demo.app import GuardrailsApplication
from langchain_guardrails_demo.presentation import build_console_payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a general inference request through the LangChain guardrails pipeline."
    )
    parser.add_argument(
        "-p",
        "--prompt",
        help="Prompt to send to the application. If omitted, the CLI opens an interactive prompt.",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print the JSON response.",
    )
    return parser.parse_args()


def read_prompt(cli_prompt: str | None) -> str:
    if cli_prompt and cli_prompt.strip():
        return cli_prompt.strip()

    user_input = input("Enter a prompt: ").strip()
    if user_input:
        return user_input

    raise SystemExit("A prompt is required.")


def main() -> None:
    args = parse_args()
    prompt = read_prompt(args.prompt)

    app = GuardrailsApplication()
    result = app.run(prompt)
    payload = build_console_payload(result)

    if args.pretty:
        print(json.dumps(payload, indent=2))
        return

    print(json.dumps(payload))


if __name__ == "__main__":
    main()
