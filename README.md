# Demo AI Agent

A LangChain-based AI agent that uses Google's Gemini models and integrates with Model Context Protocol (MCP) servers. The project features both a Command Line Interface (CLI) and a Streamlit-based web chat interface.

## Features

- **Google Gemini Integration**: Uses `gemini-3.5-flash-lite` via LangChain.
- **MCP Tool Integration**: Dynamically loads external tools using the Model Context Protocol (e.g., OpenWeather MCP server).
- **Dual Interfaces**: 
  - A robust Streamlit web application with session history.
  - A command-line interface with single-prompt and continuous chat modes.

## Prerequisites

1. Python 3.9+
2. A Google API Key for Gemini.

## Installation

1. Clone this repository. Since this project uses Git submodules (for external MCP servers), make sure to clone it recursively:
   ```bash
   git clone --recurse-submodules <repository_url>
   ```
   *(If you already cloned the repository normally, you can fetch the submodules by running: `git submodule update --init --recursive`)*
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory and add your Google API key:
   ```env
   GOOGLE_API_KEY=your_api_key_here
   ```

## Usage

### 1. Web Chat UI (Recommended)
Run the Streamlit application to chat with the agent in your web browser. This interface automatically remembers your chat history.
```bash
streamlit run src/chat_ui.py
```

### 2. Command Line Interface
You can run the agent directly in your terminal.

**One-time prompt mode:**
```bash
python -m src.main
```

**Continuous chat bot mode:**
```bash
python -m src.main --chat
```

### 3. Running with Docker

You can run the entire application inside an isolated Docker container. 

1. **Build the image:**
   ```bash
   docker build -t demo-ai-agent .
   ```

2. **Run the Streamlit Web UI:**
   Pass your Google API key using the `-e` flag. The app will be available at `http://localhost:8501`.
   ```bash
   docker run -p 8501:8501 -e GOOGLE_API_KEY="your_actual_api_key_here" demo-ai-agent
   ```

3. **Run the Command Line Interface:**
   If you want to run the terminal chat bot inside Docker, override the default command and run in interactive mode (`-it`):
   ```bash
   docker run -it -e GOOGLE_API_KEY="your_api_key_here" demo-ai-agent python -m src.main --chat
   ```

## Testing

Unit tests are included to verify the core agent logic and tools.
Run the tests using the built-in `unittest` module:
```bash
python -m unittest discover -s tests -p "test_*.py"
```
