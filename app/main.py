from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.receipts import router as receipts_router

# Create FastAPI instance
app = FastAPI(
    title="Receipt Splitter API",
    description="An async FastAPI backend for splitting receipts using Gemini AI and LangChain",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(receipts_router)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Main health check endpoint"""
    return {"status": "ok", "message": "Receipt Splitter API is running"}

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to Receipt Splitter API",
        "docs": "/docs",
        "health": "/health",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 