import streamlit as st
import random
from datetime import datetime

# --- Page Config ---
st.set_page_config(page_title="Frizo Fastwin", layout="centered")

# --- Session State ---
if "coins" not in st.session_state:
    st.session_state.coins = 100
if "page" not in st.session_state:
    st.session_state.page = "home"
if "last_round" not in st.session_state:
    st.session_state.last_round = datetime.now()
if "result" not in st.session_state:
    st.session_state.result = None
if "choice" not in st.session_state:
    st.session_state.choice = None
if "history" not in st.session_state:
    st.session_state.history = []

# --- Styling ---
st.markdown("""
<style>
.balance-box {
    background: white; padding: 20px; border-radius: 15px;
    box-shadow: 0 0 10px rgba(0,0,0,0.05); margin-bottom: 10px;
}
.action-btn {
    background: #008CFF; color: white; padding: 8px 16px;
    border: none; border-radius: 10px; font-weight: bold;
    margin: 5px;
}
.gray-btn {
    background: #eee; color: gray; padding: 8px 16px;
    border: none; border-radius: 10px;
}
.grid {
    display: grid; grid-template-columns: 1fr 1fr;
    gap: 20px; margin-top: 20px;
}
.card {
    background: white; padding: 20px; border-radius: 15px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05); text-align: center;
    cursor: pointer;
}
.navbar {
    position: fixed; bottom: 0; left: 0; right: 0;
    background: white; padding: 10px;
    display: flex; justify-content: space-around;
    box-shadow: 0 -1px 10px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# --- Top Section ---
st.markdown(f"""
<div class="balance-box">
    <h3>Balance: ₹{st.session_state.coins}</h3>
    <p style='margin: 5px 0;'>ID: 1026502</p>
    <button class='action-btn'>Recharge</button>
    <button class='gray-btn'>Withdraw</button>
</div>
""", unsafe_allow_html=True)

# --- Page Router ---
if st.session_state.page == "home":
    # Game Cards
    st.markdown("""
    <div class="grid">
        <div class="card" onclick="window.location.href='/?page=fast-parity'">🔴🟢<br/>FAST PARITY</div>
        <div class="card" onclick="window.location.href='/?page=parity'">🔴🟢<br/>PARITY</div>
    </div>
    """, unsafe_allow_html=True)
    # Buttons fallback
    if st.button("FAST PARITY"):
        st.session_state.page = "fast-parity"
    if st.button("PARITY"):
        st.session_state.page = "parity"

elif st.session_state.page in ["fast-parity", "parity"]:
    st.markdown("### 🔴 RED vs 🟢 GREEN")
    st.markdown("Predict and win! 0-49 = Red, 50-99 = Green")

    bet = st.number_input("Enter bet amount:", min_value=1, max_value=st.session_state.coins, value=10)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔴 Bet on Red"):
            st.session_state.choice = "Red"
    with col2:
        if st.button("🟢 Bet on Green"):
            st.session_state.choice = "Green"

    now = datetime.now()
    if (now - st.session_state.last_round).seconds >= 60:
        number = random.randint(0, 99)
        result_color = "Green" if number >= 50 else "Red"
        outcome = "Win" if st.session_state.choice == result_color else "Lose"

        if outcome == "Win":
            st.success(f"You WON! Result was {number} ({result_color})")
            st.session_state.coins += bet
        else:
            st.error(f"You LOST! Result was {number} ({result_color})")
            st.session_state.coins -= bet

        st.session_state.history.insert(0, {
            "choice": st.session_state.choice,
            "result": number,
            "color": result_color,
            "outcome": outcome
        })

        st.session_state.last_round = datetime.now()
        st.session_state.choice = None

    if st.session_state.history:
        st.markdown("### History")
        for i, h in enumerate(st.session_state.history[:5]):
            st.write(f"{i+1}. You chose {h['choice']} | Result: {h['result']} ({h['color']}) → {h['outcome']}")

    if st.button("⬅ Back to Home"):
        st.session_state.page = "home"

# --- Bottom Nav Placeholder ---
st.markdown("""
<div class="navbar">
    <div>🏠<br/>Home</div>
    <div>👥<br/>Invite</div>
    <div>💰<br/>Recharge</div>
    <div>👤<br/>Profile</div>
</div>
""", unsafe_allow_html=True)
