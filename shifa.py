import streamlit as st
from geopy.distance import geodesic
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import folium

st.set_page_config(page_title="Shifa Pro", layout="wide")

# ---------- Login ----------
USERS = {"admin": "1234", "manar": "1111"}

if "logged" not in st.session_state:
    st.session_state.logged = False

if not st.session_state.logged:
    st.title("🔐 Login")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        if u in USERS and USERS[u] == p:
            st.session_state.logged = True
            st.success("تم تسجيل الدخول")
            st.rerun()
        else:
            st.error("❌ بيانات غلط")

    st.stop()

# ---------- Sidebar ----------
st.sidebar.title("🚀 Shifa Pro")
page = st.sidebar.radio("Menu", ["Dashboard", "Chat AI", "Hospitals"])

# ---------- Dashboard ----------
if page == "Dashboard":
    st.title("📊 Dashboard")
    st.success("أهلا بيكي 👑")

# ---------- Chat ----------
elif page == "Chat AI":
    st.title("🤖 AI Doctor")

    if "msgs" not in st.session_state:
        st.session_state.msgs = []

    for m in st.session_state.msgs:
        st.write(m)

    txt = st.text_input("اكتب حالتك")

    if st.button("Send"):
        if txt:
            if "صداع" in txt:
                reply = "💊 إجهاد أو قلة نوم"
            elif "برد" in txt:
                reply = "🤧 نزلة برد"
            else:
                reply = "👨‍⚕️ استشير دكتور"

            st.session_state.msgs.append("👤 " + txt)
            st.session_state.msgs.append("🤖 " + reply)

# ---------- Hospitals + Map ----------
elif page == "Hospitals":
    st.title("🏥 أقرب مستشفى (خريطة حقيقية)")

    loc = get_geolocation()

    if loc:
        user_lat = loc["coords"]["latitude"]
        user_lon = loc["coords"]["longitude"]

        st.success("📍 تم تحديد موقعك")

        hospitals = [
            {"name": "Cairo Hospital", "lat": 30.0500, "lon": 31.2333},
            {"name": "Nile Clinic", "lat": 30.0300, "lon": 31.2400},
            {"name": "Health Center", "lat": 30.0600, "lon": 31.2200},
        ]

        nearest = None
        min_dist = 999

        for h in hospitals:
            dist = geodesic((user_lat, user_lon), (h["lat"], h["lon"])).km
            if dist < min_dist:
                min_dist = dist
                nearest = h

        st.write(f"🏥 أقرب مستشفى: {nearest['name']}")
        st.write(f"📏 المسافة: {round(min_dist,2)} كم")

        # 🗺️ خريطة
        m = folium.Map(location=[user_lat, user_lon], zoom_start=13)

        folium.Marker([user_lat, user_lon], tooltip="You", icon=folium.Icon(color="blue")).add_to(m)
        folium.Marker([nearest["lat"], nearest["lon"]], tooltip=nearest["name"], icon=folium.Icon(color="red")).add_to(m)

        st_folium(m, width=700)

    else:
        st.warning("اضغطي Allow عشان نحدد موقعك")
