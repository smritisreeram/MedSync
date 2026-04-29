from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "MedSync Kitchen is Open!",
        "status": "Ready to process prescriptions"
    }