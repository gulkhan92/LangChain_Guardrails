# LangChain Guardrails with Gemini

This repository is intended to provide a baseline for hands-on practice with LangChain guardrails, structured output, and Gemini-based application workflows. It is organized to help developers study a maintainable project layout, understand how input and output safety controls can be layered into an agent pipeline, and extend the implementation with additional policies, tools, or domain-specific behaviors.

The codebase separates configuration, schemas, prompts, middleware, model construction, and application orchestration into distinct modules. That separation makes it easier to evolve the guardrail rules, replace providers, and add tests without coupling unrelated concerns.

## Architecture

- Custom input middleware blocks clearly disallowed requests before model inference starts.
- Built-in PII middleware redacts or masks sensitive information in the request and response path.
- A model-based output review performs a final safety check on the generated answer.
- Pydantic schemas define the structured response contract returned by the agent.
- Gemini is used as the underlying chat model through `langchain-google-genai`.

## Project Structure

```text
.
├── .env.example
├── app.py
├── main.py
├── requirements.txt
├── src/langchain_guardrails_demo/
│   ├── agent.py
│   ├── app.py
│   ├── config.py
│   ├── presentation.py
│   ├── prompts.py
│   ├── schemas.py
│   ├── guardrails/
│   │   ├── input_guardrail.py
│   │   └── output_guardrail.py
│   └── services/
│       └── model_factory.py
└── tests/
```

## Key Components

- `KeywordBlocklistMiddleware` in [input_guardrail.py](/Users/dev/Documents/LangChain_Guardrails/src/langchain_guardrails_demo/guardrails/input_guardrail.py) provides deterministic pre-inference filtering for unsafe prompts.
- `PIIMiddleware` is configured in [agent.py](/Users/dev/Documents/LangChain_Guardrails/src/langchain_guardrails_demo/agent.py) to redact email addresses and mask payment-card data.
- `LLMOutputSafetyMiddleware` in [output_guardrail.py](/Users/dev/Documents/LangChain_Guardrails/src/langchain_guardrails_demo/guardrails/output_guardrail.py) validates the final answer with a structured safety verdict.
- `AssistantResponse` and `SafetyVerdict` in [schemas.py](/Users/dev/Documents/LangChain_Guardrails/src/langchain_guardrails_demo/schemas.py) formalize the response and safety-review contracts.
- `GuardrailsApplication` in [app.py](/Users/dev/Documents/LangChain_Guardrails/src/langchain_guardrails_demo/app.py) exposes a minimal application entrypoint for interactive use or future service integration.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Set your Gemini key in `.env`:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.0-flash
```

Optional:

```env
GEMINI_SAFETY_MODEL=gemini-2.0-flash
```

Recommended Python version: `3.12` or `3.13`. The current LangChain dependency stack still emits compatibility warnings on Python `3.14`.

## Run

```bash
PYTHONPATH=src python main.py
```

Interactive prompt:

```text
Summarize the benefits of structured output in LangChain.
```

Direct prompt:

```bash
PYTHONPATH=src python main.py --prompt "Explain how guardrails reduce unsafe output." --pretty
```

## Streamlit Interface

```bash
PYTHONPATH=src streamlit run app.py
```

The Streamlit frontend provides:

- a styled single-page interface for general inference
- structured rendering for topic, answer, safety notes, and sources
- recent prompt history within the active session
- a raw-response view for inspection and debugging

## Testing

```bash
PYTHONPATH=src pytest
```

The test suite is designed to validate the project at multiple layers:

- `tests/test_agent_build.py` confirms that the guarded LangChain agent can be assembled with the configured middleware and structured-output strategy.
- `tests/test_input_guardrail.py` verifies deterministic input blocking for restricted requests and confirms normal requests are allowed to continue.
- `tests/test_output_guardrail.py` validates the output-review middleware behavior for both safe and unsafe model responses.
- `tests/test_config.py` checks environment-driven configuration loading, including required-key enforcement and default model fallback behavior.
- `tests/test_app.py` covers the application inference path by verifying that user input is packaged and sent to the underlying agent correctly.
- `tests/test_presentation.py` verifies response formatting for both structured and fallback inference outputs.
- `tests/test_schemas.py` validates the Pydantic data contracts, including successful parsing and failure behavior for invalid payloads.

These tests are intentionally network-independent so they can run in CI without requiring a live Gemini API call.

## References

- [LangChain Guardrails Documentation](https://docs.langchain.com/oss/python/langchain/guardrails)
- [LangChain Structured Output Concepts](https://docs.langchain.com/oss/python/langchain/structured-output)

## Notes

- `.env` is excluded through [.gitignore](/Users/dev/Documents/LangChain_Guardrails/.gitignore) and should not be committed.
- The repository uses Gemini through `langchain-google-genai`.
- The current implementation is suitable as a starting point for experiments, local practice, and future extension into a service or API layer.
