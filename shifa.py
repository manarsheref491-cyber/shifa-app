import streamlit as st
import json, os
from geopy.distance import geodesic
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import folium
from openai import OpenAI

st.set_page_config(page_title="Shifa Pro", layout="wide")

# ---------- AI ----------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---------- STYLE ----------
st.markdown("""
<style>
html, body {background:#0e1117; color:white;}
.metric-card {background:#1f2937; padding:20px; border-radius:15px; text-align:center;}
.chat-user {background:#2563eb; padding:10px; border-radius:10px; margin:5px;}
.chat-bot {background:#1f2937; padding:10px; border-radius:10px; margin:5px;}
</style>
""", unsafe_allow_html=True)

# ---------- LOGIN ----------
USERS = {"manar": "1111", "admin": "1234"}

if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.title("🔐 Login")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        if u in USERS and USERS[u] == p:
            st.session_state.login = True
            st.rerun()
        else:
            st.error("❌ بيانات غلط")
    st.stop()

# ---------- DATA ----------
DATA_FILE = "data.json"
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

with open(DATA_FILE, "r") as f:
    bookings = json.load(f)

# ---------- SIDEBAR ----------
st.sidebar.title("🚀 Shifa Pro")
menu = st.sidebar.radio("Menu", ["Dashboard", "Bookings", "AI Doctor", "Hospitals"])

# ---------- DASHBOARD ----------
if menu == "Dashboard":
    st.title("📊 Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.markdown(f"<div class='metric-card'>👨‍⚕️<br>{len(bookings)}</div>", unsafe_allow_html=True)
    col2.markdown(f"<div class='metric-card'>💰<br>{sum([b['price'] for b in bookings]) if bookings else 0}</div>", unsafe_allow_html=True)
    col3.markdown("<div class='metric-card'>⭐<br>99%</div>", unsafe_allow_html=True)

# ---------- BOOKINGS ----------
elif menu == "Bookings":
    st.title("🏥 Booking")

    name = st.text_input("Patient Name")
    doctor = st.selectbox("Doctor", ["Dr Ahmed", "Dr Ali"])
    price = st.number_input("Price", value=300)

    if st.button("Book"):
        if name:
            bookings.append({"name": name, "doctor": doctor, "price": price})
            with open(DATA_FILE, "w") as f:
                json.dump(bookings, f)
            st.success("تم الحجز")
        else:
            st.error("اكتب الاسم")

# ---------- AI CHAT ----------
elif menu == "AI Doctor":
    st.title("🤖 AI Doctor (Real)")

    if "chat" not in st.session_state:
        st.session_state.chat = []

    for msg in st.session_state.chat:
        if msg["role"] == "user":
            st.markdown(f"<div class='chat-user'>👤 {msg['text']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-bot'>🤖 {msg['text']}</div>", unsafe_allow_html=True)

    user_input = st.text_input("اكتب حالتك")

    if st.button("Send"):
        if user_input:
            st.session_state.chat.append({"role":"user","text":user_input})

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role":"system","content":"انت دكتور مساعد طبي ذكي"},
                    {"role":"user","content":user_input}
                ]
            )

            reply = response.choices[0].message.content

            st.session_state.chat.append({"role":"bot","text":reply})
            st.rerun()

# ---------- MAP ----------
elif menu == "Hospitals":
    st.title("🗺️ أقرب مستشفى")

    loc = get_geolocation()

    if loc:
        lat = loc["coords"]["latitude"]
        lon = loc["coords"]["longitude"]

        hospitals = [
            {"name":"Cairo Hospital","lat":30.05,"lon":31.23},
            {"name":"Nile Clinic","lat":30.03,"lon":31.24},
        ]

        nearest = None
        dist_min = 999

        for h in hospitals:
            d = geodesic((lat,lon),(h["lat"],h["lon"])).km
            if d < dist_min:
                dist_min = d

  
