import requests
import streamlit as st
import os

if os.environ.get("MODE", "not_local") == "local":
    BACKEND_API_BASE = "http://localhost:8000"
else:
    BACKEND_API_BASE = st.secrets.get("BACKEND_API")

def get_profile(username):
    profile_url = f"{BACKEND_API_BASE}/player/{username}"
    result = requests.get(profile_url)
    result.raise_for_status()

    return result.json()

def get_stats(username):
    profile_stats_url = f"{BACKEND_API_BASE}/player/{username}/stats"
    result = requests.get(profile_stats_url)
    result.raise_for_status()

    return result.json()

def test_change():
    url = BACKEND_API_BASE + "/test_change"
    r = requests.get(url)
    r.raise_for_status()

    return r.json()

def test_bq():
    print("running in mode:", os.environ.get("MODE", None))
    url = BACKEND_API_BASE + "/test_bq"
    r = requests.get(url)
    r.raise_for_status()
    
    return r.json()
