import re

def main():
    file_path = "/Users/amitkumar/Downloads/ai-trading-platform/app/streamlit_app.py"
    with open(file_path, "r") as f:
        content = f.read()

    # 1. Update the 'Get Started' button in render_home
    # Currently it is:
    # if st.button("🚀 Get Started", use_container_width=True, type="primary"):
    #     st.session_state.page = "dashboard"
    content = content.replace(
        'if st.button("🚀 Get Started", use_container_width=True, type="primary"):\n            st.session_state.page = "dashboard"',
        'if st.button("🚀 Get Started", use_container_width=True, type="primary"):\n            st.session_state.page = "get_started"'
    )

    # 2. Add the render_get_started function before render_features
    get_started_func = '''def render_get_started():
    st.title("🚀 Get Started with TradeAI")
    st.write("Welcome to the next generation of algorithmic trading. Follow these steps to set up your environment.")
    
    st.markdown("### Step 1: Create an Account")
    st.info("Currently in open beta. No registration required for Paper Trading mode!")
    
    st.markdown("### Step 2: Configure Your Broker")
    st.write("Connect your exchange to enable live trading.")
    broker = st.selectbox("Select Broker", ["Paper Trading (Simulated)", "Alpaca", "Binance", "Interactive Brokers"])
    if broker != "Paper Trading (Simulated)":
        st.text_input("API Key", type="password")
        st.text_input("API Secret", type="password")
        st.button("Connect Broker")
        
    st.markdown("### Step 3: Select Initial Assets")
    st.write("Choose the assets you want the AI to analyze.")
    st.multiselect("Select Tickers", ["AAPL", "TSLA", "MSFT", "GOOGL", "AMZN", "NVDA", "BTC-USD"], default=["AAPL", "TSLA"])
    
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Launch Dashboard ➡️", type="primary", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()

def render_features():'''
    content = content.replace('def render_features():', get_started_func)

    # 3. Add the routing logic at the end of the file
    routing_logic = '''
elif st.session_state.page == "features":
    render_features()
elif st.session_state.page == "get_started":
    render_get_started()
'''
    content = content.replace('\nelif st.session_state.page == "features":\n    render_features()', routing_logic)

    with open(file_path, "w") as f:
        f.write(content)

if __name__ == "__main__":
    main()
