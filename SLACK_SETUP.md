# Slack App Configuration Guide

To run the AI agent as a Slack bot, you need to configure an app on [api.slack.com](https://api.slack.com/apps) and generate the necessary connection tokens. This guide walks you through setting up Socket Mode, Event Subscriptions, and Slash Commands.

## 1. Create the App
1. Go to [https://api.slack.com/apps](https://api.slack.com/apps) and log in.
2. Click the **Create New App** button.
3. Select **From scratch**.
4. Name your app (e.g., "AI Agent") and pick your Slack workspace. Click **Create App**.

## 2. Enable Socket Mode & Get App Token
Socket Mode allows your bot to communicate securely with Slack without needing a public HTTP server or webhook.

1. In the left sidebar under **Settings**, click on **Socket Mode**.
2. Toggle **Enable Socket Mode** to *On*.
3. You will be prompted to generate an **App-Level Token**. 
   - Name it something like `socket-token`.
   - Add the `connections:write` scope.
   - Click **Generate**.
4. **Copy the generated token.** It starts with `xapp-`.
5. Open your project's `.env` file and add it:
   ```env
   SLACK_APP_TOKEN=xapp-...
   ```

## 3. Enable Event Subscriptions
Your bot needs permission to listen to mentions and direct messages.

1. In the left sidebar under **Features**, click **Event Subscriptions**.
2. Toggle **Enable Events** to *On*.
3. Scroll down to **Subscribe to bot events** and click *Add Bot User Event*.
4. Add the following events:
   - `app_mention` (so the bot hears when it is @mentioned)
   - `message.im` (so the bot can respond to 1-on-1 direct messages)
5. Click **Save Changes** at the bottom.

## 4. Set Up Slash Commands (Optional)
If you want to use the `/ask-agent` command included in the code:

1. Under **Features**, click **Slash Commands**.
2. Click **Create New Command**.
3. Set the Command to `/ask-agent`.
4. Add a short description (e.g., "Ask the AI agent a question silently").
5. Click **Save**.

## 5. Enable Interactivity (Optional)
If you plan to use interactive buttons, shortcuts, or modals:

1. Under **Features**, click **Interactivity & Shortcuts**.
2. Toggle **Interactivity** to *On*.
3. Click **Save Changes**.

## 6. Install App & Get Bot Token
Finally, you need to install the app to your workspace to get the bot token.

1. Under **Features**, click **OAuth & Permissions**.
2. Scroll down to **Scopes** -> **Bot Token Scopes** and ensure you have the following (they may have been added automatically):
   - `app_mentions:read`
   - `chat:write`
   - `im:history`
   - `im:read`
   - `commands`
3. Scroll back up and click **Install to Workspace**. 
4. Review the permissions and click **Allow**.
5. You will be redirected back to the OAuth page. Copy the **Bot User OAuth Token**. It starts with `xoxb-`.
6. Open your `.env` file and add it:
   ```env
   SLACK_BOT_TOKEN=xoxb-...
   ```

## 7. Run Your Bot
Your `.env` file should now look like this:
```env
GOOGLE_API_KEY=your_google_key
SLACK_APP_TOKEN=xapp-...
SLACK_BOT_TOKEN=xoxb-...
```

Start the bot from your terminal:
```bash
python -m src.slack_bot
```
Go to your Slack workspace, find the app under the "Apps" section in the sidebar, and send it a direct message!
