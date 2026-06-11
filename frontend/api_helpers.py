import requests
import streamlit as st

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
