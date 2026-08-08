# AI News Agentic Chatbot

A multi-mode agentic AI application built with **LangGraph** and **Streamlit**, supporting three selectable use cases: a basic LLM chatbot, a chatbot with web search tool-calling, and an automated AI news fetch-summarize-save pipeline.

## Features

- **Basic Chatbot** — a simple LangGraph graph (`START → chatbot → END`) for direct conversation with the selected LLM.
- **Chatbot With Web** — an agentic graph that adds a `tools` node and conditional routing (`tools_condition`) so the LLM can call a web search tool (Tavily) when it needs current information, then loop back to the chatbot node with the results.
- **AI News** — a three-step pipeline (`fetch_news → summarize_news → save_result`) that pulls recent AI news, summarizes it with the LLM, and writes the result to `AINews/daily_summary.md`, `weekly_summary.md`, or `monthly_summary.md` depending on the selected timeframe.
- **Live Groq model discovery** — instead of a hardcoded model dropdown, `groq_models.py` calls Groq's `/openai/v1/models` endpoint at runtime, filters out non-chat models (Whisper, TTS, Guard, embedding models), and caches the result for an hour so the UI always shows models Groq currently hosts.
- Streamlit UI for entering your Groq API key, picking a use case, and picking a model.

## Architecture

```
app.py
└── src/langgraphagenticai/
    ├── main.py                     # orchestrates UI → LLM → graph → display
    ├── ui/uiconfigfile.py          # Config: reads page title / LLM / use-case options
    ├── ui/uiconfigfile.ini         # backing config values for the above
    ├── ui/streamlitui/             # Streamlit UI components
    ├── LLMS/groqllm.py             # wraps ChatGroq
    ├── LLMS/groq_models.py         # live model list fetch + cache
    ├── graph/graph_builder.py      # builds the LangGraph graph per use case
    ├── nodes/                      # basic_chatbot_node, chatbot_with_Tool_node, ai_news_node
    ├── tools/search_tool.py        # Tavily search tool wiring
    └── state/state.py              # shared LangGraph state schema
```

## Requirements

- Python 3.13+ (see `pyproject.toml` / `.python-version`)
- A [Groq API key](https://console.groq.com/keys) (free tier available)
- A [Tavily API key](https://tavily.com/) for the web-search use case

## Installation

```bash
git clone <this-repo>
cd AINEWSAgentic_updated
pip install -r requirements.txt
```

## Usage

```bash
streamlit run app.py
```

Then in the browser UI:
1. Enter your Groq API key.
2. Select an LLM model from the live dropdown.
3. Pick a use case: **Basic Chatbot**, **Chatbot With Web**, or **AI News**.
4. For the AI News use case, pick a timeframe (daily/weekly/monthly) and click Fetch; for the other use cases, type a message in the chat box.

## Environment variables

You can also set keys via environment variables instead of entering them in the UI:

```bash
export GROQ_API_KEY="your-groq-key"
export TAVILY_API_KEY="your-tavily-key"
```

## Notes on model selection

Groq periodically deprecates and retires model IDs. This project's live model-fetch handles that gracefully for the dropdown, but the fallback list used when the API call fails is hardcoded in `groq_models.py`:

```python
_FALLBACK_MODELS = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]
```

Check [Groq's model deprecation page](https://console.groq.com/docs/deprecations) periodically and update this fallback list if the models listed there have been retired, so the dropdown doesn't offer a dead model ID when the live fetch is unavailable.

## Tech stack

LangChain · LangGraph · langchain-groq · Streamlit · Tavily · FAISS · Groq (LLM inference)

## Credits

This project is based on a project idea/tutorial from [Krish Naik's Projects](https://www.krishnaik.in/projects). I built and extended it as a hands-on learning project, including the live Groq model-discovery feature described above.