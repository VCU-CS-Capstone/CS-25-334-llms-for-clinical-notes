import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("GROQ_API_KEY")

if key:
    print(f"API Key Loaded: {key[:10]}...")  # Print only part of the key for security
else:
    print("Error: API Key not loaded!")
