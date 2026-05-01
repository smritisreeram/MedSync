import os
from PIL import Image
from google import genai
from dotenv import load_dotenv
import json

load_dotenv()

# Initialize the Gemini Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_prescription(image_path):
    """
    Takes a local image path, sends it to Gemini, and returns structured JSON.
    """
    img = Image.open(image_path)
    
    prompt = """
    You are a medical prescription assistant. 
    Look at this image and extract the medications. 
    Return the data ONLY as a JSON list. 
    
    Format:
    [
      {"medication_name": "Name", "dosage": "Amount", "schedule": "Frequency"}
    ]
    """
    
    # We use the ID you found earlier (e.g., gemini-1.5-flash)
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=[prompt, img]
    )
    
    # Clean and parse JSON
    clean_text = response.text.replace('```json', '').replace('```', '').strip()
    return json.loads(clean_text)