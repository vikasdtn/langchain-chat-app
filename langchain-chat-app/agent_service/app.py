from fastapi import FastAPI
from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage
import uvicorn
import os
import logging
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("=" * 80)
    logger.info("🚀 BEDROCK AGENTCORE SERVICE STARTED")
    logger.info("=" * 80)
    
    # Log environment information
    port = os.getenv("PORT", "8080")
    region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
    
    logger.info(f"📍 Service running on port: {port}")
    logger.info(f"🌍 AWS Region: {region}")
    logger.info(f"🔍 Environment variables:")
    for key, value in os.environ.items():
        if any(keyword in key.upper() for keyword in ['AGENT', 'PORT', 'AWS', 'BEDROCK']):
            logger.info(f"   {key}={value}")
    
    logger.info("📋 AgentCore endpoints:")
    logger.info("   POST /invoke - Main AgentCore invoke endpoint")
    logger.info("   POST /invocations - AgentCore alias endpoint")
    logger.info("   GET /health - Health check")
    logger.info("=" * 80)
    
    yield
    
    # Shutdown
    logger.info("🛑 BEDROCK AGENTCORE SERVICE SHUTTING DOWN")

app = FastAPI(title="Bedrock AgentCore Service", lifespan=lifespan)

def get_llm():
    return ChatBedrock(
        model_id="us.anthropic.claude-3-5-sonnet-20241022-v2:0",
        region_name="us-east-1",
        model_kwargs={
            "temperature": 0.7,
            "max_tokens": 2048
        }
    )

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/invoke")
@app.post("/invocations")  # AgentCore calls this endpoint
async def invoke_agent(request: dict):
    try:
        logger.info("=== INVOKE ENDPOINT CALLED ===")
        logger.info(f"Received invoke request: {request}")
        
        # Extract message from AgentCore request format
        message = (
            request.get("prompt", "") or 
            request.get("inputText", "") or 
            request.get("message", "") or
            request.get("input", "") or
            request.get("text", "")
        )
        logger.info(f"Extracted message: '{message}'")
        
        if not message:
            logger.error("No message found in request")
            logger.error(f"Available keys in request: {list(request.keys())}")
            # Try to extract any text-like field as fallback
            for key in request.keys():
                if isinstance(request[key], str) and len(request[key].strip()) > 0:
                    message = request[key]
                    logger.info(f"Using fallback field '{key}': {message}")
                    break
            
            if not message:
                return {
                    "completion": "Error: No input text found in request. Please provide 'input', 'prompt', 'inputText', or 'message' field.",
                    "stopReason": "error",
                    "usage": {"inputTokens": 0, "outputTokens": 0}
                }
        
        logger.info(f"Processing message: {message}")
        
        # Call Bedrock to get AI response
        try:
            llm = get_llm()
            messages = [
                SystemMessage(content="You are a helpful general knowledge assistant. Provide clear, accurate, and concise answers to questions."),
                HumanMessage(content=message)
            ]
            bedrock_response = llm.invoke(messages)
            ai_response = bedrock_response.content
            logger.info(f"Bedrock response: {ai_response[:100]}...")
        except Exception as bedrock_error:
            logger.error(f"Bedrock error: {str(bedrock_error)}")
            ai_response = f"I apologize, but I encountered an error while processing your request: {str(bedrock_error)}"
        
        logger.info(f"Returning response: {ai_response}")
        
        # Return in AgentCore expected format
        result = {
            "completion": ai_response,
            "stopReason": "end_turn",
            "usage": {
                "inputTokens": len(message.split()),
                "outputTokens": len(ai_response.split())
            }
        }
        
        logger.info(f"Final result: {result}")
        return result
        
    except Exception as e:
        logger.error(f"Error processing invoke request: {str(e)}")
        error_result = {
            "completion": f"Error: {str(e)}",
            "stopReason": "error",
            "usage": {"inputTokens": 0, "outputTokens": 0}
        }
        logger.info(f"Error result: {error_result}")
        return error_result

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    logger.info(f"🚀 Starting FastAPI server on port {port}")
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=port,
        log_level="info",
        access_log=True
    )