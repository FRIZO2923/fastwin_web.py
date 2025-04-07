import streamlit as st
import random
from datetime import datetime, timedelta

# --- Session State Initialization ---
if "coins" not in st.session_state:
    st.session_state.coins = 100
if "current_tab" not in st.session_state:
    st.session_state.current_tab = "Red vs Green"
if "bet_amount" not in st.session_state:
    st.session_state.bet_amount = 10
if "choice" not in st.session_state:
    st.session_state.choice = None
if "result" not in st.session_state:
    st.session_state.result = None
if "last_round_time" not in st.session_state:
    st.session_state.last_round_time = datetime.now()
if "history" not in st.session_state:
    st.session_state.history = []

# --- App Title ---
st.set_page_config(page_title="Fastwin Lite", layout="centered")
st.markdown("## 🎮 Fastwin Lite – Web Version")

# --- Tabs Navigation ---
tabs = ["Red vs Green", "Coming Soon 🎲", "Coming Soon 🎯"]
selected_tab = st.selectbox("Choose a game", tabs, index=tabs.index(st.session_state.current_tab))
st.session_state.current_tab = selected_tab

# --- Wallet Display ---
st.markdown(f"### 💰 Coins: {st.session_state.coins}")

# --- Timer ---
now = datetime.now()
time_elapsed = (now - st.session_state.last_round_time).total_seconds()
seconds_left = int(60 - (time_elapsed % 60))
st.markdown(f"⏱️ **Next Result In: {seconds_left} seconds**")

# --- Red vs Green Game Logic ---
if selected_tab == "Red vs Green":
    st.markdown("### 🔴 Red vs 🟢 Green")

    st.session_state.bet_amount = st.number_input(
        "Enter your bet amount:", min_value=1,
        max_value=st.session_state.coins, value=st.session_state.bet_amount
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔴 Bet on Red"):
            st.session_state.choice = "Red"
    with col2:
        if st.button("🟢 Bet on Green"):
            st.session_state.choice = "Green"

    if time_elapsed >= 60:
        number = random.randint(0, 99)
        result_color = "Green" if number >= 50 else "Red"
        st.session_state.result = result_color

        outcome = ""
        if st.session_state.choice:
            if st.session_state.choice == result_color:
                st.success(f"🎉 You WON! Result was {number} ({result_color})")
                st.session_state.coins += st.session_state.bet_amount
                outcome = "Win"
            else:
                st.error(f"😞 You LOST! Result was {number} ({result_color})")
                st.session_state.coins -= st.session_state.bet_amount
                outcome = "Lose"

            # Add to history
            st.session_state.history.insert(0, {
                "choice": st.session_state.choice,
                "bet": st.session_state.bet_amount,
                "result": number,
                "color": result_color,
                "outcome": outcome
            })

            # Reset
            st.session_state.choice = None
            st.session_state.last_round_time = datetime.now()

    # --- History ---
    if st.session_state.history:
        st.markdown("### 📜 Result History")
        for i, round in enumerate(st.session_state.history[:5]):
            st.write(
                f"{i+1}. You chose {round['choice']} | Bet: {round['bet']} | "
                f"Result: {round['result']} ({round['color']}) → {round['outcome']}"
            )

    if st.session_state.coins <= 0:
        st.warning("🚫 You are out of coins! Please refresh to restart.")

# --- Placeholder Tabs ---
else:
    st.info("🚧 This game mode is under development. Stay tuned!")

