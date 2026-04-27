import re

def main():
    file_path = "/Users/amitkumar/Downloads/ai-trading-platform/app/streamlit_app.py"
    with open(file_path, "r") as f:
        content = f.read()

    # 1. Update State Initialization
    content = content.replace(
        'if "password_correct" not in st.session_state: st.session_state.password_correct = False',
        'if "authenticated" not in st.session_state: st.session_state.authenticated = False'
    )
    content = content.replace(
        'elif "page" not in st.session_state:\n    st.session_state.page = "home"',
        'elif "page" not in st.session_state:\n    st.session_state.page = "landing"'
    )

    # 2. Update Header
    content = content.replace('current_page = st.session_state.get("page", "home")', 'current_page = st.session_state.get("page", "landing")')
    content = content.replace('type="primary" if current_page == "home"', 'type="primary" if current_page == "landing"')
    content = content.replace('st.session_state.page = "home"; st.rerun()', 'st.session_state.page = "landing"; st.rerun()')
    content = content.replace('st.session_state.get("password_correct", False)', 'st.session_state.get("authenticated", False)')
    content = content.replace('st.session_state.page = "dashboard"\n                st.rerun()', 'st.session_state.page = "login"\n                st.rerun()', 1) # only replace the first occurrence (which is the login button in header)

    # 3. Update render_home to render_landing
    content = content.replace('def render_home():', 'def render_landing():')
    content = content.replace('st.session_state.page = "get_started"\n            st.rerun()', 'st.session_state.page = "login"\n            st.rerun()')
    # Update the "Explore Dashboard" button to point to login as requested
    content = content.replace('if st.button("📊 Explore Dashboard", use_container_width=True):\n            st.session_state.page = "dashboard"\n            st.rerun()', 'if st.button("📊 Explore Dashboard", use_container_width=True):\n            st.session_state.page = "login"\n            st.rerun()')

    # 4. Remove check_password and GLOBAL SIDEBAR NAVIGATION blocks, insert render_login and first half of render_dashboard
    old_sidebar_block = content[content.find('DEMO_USER = "admin"'):content.find('def render_get_started()')]
    
    new_auth_sidebar_block = """
def render_login():
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.title("🔐 Login to TradeAI")
        st.write("Please sign in to access your secure dashboard.")
        st.info("Demo credentials - Username: admin | Password: admin123")
        
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login", type="primary", use_container_width=True)
            
            if submit:
                if username == "admin" and password == "admin123":
                    st.session_state.authenticated = True
                    st.session_state.page = "dashboard"
                    st.rerun()
                else:
                    st.error("Invalid credentials. Please try again.")

def render_dashboard():
    if not st.session_state.get("authenticated", False):
        st.warning("Please login first")
        st.session_state.page = "login"
        st.rerun()
        
    # --- GLOBAL SIDEBAR NAVIGATION ---
    with st.sidebar:
        st.markdown("### 🧭 Navigation Menu")
        st.write("")
        
        if "module" not in st.session_state:
            st.session_state.module = "📊 Stock Selection"
            
        modules = [
            "📊 Stock Selection",
            "🧠 AI Analysis",
            "📈 Prediction",
            "📰 Sentiment Analysis",
            "💰 Buy / Sell Signals",
            "💼 Portfolio Manager",
            "⚙️ Settings",
            "🔔 Alerts"
        ]
        
        for mod in modules:
            btn_type = "primary" if st.session_state.module == mod else "secondary"
            if st.button(mod, use_container_width=True, type=btn_type):
                st.session_state.module = mod
                st.rerun()
                
        st.markdown("---")
        st.markdown("### ⚙️ Trading Mode")
        
        mode_col1, mode_col2 = st.columns(2)
        with mode_col1:
            if st.button("Paper", use_container_width=True, type="primary" if st.session_state.trading_mode == "Paper Trading (Default)" else "secondary"):
                if st.session_state.trading_mode != "Paper Trading (Default)":
                    st.session_state.trading_mode = "Paper Trading (Default)"
                    st.rerun()
        with mode_col2:
            if st.button("Real ⚠️", use_container_width=True, type="primary" if st.session_state.trading_mode == "Real Trading ⚠️" else "secondary"):
                if st.session_state.trading_mode != "Real Trading ⚠️":
                    st.session_state.trading_mode = "Real Trading ⚠️"
                    st.rerun()
                    
        st.write("")
        st.write("")
        st.write("")
        if st.button("🚪 Logout Securely", type="primary", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.page = "landing"
            st.rerun()
            
    module = st.session_state.module

"""
    content = content.replace(old_sidebar_block, new_auth_sidebar_block + "\n# --- STATIC CONTENT PAGES ---\n")

    # 5. Fix the bottom routing logic
    old_routing_block = content[content.find('# --- ROUTING LOGIC ---'):]
    
    # We need to take the logic inside the old dashboard routing and indent it inside render_dashboard
    # Actually, we can just replace the bottom router and move the dashboard setup logic into render_dashboard
    
    dashboard_core_logic = """
    # Setup Broker based on selection
    try:
        if st.session_state.trading_mode == "Paper Trading (Default)": broker = PaperTradingEngine()
        else: broker = LiveTradingEngine()
    except: broker = PaperTradingEngine()
    
    data = load_all_data(st.session_state.selected_tickers)
    
    # Pre-compute Portfolio Data if needed
    df_summary, metadata = pd.DataFrame(), {}
    if data and module in ["💼 Portfolio Manager", "🔔 Alerts"]:
        summary_rows = []
        for ticker, df_asset in data.items():
            if not df_asset.empty:
                last_row = df_asset.iloc[-1]
                current_price = last_row['Close']
                predicted_price = last_row.get('Predicted_Price', current_price)
                summary_rows.append({
                    "Symbol": ticker, "Price": current_price,
                    "Predicted_Price": predicted_price,
                    "Expected_Return_%": ((predicted_price - current_price) / current_price) * 100 if current_price>0 else 0,
                    "Sentiment": last_row.get('Sentiment_Score', 0.0),
                    "Signal": last_row.get('Signal_Text', 'HOLD'),
                    "Confidence": last_row.get('Confidence', 0.0),
                    "Annualized_Risk": RiskAnalyzer.calculate_annualized_risk(df_asset)
                })
        df_summary = pd.DataFrame(summary_rows)
        df_summary, metadata = PortfolioOptimizer.allocate_capital(df_summary)
        if not df_summary.empty and "Allocation_%" in df_summary.columns:
            df_summary = df_summary.sort_values(by="Allocation_%", ascending=False).reset_index(drop=True)

    # Module Router
    if module == "📊 Stock Selection": render_dashboard_stock_selection()
    elif module == "⚙️ Settings": render_dashboard_settings()
    elif module == "🔔 Alerts": render_dashboard_alerts(df_summary)
    else:
        if not data: st.warning("No data found for the selected tickers. Add valid tickers in Stock Selection.")
        else:
            if module == "🧠 AI Analysis": render_dashboard_ai_analysis(data)
            elif module == "📈 Prediction": render_dashboard_prediction(data)
            elif module == "📰 Sentiment Analysis":
                st.title("📰 Sentiment Analysis")
                selected_asset = st.selectbox("Select Asset to view Sentiment:", list(data.keys()))
                if selected_asset and 'Sentiment_Score' in data[selected_asset].columns:
                    df_asset = data[selected_asset]
                    st.metric("Latest Sentiment", f"{df_asset['Sentiment_Score'].iloc[-1]:.2f}")
                    fig = go.Figure(data=[go.Bar(x=df_asset.index, y=df_asset['Sentiment_Score'], marker_color=['#10b981' if s>0 else '#ef4444' for s in df_asset['Sentiment_Score']])])
                    fig.update_layout(height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white' if st.session_state.theme=='dark' else 'black'))
                    st.plotly_chart(fig, use_container_width=True)
            elif module == "💰 Buy / Sell Signals":
                st.title("💰 Buy / Sell Signals")
                selected_asset = st.selectbox("Select Asset to view Signals:", list(data.keys()))
                if selected_asset:
                    df_asset = data[selected_asset]
                    fig = go.Figure()
                    fig.add_trace(go.Candlestick(x=df_asset.index, open=df_asset['Open'], high=df_asset['High'], low=df_asset['Low'], close=df_asset['Close']))
                    if 'Signal' in df_asset.columns:
                        buy_signals = df_asset[df_asset['Signal'] == 1]
                        sell_signals = df_asset[df_asset['Signal'] == -1]
                        fig.add_trace(go.Scatter(x=buy_signals.index, y=buy_signals['Close']*0.95, mode='markers', marker=dict(symbol='triangle-up', size=14, color='#10b981'), name='Buy'))
                        fig.add_trace(go.Scatter(x=sell_signals.index, y=sell_signals['Close']*1.05, mode='markers', marker=dict(symbol='triangle-down', size=14, color='#ef4444'), name='Sell'))
                    fig.update_layout(height=600, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white' if st.session_state.theme=='dark' else 'black'), xaxis_rangeslider_visible=False)
                    st.plotly_chart(fig, use_container_width=True)
            elif module == "💼 Portfolio Manager": render_dashboard_portfolio_manager(df_summary, metadata, broker, st.session_state.trading_mode)
"""
    
    new_routing_block = """# --- ROUTING LOGIC ---

if st.session_state.page == "landing":
    render_landing()
elif st.session_state.page == "login":
    render_login()
elif st.session_state.page == "dashboard":
    render_dashboard()
elif st.session_state.page == "features":
    render_features()
elif st.session_state.page == "get_started":
    render_get_started()
elif st.session_state.page == "news":
    render_news()
elif st.session_state.page == "pricing":
    render_pricing()
"""

    # Inject dashboard core logic at the end of render_dashboard
    content = content.replace('    module = st.session_state.module\n\n', '    module = st.session_state.module\n' + dashboard_core_logic + '\n\n')

    # Replace old routing block with new one
    content = content.replace(old_routing_block, new_routing_block)

    with open(file_path, "w") as f:
        f.write(content)

if __name__ == "__main__":
    main()
