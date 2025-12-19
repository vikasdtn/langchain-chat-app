import streamlit as st
import requests
import os
from urllib.parse import quote
import logging
import boto3
import json
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
AGENT_ARN = "arn:aws:bedrock-agentcore:us-east-1:771400414730:runtime/langchain_kb-2F76dQB2Tv"

# Log the configuration
logger.info(f"Using AgentCore ARN: {AGENT_ARN}")

def call_agentcore_runtime(message):
    """Call AgentCore using the official boto3 method from the console"""
    try:
        # Use the exact method from AgentCore console
        client = boto3.client('bedrock-agentcore', region_name='us-east-1')
        
        # Use the exact payload format from the console
        payload = json.dumps({"prompt": message})
        
        response = client.invoke_agent_runtime(
            agentRuntimeArn=AGENT_ARN,
            runtimeSessionId='streamlit-session-001-12345678901234567890',  # Must be 33+ chars
            payload=payload
        )
        
        # Extract response
        response_body = response['response'].read()
        response_data = json.loads(response_body)
        
        logger.info(f"AgentCore response: {response_data}")
        
        # Return the response in the expected format
        if 'completion' in response_data:
            return {"completion": response_data['completion']}
        elif 'response' in response_data:
            return {"completion": response_data['response']}
        else:
            # Fallback: return the entire response as string
            return {"completion": str(response_data)}
            
    except Exception as e:
        logger.error(f"Error calling AgentCore: {str(e)}")
        return {"completion": f"Error calling AgentCore: {str(e)}"}



# AWS-styled custom CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #232F3E 0%, #1a242f 100%);
    }
    
    .main .block-container {
        padding-top: 2rem;
        max-width: 1200px;
    }
    
    /* Header styling */
    .aws-header {
        background: #232F3E;
        padding: 1rem 2rem;
        border-bottom: 3px solid #FF9900;
        margin: -1rem -1rem 2rem -1rem;
        display: flex;
        align-items: center;
    }
    
    .aws-logo {
        font-size: 28px;
        font-weight: bold;
        color: #FF9900;
        margin-right: 1rem;
    }
    
    .aws-title {
        font-size: 24px;
        color: #FFFFFF;
        font-weight: 500;
    }
    
    .aws-subtitle {
        color: #AAB7B8;
        font-size: 14px;
        margin-left: 1rem;
    }
    
    /* Chat container */
    .chat-container {
        background: #FFFFFF;
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
        margin-bottom: 1rem;
    }
    
    /* Message styling */
    .user-message {
        background: #FF9900;
        color: #FFFFFF;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        margin-left: 20%;
        border-bottom-right-radius: 4px;
    }
    
    .assistant-message {
        background: #F7F9FA;
        color: #232F3E;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        margin-right: 20%;
        border: 1px solid #D5DBDB;
        border-bottom-left-radius: 4px;
    }
    
    .message-label {
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 0.25rem;
        letter-spacing: 0.5px;
    }
    
    .user-label { color: #FF9900; }
    .assistant-label { color: #546E7A; }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border: 2px solid #D5DBDB;
        border-radius: 6px;
        padding: 0.75rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #FF9900;
        box-shadow: 0 0 0 1px #FF9900;
    }
    
    /* Button styling */
    .stButton > button {
        background: #FF9900;
        color: #FFFFFF;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        width: 100%;
    }
    
    .stButton > button:hover {
        background: #EC7211;
    }
    
    /* Status indicator */
    .status-connected {
        color: #16A34A;
        font-size: 13px;
        text-align: center;
        padding: 0.5rem;
    }
    
    .status-error {
        color: #DC2626;
        font-size: 13px;
        text-align: center;
        padding: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="aws-header">
    <div class="aws-logo">AWS</div>
    <div class="aws-title">Bedrock Chat Assistant</div>
    <div class="aws-subtitle">Powered by AWS AgentCore and LangChain </div>
</div>
""", unsafe_allow_html=True)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your AWS-powered assistant. Ask me anything, and I'll help you with general knowledge questions."}
    ]

# Chat container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display chat messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"""
        <div class="user-message">
            <div class="message-label user-label">You</div>
            <div>{message["content"]}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="assistant-message">
            <div class="message-label assistant-label">Assistant</div>
            <div>{message["content"]}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Input area
col1, col2 = st.columns([5, 1])

with col1:
    user_input = st.text_input("Type your question here...", key="user_input", label_visibility="collapsed")

with col2:
    send_button = st.button("Send", use_container_width=True)

# Handle message sending
if send_button and user_input:
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Call agent service
    try:
        with st.spinner("Thinking..."):
            # Call AgentCore directly with AWS authentication
            response = call_agentcore_runtime(user_input)
            agent_response = response.get("completion", "No response received")
            
            # Handle response
            st.session_state.messages.append({"role": "assistant", "content": agent_response})
            
            if "Error:" in agent_response:
                st.markdown('<div class="status-error">✗ Agent Service Error</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="status-connected">✓ Connected to Agent Service</div>', unsafe_allow_html=True)
    except requests.exceptions.RequestException as e:
        error_msg = f"Error: Cannot connect to agent service. Please check if the service is running."
        st.session_state.messages.append({"role": "assistant", "content": error_msg})
        st.markdown('<div class="status-error">✗ Connection Failed</div>', unsafe_allow_html=True)
    
    st.rerun()

# Connection status - AgentCore doesn't have health endpoint, so just show ready
st.markdown('<div class="status-connected">✓ AgentCore Ready</div>', unsafe_allow_html=True)