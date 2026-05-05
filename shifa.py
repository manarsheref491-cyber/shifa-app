
import json
import os

st.set_page_config(page_title="MedVerse", layout="wide")

# تحميل البيانات
DATA_FILE = "data.json"

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

with open(DATA_FILE, "r") as f:
    bookings = json.load(f)

# Sidebar
st.sidebar.title("📊 MedVerse")
menu = st.sidebar.radio("Menu", ["Dashboard", "Booking", "AI Doctor"])

# ================= Dashboard =================
if menu == "Dashboard":
    st.title("💰 MedVerse Revenue Edition")

    col1, col2, col3 = st.columns(3)

    col1.metric("👨‍⚕️ عدد الحجوزات", len(bookings))
    col2.metric("💵 إجمالي الإيرادات", sum([b["price"] for b in bookings]) if bookings else 0)
    col3.metric("⭐ التقييم", "99%")

    st.subheader("📋 آخر الحجوزات")
    st.write(bookings)

# ================= Booking =================
elif menu == "Booking":
    st.title("🏥 Patient Booking System")

    name = st.text_input("Patient Name")
    doctor = st.selectbox("Choose Doctor", ["Dr Ahmed", "Dr Ali", "Dr Sara"])
    price = st.number_input("Booking Price", value=300)

    if st.button("Book Now"):
        if name:
            new_booking = {
                "name": name,
                "doctor": doctor,
                "price": price
            }
            bookings.append(new_booking)

            with open(DATA_FILE, "w") as f:
                json.dump(bookings, f)

            st.success("✅ تم الحجز بنجاح")
        else:
            st.error("❌ اكتب اسم المريض")

# ================= AI Doctor =================
elif menu == "AI Doctor":
    st.title("🤖 الطبيب الذكي")

    user_input = st.text_input("اكتب شكوتك")

    if st.button("تشخيص"):
        if user_input:
            if "صداع" in user_input:
                reply = "💊 ممكن يكون إجهاد أو قلة نوم"
            elif "برد" in user_input:
                reply = "🤧 نزلة برد - اشرب سوائل"
            elif "معدة" in user_input:
                reply = "🍽️ اضطراب معدة - خفف أكل تقيل"
            else:
                reply = "👨‍⚕️ يفضل استشارة دكتور"

            st.success(reply)
        else:
            st.error("❌ اكتب شكوتك الأول")
