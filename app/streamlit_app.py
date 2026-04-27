import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import sys
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


# Add root directory to path so we can import config
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.append(root_dir)

from config.settings import Config
from portfolio.optimizer import PortfolioOptimizer
from portfolio.risk import RiskAnalyzer
from execution.paper_trading import PaperTradingEngine
from execution.real_trading import LiveTradingEngine

st.set_page_config(page_title="TradeAI Platform", layout="wide", page_icon="🏦", initial_sidebar_state="expanded")

# --- STATE INITIALIZATION ---
if "theme" not in st.session_state: st.session_state.theme = "light"
if "authenticated" not in st.session_state: st.session_state.authenticated = False
if "selected_tickers" not in st.session_state: st.session_state.selected_tickers = Config.DEFAULT_TICKERS.copy()
if "trading_mode" not in st.session_state: st.session_state.trading_mode = "Paper Trading (Default)"
if "sidebar_open" not in st.session_state: st.session_state.sidebar_open = True
# Sync query params with session state for URL routing
url_page = st.query_params.get("page")
if url_page and url_page != st.session_state.get("page"):
    st.session_state.page = url_page
elif "page" not in st.session_state:
    st.session_state.page = "landing"



# --- PREMIUM NAVBAR ---
def render_header():
    # Use native Streamlit columns for a robust, responsive header
    # Adjusted weights to prevent text wrapping on "Dashboard" and align items perfectly
    col_logo, nav1, nav2, nav3, nav4, nav5, col_spacer, col_action = st.columns([2.5, 1.2, 1.6, 1.3, 1.2, 1.2, 0.5, 2.5])
    
    with col_logo:
        st.markdown("### ⬡ TradeAI")
        
    current_page = st.session_state.get("page", "landing")
    
    with nav1:
        if st.button("🏠 Home", use_container_width=True, type="primary" if current_page == "landing" else "secondary"): 
            st.session_state.page = "landing"; st.rerun()
    with nav2:
        if st.button("📊 Dashboard", use_container_width=True, type="primary" if current_page == "dashboard" else "secondary"): 
            st.session_state.page = "dashboard"; st.rerun()
    with nav3:
        if st.button("🌟 Features", use_container_width=True, type="primary" if current_page == "features" else "secondary"): 
            st.session_state.page = "features"; st.rerun()
    with nav4:
        if st.button("📰 News", use_container_width=True, type="primary" if current_page == "news" else "secondary"): 
            st.session_state.page = "news"; st.rerun()
    with nav5:
        if st.button("💳 Pricing", use_container_width=True, type="primary" if current_page == "pricing" else "secondary"): 
            st.session_state.page = "pricing"; st.rerun()
            
    with col_action:
        # Profile / Action Button Area
        if st.session_state.get("authenticated", False):
            if st.button("👤 My Profile", type="secondary", use_container_width=True):
                st.session_state.page = "dashboard"
                st.session_state.module = "⚙️ Settings"
                st.rerun()
        else:
            if st.button("👤 Login / Sign Up", type="primary", use_container_width=True):
                st.session_state.page = "login"
                st.rerun()
    st.markdown("---")

render_header()

# --- GLOBAL DATA LOADER ---
@st.cache_data
def load_all_data(tickers):
    data_dict = {}
    for ticker_symbol in tickers:
        filepath = os.path.join(Config.DATA_DIR, f"{ticker_symbol}_final_signals.csv")
        if os.path.exists(filepath):
            df = pd.read_csv(filepath, index_col=0, parse_dates=True)
            data_dict[ticker_symbol] = df
    return data_dict

# --- MODULAR DASHBOARD VIEWS ---

def render_dashboard_stock_selection():
    st.title("📊 Stock Selection")
    st.markdown("Manage the assets you want the AI to track and analyze.")
    
    st.markdown("### Quick Add Popular Stocks")
    popular = ["AAPL", "TSLA", "MSFT", "GOOGL", "AMZN", "NVDA", "META"]
    
    cols = st.columns(len(popular))
    for i, stock in enumerate(popular):
        with cols[i]:
            if stock not in st.session_state.selected_tickers:
                if st.button(f"+ {stock}", key=f"quick_{stock}"):
                    st.session_state.selected_tickers.append(stock)
                    st.rerun()
            else:
                st.button(f"✓ {stock}", key=f"quick_{stock}", disabled=True)
                
    
    
    st.markdown("### Manage Portfolio")
    selected = st.multiselect(
        "Active Portfolio Stocks (Search and Add/Remove)",
        options=list(set(Config.DEFAULT_TICKERS + popular + st.session_state.selected_tickers)),
        default=st.session_state.selected_tickers
    )
    if selected != st.session_state.selected_tickers:
        st.session_state.selected_tickers = selected
        st.rerun()

