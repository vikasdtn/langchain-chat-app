# Langchain Knowledge App on Amazon Bedrock AgentCore 

A streamlit chat application powered by Amazon Bedrock, Amazon Bedrock AgentCore, Amazon ECS and LangChain, featuring a Streamlit frontend and FastAPI backend service. 
While this application servers as a good demo to learn about how these service & framework works together, it can also be expanded to the following use cases where the application can download and build upon :
1. **Customer Support Systems** - Add knowledge bases, ticket creation, escalation workflows
2. **Internal Help Desks** - Integrate with company documentation, HR policies, IT procedures
3. **Sales Assistant Bots** - Connect to CRM systems, product catalogs, pricing engines
4. **Healthcare Assistant** - Add medical knowledge bases, patient data integration, HIPAA compliance
5. **Legal Research Tool** - Integrate case law databases, document analysis, citation management
6. **Educational Tutor** - Add curriculum content, progress tracking, personalized learning paths
7. **Document Q&A Systems** - Upload PDFs, integrate with SharePoint, add semantic search
8. **Wiki/Knowledge Base Chat** - Connect to Confluence, Notion, internal documentation
9. **Research Assistant** - Add academic databases, citation tools, research methodology guidance
10. **Data Analysis Helper** - Connect to databases, add visualization capabilities, reporting
11. **Meeting Assistant** - Add calendar integration, note-taking, action item tracking
12. **Image Analysis Chat** - Add computer vision capabilities, image upload/processing
13. **Voice-Enabled Assistant** - Integrate speech-to-text, text-to-speech capabilities
14. **Document Processing** - Add OCR, form extraction, automated data entry

NOTE: To be able to extend, ensure the following components are added - Frontend Enhancements (auth, multi tennancy, mobile responseivemenss), Backend Capabilities, and standard devops pipelines

## 🏗️ Architecture

This application follows a microservices architecture leveraging AWS services for AI-powered chat functionality:

![Architecture Diagram](https://github.com/vikasdtn/langchain-chat-app/blob/main/langchain-chat-app/arch.jpg)


## ✨ Features

- **AWS Bedrock Integration** - Powered by Claude 3.5 Sonnet model
- **Modern Chat Interface** - AWS-styled Streamlit frontend
- **Docker Support** - Containerized services for easy deployment
- **Real-time Chat** - Interactive conversation with AI assistant
- **AWS Authentication** - Secure integration with AWS services


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
└── README.md               # setup instructions
| README.md                 # This readme
```

