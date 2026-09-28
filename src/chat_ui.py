import streamlit as st
import asyncio
from main import get_agent

# 1. Set up the look of the web page
st.set_page_config(page_title="My agent chat", page_icon="🦜")
st.title("🦜 My agent chat ui")

# 2. Give Streamlit a memory box!
# By default, Streamlit forgets everything when you type a new message.
# "st.session_state" is a special backpack where it can store history.
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Show all the past messages on the screen
# This loops through our memory box and prints past chats
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 4. Wait for the user to type something new
if user_input := st.chat_input(placeholder="Ask me anything..."):

    # Save the user's message to the memory box
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display the user's message immediately on the screen
    with st.chat_message("user"):
        st.write(user_input)

    # 5. Get the agent's response
    with st.chat_message("assistant"):
        # Show a little loading spinner while the bot thinks
        with st.spinner("Thinking..."):

            # Since our agent setup is 'async' (meaning it can do multiple things at once),
            # we need to wrap it in a special mini-function to run inside Streamlit.
            async def get_response():
                # Plug into the brain from main.py
                agent = await get_agent()

                # Send the entire chat history so it remembers what we talked about
                result = await agent.ainvoke({"messages": st.session_state.messages})

                # Dig through the result to find the actual text reply
                # print(f"---------Result---------{result}")
                last_msg = result["messages"][-1]
                # print(f"---------last_msg---------{last_msg}")
                reply_text = getattr(last_msg, "text", getattr(last_msg, "content", str(last_msg)))
                return reply_text

            # Run the background task and get the reply
            bot_reply = asyncio.run(get_response())

            # Print the reply to the screen
            st.write(bot_reply)

            # Save the bot's reply to the memory box so it remembers it next time
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})