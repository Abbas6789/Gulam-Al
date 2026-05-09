import streamlit as st
import pandas as pd
from supabase import create_client, Client
import datetime
import re
import uuid
import google.generativeai as genai
from gtts import gTTS
import os

# --- 1. تھیم اور ابتدائی سیٹ اپ ---
st.set_page_config(page_title="Ghulam AI V2.2", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    .stButton>button { background-color: #FFD700; color: black; font-weight: bold; border-radius: 12px; border: none; height: 45px; }
    .stTextInput>div>div>input { background-color: #111; color: white; border: 1px solid #333; }
    .user-card { background-color: #111; padding: 20px; border-radius: 15px; border: 1px solid #FFD700; margin-bottom: 10px; }
    .vip-timer { color: #FFD700; font-family: monospace; font-size: 1.2em; font-weight: bold; }
    .strike { text-decoration: line-through; color: #ff4b4b; margin-right: 10px; }
    .pkr-label { font-size: 0.8em; color: #888; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. سپربیس کنکشن (پاپ اپ لاجک) ---
if 'supabase_url' not in st.session_state:
    with st.container():
        st.title("🛡️ Ghulam AI Master Setup")
        st.info("پہلی بار چلانے پر سپربیس کنکشن ضروری ہے")
        u = st.text_input("Supabase URL (Example: https://xyz.supabase.co)")
        k = st.text_input("Supabase Anon Key", type="password")
        if st.button("Connect & Start System"):
            if u and k:
                st.session_state.supabase_url = u
                st.session_state.supabase_key = k
                st.rerun()
    st.stop()

supabase: Client = create_client(st.session_state.supabase_url, st.session_state.supabase_key)

# --- 3. ماسٹر فنکشنز (No-Bug Logic) ---
def clean_for_tts(text):
    return re.sub(r'[*#_~]', '', text)

def get_unique_hashtag(tag):
    now = datetime.datetime.now()
    return f"#{tag}_{now.strftime('%A_%d_%b_%Y_%H%M%S')}"

# --- 4. سیکیورٹی اور ایڈمن ایکسیس ---
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

with st.sidebar:
    if not st.session_state.is_admin:
        secret = st.text_input("Secret Admin Access Code", type="password")
        if st.button("Unlock Admin Panel"):
            if secret == "GHULAM_V22_MASTER": # یہ آپ کا خفیہ کوڈ ہے
                st.session_state.is_admin = True
                st.rerun()
    else:
        if st.button("Logout Admin"):
            st.session_state.is_admin = False
            st.rerun()

# --- 5. ایڈمن ڈیش بورڈ (16-Table Interface) ---
if st.session_state.is_admin:
    st.title("👨‍💻 Admin Command Center")
    tabs = st.tabs(["Dashboard", "Users Control", "Grari (Settings)", "Finance"])

    with tabs[0]: # Dashboard Overview
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Users", "4")
        c2.metric("Active VIP", "1")
        c3.metric("Pending TID", "0")
        c4.metric("Total USD", "$0.05")

    with tabs[1]: # User Management (Screenshot 2 Logic)
        st.subheader("Active Users List")
        # یہاں سپربیس سے ڈیٹا فیچ ہوگا
        with st.expander("👤 Ghulam Hussain (03461785207)"):
            st.write("Device ID: DEVICE_V2_X99")
            st.write("Violations: 0/5")
            col_a, col_b, col_c = st.columns(3)
            if col_a.button("Reset HWID"): st.toast("HWID Cleared!")
            if col_b.button("Block User"): st.error("User Blocked!")
            if col_c.button("Add Balance"): st.success("Balance Added!")

    with tabs[2]: # Grari Settings
        st.subheader("⚙️ Master Grari")
        st.text_input("Gemini API Key")
        st.number_input("USD to PKR Rate", value=280.0)
        st.toggle("AI Generation Features", value=True)
        if st.button("Sync All Settings"):
            st.success("Real-time Sync Active!")

# --- 6. یوزر سوشل ایپ (Frontend) ---
else:
    # Top Header Icons
    col_h1, col_h2 = st.columns([8, 1])
    with col_h2:
        st.markdown("<div style='font-size: 24px;'>👑 💰</div>", unsafe_allow_html=True)
    
    st.title("Ghulam AI Social")
    
    # VIP Card With Live Timer
    st.markdown("""
        <div class='user-card'>
            <h3>💎 VIP Flash Sale</h3>
            <p><span class='strike'>$20</span> <b style='font-size: 1.5em;'>$10</b></p>
            <p class='pkr-label'>Current Rate: 2,800 PKR</p>
            <p class='vip-timer'>Ends In: 02:59:45</p>
        </div>
    """, unsafe_allow_html=True)

    # Compulsory Referral Activation
    with st.expander("🔗 Activate Referral Link"):
        code_input = st.text_input("Enter Invitation Code")
        if st.button("Activate"):
            st.success("Account Activated! Your link is now visible.")

    # Action Bar (Bottom Fixed Icons)
    st.write("---")
    u_input = st.chat_input("Message Ghulam AI...")
    if u_input:
        st.write(f"Hashtag: {get_unique_hashtag('GhulamAI')}")

    cols = st.columns([1,1,1,10])
    cols[0].button("🖼️")
    cols[1].button("🎥")
    cols[2].button("🎤")

