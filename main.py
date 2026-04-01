from __future__ import annotations

from pprint import pprint

from langchain_guardrails_demo.app import GuardrailsApplication


def main() -> None:
    user_input = input("Enter a prompt: ").strip()
    if not user_input:
        raise SystemExit("A prompt is required.")

    app = GuardrailsApplication()
    result = app.run(user_input)
    pprint(result)


if __name__ == "__main__":
    main()
