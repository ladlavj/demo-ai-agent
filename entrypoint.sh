#!/bin/bash
# entrypoint.sh

# Default to "all" if RUN_MODE is not set
MODE=${RUN_MODE:-all}

if [ "$MODE" = "web" ]; then
    echo "Starting Web UI..."
    exec streamlit run src/chat_ui.py --server.port=8501 --server.address=0.0.0.0
elif [ "$MODE" = "slack" ]; then
    echo "Starting Slack Bot..."
    exec python -m src.slack_bot
elif [ "$MODE" = "cli" ]; then
    echo "Starting CLI mode..."
    exec python -m src.main --chat
elif [ "$MODE" = "all" ]; then
    echo "Starting BOTH Web UI and Slack Bot..."
    # Start Slack bot in the background
    python -m src.slack_bot &
    # Start Streamlit in the foreground to keep the container running
    exec streamlit run src/chat_ui.py --server.port=8501 --server.address=0.0.0.0
else
    echo "Error: Unknown RUN_MODE '$MODE'. Valid options are: web, slack, cli, all."
    exit 1
fi

