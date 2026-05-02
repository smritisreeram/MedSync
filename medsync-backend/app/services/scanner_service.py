import os
from PIL import Image
from google import genai
from dotenv import load_dotenv
import json

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_prescription(image_path):
    """
    Takes a local image path, sends it to Gemini, and returns structured JSON.
    """
    img = Image.open(image_path)
    
    prompt = """
    ACT AS: An expert medical pharmacist.
    TASK: Extract medication data from this prescription image.
    
    CRITICAL INSTRUCTIONS FOR 'schedule':
    You must map medical abbreviations to these specific phrases:
    - If you see "TDS", "TID", or "1-1-1", write "Three times a day".
    - If you see "BID", "BD", or "1-0-1", write "Twice a day".
    - If you see "OD", "Daily", or "1-0-0", write "Once a day".
    - If you see "Q6H", write "Every 6 hours".
    - If you see "SOS" or "PRN", write "As needed".
    
    If the handwriting is messy, use your medical knowledge to identify the drug name.
    
    OUTPUT FORMAT: Return ONLY a JSON list of objects.
    Example: [{"medication_name": "Calpol", "dosage": "500mg", "schedule": "Every 6 hours"}]
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[prompt, img]
    )
    clean_text = response.text.replace('```json', '').replace('```', '').strip()
    return json.loads(clean_text)