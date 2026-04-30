import easyocr
import os
import cv2
import numpy as np
from PIL import Image

# 1. Setup paths
base_path = os.path.dirname(os.path.abspath(__file__))
img_path = os.path.join(base_path, 'image.png')

def clean_image(path):
    # Read the image
    img = cv2.imread(path)
    
    # Step 1: Convert to Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Step 2: Adaptive Thresholding (Handles shadows/uneven light)
    # This turns the image into sharp black and white
    cleaned = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 11, 2
    )
    
    # Step 3: Denoising
    kernel = np.ones((1, 1), np.uint8)
    final = cv2.morphologyEx(cleaned, cv2.MORPH_OPEN, kernel)
    
    return final

if not os.path.exists(img_path):
    print("❌ Image not found")
else:
    print("🎨 OpenCV is cleaning the prescription...")
    processed_img = clean_image(img_path)
    
    # Save a preview so you can see if it looks better!
    cv2.imwrite(os.path.join(base_path, 'cleaned_preview.png'), processed_img)
    
    print("🚀 Starting AI Recognition on cleaned image...")
    reader = easyocr.Reader(['en'], gpu=False)
    results = reader.readtext(processed_img, detail=0)

    print("\n--- NEW OCR RESULTS ---")
    for text in results:
        print(f"📄 {text}")