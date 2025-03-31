# api/index.py
from app.main import app

# This is important for Vercel serverless functions
# It must be named "app" for Vercel to detect it
app = app