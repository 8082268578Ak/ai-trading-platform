import re

def main():
    file_path = "/Users/amitkumar/Downloads/ai-trading-platform/app/streamlit_app.py"
    with open(file_path, "r") as f:
        content = f.read()

    trade_module_code = """
def render_dashboard_trade(broker, data):
    st.markdown(\"\"\"
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
    \"\"\", unsafe_allow_html=True)
    
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

"""
    # 1. Insert render_dashboard_trade into the file (before def render_dashboard())
    content = content.replace("def render_dashboard():", trade_module_code + "\ndef render_dashboard():")

    # 2. Add the module to the sidebar array between Prediction and Buy/Sell Signals
    content = content.replace(
        '"📈 Prediction",\n            "📰 Sentiment Analysis",\n            "💰 Buy / Sell Signals",',
        '"📈 Prediction",\n            "💱 Trade (Buy / Sell)",\n            "📰 Sentiment Analysis",\n            "💰 Buy / Sell Signals",'
    )

    # 3. Add the routing for the module at the bottom of the dashboard logic
    routing_insertion = """            elif module == "📰 Sentiment Analysis":"""
    new_routing = """            elif module == "💱 Trade (Buy / Sell)":
                render_dashboard_trade(broker, data)
            elif module == "📰 Sentiment Analysis":"""
    content = content.replace(routing_insertion, new_routing)

    with open(file_path, "w") as f:
        f.write(content)

if __name__ == "__main__":
    main()
