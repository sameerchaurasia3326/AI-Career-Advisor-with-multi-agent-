from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import asyncio
import uvicorn
from pathlib import Path
import logging
import warnings

# Import your main CrewAI system
from main import career_advisor_crew

# Suppress warnings
warnings.filterwarnings('ignore')
logging.getLogger("httpx").setLevel(logging.WARNING)

app = FastAPI(
    title="AI Career Advisor API",
    description="AI-powered career guidance system using CrewAI",
    version="1.0.0"
)

# Serve static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="."), name="static")

class CareerRequest(BaseModel):
    user_info: str

class CareerResponse(BaseModel):
    report: str
    success: bool
    message: str

@app.get("/")
async def read_root():
    """Serve the demo landing page first"""
    return FileResponse('demo.html')

@app.get("/app")
async def read_app():
    """Serve the main application"""
    return FileResponse('index.html')

@app.post("/api/generate-career-report", response_model=CareerResponse)
async def generate_career_report(request: CareerRequest):
    """
    Generate a comprehensive career report using the CrewAI system
    """
    try:
        print(f"🚀 Starting career analysis for user...")
        print(f"📋 User Info Preview: {request.user_info[:100]}...")
        
        # Prepare inputs for CrewAI
        inputs = {
            "user_info": request.user_info
        }
        
        # Run the CrewAI system with robust error handling
        print("🤖 Initializing AI agents with robust error handling...")
        result = career_advisor_crew.kickoff(inputs=inputs)
        
        # Convert result to string if it's not already
        report_text = str(result)
        
        print("✅ Career report generated successfully!")
        print(f"📄 Report length: {len(report_text)} characters")
        
        return CareerResponse(
            report=report_text,
            success=True,
            message="Career report generated successfully!"
        )
        
    except Exception as e:
        print(f"❌ Error generating career report: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to generate career report: {str(e)}"
        )

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "AI Career Advisor API is running",
        "agents": 7,
        "apis_configured": 5
    }

@app.get("/api/status")
async def get_system_status():
    """Get system status and configuration"""
    return {
        "system": "AI Career Advisor",
        "version": "1.0.0",
        "agents": [
            "User Profiler Agent",
            "Career Exploration Agent", 
            "Skill Development Agent",
            "Job Market Insights Agent",
            "Roadmap Strategy Agent",
            "Learning Resource Agent",
            "Report Generation Agent"
        ],
        "llm_providers": [
            "Google Gemini",
            "Perplexity",
            "OpenRouter Claude (Primary)",
            "OpenRouter Claude (Secondary)"
        ],
        "search_provider": "Serper Dev",
        "status": "operational"
    }

if __name__ == "__main__":
    print("🚀 Starting AI Career Advisor Server...")
    print("📡 Server will be available at: http://localhost:8000")
    print("🌐 Open your browser and navigate to the URL above")
    print("=" * 60)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False,  # Set to True for development
        log_level="info"
    )
