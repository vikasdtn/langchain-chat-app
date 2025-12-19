# AWS Bedrock Chat Assistant

A modern chat application powered by AWS Bedrock and LangChain, featuring a Streamlit frontend and FastAPI backend service.

## 🏗️ Architecture

This application follows a microservices architecture leveraging AWS services for AI-powered chat functionality:

![Architecture Diagram](https://github.com/vikasdtn/langchain-chat-app/blob/main/langchain-chat-app/arch.jpg))

The system consists of three main components working together:

### Data Flow:

1. **User** submits a question through the web interface
2. **AWS ECS Fargate (Streamlit Frontend)** receives and processes the user input
3. **Amazon Bedrock AgentCore** enriches the question with additional context and routing logic
4. **Amazon Bedrock** processes the enriched question using Claude 3.5 Sonnet LLM
5. **Response flows back** through the same path to deliver the AI-generated answer to the user

### Component Details:

- **AWS ECS Fargate (Streamlit Frontend)** (`streamlit_app/`)
  - Containerized web application running on AWS ECS Fargate
  - AWS-styled chat interface for user interactions
  - Manages session state and chat history
  - Communicates with AgentCore via AWS SDK

- **Amazon Bedrock AgentCore** (`agent_service/`)
  - Intelligent routing and question enrichment service
  - Processes and refines user questions before sending to LLM
  - Handles response formatting and error management
  - Integrates with AWS Bedrock using LangChain framework

- **Amazon Bedrock**
  - Fully managed AI service providing Claude 3.5 Sonnet model
  - Processes natural language queries and generates contextual responses
  - Scalable and secure cloud-based inference
  - Requires proper AWS IAM permissions and credentials

## 📁 Project Structure

```
├── agent_service/
│   ├── app.py              # FastAPI backend service
│   ├── Dockerfile          # Docker configuration
│   └── requirements.txt    # Python dependencies
├── streamlit_app/
│   ├── app.py              # Streamlit frontend
│   ├── Dockerfile          # Docker configuration
│   └── requirements.txt    # Python dependencies
└── README.md
```

## ✨ Features

- **AWS Bedrock Integration** - Powered by Claude 3.5 Sonnet model
- **Modern Chat Interface** - AWS-styled Streamlit frontend
- **Docker Support** - Containerized services for easy deployment
- **Real-time Chat** - Interactive conversation with AI assistant
- **AWS Authentication** - Secure integration with AWS services



**Built with ❤️ using AWS Bedrock, LangChain, FastAPI, and Streamlit**
