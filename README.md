# Demo AI Agent

A LangChain-based AI agent that uses Google's Gemini models and integrates with Model Context Protocol (MCP) servers. The project features three distinct ways to interact with the agent: a Command Line Interface (CLI), a Streamlit-based web chat UI, and a fully functional Slack Bot.

## Features

- **Google Gemini Integration**: Uses `gemini-3.5-flash-lite` via LangChain.
- **MCP Tool Integration**: Dynamically loads external tools using the Model Context Protocol (e.g., OpenWeather MCP server).
- **Multiple Interfaces**: 
  - **Slack Bot:** Integrates seamlessly into your workspace via Socket Mode. Supports `@mentions`, Direct Messages, and Slash Commands (`/ask-agent`).
  - **Streamlit UI:** A robust web application with session history.
  - **CLI:** A command-line interface with single-prompt and continuous chat modes.

## Prerequisites

1. Python 3.10+
2. A **Google API Key** for Gemini.
3. (Optional) **Slack App Tokens** (`SLACK_BOT_TOKEN` and `SLACK_APP_TOKEN`) if you intend to run the Slack Bot.

## Installation

1. Clone this repository. Since this project uses Git submodules (for external MCP servers), make sure to clone it recursively:
   ```bash
   git clone --recurse-submodules <repository_url>
   ```
   *(If you already cloned the repository normally, you can fetch the submodules by running: `git submodule update --init --recursive`)*

2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory and add your API keys:
   ```env
   # Required for AI generation
   GOOGLE_API_KEY=your_google_api_key_here
   
   # Required only for the Slack Bot
   SLACK_APP_TOKEN=xapp-...
   SLACK_BOT_TOKEN=xoxb-...
   ```
   > **Note:** For detailed instructions on how to configure your Slack app and generate these tokens, see the [SLACK_SETUP.md](SLACK_SETUP.md) guide.

## Usage

### 1. Slack Bot Interface (New!)
You can run the agent as a fully functional Slack bot using Socket Mode. Once running, you can interact with it via `@mentions`, Direct Messages, or the `/ask-agent` command.
```bash
python -m src.slack_bot
```

### 2. Web Chat UI
Run the Streamlit application to chat with the agent in your web browser. This interface automatically remembers your chat history.
```bash
streamlit run src/chat_ui.py
```

### 3. Command Line Interface
You can run the agent directly in your terminal.

**Continuous chat bot mode:**
```bash
python -m src.main --chat
```

**One-time prompt mode:**
```bash
python -m src.main
```

## Running with Docker

You can run the entire application inside an isolated Docker container. The container uses an intelligent entrypoint script that can run all interfaces simultaneously, or let you pick exactly which one you want using the `RUN_MODE` environment variable.

1. **Build the image:**
   ```bash
   docker build -t demo-ai-agent .
   ```

2. **Run EVERYTHING (Default behavior):**
   By default, it will start both the Slack Bot in the background and the Streamlit Web UI in the foreground.
   ```bash
   docker run -p 8501:8501 --env-file .env demo-ai-agent
   ```

3. **Run ONLY the Web UI:**
   ```bash
   docker run -p 8501:8501 --env-file .env -e RUN_MODE=web demo-ai-agent
   ```

4. **Run ONLY the Slack Bot:**
   ```bash
   docker run -d --env-file .env -e RUN_MODE=slack demo-ai-agent
   ```

5. **Run ONLY the CLI Chat Bot:**
   ```bash
   docker run -it --env-file .env -e RUN_MODE=cli demo-ai-agent
   ```

## Testing

Unit tests are included to verify the core agent logic and tools.
Run the tests using the built-in `unittest` module:
```bash
python -m unittest discover -s tests -p "test_*.py"
```
