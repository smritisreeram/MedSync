import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

# 1. Initialize the Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("Listing models that support content generation:\n")

# 2. Loop through and print model names
# We filter for 'generateContent' to find models that can process your image
for m in client.models.list():
    if "generateContent" in m.supported_actions:
        print(f"ID: {m.name} | Display Name: {m.display_name}")