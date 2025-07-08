import os

import streamlit as st
import requests
import pydeck as pdk
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL")

st.title("AI Путівник по місту")

city = st.text_input("Місто, в якому ти хочеш знайти локації", placeholder="Наприклад, Львів")
text = st.text_input("Що ти хочеш знайти (музеї, фотозони, архітектура...)", placeholder="Опиши свої побажання")
exclude = st.text_input("Які локації виключити (через кому)", placeholder="Наприклад, Оперний театр, Ратуша")
num_places = st.number_input("Скільки локацій потрібно?", min_value=1, max_value=50, value=3, step=1)

if st.button("Знайти локації"):
    if not city:
        st.warning("Будь ласка, введи місто.")
    else:
        payload = {
            "city": city,
            "text": text,
            "exclude": [c.strip() for c in exclude.split(",") if c.strip()],
            "num_places": num_places
        }

        response = requests.post(f"{API_URL}/generate", json=payload)

        if response.status_code == 200:
            st.success("Ось, що я знайшов(ла):")

            data = response.json()
            locations = data["response_json"]

            coordinates = [
                {"lat": loc["coordinates"]["lat"], "lon": loc["coordinates"]["lng"]}
                for loc in locations
            ]

            if coordinates:
                midpoint = {
                    "lat": sum(p["lat"] for p in coordinates) / len(coordinates),
                    "lon": sum(p["lon"] for p in coordinates) / len(coordinates)
                }

                layer = pdk.Layer(
                    "ScatterplotLayer",
                    data=coordinates,
                    get_position="[lon, lat]",
                    get_color="[200, 30, 0, 160]",
                    get_radius=100,
                    pickable=True,
                )

                view_state = pdk.ViewState(
                    latitude=midpoint["lat"],
                    longitude=midpoint["lon"],
                    zoom=10,
                    pitch=0
                )

                st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))

            for loc in locations:
                st.markdown(f"**{loc['name']}**")
                st.markdown(loc["description"])
                st.markdown(f"_{loc['coordinates']['lat']}, {loc['coordinates']['lng']}_")
                st.markdown("---")

        else:
            st.error(f"Помилка: {response.status_code} — {response.text}")

st.markdown("---")

if st.button("Переглянути історію"):
    r = requests.get(f"{API_URL}/history")
    if r.status_code == 200:
        history = r.json()
        for q in history:
            st.markdown(f"### {q['city']} — {q['text']}")
            for loc in q["response_json"]:
                st.markdown(
                    f"- **{loc['name']}** — {loc['description']} (_{loc['coordinates']['lat']}, {loc['coordinates']['lng']}_)")
            st.markdown("---")
    else:
        st.error("Не вдалося завантажити історію.")
