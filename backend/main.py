import os
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from all_stock_no_fish.sources import get_profile, get_stats

app = FastAPI(title="All Stock No Fish API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tighten this to your Streamlit URL in production
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/player/{username}")
def player_profile(username: str):
    try:
        return get_profile(username)
    except requests.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@app.get("/player/{username}/stats")
def player_stats(username: str):
    try:
        return get_stats(username)
    except requests.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


#wut
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
