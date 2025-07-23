# 📘 Mama Dashboard — контрольный центр для мамы 🧡

import streamlit as st
import json
from datetime import datetime

DATA_FILE = "notebook_data.json"

# --- UI CONFIG ---
st.set_page_config(page_title="יומן אמא 🧡", layout="wide")

# --- Load data ---
def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

data = load_data()

# --- Style ---
st.markdown("""
    <style>
    .mama-header {
        font-size: 32px;
        text-align: center;
        color: darkslateblue;
        margin-top: 10px;
        font-weight: bold;
    }
    .balance-box {
        background-color: #f7f0ff;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 10px;
    }
    .history-table {
        font-family: sans-serif;
        font-size: 16px;
    }
    </style>
    <div class='mama-header'>📊 יומן מעקב של אמא 🧡</div>
    <div style='text-align: center; color: grey;'>מעקב אחרי קירה וורה — כל הכספים במקום אחד</div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- Show current balances ---
st.markdown("### 💰 יתרות נוכחיות")
col1, col2 = st.columns(2)

with col1:
    kira = data.get("kira", {"balance": 0})
    st.markdown(f"<div class='balance-box'>🐱 <b>קירה:</b> {kira['balance']:.2f} ₪</div>", unsafe_allow_html=True)

with col2:
    varya = data.get("varya", {"balance": 0})
    st.markdown(f"<div class='balance-box'>🐰 <b>ורה:</b> {varya['balance']:.2f} ₪</div>", unsafe_allow_html=True)

st.markdown("---")

# --- Combined history ---
st.markdown("### 📝 היסטוריה אחרונה (מ-2 הפנקסים)")

# Build full history
all_records = []
for child_name, child_data in data.items():
    for record in child_data.get("history", []):
        all_records.append({
            "שם": "קירה" if child_name == "kira" else "ורה",
            "סוג": record["type"],
            "סכום": f"{record['amount']:.2f} ₪",
            "מתי": record["time"]
        })

# Sort by time DESC
all_records.sort(key=lambda x: datetime.strptime(x["מתי"], "%d.%m.%Y %H:%M"), reverse=True)

# Show table
if all_records:
    st.markdown("<div class='history-table'>", unsafe_allow_html=True)
    for r in all_records[:30]:
        st.markdown(f"📌 {r['מתי']} — <b>{r['שם']}</b> — {r['סוג']} — <code>{r['סכום']}</code>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("אין עדיין פעולות במערכת.")
