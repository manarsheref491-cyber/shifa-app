
import streamlit as st
import json, os, tempfile
from geopy.distance import geodesic
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import folium
from openai import OpenAI
import firebase_admin
from firebase_admin import credentials, firestore
import stripe
from gtts import gTTS

st.set_page_config(page_title="Shifa Pro Max", layout="wide")

# ---------- API ----------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
stripe.api_key = st.secrets["STRIPE_SECRET_KEY"]

# ---------- Firebase --------- 


# ---------- STYLE ----------
st.markdown("""
<style>
html, body {background:#0e1117; color:white;}
section[data-testid="stSidebar"] {background:#111827;}
.metric {background:#1f2937; padding:15px; border-radius:12px; text-align:center;}
.chat-user {background:#2563eb; padding:10px; border-radius:10px; margin:5px;}
.chat-bot {background:#1f2937; padding:10px; border-radius:10px; margin:5px;}
</style>
""", unsafe_allow_html=True)

# ---------- LOGIN ----------
USERS = {"manar":"1111","admin":"1234"}
if "login" not in st.session_state:
    st.session_state.login=False

if not st.session_state.login:
    st.title("🔐 Login")
    u=st.text_input("Username")
    p=st.text_input("Password", type="password")

    if st.button("Login"):
        if u in USERS and USERS[u]==p:
            st.session_state.login=True
            st.rerun()
        else:
            st.error("❌ غلط")
    st.stop()

# ---------- SIDEBAR ----------
st.sidebar.title("🚀 Shifa Pro Max")
menu = st.sidebar.radio("Menu",[
    "Dashboard","Doctors","Add Doctor","Bookings",
    "AI Doctor","Voice AI","Hospitals","Payment","Settings"
])

# ---------- DASHBOARD ----------
if menu=="Dashboard":
    st.title("📊 Dashboard")
    bookings = list(db.collection("bookings").stream())
    st.metric("عدد الحجوزات", len(bookings))

# ---------- ADD DOCTOR ----------
elif menu=="Add Doctor":
    st.title("➕ إضافة دكتور")

    name=st.text_input("اسم الدكتور")
    spec=st.text_input("التخصص")
    loc=st.text_input("المكان")
    phone=st.text_input("الهاتف")

    times=st.multiselect("المواعيد",["10","12","2","4","6"])

    if st.button("إضافة"):
        db.collection("doctors").add({
            "name":name,
            "specialty":spec,
            "location":loc,
            "phone":phone,
            "rating":0,
            "times":times
        })
        st.success("تم")

# ---------- DOCTORS ----------
elif menu=="Doctors":
    st.title("👨‍⚕️ الدكاترة")

    docs=db.collection("doctors").stream()

    for doc in docs:
        d=doc.to_dict()
        doc_id=doc.id

        st.write(d["name"],"⭐",d.get("rating",0))

        if d.get("times"):
            t=st.selectbox("ميعاد",d["times"],key=doc_id)

            if st.button("احجز",key="b"+doc_id):
                db.collection("bookings").add({
                    "doctor":d["name"],
                    "time":t
                })
                st.success("تم الحجز")

        r=st.slider("قيم",1,5,key="r"+doc_id)
        if st.button("تقييم",key="rt"+doc_id):
            new=(d.get("rating",0)+r)/2
            db.collection("doctors").document(doc_id).update({"rating":new})

        st.markdown("---")

# ---------- BOOKINGS ----------
elif menu=="Bookings":
    st.title("📋 الحجوزات")
    data=db.collection("bookings").stream()
    for d in data:
        st.write(d.to_dict())

# ---------- AI ----------
elif menu=="AI Doctor":
    st.title("🤖 AI")

    q=st.text_input("اكتب سؤالك")

    if st.button("Send"):
        res=client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content":q}]
        )
        st.success(res.choices[0].message.content)

