import streamlit as st
import json
from datetime import date, datetime
from decimal import Decimal, ROUND_HALF_UP

CHILD_NAME = "varya"
BIRTH_DAY = (3, 1)
DATA_FILE = "notebook_data.json"

def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def init_child(data):
    if CHILD_NAME not in data:
        data[CHILD_NAME] = {"balance": 0.00, "history": []}

def round_money(n):
    return float(Decimal(n).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))

data = load_data()
init_child(data)
child = data[CHILD_NAME]

st.set_page_config(page_title="פנקס ורה 🐰", layout="centered")

st.markdown("""
    <style>
    .kawaii-bunny {
        width: 80px;
        animation: hop 2s infinite;
    }
    @keyframes hop {
        0% {transform: translateY(0);}
        50% {transform: translateY(-5px);}
        100% {transform: translateY(0);}
    }
    </style>
    <div style='text-align: center;'>
        <img src='https://media.tenor.com/P_t_8sGnaCkAAAAi/bunny-rabbit.gif' class='kawaii-bunny'>
        <div style='font-size: 30px; color: mediumslateblue; font-weight: bold;'>🐰 פנקס הקסם של ורה 🐰</div>
        <div style='font-size: 18px; color: slateblue;'>ארנבת חכמה יודעת לשמור על הכסף שלה! 💸🐇</div>
    </div>
""", unsafe_allow_html=True)

action = st.radio("מה את רוצה לעשות היום? 🌸", ["➕ קיבלתי כסף", "➖ הוצאתי כסף", "💰 כמה נשאר לי?", "📜 היסטוריה"])

if action == "➕ קיבלתי כסף":
    amount = st.number_input("כמה קיבלת? 🐇", min_value=0.0, step=0.01, format="%.2f")
    if st.button("הוסף! 🌟"):
        child["balance"] = round_money(child["balance"] + amount)
        child["history"].append({"type": "הוספה", "amount": amount, "time": datetime.now().strftime("%d.%m.%Y %H:%M")})
        save_data(data)
        st.success(f"הוספת {amount:.2f} ₪! עכשיו יש לך {child['balance']:.2f} ₪ 💜")

elif action == "➖ הוצאתי כסף":
    amount = st.number_input("כמה הוצאת? 🎀", min_value=0.0, step=0.01, format="%.2f")
    if st.button("הפחת! 🌟"):
        child["balance"] = round_money(child["balance"] - amount)
        child["history"].append({"type": "הוצאה", "amount": amount, "time": datetime.now().strftime("%d.%m.%Y %H:%M")})
        save_data(data)
        st.success(f"הפחתת {amount:.2f} ₪! עכשיו יש לך {child['balance']:.2f} ₪ 💜")

elif action == "💰 כמה נשאר לי?":
    st.info(f"יש לך עכשיו {child['balance']:.2f} ₪ 🐰✨")

elif action == "📜 היסטוריה":
    st.markdown("### ✏️ הפעולות האחרונות (עד 30):")
    for item in reversed(child["history"][-30:]):
        st.write(f"{item['time']} — {item['type']}: {item['amount']:.2f} ₪")

if st.button("🎉 כמה ימים עד יום ההולדת שלי?"):
    today = date.today()
    bday = date(today.year, BIRTH_DAY[0], BIRTH_DAY[1])
    if bday < today:
        bday = date(today.year + 1, BIRTH_DAY[0], BIRTH_DAY[1])
    days_left = (bday - today).days
    st.info(f"נותרו {days_left} ימים ליום ההולדת שלך, ארנבת מתוקה! 🎂🐇")

