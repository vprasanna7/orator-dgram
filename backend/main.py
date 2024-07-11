from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Orator Backend is running"}

@app.get("/env-check")
async def env_check():
    return {
        "DAILY_ROOM_URL": os.getenv("DAILY_ROOM_URL", "Not set"),
        "DAILY_API_KEY": "Set" if os.getenv("DAILY_API_KEY") else "Not set",
        "DEEPGRAM_API_KEY": "Set" if os.getenv("DEEPGRAM_API_KEY") else "Not set"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)