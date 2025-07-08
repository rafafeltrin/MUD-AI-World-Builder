import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Retrieve the Gemini API key from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Basic validation to ensure the key is loaded
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found. Please set it in your .env file.")