from fastapi import FastAPI
import openai

app = FastAPI()

openai.api_key = "YOUR_API_KEY"

@app.post("/analyze")
def analyze(data: dict):
    message = data["message"]

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "أنت طبيب ذكي تعطي نصائح طبية مبدئية فقط"},
            {"role": "user", "content": message}
        ]
    )
 as st
import openai
from gtts import gTTS

# API KEY
openai.api_key = "YOUR_API_KEY"

st.set_page_config(page_title="شفا", page_icon="🩺")

st.title("🩺 شفا - المعالج الطبي الذكي")

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الشات
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# إدخال المستخدم
user_input = st.chat_input("اكتب الأعراض...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        with st.spinner("جاري التحليل..."):
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "أنت طبيب يقدم نصائح مبدئية فقط"},
                    {"role": "user", "content": user_input}
                ]
            )

            reply = response['choices'][0]['message']['content']
            st.write(reply)

            # صوت
            tts = gTTS(reply, lang='ar')
            tts.save("reply.mp3")
            st.audio("reply.mp3")

            st.session_state.messages.append(
            
                {"role": "assistant", "content": reply}
                
            )
import streamlit as st
import openai
import json
import os
from gtts import gTTS

# API
openai.api_key = "YOUR_API_KEY"

# ملف المستخدمين
USER_FILE = "users.json"

def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

users = load_users()

# إعداد الصفحة
st.set_page_config(page_title="شفا", page_icon="🩺", layout="wide")

# 🎨 تصميم احترافي
st.markdown("""
<style>
body { direction: rtl; }
.stApp { background-color: #f0f2f6; }
.card {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
    margin: 10px;
}
.title {
    color: #008080;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "page" not in st.session_state:
    st.session_state.page = "login"

# 🟢 LOGIN
def login():
    st.markdown("<h1 class='title'>🩺 شفا</h1>", unsafe_allow_html=True)
    st.subheader("تسجيل الدخول")

    user = st.text_input("اسم المستخدم")
    pw = st.text_input("كلمة المرور", type="password")

    if st.button("دخول"):
        if user in users and users[user] == pw:
            st.session_state.logged_in = True
            st.session_state.username = user
            st.rerun()
        else:
            st.error("بيانات غلط")

    if st.button("إنشاء حساب"):
        st.session_state.page = "register"
        st.rerun()

# 🟢 REGISTER
def register():
    st.title("إنشاء حساب")

    new_user = st.text_input("اسم المستخدم")
    new_pass = st.text_input("كلمة المرور", type="password")

    if st.button("تسجيل"):
        if new_user in users:
            st.error("موجود")
        else:
            users[new_user] = new_pass
            save_users(users)
            st.success("تم")
            st.session_state.page = "login"
            st.rerun()

# 🟢 DASHBOARD
def dashboard():
    st.sidebar.title("🩺 شفا")
    st.sidebar.write(f"👤 {st.session_state.username}")

    choice = st.sidebar.radio("القائمة", ["الرئيسية", "الشات", "تسجيل خروج"])

    if choice == "الرئيسية":
        st.markdown("<h1 class='title'>لوحة التحكم</h1>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("<div class='card'>💬 عدد المحادثات<br><h2>10</h2></div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='card'>🧑‍⚕️ الحالات<br><h2>5</h2></div>", unsafe_allow_html=True)

        with col3:
            st.markdown("<div class='card'>⭐ التقييم<br><h2>4.5</h2></div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>👋 مرحبًا بك في شفا</div>", unsafe_allow_html=True)

    elif choice == "الشات":
        chat()

    elif choice == "تسجيل خروج":
        st.session_state.logged_in = False
        st.rerun()

# 🟢 CHAT
def chat():
    st.title("💬 الشات الطبي")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("اكتب الأعراض...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("assistant"):
            with st.spinner("جاري التحليل..."):
                response = openai.ChatCompletion.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "أنت طبيب يقدم نصائح مبدئية فقط"},
                        {"role": "user", "content": user_input}
                    ]
                )

                reply = response["choices"][0]["message"]["content"]
                st.write(reply)

                # صوت
                tts = gTTS(reply, lang='ar')
                tts.save("reply.mp3")
                st.audio("reply.mp3")

                st.session_state.messages.append(
                    {"role": "assistant", "content": reply}
                )

# تشغيل الصفحات
if not st.session_state.logged_in:
    if st.session_state.page == "login":
        login()
    else:
        register()
else:
    dashboard()
