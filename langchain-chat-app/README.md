## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- AWS credentials configured
- Python 3.11+ (for local development)

### Environment Setup

1. **Configure AWS Credentials**
   ```bash
   # Set your AWS credentials
   export AWS_ACCESS_KEY_ID=your_access_key
   export AWS_SECRET_ACCESS_KEY=your_secret_key
   export AWS_DEFAULT_REGION=us-east-1
   ```

2. **Update Agent ARN**
   
   Edit `streamlit_app/app.py` and update the `AGENT_ARN` variable with your Bedrock agent ARN:
   ```python
   AGENT_ARN = "arn:aws:bedrock-agentcore:us-east-1:YOUR_ACCOUNT:runtime/YOUR_AGENT"
   ```

### Running with Docker

1. **Build and run the services**
   ```bash
   # Build the agent service
   cd agent_service
   docker build -t bedrock-agent .
   docker run -p 8000:8000 -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -e AWS_DEFAULT_REGION bedrock-agent
   
   # Build and run the streamlit app (in another terminal)
   cd streamlit_app
   docker build -t streamlit-chat .
   docker run -p 8501:8501 -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -e AWS_DEFAULT_REGION streamlit-chat
   ```

2. **Access the application**
   - Open your browser to `http://localhost:8501`
   - Start chatting with the AI assistant!

### Local Development

1. **Install dependencies**
   ```bash
   # Agent service
   cd agent_service
   pip install -r requirements.txt
   
   # Streamlit app
   cd streamlit_app
   pip install -r requirements.txt
   ```

2. **Run the services**
   ```bash
   # Terminal 1: Start the agent service
   cd agent_service
   python app.py
   
   # Terminal 2: Start the streamlit app
   cd streamlit_app
   streamlit run app.py
   ```

## � ConfigurSation

### Agent Service Configuration

The agent service uses the following environment variables:

- `PORT` - Service port (default: 8080)
- `AWS_DEFAULT_REGION` - AWS region (default: us-east-1)
- `AWS_ACCESS_KEY_ID` - AWS access key
- `AWS_SECRET_ACCESS_KEY` - AWS secret key

### Streamlit App Configuration

Update the `AGENT_ARN` in `streamlit_app/app.py` to match your AWS Bedrock agent:

```python
AGENT_ARN = "arn:aws:bedrock-agentcore:us-east-1:YOUR_ACCOUNT:runtime/YOUR_AGENT"
```

## 🛠️ API Endpoints

### Agent Service

- `POST /invoke` - Main agent invocation endpoint
- `POST /invocations` - Alternative invocation endpoint (AgentCore compatible)
- `GET /health` - Health check endpoint

### Request Format

```json
{
  "prompt": "Your question here",
  "inputText": "Alternative input field",
  "message": "Another input option"
}
```

### Response Format

```json
{
  "completion": "AI response text",
  "stopReason": "end_turn",
  "usage": {
    "inputTokens": 10,
    "outputTokens": 50
  }
}
```

## 🎨 UI Features

- **AWS-styled Design** - Professional AWS console appearance
- **Real-time Chat** - Smooth conversation flow
- **Message History** - Persistent chat session
- **Status Indicators** - Connection and error status
- **Responsive Layout** - Works on desktop and mobile

## 🔍 Troubleshooting

### Common Issues

1. **AWS Credentials Error**
   - Ensure AWS credentials are properly configured
   - Check that your AWS account has Bedrock access

2. **Agent ARN Issues**
   - Verify the AGENT_ARN is correct in `streamlit_app/app.py`
   - Ensure the agent exists in your AWS account

3. **Connection Errors**
   - Check that both services are running
   - Verify port configurations (8000 for agent, 8501 for streamlit)

### Logs

Both services provide detailed logging:

```bash
# View agent service logs
docker logs <agent-container-id>

# View streamlit logs
docker logs <streamlit-container-id>
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

