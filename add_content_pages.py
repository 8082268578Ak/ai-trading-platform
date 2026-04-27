import re

def main():
    file_path = "/Users/amitkumar/Downloads/ai-trading-platform/app/streamlit_app.py"
    with open(file_path, "r") as f:
        content = f.read()

    # 1. Define the 3 functions using native Streamlit
    pages_code = '''
# --- STATIC CONTENT PAGES ---
def render_features():
    st.title("🌟 Features")
    st.info("Track live asset prices and order book data with microsecond precision using WebSocket integrations with major exchanges.")
    st.info("Leverage ensemble models combining LSTM, XGBoost, and Random Forests to predict market volatility and identify entry/exit signals.")
    st.info("Analyze thousands of financial news articles and social media posts every minute using specialized FinBERT language models.")

def render_news():
    st.title("📰 Market News")
    st.subheader("Fed Announces New Rate Decision")
    st.write("Markets react as the Federal Reserve announces a surprise 25bps cut to the benchmark interest rate...")
    st.success("Sentiment: Positive (0.78)")
    st.markdown("---")
    st.subheader("Tech Giants Report Earnings")
    st.write("Major technology companies posted mixed results for Q3, leading to increased volatility in the Nasdaq...")
    st.warning("Sentiment: Neutral (0.12)")

def render_pricing():
    st.title("💳 Pricing")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Basic")
        st.metric("Price", "$0/mo")
        st.write("End-of-day predictions\\n3 tracked assets\\nCommunity Support")
    with col2:
        st.subheader("Pro")
        st.metric("Price", "$49/mo")
        st.write("15-minute intervals\\nUnlimited assets\\nAPI Access")
    with col3:
        st.subheader("Enterprise")
        st.metric("Price", "Custom")
        st.write("Tick-level analytics\\nDedicated infrastructure\\n24/7 Phone Support")

# --- ROUTING LOGIC ---
'''

    # Insert the functions right before ROUTING LOGIC
    content = content.replace('# --- ROUTING LOGIC ---', pages_code)

    # 2. Add the routing hooks at the very end of the file
    routing_hooks = '''
elif st.session_state.page == "features":
    render_features()
elif st.session_state.page == "news":
    render_news()
elif st.session_state.page == "pricing":
    render_pricing()
'''
    # The file currently ends with the end of the dashboard if/else logic.
    content = content + routing_hooks

    with open(file_path, "w") as f:
        f.write(content)

if __name__ == "__main__":
    main()
