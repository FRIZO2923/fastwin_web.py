import streamlit as st
from streamlit.components.v1 import html

# --- Page Config ---
st.set_page_config(page_title="Fastwin Clone", layout="centered")

# --- Custom CSS Styling ---
st.markdown("""
<style>
body { background-color: #f4f9ff; }
.balance-box {
    background: white; padding: 20px; border-radius: 15px;
    box-shadow: 0 0 10px rgba(0,0,0,0.05); margin-bottom: 10px;
}
.balance-box h2 { margin: 0; }
.action-btn {
    background: #008CFF; color: white; padding: 8px 16px;
    border: none; border-radius: 10px; font-weight: bold;
    margin-left: 5px; margin-right: 5px;
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
}
.navbar {
    position: fixed; bottom: 0; left: 0; right: 0;
    background: white; padding: 10px;
    display: flex; justify-content: space-around;
    box-shadow: 0 -1px 10px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# --- Top Balance Area ---
st.markdown(f"""
<div class="balance-box">
    <h2>Balance: ₹0</h2>
    <p style="margin: 5px 0;">ID: 1026502</p>
    <button class="action-btn">Recharge</button>
    <button class="gray-btn">Withdraw</button>
</div>
""", unsafe_allow_html=True)

# --- Mini Tasks ---
st.markdown("""
<div style="display: flex; justify-content: space-around; margin: 10px 0;">
    <div style="text-align: center;">
        <img src="https://cdn-icons-png.flaticon.com/512/3523/3523887.png" width="40"/>
        <p style="margin: 0;">Task reward</p>
    </div>
    <div style="text-align: center;">
        <img src="https://cdn-icons-png.flaticon.com/512/1828/1828970.png" width="40"/>
        <p style="margin: 0;">Check in</p>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Game Cards ---
st.markdown("""
<div class="grid">
    <div class="card">
        <img src="https://img.icons8.com/color/96/rocket--v1.png" width="50"/>
        <h4>FAST-PARITY</h4>
    </div>
    <div class="card">
        <img src="https://img.icons8.com/fluency/96/ball.png" width="50"/>
        <h4>PARITY</h4>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Bottom Nav ---
st.markdown("""
<div class="navbar">
    <div>🏠<br/>Home</div>
    <div>👥<br/>Invite</div>
    <div>💰<br/>Recharge</div>
    <div>👤<br/>Profile</div>
</div>
""", unsafe_allow_html=True)
