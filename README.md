# Hugging Face AI Agents

A `smolagents`-based `CodeAgent` with a few custom tools (timezone lookup, weather, image
generation) exposed through a simple Gradio chat UI.

## Setup

```bash
pip install -r requirements.txt
python app.py
```

Requires a Hugging Face API token available in the environment for `HfApiModel`
(set `HF_TOKEN`).

## Structure

- `app.py` — defines the tools and the agent, launches the Gradio UI.
- `tools/final_answer.py` — the `final_answer` tool the agent calls to return its result.
- `Gradio_UI.py` — minimal chat interface wrapping `agent.run()`.
- `prompts.yaml` — system prompt template passed to the agent.
