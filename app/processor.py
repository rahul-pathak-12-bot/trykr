import os
from typing import Optional
from .utils import extract_zip_file, clean_temp_files
from .question_handlers import identify_question_type, handle_question

def process_question(question: str, file_path: Optional[str] = None) -> str:
    """
    Main function to process questions and return answers
    """
    # List to keep track of temporary files to clean up later
    temp_files = []
    
    if file_path:
        temp_files.append(file_path)
    
    try:
        # Identify what type of question we're dealing with
        question_type = identify_question_type(question)
        
        # Handle the question based on its type
        answer = handle_question(question, question_type, file_path)
        
        return answer
    
    finally:
        # Clean up temporary files
        if temp_files:
            clean_temp_files(temp_files)