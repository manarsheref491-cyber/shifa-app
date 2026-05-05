import streamlit as st

st.set_page_config(page_title="Shifa AI", page_icon="💊")

st.title("💊 Shifa - AI Medical Assistant")
st.write("اكتب الأعراض اللي عندك وهنحاول نساعدك ❤️")

user_input = st.text_input("اكتب الأعراض هنا:")

if st.button("تشخيص مبدئي"):
    if user_input:
        if "صداع" in user_input:
            st.success("ممكن يكون إجهاد أو قلة نوم 😴")
        elif "برد" in user_input:
            st.success("ممكن نزلة برد 🤧")
        elif "معدة" in user_input:
            st.success("ممكن مشكلة في المعدة 🍽️")
        else:
            st.warning("يفضل استشارة دكتور 👨‍⚕️")
    else:
        st.error("اكتب الأعراض الأول!")

st.markdown("---")
st.caption("⚠️ هذا التطبيق لا يغني عن استشارة الطبيب")
