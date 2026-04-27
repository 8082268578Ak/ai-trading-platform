import re

def main():
    file_path = "/Users/amitkumar/Downloads/ai-trading-platform/app/streamlit_app.py"
    with open(file_path, "r") as f:
        content = f.read()

    # 1. Update State Initialization
    state_pattern = r'page = st\.query_params\.get\("page", "home"\)'
    state_replacement = r'if "page" not in st.session_state: st.session_state.page = "home"'
    content = re.sub(state_pattern, state_replacement, content)

    # 2. Update Login Button
    login_pattern = r'st\.query_params\["page"\] = "home"\n\s+else:\n\s+st\.query_params\["page"\] = "dashboard"'
    login_replacement = r'st.session_state.page = "home"\n            else:\n                st.session_state.page = "dashboard"'
    content = re.sub(login_pattern, login_replacement, content)

    # 3. Update Get Started Button
    get_started_pattern = r'st\.query_params\["page"\] = "dashboard"'
    get_started_replacement = r'st.session_state.page = "dashboard"'
    content = re.sub(get_started_pattern, get_started_replacement, content)

    # 5. Update Sidebar and Routing block
    routing_pattern = r'# --- GLOBAL SIDEBAR NAVIGATION ---.*?render_footer\(\)'
    routing_replacement = '''# --- GLOBAL SIDEBAR NAVIGATION ---
if st.session_state.page == "dashboard":
    with st.sidebar:
        st.markdown("<br>", unsafe_allow_html=True)
        module = st.radio("Navigation Menu", [
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
        new_mode = st.radio("Trading Mode", ["Paper Trading (Default)", "Real Trading ⚠️"], index=0 if st.session_state.trading_mode == "Paper Trading (Default)" else 1)
        if new_mode != st.session_state.trading_mode:
            st.session_state.trading_mode = new_mode
            st.rerun()

# --- ROUTING LOGIC ---
if st.session_state.page == "home":
    render_home()
    render_footer()
elif st.session_state.page == "dashboard":
    if check_password():
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
    render_footer()'''

    content = re.sub(routing_pattern, routing_replacement, content, flags=re.DOTALL)

    with open(file_path, "w") as f:
        f.write(content)

if __name__ == "__main__":
    main()