def render_dashboard_ai_analysis(data):
    st.title("🧠 AI Analysis")
    st.markdown("Review the final intelligence outputs generated by the ensemble models.")
    
    selected_asset = st.selectbox("Select Asset to view AI Breakdown:", list(data.keys()))
    if selected_asset:
        df_asset = data[selected_asset]
        last_row = df_asset.iloc[-1]
        
        ai_signal = last_row.get('Signal_Text', 'HOLD')
        explanation = last_row.get('Explanation', 'No explanation available.')
        confidence = last_row.get('Confidence', 0.0) * 100
        
        if f"analyzed_{selected_asset}" not in st.session_state:
            with st.spinner(f"Analyzing {selected_asset} market data using AI..."):
                time.sleep(1.5)
            st.session_state[f"analyzed_{selected_asset}"] = True
            
        st.success(f"Analysis complete for {selected_asset}!")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.metric("AI Recommendation", ai_signal)
            st.metric("Confidence Score", f"{confidence:.1f}%")
            
        with col2:
            st.info(f"**AI Reasoning:**\n\n{explanation}")
            

def render_dashboard_prediction(data):
    st.title("📈 Price Prediction")
    st.markdown("Interactive forecasting models showing expected price returns.")
    
    selected_asset = st.selectbox("Select Asset to view Prediction:", list(data.keys()))
    if selected_asset:
        df_asset = data[selected_asset]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_asset.index, y=df_asset['Close'], name='Actual Price', line=dict(color='#3b82f6')))
        if 'Predicted_Price' in df_asset.columns:
            fig.add_trace(go.Scatter(x=df_asset.index, y=df_asset['Predicted_Price'], name='Predicted Price', line=dict(color='#a855f7', dash='dot')))
            
        fig.update_layout(height=500, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white' if st.session_state.theme=='dark' else 'black'))
        st.plotly_chart(fig, use_container_width=True)

def render_dashboard_portfolio_manager(df_summary, metadata, broker, trading_mode):
    st.title("💼 Portfolio Manager")
    
    account = broker.get_account_balance()
    positions = broker.get_positions()
    
    b_col1, b_col2, b_col3, b_col4 = st.columns(4)
    val_placeholder = b_col1.empty()
    target_val = float(account.get('portfolio_value', 0.0))
    if target_val > 0 and "portfolio_animated" not in st.session_state:
        step = target_val / 20
        current = 0.0
        for _ in range(20):
            current += step
            val_placeholder.metric("Account Value", f"${current:,.2f}")
            time.sleep(0.02)
        st.session_state.portfolio_animated = True
    val_placeholder.metric("Account Value", f"${target_val:,.2f}")
    b_col2.metric("Cash Balance", f"${account.get('cash', 0.0):,.2f}")
    b_col3.metric("Buying Power", f"${account.get('buying_power', 0.0):,.2f}")
    b_col4.metric("Open Positions", len(positions))
    
    
    
    col1, col2 = st.columns([1.5, 1])
    with col1:
        
        st.subheader("🥧 Capital Allocation")
        st.info(f"**AI Recommendation:** {metadata.get('Recommendation', '')}")
        allocations = df_summary[df_summary['Allocation_%'] > 0]
        if not allocations.empty:
            fig_pie = go.Figure(data=[go.Pie(labels=allocations['Symbol'], values=allocations['Allocation_%'], hole=.4)])
            fig_pie.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=300, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white' if st.session_state.theme=='dark' else 'black'))
            st.plotly_chart(fig_pie, use_container_width=True)
        
            
    with col2:
        
        st.subheader("📈 Portfolio Metrics")
        st.metric("Expected Return", f"{metadata.get('Total_Expected_Return_%', 0):.2f}%")
        st.metric("Volatility (Risk)", f"{metadata.get('Total_Risk', 0)*100:.2f}%")
        st.metric("Diversification Score", f"{metadata.get('Diversification_Score', 0):.2f}")
        

def render_dashboard_settings():
    st.title("⚙️ Settings")
    st.markdown("Configure your AI Trading System preferences.")
    
    
    st.subheader("Model Configuration")
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("Primary Prediction Model", ["LSTM (Deep Learning)", "Random Forest", "XGBoost"], index=0)
        st.selectbox("Risk Level", ["Low", "Medium", "High"], index=1)
    with col2:
        st.selectbox("Analysis Timeframe", ["Daily", "Weekly", "Intraday (1h)"], index=0)
        st.toggle("Enable Sentiment Analysis", value=True)
    
    
    
    st.subheader("System Options")
    st.toggle("Auto-Refresh Data (15m)", value=False)
    st.toggle("Push Notifications", value=True)
    if st.button("Save Settings", type="primary"):
        st.success("Settings saved successfully!")
    

def render_dashboard_alerts(df_summary):
    st.title("🔔 Alerts & Notifications")
    st.markdown("Latest market events and AI-generated trading opportunities.")
    
    if df_summary.empty:
        st.info("No active alerts or signals at this time.")
        return
        
    
    for idx, row in df_summary.iterrows():
        signal = row.get("Signal", "HOLD")
        if signal in ["BUY", "STRONG BUY"]:
            st.success(f"📈 **{row['Symbol']}** - {signal} Opportunity! Expected Return: {row.get('Expected_Return_%', 0):.2f}%")
        elif signal in ["SELL", "STRONG SELL"]:
            st.error(f"📉 **{row['Symbol']}** - {signal} Warning! Consider reducing position.")
    

# --- PUBLIC PAGES ---
def render_landing():
    # 🔥 1. Hero Section
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
            st_lottie(lottie_finance, height=250, key="hero_lottie")

    scroll_html = """
    <style>
    .scroll-arrow-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 1rem;
        margin-bottom: 2rem;
    }
    .scroll-arrow {
        font-size: 2.5rem;
        color: #60a5fa;
        animation: bounce 2s infinite;
        opacity: 0.8;
    }
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-15px); }
        60% { transform: translateY(-7px); }
    }
    </style>
    <div class="scroll-arrow-container">
        <div class="scroll-arrow">⬇️</div>
    </div>
    """
    st.markdown(scroll_html, unsafe_allow_html=True)
    
    st.markdown("---")

    # 📊 2. Feature Section
    st.header("Platform Features")
    f_col1, f_col2, f_col3, f_col4 = st.columns(4)
    
    with f_col1:
        st.subheader("📈 AI Prediction")
        st.write("Leverage LSTM models to forecast future asset prices.")
        
    with f_col2:
        st.subheader("🧠 Sentiment Analysis")
        st.write("Scan the web for news to gauge market sentiment.")
        
    with f_col3:
        st.subheader("💼 Portfolio Optimization")
        st.write("Automatically allocate funds for maximum risk-adjusted returns.")
        
    with f_col4:
        st.subheader("⚡ Multi-Asset Analysis")
        st.write("Monitor and trade hundreds of tickers simultaneously.")

    st.markdown("---")

    # 💡 3. Highlights Section
    with st.container():
        st.header("Why Choose Us?")
        st.write("• Data-driven decisions")
        st.write("• Risk-aware trading")
        st.write("• AI-based insights")
        st.write("• Multi-stock analysis")

    st.markdown("---")

    # 🔄 4. How It Works
    st.header("How It Works")
    hw_col1, hw_col2, hw_col3 = st.columns(3)
    with hw_col1:
        st.info("### 1. Select Stocks\nChoose the assets you want to track from our global index.")
    with hw_col2:
        st.warning("### 2. Analyze Data\nOur engine streams live data and applies predictive modeling.")
    with hw_col3:
        st.success("### 3. Get Signals\nReceive automated buy, sell, and hold recommendations.")

    st.markdown("---")

    # 🖼️ 5. Dashboard Preview (Simple)
    st.header("Dashboard Preview")
    st.image("/Users/amitkumar/.gemini/antigravity/brain/8fbbc202-8f16-4b79-85fc-94356ed73fba/trading_hero_banner_1777230597115.png", use_container_width=True, caption="AI Trading Dashboard Overview")

    # 🧾 6. Footer
    st.markdown("---")
    st.write("© 2026 AI Trading Platform")

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


def render_dashboard_trade(broker, data):
    st.markdown("""
    <style>
    .trade-panel {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .buy-glow {
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.3) !important;
    }
    .sell-glow {
        box-shadow: 0 0 15px rgba(239, 68, 68, 0.3) !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("💱 Trade Execution Panel")
    
    # Initialize trade history in session state
    if "trade_history" not in st.session_state:
        st.session_state.trade_history = []
        
    # Get Account Info
    account = broker.get_account_balance()
    positions = broker.get_positions()
    
    # Layout
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.markdown("### ⚡ Execute Order")
        with st.container(border=True):
            target_asset = st.selectbox("Select Asset", list(data.keys()) if data else ["AAPL"])
            
            # Live price preview
            current_price = 0.0
            if data and target_asset in data and not data[target_asset].empty:
                current_price = data[target_asset].iloc[-1]['Close']
            st.metric("Live Market Price", f"${current_price:.2f}" if current_price else "N/A")
            
            c1, c2 = st.columns(2)
            with c1:
                qty = st.number_input("Quantity (Shares)", min_value=1, value=1, step=1)
            with c2:
                order_type = st.selectbox("Order Type", ["Market", "Limit", "Stop"])
                
            # Quick buttons (Optional Bonus)
            st.write("Quick Qty:")
            qc1, qc2, qc3 = st.columns(3)
            if qc1.button("1 Share", use_container_width=True): qty = 1
            if qc2.button("5 Shares", use_container_width=True): qty = 5
            if qc3.button("10 Shares", use_container_width=True): qty = 10
            
            # Preview Cost
            est_cost = current_price * qty
            st.info(f"Estimated Cost: **${est_cost:.2f}**")
            
            # Buttons
            bc1, bc2 = st.columns(2)
            with bc1:
                if st.button("🟢 BUY", use_container_width=True):
                    st.session_state.pending_order = {"action": "buy", "symbol": target_asset, "qty": qty}
            with bc2:
                if st.button("🔴 SELL", use_container_width=True):
                    st.session_state.pending_order = {"action": "sell", "symbol": target_asset, "qty": qty}
                    
        # Handle Pending Order Confirmation
        if "pending_order" in st.session_state:
            order = st.session_state.pending_order
            with st.expander("⚠️ Confirm Trade Execution", expanded=True):
                st.warning(f"Are you sure you want to {order['action'].upper()} {order['qty']} shares of {order['symbol']}?")
                conf_c1, conf_c2 = st.columns(2)
                if conf_c1.button("Confirm Execute", type="primary", use_container_width=True):
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
                    st.rerun()
                if conf_c2.button("Cancel", use_container_width=True):
                    del st.session_state.pending_order
                    st.rerun()

    with col2:
        st.markdown("### 📊 Account Summary")
        with st.container(border=True):
            if "error" in account:
                st.error("Account data unavailable. Ensure API keys are correct.")
            else:
                st.metric("Total Portfolio Value", f"${float(account.get('portfolio_value', 0)):,.2f}")
                st.metric("Available Buying Power", f"${float(account.get('buying_power', 0)):,.2f}")
                st.metric("Cash Balance", f"${float(account.get('cash', 0)):,.2f}")
                
                st.markdown("#### Open Positions")
                if isinstance(positions, list) and len(positions) > 0:
                    for p in positions:
                        # Alpaca returns symbol, qty, current_price, etc.
                        sym = p.get('symbol', 'N/A')
                        p_qty = p.get('qty', 0)
                        p_price = float(p.get('current_price', 0))
                        st.write(f"**{sym}**: {p_qty} shares @ ${p_price:.2f}")
                else:
                    st.write("No open positions.")
                    
    st.markdown("---")
    st.markdown("### 📜 Trade History")
    if st.session_state.trade_history:
        st.dataframe(st.session_state.trade_history, use_container_width=True)
    else:
        st.info("No trades executed in this session yet.")


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
            "💱 Trade (Buy / Sell)",
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
            elif module == "💱 Trade (Buy / Sell)":
                render_dashboard_trade(broker, data)
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



# --- STATIC CONTENT PAGES ---
def render_get_started():
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
        st.write("End-of-day predictions\n3 tracked assets\nCommunity Support")
    with col2:
        st.subheader("Pro")
        st.metric("Price", "$49/mo")
        st.write("15-minute intervals\nUnlimited assets\nAPI Access")
    with col3:
        st.subheader("Enterprise")
        st.metric("Price", "Custom")
        st.write("Tick-level analytics\nDedicated infrastructure\n24/7 Phone Support")



# --- GLOBAL FOOTER ---
def render_footer():
    footer_html = """
    <style>
    .tradeai-footer {
        background: rgba(11, 15, 26, 0.4);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        color: #a0aec0;
        padding: 4rem 2rem 2rem;
        font-family: 'Inter', -apple-system, sans-serif;
        margin-top: 5rem;
        border-radius: 16px 16px 0 0;
        box-shadow: 0 -10px 40px rgba(0, 0, 0, 0.2);
    }
    .tradeai-footer-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 3rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    .tradeai-footer-col h4 {
        color: #e2e8f0;
        margin-bottom: 1.2rem;
        font-size: 1.1rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .tradeai-footer-col ul {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    .tradeai-footer-col ul li {
        margin-bottom: 0.8rem;
        font-size: 0.9rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        display: flex;
        align-items: center;
    }
    .tradeai-footer-col ul li:before {
        content: "›";
        margin-right: 8px;
        color: #4a5568;
        transition: all 0.3s ease;
    }
    .tradeai-footer-col ul li:hover {
        color: #60a5fa;
        transform: translateX(6px);
        text-shadow: 0 0 12px rgba(96, 165, 250, 0.4);
    }
    .tradeai-footer-col ul li:hover:before {
        color: #60a5fa;
    }
    .tradeai-footer-bottom {
        max-width: 1200px;
        margin: 3rem auto 0;
        padding-top: 2rem;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        text-align: center;
        font-size: 0.85rem;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 1rem;
    }
    .tradeai-disclaimer {
        font-size: 0.75rem;
        color: #718096;
        max-width: 800px;
        text-align: center;
        line-height: 1.6;
    }
    .tradeai-copyright {
        color: #a0aec0;
        font-weight: 500;
    }
    </style>
    <div class="tradeai-footer">
        <div class="tradeai-footer-grid">
            <div class="tradeai-footer-col">
                <h4>🧠 About TradeAI</h4>
                <p style="font-size: 0.9rem; line-height: 1.6;">TradeAI is an AI-driven trading intelligence platform that combines machine learning, sentiment analysis, and predictive modeling.<br><br>Our goal is to simplify trading by providing data-driven insights, reducing emotional bias, and enabling intelligent portfolio management.</p>
            </div>
            <div class="tradeai-footer-col">
                <h4>🚀 Features</h4>
                <ul>
                    <li>AI Price Prediction</li>
                    <li>Sentiment Analysis</li>
                    <li>Buy/Sell Signal Engine</li>
                    <li>Portfolio Optimization</li>
                    <li>Risk Analysis & Diversification</li>
                    <li>Real-time Dashboard</li>
                </ul>
            </div>
            <div class="tradeai-footer-col">
                <h4>🛠️ Technologies</h4>
                <ul>
                    <li>Frontend: Streamlit</li>
                    <li>Backend: Python, Pandas</li>
                    <li>ML: Scikit-learn, XGBoost</li>
                    <li>DL: PyTorch</li>
                    <li>NLP: FinBERT, VADER</li>
                    <li>Viz: Plotly</li>
                </ul>
            </div>
            <div class="tradeai-footer-col">
                <h4>🔌 Integrations</h4>
                <ul>
                    <li>Alpaca API (Execution)</li>
                    <li>NewsAPI (Sentiment)</li>
                    <li style="opacity: 0.6;">TradingView (Upcoming)</li>
                    <li style="opacity: 0.6;">Binance (Upcoming)</li>
                </ul>
                <h4 style="margin-top: 2rem;">📬 Contact</h4>
                <ul>
                    <li><a href="https://github.com/8082268578Ak" target="_blank" style="color: inherit; text-decoration: none;">GitHub</a></li>
                    <li><a href="https://www.linkedin.com/in/amit-kumar-842909252" target="_blank" style="color: inherit; text-decoration: none;">LinkedIn</a></li>
                    <li><a href="mailto:a.k8082268578@gmail.com" style="color: inherit; text-decoration: none;">Email</a></li>
                </ul>
            </div>
        </div>
        <div class="tradeai-footer-bottom">
            <div class="tradeai-disclaimer">
                📊 <strong>Disclaimer:</strong> This platform is for educational and research purposes only. It does not provide financial advice or guarantee profits. All predictions and signals are generated algorithmically and carry inherent risk.
            </div>
            <div class="tradeai-copyright">
                © 2026 TradeAI. All rights reserved.
            </div>
        </div>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)

# --- ROUTING LOGIC ---

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


# Render global footer across all pages
render_footer()
