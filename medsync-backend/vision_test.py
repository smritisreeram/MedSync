import os
from pathlib import Path
from PIL import Image
from dotenv import load_dotenv
from google import genai
import json

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

img_path = os.path.join(os.path.dirname(__file__), 'image.png')

def analyze_prescription(path):

    img = Image.open(path)
    
    prompt = """
    You are a medical prescription assistant. 
    Look at this image and extract the medications. 
    For each medication, find the name, dosage, and frequency/schedule.
    
    Return the data ONLY as a JSON list. 
    If handwriting is messy, use your medical knowledge to make the most likely guess.
    
    Format:
    [
      {"medication_name": "Name", "dosage": "Amount", "schedule": "Frequency"}
    ]
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[prompt, img]
    )

    clean_text = response.text.replace('```json', '').replace('```', '').strip()
    return json.loads(clean_text)

if not os.path.exists(img_path):
    print(f" Image not found at {img_path}")
else:
    try:
        results = analyze_prescription(img_path)
        print("\n--- 💊 EXTRACTED MEDICATIONS ---")
        print(json.dumps(results, indent=2))
    except Exception as e:
        print(f"❌ Error: {e}")