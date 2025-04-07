import streamlit as st
import random
from datetime import datetime, timedelta

# --- Page Config ---
st.set_page_config(page_title="Frizo Fast-Parity", layout="centered")

# --- Session State ---
if "coins" not in st.session_state:
    st.session_state.coins = 100
if "page" not in st.session_state:
    st.session_state.page = "home"
if "history" not in st.session_state:
    st.session_state.history = []
if "period" not in st.session_state:
    st.session_state.period = int(datetime.now().strftime("%Y%m%d%H%M%S"))
if "countdown" not in st.session_state:
    st.session_state.countdown = 60
if "user_bet" not in st.session_state:
    st.session_state.user_bet = None
if "bet_amount" not in st.session_state:
    st.session_state.bet_amount = 10
if "last_update" not in st.session_state:
    st.session_state.last_update = datetime.now()

# --- Timer Logic ---
def update_timer():
    now = datetime.now()
    elapsed = (now - st.session_state.last_update).seconds
    if elapsed >= 1:
        st.session_state.countdown -= elapsed
        st.session_state.last_update = now
        if st.session_state.countdown <= 0:
            resolve_round()
            st.session_state.countdown = 60
            st.session_state.period += 1
            st.session_state.user_bet = None

# --- Game Logic ---
def resolve_round():
    result_number = random.randint(0, 9)
    if result_number in [1, 3, 7, 9]:
        result_color = "Red"
    elif result_number in [0, 2, 4, 6, 8]:
        result_color = "Green"
    else:
        result_color = "Violet"

    win = st.session_state.user_bet == result_color
    outcome = "Win" if win else "Lose"

    if win:
        if result_color == "Violet":
            payout = st.session_state.bet_amount * 4.5
        else:
            payout = st.session_state.bet_amount * 2
        st.session_state.coins += payout
    else:
        st.session_state.coins -= st.session_state.bet_amount

    st.session_state.history.insert(0, {
        "period": st.session_state.period,
        "number": result_number,
        "color": result_color,
        "outcome": outcome
    })

# --- Update timer ---
update_timer()

# --- UI ---
st.title("Fast-Parity")

col1, col2 = st.columns(2)
col1.markdown(f"**Period**: {st.session_state.period}")
col2.markdown(f"**Countdown**: {st.session_state.countdown:02d}s")

# --- Betting Buttons ---
st.markdown("### Join Bet")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🟢 Join Green (1:2)"):
        st.session_state.user_bet = "Green"
with col2:
    if st.button("🟣 Join Violet (1:4.5)"):
        st.session_state.user_bet = "Violet"
with col3:
    if st.button("🔴 Join Red (1:2)"):
        st.session_state.user_bet = "Red"

st.markdown("### Select Amount")
amount_col = st.columns(5)
amounts = [1, 2, 5, 10, 20]
for i, col in enumerate(amount_col):
    if col.button(str(amounts[i])):
        st.session_state.bet_amount = amounts[i]

st.info(f"Selected Bet: {st.session_state.user_bet} | Amount: ₹{st.session_state.bet_amount}")

# --- Record History ---
st.markdown("### Fast-Parity Record(s)")
record_display = ""
colors = {"Red": "🔴", "Green": "🟢", "Violet": "🟣"}
for item in st.session_state.history[:12]:
    color = colors[item['color']]
    record_display += f"<span style='font-size:24px; margin:4px;'>{item['number']} {color}</span>"

st.markdown(record_display, unsafe_allow_html=True)

# --- Bottom Navigation ---
st.markdown("""
<style>
.navbar {
    position: fixed; bottom: 0; left: 0; right: 0;
    background: white; padding: 10px;
    display: flex; justify-content: space-around;
    box-shadow: 0 -1px 10px rgba(0,0,0,0.1);
}
</style>
<div class="navbar">
    <div>🏠<br/>Home</div>
    <div>👥<br/>Invite</div>
    <div>💰<br/>Recharge</div>
    <div>👤<br/>Profile</div>
</div>
""", unsafe_allow_html=True)
