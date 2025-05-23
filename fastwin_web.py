""import streamlit as st
import random
from datetime import datetime, timedelta
import pytz

# --- Session Setup ---
if "balance" not in st.session_state:
    st.session_state.balance = 100

if "fast_parity_bets" not in st.session_state:
    st.session_state.fast_parity_bets = []

if "fast_parity_results" not in st.session_state:
    st.session_state.fast_parity_results = []

if "last_period" not in st.session_state:
    st.session_state.last_period = None

if "forced_result" not in st.session_state:
    st.session_state.forced_result = None

if "admin_enabled" not in st.session_state:
    st.session_state.admin_enabled = False

# --- Utility Functions ---
def get_current_ist_period():
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    return now.strftime("%Y%m%d%H%M"), 60 - now.second

def get_random_result():
    return random.randint(0, 9)

def determine_color(num):
    if num == 0 or num == 5:
        return "Violet"
    elif num % 2 == 0:
        return "Green"
    else:
        return "Red"

# --- Layout Setup ---
st.set_page_config(layout="centered")
st.title("🚀 Fast-Parity Game")

# Navigation (Tab Simulation)
tab = st.selectbox("Select Tab", ["Home", "Fast-Parity"])

if tab == "Home":
    st.header("🏠 Home")
    st.markdown(f"### 💰 Balance: ₹{st.session_state.balance:.2f}")
    st.write("Enjoy games like Fast-Parity and more coming soon.")

    st.write("### Recharge Your Wallet")
    recharge_amount = st.number_input("Enter amount to recharge", min_value=10, max_value=10000, step=10)
    if st.button("Recharge Now"):
        st.session_state.balance += recharge_amount
        st.success(f"₹{recharge_amount} added to your balance!")

elif tab == "Fast-Parity":
    period, countdown = get_current_ist_period()

    st.subheader(f"🎲 Period: {period}")
    st.markdown(f"⏳ Countdown: **{countdown} seconds**")
    st.markdown(f"### 💰 Available Balance: ₹{st.session_state.balance:.2f}")

    st.markdown("---")
    st.write("### Place Your Bet")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🟢 Join Green"):
            st.session_state.bet_choice = "Green"
    with col2:
        if st.button("🟣 Join Violet"):
            st.session_state.bet_choice = "Violet"
    with col3:
        if st.button("🔴 Join Red"):
            st.session_state.bet_choice = "Red"

    if "bet_choice" in st.session_state:
        st.markdown(f"#### Selected: {st.session_state.bet_choice}")
        amount = st.selectbox("Select Contract Money", [10, 100, 1000])
        number = st.number_input("Select a Number (0–9)", min_value=0, max_value=9, step=1)
        if st.button("✅ Confirm Bet"):
            if st.session_state.balance >= amount:
                st.session_state.balance -= amount
                st.session_state.fast_parity_bets.append({
                    "period": period,
                    "choice": st.session_state.bet_choice,
                    "amount": amount,
                    "number": number
                })
                st.success(f"Bet confirmed on {st.session_state.bet_choice} with ₹{amount} and number {number}!")
            else:
                st.error("Insufficient balance!")

    # --- Admin Panel ---
    with st.expander("🛠 Admin Control Panel"):
        password = st.text_input("Enter admin password", type="password")
        if password == "yoursecret123":
            st.session_state.admin_enabled = True
        if st.session_state.admin_enabled:
            forced_num = st.number_input("Force Result Number (0–9)", 0, 9, step=1)
            if st.checkbox("✅ Force this result for next period"):
                st.session_state.forced_result = forced_num
                st.success(f"Next result will be forced as {forced_num}")
        else:
            st.warning("Access denied. Incorrect password.")

    # --- Result Generation on Period Change ---
    if st.session_state.last_period != period:
        result_number = st.session_state.forced_result if st.session_state.forced_result is not None else get_random_result()
        result_color = determine_color(result_number)

        st.session_state.fast_parity_results.append({
            "period": st.session_state.last_period if st.session_state.last_period else period,
            "number": result_number,
            "color": result_color
        })

        for bet in st.session_state.fast_parity_bets:
            if bet["period"] == (st.session_state.last_period if st.session_state.last_period else period):
                if result_color == bet["choice"]:
                    multiplier = 2 if result_color in ["Red", "Green"] else 4.5
                    winnings = int(bet["amount"] * multiplier)
                    st.session_state.balance += winnings
                    st.toast(f"🎉 You won ₹{winnings} on {result_color}!")

        st.session_state.fast_parity_bets = []
        st.session_state.last_period = period
        st.session_state.forced_result = None

    st.markdown("---")
    st.write("### 🎯 Latest Result")
    if len(st.session_state.fast_parity_results) > 0:
        last = st.session_state.fast_parity_results[-1]
        st.success(f"Result for Period {last['period']}: Number = {last['number']} | Color = {last['color']}")

    st.markdown("---")
    st.write("### 📜 Bet History")
    for b in reversed(st.session_state.fast_parity_bets[-5:]):
        st.write(f"Period {b['period']} - {b['choice']} | ₹{b['amount']} | Number: {b['number']}")
