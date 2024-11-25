import streamlit as st
import ollama
import time
from datetime import datetime

# Must be the first Streamlit command
st.set_page_config(
    page_title="Ollama Chat",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern design
st.markdown("""
<style>
    /* Modern color scheme */
    :root {
        --primary-color: #1E1E1E;
        --secondary-color: #2D2D2D;
        --accent-color: #4A4A4A;
        --text-color: #FFFFFF;
    }
    
    /* Remove border radius */
    .stButton>button, .stSelectbox>div>div>select, 
    .stTextInput>div>div>input, .stSlider>div>div>div,
    .element-container, .stMarkdown, div[data-testid="stChatMessageContent"] {
        border-radius: 0 !important;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: var(--secondary-color);
        padding: 2rem 1rem;
    }
    
    /* Tab styling */
    .sidebar-tab {
        background-color: var(--secondary-color);
        padding: 1rem;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: background-color 0.3s;
        border-left: 4px solid transparent;
    }
    
    .sidebar-tab:hover {
        background-color: var(--accent-color);
    }
    
    .sidebar-tab.active {
        border-left-color: #00ADB5;
        background-color: var(--accent-color);
    }
    
    /* Chat message styling */
    div[data-testid="stChatMessageContent"] {
        background-color: var(--secondary-color) !important;
        border: none !important;
        padding: 1rem !important;
        margin-bottom: 1rem !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    }
    
    /* User message styling */
    [data-testid="stChatMessageContent"].user {
        background-color: var(--accent-color) !important;
    }
    
    /* Chat container */
    .chat-container {
        height: calc(100vh - 100px);
        overflow-y: auto;
        padding: 1rem;
        background-color: var(--primary-color);
    }
    
    /* Input box styling */
    .input-container {
        position: fixed;
        bottom: 0;
        left: 22rem;
        right: 2rem;
        padding: 1rem;
        background-color: var(--primary-color);
        border-top: 1px solid var(--accent-color);
    }
    
    /* Button styling */
    .stButton>button {
        width: 100%;
        background-color: var(--accent-color);
        color: var(--text-color);
        border: none;
        padding: 0.5rem;
        margin: 0.25rem 0;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #00ADB5;
        transform: translateY(-1px);
    }
    
    /* Conversation list styling */
    .conversation-list {
        margin-top: 1rem;
        border-top: 1px solid var(--accent-color);
        padding-top: 1rem;
    }
    
    .conversation-item {
        padding: 0.5rem;
        margin: 0.25rem 0;
        background-color: var(--secondary-color);
        cursor: pointer;
        transition: background-color 0.3s;
    }
    
    .conversation-item:hover {
        background-color: var(--accent-color);
    }
    
    /* Status indicators */
    .status-indicator {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-right: 0.5rem;
    }
    
    .status-connected {
        background-color: #4CAF50;
    }
    
    .status-disconnected {
        background-color: #F44336;
    }
    
    /* Model info styling */
    .model-info {
        padding: 1rem;
        background-color: var(--secondary-color);
        margin: 1rem 0;
    }
    
    /* Settings section styling */
    .settings-section {
        padding: 1rem;
        background-color: var(--secondary-color);
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_tab' not in st.session_state:
    st.session_state.current_tab = 'Chat'
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'conversations' not in st.session_state:
    st.session_state.conversations = []
if 'current_conversation' not in st.session_state:
    st.session_state.current_conversation = 0
if 'selected_model' not in st.session_state:
    st.session_state.selected_model = None
if 'temperature' not in st.session_state:
    st.session_state.temperature = 0.7

# Initialize Ollama connection
@st.cache_resource
def init_ollama():
    try:
        models = ollama.list()
        return [model.name for model in models.models]
    except Exception as e:
        st.error(f"Failed to connect to Ollama server: {str(e)}")
        return []

# Sidebar
with st.sidebar:
    st.title("🤖 Ollama Chat")
    
    # Main navigation tabs
    tabs = ['Chat', 'Settings', 'History']
    st.markdown("### Navigation")
    for tab in tabs:
        if st.button(
            tab,
            key=f"tab_{tab}",
            help=f"Switch to {tab} view",
            use_container_width=True,
            type="secondary" if st.session_state.current_tab != tab else "primary"
        ):
            st.session_state.current_tab = tab
            st.rerun()
    
    st.markdown("---")
    
    # Model selection and settings
    available_models = init_ollama()
    if available_models:
        st.markdown("### Model Settings")
        st.session_state.selected_model = st.selectbox("Select Model", available_models)
        st.session_state.temperature = st.slider("Temperature", 0.1, 2.0, st.session_state.temperature, 0.1)
        
        # Connection status
        st.markdown(
            f"""
            <div style='display: flex; align-items: center;'>
                <div class='status-indicator status-connected'></div>
                <span>Connected to Ollama</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div style='display: flex; align-items: center;'>
                <div class='status-indicator status-disconnected'></div>
                <span>Disconnected</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Conversations list
    st.markdown("### Conversations")
    if st.button("New Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.current_conversation = len(st.session_state.conversations)
        st.session_state.conversations.append([])
        st.rerun()
    
    # Display conversations
    for idx, conversation in enumerate(st.session_state.conversations):
        if st.button(
            f"Conversation {idx + 1}",
            key=f"conv_{idx}",
            use_container_width=True,
            type="secondary" if st.session_state.current_conversation != idx else "primary"
        ):
            st.session_state.current_conversation = idx
            st.session_state.messages = conversation
            st.rerun()

# Main content area
if st.session_state.current_tab == 'Chat':
    # Chat interface
    chat_container = st.container()
    
    with chat_container:
        # Display messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Message Ollama..."):
            if available_models and st.session_state.selected_model:
                # Display user message
                with st.chat_message("user"):
                    st.markdown(prompt)
                st.session_state.messages.append({"role": "user", "content": prompt})
                
                # Generate response
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    full_response = ""
                    
                    try:
                        for chunk in ollama.chat(
                            model=st.session_state.selected_model,
                            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                            stream=True,
                            options={"temperature": st.session_state.temperature}
                        ):
                            if chunk and "content" in chunk.get("message", {}):
                                full_response += chunk["message"]["content"]
                                message_placeholder.markdown(full_response + "▌")
                        
                        message_placeholder.markdown(full_response)
                        st.session_state.messages.append({"role": "assistant", "content": full_response})
                        
                        # Update conversation history
                        st.session_state.conversations[st.session_state.current_conversation] = st.session_state.messages
                        
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                        st.info("Please ensure Ollama server is running")
            else:
                st.error("Please ensure Ollama is running and a model is selected")

elif st.session_state.current_tab == 'Settings':
    st.markdown("### Advanced Settings")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Model Configuration")
        st.markdown(f"Current model: {st.session_state.selected_model if st.session_state.selected_model else 'None'}")
        st.markdown(f"Temperature: {st.session_state.temperature}")
    
    with col2:
        st.markdown("#### System Status")
        st.markdown("Connected: " + ("Yes" if available_models else "No"))
        st.markdown("Available models: " + (", ".join(available_models) if available_models else "None"))

elif st.session_state.current_tab == 'History':
    st.markdown("### Chat History")
    
    if st.session_state.conversations:
        for idx, conversation in enumerate(st.session_state.conversations):
            with st.expander(f"Conversation {idx + 1}"):
                for message in conversation:
                    st.markdown(f"**{message['role']}**: {message['content']}")
    else:
        st.info("No conversation history yet. Start chatting to create some!")

# Footer
st.markdown(
    """
    <div style='position: fixed; bottom: 0; left: 0; right: 0; background-color: var(--secondary-color); padding: 0.5rem; text-align: center; font-size: 0.8rem;'>
        Made with Streamlit and Ollama
    </div>
    """,
    unsafe_allow_html=True
)
