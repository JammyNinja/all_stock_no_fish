import streamlit as st
import requests

from api_helpers import get_profile, get_stats
from api_helpers import test_change, test_bq

st.set_page_config(page_title="All Stock No Fish", page_icon="♟️")

st.title("All Stock No Fish")
st.divider()

username = st.text_input("Chess.com username")

if username:
    try:
        with st.spinner("Loading..."):
            profile = get_profile(username)
            stats   = get_stats(username)

    except requests.HTTPError as e:
        if e.response.status_code == 404:
            st.error(f"User '{username}' not found on Chess.com.")
        else:
            st.error("Something went wrong. Try again.")
        st.stop()

    # Profile
    col1, col2 = st.columns([1, 4])
    with col1:
        if profile.get("avatar"):
            st.image(profile["avatar"], width=80)
    with col2:
        st.subheader(profile.get("name") or profile["username"])
        st.caption(f"@{profile['username']}")

    st.divider()

    # Ratings
    TIME_CONTROLS = [
        ("chess_rapid",    "Rapid"),
        ("chess_blitz",    "Blitz"),
        ("chess_bullet",   "Bullet"),
        ("chess_daily",    "Daily"),
    ]

    cols = st.columns(2)
    for i, (key, label) in enumerate(TIME_CONTROLS):
        tc = stats.get(key)
        if tc and tc.get("last"):
            rating = tc["last"]["rating"]
            best   = tc.get("best", {}).get("rating", "—")
            record = tc.get("record", {})
            w, l, d = record.get("win", 0), record.get("loss", 0), record.get("draw", 0)
            with cols[i % 2]:
                st.metric(label=label, value=rating, help=f"Best: {best}")
                st.caption(f"W {w} / L {l} / D {d}")

st.divider()
st.subheader("Debug")

if st.button("Test BigQuery Connection"):
    with st.spinner("Connecting to BigQuery..."):
        response = test_bq()
        st.write("running in mode:", response['mode'])
        st.success(f"Connected! Datasets found: {', '.join(response['datasets_available']) or 'none'}")
