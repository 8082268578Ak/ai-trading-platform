import re
import os

def main():
    file_path = "/Users/amitkumar/Downloads/ai-trading-platform/app/streamlit_app.py"
    with open(file_path, "r") as f:
        content = f.read()

    # 1. Remove inject_css completely
    pattern_inject_css = r'# --- CSS STYLING ---.*?inject_css\(\)\n'
    content = re.sub(pattern_inject_css, '', content, flags=re.DOTALL)

    # 2. Refactor render_header
    pattern_header_logo = r'st\.markdown\(f"""\s*<div.*?</div>\s*""", unsafe_allow_html=True\)'
    content = re.sub(pattern_header_logo, 'st.markdown("### ⬡ TradeAI")', content, flags=re.DOTALL)

    # 3. Refactor check_password
    pattern_pass_start = r'st\.markdown\("<div style=\'max-width: 400px; margin: 4rem auto;\' class=\'dash-card\'>", unsafe_allow_html=True\)\n\s+st\.markdown\("<h2 style=\'text-align:center; margin-bottom: 2rem;\'>Secure Login</h2>", unsafe_allow_html=True\)'
    content = re.sub(pattern_pass_start, 'st.subheader("Secure Login")', content)
    content = content.replace('st.markdown("</div>", unsafe_allow_html=True)', '')

    # 4. Refactor render_home
    # Remove hero-title
    pattern_hero = r'st\.markdown\("""\s*<div style="text-align: center; padding: 4rem 1rem;">.*?</div>\s*""", unsafe_allow_html=True\)'
    hero_replacement = '''st.title("AI-Powered Trading Intelligence")
    st.write("Leverage advanced AI models, real-time market data, and smart insights to make informed trading decisions and maximize your returns.")'''
    content = re.sub(pattern_hero, hero_replacement, content, flags=re.DOTALL)
    
    # Remove stats-bar
    pattern_stats = r'st\.markdown\("""\s*<div class="stats-bar">.*?</div>\s*""", unsafe_allow_html=True\)'
    stats_replacement = '''col1, col2, col3, col4 = st.columns(4)
    col1.metric("Assets Analyzed", "500+")
    col2.metric("Prediction Accuracy", "87.4%")
    col3.metric("Active Traders", "12,000+")
    col4.metric("Live Markets", "24/7")'''
    content = re.sub(pattern_stats, stats_replacement, content, flags=re.DOTALL)

    # Remove platform capabilities HTML
    pattern_capabilities = r'st\.markdown\("<h2 style=\'text-align:center; margin: 4rem 0 2rem 0;\'>Platform Capabilities</h2>", unsafe_allow_html=True\).*?unsafe_allow_html=True\)'
    cap_replacement = '''st.header("Platform Capabilities")
    c1, c2, c3, c4 = st.columns(4)
    c1.subheader("📈 Smart Predictions")
    c1.write("AI models that predict market movements.")
    c2.subheader("🧠 Market Insights")
    c2.write("Real-time sentiment and NLP news analysis.")
    c3.subheader("🛡️ Risk Management")
    c3.write("Advanced risk assessment and optimization.")
    c4.subheader("⚡ Live Execution")
    c4.write("Execute trades seamlessly via Broker APIs.")'''
    content = re.sub(pattern_capabilities, cap_replacement, content, flags=re.DOTALL)

    # 5. Remove all 9 extra pages and render_footer
    pattern_pages = r'# --- STATIC PAGES ---.*?def check_password\(\):'
    content = re.sub(pattern_pages, 'def check_password():', content, flags=re.DOTALL)

    # 6. Update routing logic at the end to remove the 9 pages and render_footer calls
    content = content.replace('render_home()\n    render_footer()', 'render_home()')
    routing_pages_pattern = r'elif st\.session_state\.page == "features": render_features\(\); render_footer\(\)\nelif st\.session_state\.page == "api": render_api_docs\(\); render_footer\(\)\nelif st\.session_state\.page == "pricing": render_pricing\(\); render_footer\(\)\nelif st\.session_state\.page == "tutorials": render_tutorials\(\); render_footer\(\)\nelif st\.session_state\.page == "news": render_market_news\(\); render_footer\(\)\nelif st\.session_state\.page == "support": render_support\(\); render_footer\(\)\nelif st\.session_state\.page == "about": render_about_us\(\); render_footer\(\)\nelif st\.session_state\.page == "careers": render_careers\(\); render_footer\(\)\nelif st\.session_state\.page == "contact": render_contact\(\); render_footer\(\)\n'
    content = re.sub(routing_pages_pattern, '', content)

    # Remove render_footer call at the very end
    content = content.replace('    render_footer()\n', '')

    # 7. Clean up other unsafe_allow_html instances like <br> or dash-cards
    content = content.replace('st.markdown("<br>", unsafe_allow_html=True)', '')
    content = content.replace('st.markdown(\'<div class="dash-card">\', unsafe_allow_html=True)', '')
    content = content.replace('st.markdown(\'</div>\', unsafe_allow_html=True)', '')
    
    # 8. Clean up Sidebar Market Card in dashboard view
    pattern_sidebar_card = r'st\.sidebar\.markdown\("""\s*<div class="sidebar-market-card">.*?</div>\s*""", unsafe_allow_html=True\)'
    sidebar_card_replacement = '''st.sidebar.subheader("Market Overview")
            st.sidebar.metric(f"{ticker}", f"${current_price:.2f}", f"{change_pct:.2f}%")'''
    content = re.sub(pattern_sidebar_card, sidebar_card_replacement, content, flags=re.DOTALL)

    with open(file_path, "w") as f:
        f.write(content)

if __name__ == "__main__":
    main()