# ---------- VOICE ----------
elif menu=="Voice AI":
    st.title("🎤 Voice")

    txt=st.text_input("نص")

    if st.button("تشغيل"):
        tts=gTTS(txt,lang='ar')
        with tempfile.NamedTemporaryFile(delete=False,suffix=".mp3") as f:
            tts.save(f.name)
            st.audio(f.name)

# ---------- MAP ----------
elif menu=="Hospitals":
    st.title("🗺️ مستشفيات")

    loc=get_geolocation()

    if loc:
        lat=loc["coords"]["latitude"]
        lon=loc["coords"]["longitude"]

        m=folium.Map(location=[lat,lon],zoom_start=13)
        folium.Marker([lat,lon]).add_to(m)

        st_folium(m)

# ---------- PAYMENT ----------
elif menu=="Payment":
    st.title("💳 دفع")

    if st.button("ادفع"):
        session=stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data":{
                    "currency":"usd",
                    "product_data":{"name":"service"},
                    "unit_amount":1000
                },
                "quantity":1
            }],
            mode="payment",
            success_url="https://success.com",
            cancel_url="https://cancel.com"
        )
        st.write(session.url)

# ---------- SETTINGS ----------
elif menu=="Settings":
    st.title("⚙️ Settings")
    st.write("جاهز")
import json, os, tempfile
from geopy.distance import geodesic
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import folium
from openai import OpenAI
import firebase_admin
from firebase_admin import credentials, firestore
import stripe
from gtts import gTTS

st.set_page_config(page_title="Shifa Pro Max", layout="wide")

# ---------- API ----------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
stripe.api_key = st.secrets["STRIPE_SECRET_KEY"]

# ---------- Firebase ----------
if not firebase_admin._apps:
    cred = credentials.Certificate(json.loads(st.secrets["FIREBASE_CRED"]))
    firebase_admin.initialize_app(cred)
db = firestore.client()

# ---------- STYLE ----------
st.markdown("""
<style>
html, body {background:#0e1117; color:white;}
section[data-testid="stSidebar"] {background:#111827;}
.metric {background:#1f2937; padding:15px; border-radius:12px; text-align:center;}
.chat-user {background:#2563eb; padding:10px; border-radius:10px; margin:5px;}
.chat-bot {background:#1f2937; padding:10px; border-radius:10px; margin:5px;}
</style>
""", unsafe_allow_html=True)

# ---------- LOGIN ----------
USERS = {"manar":"1111","admin":"1234"}
if "login" not in st.session_state:
    st.session_state.login=False

if not st.session_state.login:
    st.title("🔐 Login")
    u=st.text_input("Username")
    p=st.text_input("Password", type="password")

    if st.button("Login"):
        if u in USERS and USERS[u]==p:
            st.session_state.login=True
            st.rerun()
        else:
            st.error("❌ غلط")
    st.stop()

# ---------- SIDEBAR ----------
st.sidebar.title("🚀 Shifa Pro Max")
menu = st.sidebar.radio("Menu",[
    "Dashboard","Doctors","Add Doctor","Bookings",
    "AI Doctor","Voice AI","Hospitals","Payment","Settings"
])

# ---------- DASHBOARD ----------
if menu=="Dashboard":
    st.title("📊 Dashboard")
    bookings = list(db.collection("bookings").stream())
    st.metric("عدد الحجوزات", len(bookings))

# ---------- ADD DOCTOR ----------
elif menu=="Add Doctor":
    st.title("➕ إضافة دكتور")

    name=st.text_input("اسم الدكتور")
    spec=st.text_input("التخصص")
    loc=st.text_input("المكان")
    phone=st.text_input("الهاتف")

    times=st.multiselect("المواعيد",["10","12","2","4","6"])

    if st.button("إضافة"):
        db.collection("doctors").add({
            "name":name,
            "specialty":spec,
            "location":loc,
            "phone":phone,
            "rating":0,
            "times":times
        })
        st.success("تم")

