import streamlit as st
import random
from datetime import datetime, timedelta
import pytz

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
    ist = pytz.timezone('Asia/Kolkata')
    st.session_state.period = int(datetime.now(ist).strftime("%Y%m%d%H%M"))
if "countdown" not in st.session_state:
    st.session_state.countdown = 60
if "user_bet" not in st.session_state:
    st.session_state.user_bet = None
if "bet_amount" not in st.session_state:
    st.session_state.bet_amount = 10
if "bet_number" not in st.session_state:
    st.session_state.bet_number = 1
if "bet_popup" not in st.session_state:
    st.session_state.bet_popup = None
if "last_update" not in st.session_state:
    st.session_state.last_update = datetime.now(pytz.timezone('Asia/Kolkata'))

# --- Timer Logic ---
def update_timer():
    now = datetime.now(pytz.timezone('Asia/Kolkata'))
    elapsed = (now - st.session_state.last_update).seconds
    if elapsed >= 1:
        st.session_state.countdown -= elapsed
        st.session_state.last_update = now
        if st.session_state.countdown <= 0:
            resolve_round()
            st.session_state.countdown = 60
            st.session_state.period = int(datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%Y%m%d%H%M"))
            st.session_state.user_bet = None
            st.session_state.bet_popup = None

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

# --- UI Navigation ---
st.title("Frizo App")

# Show available balance always
top_col1, top_col2 = st.columns([2, 1])
top_col1.markdown(f"### 💰 Balance: ₹{st.session_state.coins:.2f}")

def show_fast_parity():
    st.subheader("Fast-Parity")

    col1, col2 = st.columns(2)
    col1.markdown(f"**Period**: {st.session_state.period}")
    col2.markdown(f"**Countdown**: {st.session_state.countdown:02d}s")

    # --- Betting Buttons ---
    st.markdown("### Join Bet")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🟢 Join Green (1:2)"):
            st.session_state.bet_popup = "Green"
    with col2:
        if st.button("🟣 Join Violet (1:4.5)"):
            st.session_state.bet_popup = "Violet"
    with col3:
        if st.button("🔴 Join Red (1:2)"):
            st.session_state.bet_popup = "Red"

    # --- Bet Popup ---
    if st.session_state.bet_popup:
        st.markdown(f"## Join {st.session_state.bet_popup}")
        st.markdown(f"### 💰 Available Balance: ₹{st.session_state.coins:.2f}")

        bet_amt_col = st.columns(4)
        for i, amt in enumerate([10, 100, 1000, 10000]):
            if bet_amt_col[i].button(str(amt)):
                st.session_state.bet_amount = amt

        num_col1, num_col2, num_center, num_col3, num_col4 = st.columns(5)
        if num_col1.button("-5"):
            st.session_state.bet_number = max(1, st.session_state.bet_number - 5)
        if num_col2.button("-1"):
            st.session_state.bet_number = max(1, st.session_state.bet_number - 1)
        num_center.markdown(f"### {st.session_state.bet_number}")
        if num_col3.button("+1"):
            st.session_state.bet_number = min(999, st.session_state.bet_number + 1)
        if num_col4.button("+5"):
            st.session_state.bet_number = min(999, st.session_state.bet_number + 5)

        total_contract = st.session_state.bet_amount * st.session_state.bet_number
        st.markdown(f"**Total contract money is ₹{total_contract}**")

        if st.button("✅ Confirm"):
            st.session_state.user_bet = st.session_state.bet_popup
            st.session_state.bet_popup = None

    # --- Record History ---
    st.markdown("### Fast-Parity Record(s)")
    record_display = ""
    colors = {"Red": "🔴", "Green": "🟢", "Violet": "🟣"}
    for item in st.session_state.history[:12]:
        color = colors[item['color']]
        record_display += f"<span style='font-size:24px; margin:4px;'>{item['number']} {color}</span>"

    st.markdown(record_display, unsafe_allow_html=True)

def show_home():
    st.subheader("🏠 Home")
    st.markdown("Welcome to the Frizo Web App!")
    st.markdown(f"### 💰 Your Current Balance: ₹{st.session_state.coins:.2f}")
    st.markdown("Enjoy games like Fast-Parity and more coming soon.")

# --- Page View ---
if st.session_state.page == "home":
    show_home()
elif st.session_state.page == "fast-parity":
    show_fast_parity()

# --- Bottom Navigation ---
st.markdown("""
<style>
.navbar {
    position: fixed; bottom: 0; left: 0; right: 0;
    background: white; padding: 10px;
    display: flex; justify-content: space-around;
    box-shadow: 0 -1px 10px rgba(0,0,0,0.1);
    z-index: 9999;
}
.nav-item {
    text-align: center; cursor: pointer;
}
</style>
<div class="navbar">
    <div class="nav-item" onclick="window.location.href='/?page=home'">🏠<br/>Home</div>
    <div class="nav-item" onclick="window.location.href='/?page=fast-parity'">🎮<br/>Fast-Parity</div>
    <div class="nav-item">💰<br/>Recharge</div>
    <div class="nav-item">👤<br/>Profile</div>
</div>
<script>
    const url = new URL(window.location);
    const params = new URLSearchParams(url.search);
    if (params.get('page')) {
        window.parent.postMessage({ type: 'streamlit:setComponentValue', value: params.get('page') }, '*');
    }
</script>
""", unsafe_allow_html=True)

# --- Navigation logic workaround ---
query_params = st.query_params
if "page" in query_params:
    st.session_state.page = query_params["page"][0]
