import streamlit as st
import pandas as pd
from data_processor import load_data
from agents.data_agent import create_data_agent

st.set_page_config(page_title="Vasanth's DAC", page_icon="🤖")

# Custom CSS for the chatbot UI and footer
st.markdown("""
<style>
    .chat-message {
        padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex;
    }
    .chat-message.user {
        background-color: #262730; justify-content: flex-end;
    }
    .chat-message.bot {
        background-color: #3f4251; justify-content: flex-start;
    }
    .chat-message.user .avatar {
        margin-left: 0.7rem;
    }
    .chat-message.bot .avatar {
        margin-right: 0.7rem;
    }
    .chat-message .avatar {
        width: 35px; height: 35px; border-radius: 50%;
        background-size: cover; background-position: center;
    }
    .chat-message .message {
        width: 80%; padding: 0.5rem 1rem;
        color: white; /* Added this line */
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #1a1a1a;
        color: white;
        text-align: center;
        padding: 10px 0;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

def show_message(text, is_user=False):
    avatar_url = "https://cdn-icons-png.flaticon.com/512/3264/3264257.png" if is_user else "https://cdn-icons-png.flaticon.com/512/4712/4712019.png"
    message_class = "user" if is_user else "bot"
    st.markdown(f"""
    <div class="chat-message {message_class}">
        <div class="avatar" style="background-image: url({avatar_url});"></div>
        <div class="message">{text}</div>
    </div>
    """, unsafe_allow_html=True)

# Main UI
st.title("🤖 Vasanth's Data Analyst Chatbot!")
st.write("Upload a file (CSV, Excel, TXT, DOCX, PDF) and ask me questions about it!")

# Session state to store uploaded data and chat history
if "df" not in st.session_state:
    st.session_state.df = None
if "agent" not in st.session_state:
    st.session_state.agent = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# File uploader
uploaded_file = st.sidebar.file_uploader("Upload your data file", type=['csv', 'xlsx', 'xls', 'txt', 'docx', 'pdf'])

if uploaded_file:
    try:
        df = load_data(uploaded_file)
        st.session_state.df = df
        st.session_state.agent = create_data_agent(df)
        st.sidebar.success("File loaded successfully!")
        st.sidebar.write("First 5 rows of your data:")
        st.sidebar.dataframe(df.head())
        
        # Clear previous chat history for new data
        st.session_state.messages = []
        st.session_state.messages.append({"role": "bot", "content": "I've successfully loaded the data! What can I analyze for you?"})

    except Exception as e:
        st.sidebar.error(f"Error loading file: {e}")
        st.session_state.df = None
        st.session_state.agent = None
        
# Display chat messages from history
for message in st.session_state.messages:
    show_message(message["content"], is_user=(message["role"] == "user"))

# Chat input
if prompt := st.chat_input("Ask a question about the data..."):
    if st.session_state.df is None:
        st.warning("Please upload a data file first.")
    else:
        # Display user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        show_message(prompt, is_user=True)
        
        # Get AI response
        try:
            with st.spinner("Thinking..."):
                response = st.session_state.agent.invoke(prompt)
                ai_response = response['output']
        except Exception as e:
            ai_response = f"An error occurred: {e}"
        
        # Display AI message
        st.session_state.messages.append({"role": "bot", "content": ai_response})
        show_message(ai_response, is_user=False)

# Add the footer at the end of the script
st.markdown("""
<div class="footer">
    Created by Vasanth Kumar S
</div>
""", unsafe_allow_html=True)