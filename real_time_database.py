import streamlit as st
import os
import firebase_admin
from firebase_admin import credentials, db
from dotenv import load_dotenv
import time  # เพิ่มการนำเข้า time

# โหลดข้อมูลจาก .env ที่จัดเก็บใน GitHub Secrets
load_dotenv()

# เอาคีย์ Firebase จาก GitHub Secrets
firebase_key_json = os.getenv("FIREBASE_SERVICE_ACCOUNT")

# เปลี่ยนไฟล์ JSON จาก string เป็นไฟล์ชั่วคราว
import json
from tempfile import NamedTemporaryFile

# สร้างไฟล์ชั่วคราวเพื่อใช้เชื่อมต่อ Firebase
with NamedTemporaryFile(delete=False) as temp_file:
    temp_file.write(json.loads(firebase_key_json))
    temp_file_name = temp_file.name

# เชื่อมต่อ Firebase
cred = credentials.Certificate(temp_file_name)
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://computer-science-34b7a-default-rtdb.asia-southeast1.firebasedatabase.app/"
})
# อ้างอิงไปยัง Firebase Database
chat_ref = db.reference("/chat_messages")

# ตั้งค่า UI ของ Chat App
st.title("💬 Real-time Chat App")
username = st.text_input("👤 Your name", key="username")

# แสดงข้อความแชทแบบ Real-time
st.subheader("📢 Chat room")

# ฟังก์ชันในการดึงข้อความจาก Firebase และแสดงบน UI
def show_messages():
    messages = chat_ref.get()
    if messages:
        for key, msg in messages.items():
            st.write(f"**{msg['username']}**: {msg['message']}")

show_messages()  # เรียกฟังก์ชันแสดงข้อความ

# ส่งข้อความ
message = st.text_input("💬 message...", key="message")

if st.button("🚀 send"):
    if username and message:
        chat_ref.push({
            "username": username,
            "message": message,
            "timestamp": time.time()
        })
        st.experimental_rerun()  # รีเฟรชหน้าจออัตโนมัติ
    else:
        st.warning("⚠️ Please fill in your name and message before sending!")

# ล้างแชท (หาก username เป็น "aekky")
if username == "aekky":
    if st.button("🗑️ ล้างแชท"):
        chat_ref.set({})
        st.experimental_rerun()