# ---------- DOCTORS ----------
elif menu=="Doctors":
    st.title("👨‍⚕️ الدكاترة")

    docs=db.collection("doctors").stream()

    for doc in docs:
        d=doc.to_dict()
        doc_id=doc.id

        st.write(d["name"],"⭐",d.get("rating",0))

        if d.get("times"):
            t=st.selectbox("ميعاد",d["times"],key=doc_id)

            if st.button("احجز",key="b"+doc_id):
                db.collection("bookings").add({
                    "doctor":d["name"],
                    "time":t
                })
                st.success("تم الحجز")

        r=st.slider("قيم",1,5,key="r"+doc_id)
        if st.button("تقييم",key="rt"+doc_id):
            new=(d.get("rating",0)+r)/2
            db.collection("doctors").document(doc_id).update({"rating":new})

        st.markdown("---")

# ---------- BOOKINGS ----------
elif menu=="Bookings":
    st.title("📋 الحجوزات")
    data=db.collection("bookings").stream()
    for d in data:
        st.write(d.to_dict())

# ---------- AI ----------
elif menu=="AI Doctor":
    st.title("🤖 AI")

    q=st.text_input("اكتب سؤالك")

    if st.button("Send"):
        res=client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content":q}]
        )
        st.success(res.choices[0].message.content)

# ---------- VOICE ----------
elif menu=="Voice AI":
    st.title("🎤 Voice")

    txt=st.text_input("نص")

    if st.button("تشغيل"):
        tts=gTTS(txt,lang='ar')
        with tempfile.NamedTemporaryFile(delete=False,suffix=".mp3") as f:
            tts.save(f.name)
            st.audio(f.name)

# ---------- MAP ----------
elif menu=="Hospitals":
    st.title("🗺️ مستشفيات")

    loc=get_geolocation()

    if loc:
        lat=loc["coords"]["latitude"]
        lon=loc["coords"]["longitude"]

        m=folium.Map(location=[lat,lon],zoom_start=13)
        folium.Marker([lat,lon]).add_to(m)

        st_folium(m)

# ---------- PAYMENT ----------
elif menu=="Payment":
    st.title("💳 دفع")

    if st.button("ادفع"):
        session=stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data":{
                    "currency":"usd",
                    "product_data":{"name":"service"},
                    "unit_amount":1000
                },
                "quantity":1
            }],
            mode="payment",
            success_url="https://success.com",
            cancel_url="https://cancel.com"
        )
        st.write(session.url)

# ---------- SETTINGS ----------
elif menu=="Settings":
    st.title("⚙️ Settings")
    st.write("جاهز") 
    import streamlit as st
import json, os, tempfile
from geopy.distance import geodesic
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import folium
from openai import OpenAI
import firebase_admin
from firebase_admin import credentials, firestore
import stripe
from gtts import gTTS

st.set_page_config(page_title="Shifa Pro Max", layout="wide")

# ---------- API ----------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
stripe.api_key = st.secrets["STRIPE_SECRET_KEY"]

# ---------- Firebase ----------
if not firebase_admin._apps:
    cred = credentials.Certificate(json.loads(st.secrets["FIREBASE_CRED"]))
    firebase_admin.initialize_app(cred)
db = firestore.client()

# ---------- STYLE ----------
st.markdown("""
<style>
html, body {background:#0e1117; color:white;}
section[data-testid="stSidebar"] {background:#111827;}
.metric {background:#1f2937; padding:15px; border-radius:12px; text-align:center;}
.chat-user {background:#2563eb; padding:10px; border-radius:10px; margin:5px;}
.chat-bot {background:#1f2937; padding:10px; border-radius:10px; margin:5px;}
</style>
""", unsafe_allow_html=True)

# ---------- LOGIN ----------
USERS = {"manar":"1111","admin":"1234"}
if "login" not in st.session_state:
    st.session_state.login=False

