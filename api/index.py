# api/index.py
import sys
import traceback
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from typing import Optional

# Create the FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/")
async def process_question(
    question: str = Form(...),
    file: Optional[UploadFile] = File(None)
):
    try:
        # Process file if provided
        file_path = None
        if file and file.filename:
            # Save the file temporarily
            file_path = f"/tmp/{file.filename}"
            with open(file_path, "wb") as f:
                f.write(await file.read())
        
        # Simple echo response for testing
        response = {
            "question_received": question,
            "file_received": file.filename if file else None
        }
        
        # Clean up temporary file if created
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
        
        return response
    except Exception as e:
        # Log the full error details
        error_details = {
            "error": str(e),
            "traceback": traceback.format_exc()
        }
        print("ERROR:", error_details, file=sys.stderr)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "API is running. Use /api/ endpoint for questions."}