import os
import zipfile
import pandas as pd
import io
import json
import numpy as np
import re
from typing import Dict, Any, Optional, List

# Create uploads directory if it doesn't exist
os.makedirs("uploads", exist_ok=True)

def extract_zip_file(file_path: str) -> Dict[str, str]:
    """
    Extract contents of a zip file and return paths to extracted files
    """
    extract_dir = os.path.splitext(file_path)[0]
    os.makedirs(extract_dir, exist_ok=True)
    
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    
    extracted_files = {}
    for root, _, files in os.walk(extract_dir):
        for file in files:
            file_path = os.path.join(root, file)
            file_ext = os.path.splitext(file)[1].lower()
            extracted_files[file] = file_path
    
    return extracted_files

def read_csv_file(file_path: str) -> pd.DataFrame:
    """
    Read a CSV file and return a pandas DataFrame
    """
    return pd.read_csv(file_path)

def clean_temp_files(file_paths: List[str]):
    """
    Clean up temporary files and directories
    """
    for path in file_paths:
        if os.path.isfile(path):
            try:
                os.remove(path)
            except Exception as e:
                print(f"Error removing file {path}: {e}")
        elif os.path.isdir(path):
            try:
                for root, dirs, files in os.walk(path, topdown=False):
                    for file in files:
                        os.remove(os.path.join(root, file))
                    for dir in dirs:
                        os.rmdir(os.path.join(root, dir))
                os.rmdir(path)
            except Exception as e:
                print(f"Error removing directory {path}: {e}")