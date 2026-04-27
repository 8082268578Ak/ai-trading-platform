import re

def main():
    file_path = "/Users/amitkumar/Downloads/ai-trading-platform/app/streamlit_app.py"
    with open(file_path, "r") as f:
        content = f.read()

    # 1. Add imports at the top
    imports = """import sys
import time
import requests
try:
    from streamlit_lottie import st_lottie
except ImportError:
    st_lottie = None

@st.cache_data
def load_lottieurl(url: str):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None
"""
    content = content.replace("import sys", imports)

    # 2. Update render_landing()
    old_landing = """    # 🔥 1. Hero Section
    st.title("🚀 AI-Powered Trading Intelligence")
    st.subheader("Predict. Analyze. Invest Smarter.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 Get Started", use_container_width=True, type="primary"):
            st.session_state.page = "login"
            st.rerun()
    with col2:
        if st.button("📊 Explore Dashboard", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()"""
            
    new_landing = """    # 🔥 1. Hero Section
    lottie_finance = load_lottieurl("https://lottie.host/8b726485-6454-4f05-924b-fb022e3579ea/lHlM8F8TfX.json")
    
    hero_col1, hero_col2 = st.columns([1.5, 1])
    with hero_col1:
        # Animated title using empty placeholder
        title_placeholder = st.empty()
        
        if "title_animated" not in st.session_state:
            titles = [
                "✨ AI-Powered Trading Intelligence",
                "⚡ AI-Powered Trading Intelligence",
                "🚀 AI-Powered Trading Intelligence"
            ]
            for t in titles:
                title_placeholder.title(t)
                time.sleep(0.15)
            st.session_state.title_animated = True
        else:
            title_placeholder.title("🚀 AI-Powered Trading Intelligence")
            
        st.subheader("Predict. Analyze. Invest Smarter.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚀 Get Started", use_container_width=True, type="primary"):
                st.session_state.page = "login"
                st.rerun()
        with col2:
            if st.button("📊 Explore Dashboard", use_container_width=True):
                st.session_state.page = "login"
                st.rerun()
                
    with hero_col2:
        if st_lottie and lottie_finance:
            st_lottie(lottie_finance, height=250, key="hero_lottie")"""
            
    content = content.replace(old_landing, new_landing)

    # 3. Update render_dashboard_ai_analysis()
    old_ai = """        col1, col2 = st.columns([1, 2])
        with col1:
            
            st.metric("AI Recommendation", ai_signal)
            st.metric("Confidence Score", f"{confidence:.1f}%")
            
        with col2:
            
            st.info(f"**AI Reasoning:**\\n\\n{explanation}")"""
            
    new_ai = """        if f"analyzed_{selected_asset}" not in st.session_state:
            with st.spinner(f"Analyzing {selected_asset} market data using AI..."):
                time.sleep(1.5)
            st.session_state[f"analyzed_{selected_asset}"] = True
            
        st.success(f"Analysis complete for {selected_asset}!")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.metric("AI Recommendation", ai_signal)
            st.metric("Confidence Score", f"{confidence:.1f}%")
            
        with col2:
            st.info(f"**AI Reasoning:**\\n\\n{explanation}")"""
            
    content = content.replace(old_ai, new_ai)

    # 4. Update render_dashboard_portfolio_manager()
    old_port = """    b_col1.metric("Account Value", f"${account.get('portfolio_value', 0.0):,.2f}")"""
    
    new_port = """    val_placeholder = b_col1.empty()
    target_val = float(account.get('portfolio_value', 0.0))
    if target_val > 0 and "portfolio_animated" not in st.session_state:
        step = target_val / 20
        current = 0.0
        for _ in range(20):
            current += step
            val_placeholder.metric("Account Value", f"${current:,.2f}")
            time.sleep(0.02)
        st.session_state.portfolio_animated = True
    val_placeholder.metric("Account Value", f"${target_val:,.2f}")"""
    
    content = content.replace(old_port, new_port)

    # 5. Update Trade Execution
    old_trade = """                if conf_c1.button("Confirm Execute", type="primary", use_container_width=True):
                    import datetime
                    res = broker.place_order(order["symbol"], order["qty"], order["action"], order_type.lower())
                    if "error" in res:
                        st.error(res["error"])
                    else:
                        st.success("Trade executed successfully!")
                        st.session_state.trade_history.append({
                            "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "Type": order["action"].upper(),
                            "Symbol": order["symbol"],
                            "Quantity": order["qty"],
                            "Price": current_price,
                            "Status": "FILLED"
                        })
                    del st.session_state.pending_order
                    st.rerun()"""
                    
    new_trade = """                if conf_c1.button("Confirm Execute", type="primary", use_container_width=True):
                    import datetime
                    with st.spinner("Executing trade..."):
                        time.sleep(1)
                        res = broker.place_order(order["symbol"], order["qty"], order["action"], order_type.lower())
                    
                    if "error" in res:
                        st.error(res["error"])
                        time.sleep(2)
                    else:
                        st.success("Trade executed successfully!")
                        if hasattr(st, "toast"):
                            st.toast("Trade executed successfully!", icon="✅")
                        st.balloons()
                        time.sleep(1.5)
                        st.session_state.trade_history.append({
                            "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "Type": order["action"].upper(),
                            "Symbol": order["symbol"],
                            "Quantity": order["qty"],
                            "Price": current_price,
                            "Status": "FILLED"
                        })
                    del st.session_state.pending_order
                    st.rerun()"""
                    
    content = content.replace(old_trade, new_trade)

    with open(file_path, "w") as f:
        f.write(content)

if __name__ == "__main__":
    main()
