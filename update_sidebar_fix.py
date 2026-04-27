import streamlit as st

# ---------------- SESSION STATE ----------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "trading_mode" not in st.session_state:
    st.session_state.trading_mode = "Paper Trading (Default)"

if "selected_tickers" not in st.session_state:
    st.session_state.selected_tickers = ["AAPL", "TSLA"]

# ---------------- HEADER ----------------
col1, col2, col3 = st.columns([1, 6, 2])

with col1:
    if st.button("🏠 Home"):
        st.session_state.page = "home"

with col3:
    if st.button("📊 Dashboard"):
        st.session_state.page = "dashboard"

st.markdown("---")

# ---------------- SIDEBAR ----------------
if st.session_state.page == "dashboard":
    with st.sidebar:
        st.title("⚡ TradeAI")

        module = st.radio("Navigation", [
            "📊 Stock Selection",
            "🧠 AI Analysis",
            "📈 Prediction",
            "📰 Sentiment Analysis",
            "💰 Buy / Sell Signals",
            "💼 Portfolio Manager",
            "⚙️ Settings",
            "🔔 Alerts"
        ])

        st.markdown("---")

        st.session_state.trading_mode = st.radio(
            "Trading Mode",
            ["Paper Trading (Default)", "Real Trading ⚠️"]
        )

# ---------------- HOME PAGE ----------------
if st.session_state.page == "home":
    st.title("🚀 AI Trading Platform")
    st.subheader("Predict. Analyze. Invest Smarter.")

    if st.button("🚀 Get Started"):
        st.session_state.page = "dashboard"
        st.rerun()

# ---------------- DASHBOARD ----------------
elif st.session_state.page == "dashboard":

    st.title("📊 Dashboard")

    # -------- STOCK SELECTION --------
    if module == "📊 Stock Selection":
        st.subheader("Select Stocks")

        tickers = st.multiselect(
            "Choose stocks",
            ["AAPL", "TSLA", "GOOGL", "MSFT", "AMZN"],
            default=st.session_state.selected_tickers
        )

        st.session_state.selected_tickers = tickers

    # -------- AI ANALYSIS --------
    elif module == "🧠 AI Analysis":
        st.subheader("AI Analysis")
        st.success("AI suggests HOLD (example)")

    # -------- PREDICTION --------
    elif module == "📈 Prediction":
        st.subheader("Prediction")
        st.write("Predicted price: 275")

    # -------- SENTIMENT --------
    elif module == "📰 Sentiment Analysis":
        st.subheader("Sentiment Analysis")
        st.write("Market sentiment: Positive")

    # -------- SIGNALS --------
    elif module == "💰 Buy / Sell Signals":
        st.subheader("Signals")
        st.write("BUY / SELL indicators here")

    # -------- PORTFOLIO --------
    elif module == "💼 Portfolio Manager":
        st.subheader("Portfolio")
        st.write("Allocation + Risk")

    # -------- SETTINGS --------
    elif module == "⚙️ Settings":
        st.subheader("Settings")
        st.write("Configure system")

    # -------- ALERTS --------
    elif module == "🔔 Alerts":
        st.subheader("Alerts")
        st.write("No alerts")

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("© 2026 TradeAI | Built with AI 🚀")