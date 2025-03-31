import os
import shutil
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse
from typing import Optional
import uuid
from .processor import process_question

app = FastAPI(title="TDS Solver API")

@app.get("/")
def read_root():
    return {"message": "Welcome to the TDS Solver API", "usage": "POST /api/ with question and optional file"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/api/")
async def solve_question(
    question: str = Form(...),
    file: Optional[UploadFile] = File(None)
):
    try:
        file_path = None
        
        # Process file if provided
        if file and file.filename:
            # Create a unique filename
            unique_id = uuid.uuid4().hex
            file_extension = os.path.splitext(file.filename)[1]
            file_path = f"uploads/{unique_id}{file_extension}"
            
            # Save the file
            os.makedirs("uploads", exist_ok=True)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        
        # Process the question and file
        answer = process_question(question, file_path)
        
        # Return the answer
        return JSONResponse(content={"answer": answer})
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"An error occurred: {str(e)}"}
        )

# For local testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)