import os
from fastapi import FastAPI, HTTPException
from supabase import create_client, Client
from dotenv import load_dotenv
from pydantic import BaseModel

# 1. Load variables from .env file
load_dotenv()

app = FastAPI()

# 2. Initialize Supabase Client
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# 3. Define the "Shape" of data we expect from the user (Schema)
class ProfileCreate(BaseModel):
    full_name: str
    role: str
    whatsapp_number: str

@app.post("/profiles")
def create_user_profile(profile: ProfileCreate):
    # This sends a "command" to Supabase to insert a new row
    try:
        data, count = supabase.table("profiles").insert({
            "full_name": profile.full_name,
            "role": profile.role,
            "whatsapp_number": profile.whatsapp_number
        }).execute()
        
        return {"message": "Profile created successfully!", "data": data}
    
    except Exception as e:
        # If something goes wrong (e.g. database is down), tell the user
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/profiles")
def get_all_profiles():
    # This asks Supabase: "Give me everything in the profiles table"
    response = supabase.table("profiles").select("*").execute()
    return {"members": response.data}