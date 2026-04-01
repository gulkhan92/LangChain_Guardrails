# LangChain Guardrails with Gemini

Production-style LangChain example that combines:

- deterministic guardrails via custom middleware
- built-in PII middleware
- model-based final output review
- typed structured responses with Pydantic
- Gemini as the application model provider

## Project structure

```text
.
├── .env.example
├── main.py
├── requirements.txt
├── src/langchain_guardrails_demo/
│   ├── agent.py
│   ├── app.py
│   ├── config.py
│   ├── prompts.py
│   ├── schemas.py
│   ├── guardrails/
│   │   ├── input_guardrail.py
│   │   └── output_guardrail.py
│   └── services/
│       └── model_factory.py
└── tests/
```

## Features

1. `KeywordBlocklistMiddleware` blocks obviously unsafe requests before the model runs.
2. `PIIMiddleware` redacts emails and masks credit-card numbers.
3. `LLMOutputSafetyMiddleware` reviews the final response with a second Gemini call.
4. `ProviderStrategy(schema=AssistantResponse)` returns structured output validated by Pydantic.

This follows the current LangChain approach documented in the official guardrails and structured output docs.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Set your Gemini key in `.env`:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.0-flash
```

Recommended Python version: `3.12` or `3.13`. The current LangChain stack still emits a compatibility warning on Python `3.14`.

## Run

```bash
PYTHONPATH=src python main.py
```

Example prompt:

```text
Summarize the benefits of structured output in LangChain.
```

## Test

```bash
PYTHONPATH=src pytest
```

## Notes

- `.env` is excluded via `.gitignore`.
- The implementation uses Gemini through `langchain-google-genai`.
- The structured output schema lives in `schemas.py`, separate from guardrail logic.