if not st.session_state.login:
    st.title("🔐 Login")
    u=st.text_input("Username")
    p=st.text_input("Password", type="password")

    if st.button("Login"):
        if u in USERS and USERS[u]==p:
            st.session_state.login=True
            st.rerun()
        else:
            st.error("❌ غلط")
    st.stop()

# ---------- SIDEBAR ----------
st.sidebar.title("🚀 Shifa Pro Max")
menu = st.sidebar.radio("Menu",[
    "Dashboard","Doctors","Add Doctor","Bookings",
    "AI Doctor","Voice AI","Hospitals","Payment","Settings"
])

# ---------- DASHBOARD ----------
if menu=="Dashboard":
    st.title("📊 Dashboard")
    bookings = list(db.collection("bookings").stream())
    st.metric("عدد الحجوزات", len(bookings))

# ---------- ADD DOCTOR ----------
elif menu=="Add Doctor":
    st.title("➕ إضافة دكتور")

    name=st.text_input("اسم الدكتور")
    spec=st.text_input("التخصص")
    loc=st.text_input("المكان")
    phone=st.text_input("الهاتف")

    times=st.multiselect("المواعيد",["10","12","2","4","6"])

    if st.button("إضافة"):
        db.collection("doctors").add({
            "name":name,
            "specialty":spec,
            "location":loc,
            "phone":phone,
            "rating":0,
            "times":times
        })
        st.success("تم")

# ---------- DOCTORS ----------
elif menu=="Doctors":
    st.title("👨‍⚕️ الدكاترة")

    docs=db.collection("doctors").stream()

    for doc in docs:
        d=doc.to_dict()
        doc_id=doc.id

        st.write(d["name"],"⭐",d.get("rating",0))

        if d.get("times"):
            t=st.selectbox("ميعاد",d["times"],key=doc_id)

            if st.button("احجز",key="b"+doc_id):
                db.collection("bookings").add({
                    "doctor":d["name"],
                    "time":t
                })
                st.success("تم الحجز")

        r=st.slider("قيم",1,5,key="r"+doc_id)
        if st.button("تقييم",key="rt"+doc_id):
            new=(d.get("rating",0)+r)/2
            db.collection("doctors").document(doc_id).update({"rating":new})

        st.markdown("---")

# ---------- BOOKINGS ----------
elif menu=="Bookings":
    st.title("📋 الحجوزات")
    data=db.collection("bookings").stream()
    for d in data:
        st.write(d.to_dict())

# ---------- AI ----------
elif menu=="AI Doctor":
    st.title("🤖 AI")

    q=st.text_input("اكتب سؤالك")

    if st.button("Send"):
        res=client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content":q}]
        )
        st.success(res.choices[0].message.content)

# ---------- VOICE ----------
elif menu=="Voice AI":
    st.title("🎤 Voice")

    txt=st.text_input("نص")

    if st.button("تشغيل"):
        tts=gTTS(txt,lang='ar')
        with tempfile.NamedTemporaryFile(delete=False,suffix=".mp3") as f:
            tts.save(f.name)
            st.audio(f.name)

# ---------- MAP ----------
elif menu=="Hospitals":
    st.title("🗺️ مستشفيات")

    loc=get_geolocation()

    if loc:
        lat=loc["coords"]["latitude"]
        lon=loc["coords"]["longitude"]

        m=folium.Map(location=[lat,lon],zoom_start=13)
        folium.Marker([lat,lon]).add_to(m)

        st_folium(m)

# ---------- PAYMENT ----------
elif menu=="Payment":
    st.title("💳 دفع")

    if st.button("ادفع"):
        session=stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data":{
                    "currency":"usd",
                    "product_data":{"name":"service"},
                    "unit_amount":1000
                },
                "quantity":1
            }],
            mode="payment",
            success_url="https://success.com",
            cancel_url="https://cancel.com"
        )
        st.write(session.url)

# ---------- SETTINGS ----------
elif menu=="Settings":
    st.title("⚙️ Settings")
    st.write("جاهز")
