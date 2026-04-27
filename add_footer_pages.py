import re

def main():
    file_path = "/Users/amitkumar/Downloads/ai-trading-platform/app/streamlit_app.py"
    with open(file_path, "r") as f:
        content = f.read()

    # 1. Update State Initialization
    state_pattern = r'if "page" not in st\.session_state: st\.session_state\.page = "home"'
    state_replacement = '''# Sync query params with session state for URL routing
url_page = st.query_params.get("page")
if url_page and url_page != st.session_state.get("page"):
    st.session_state.page = url_page
elif "page" not in st.session_state:
    st.session_state.page = "home"'''
    content = re.sub(state_pattern, state_replacement, content)

    # 2. Update Footer Links
    footer_pattern = r'<div class="footer-col" style="flex: 1;">\n\s+<h4>Product</h4>\n\s+<a href="#">Features</a>\n\s+<a href="#">API Documentation</a>\n\s+<a href="#">Pricing</a>\n\s+</div>\n\s+<div class="footer-col" style="flex: 1;">\n\s+<h4>Resources</h4>\n\s+<a href="#">Tutorials</a>\n\s+<a href="#">Market News</a>\n\s+<a href="#">Support</a>\n\s+</div>\n\s+<div class="footer-col" style="flex: 1;">\n\s+<h4>Company</h4>\n\s+<a href="#">About Us</a>\n\s+<a href="#">Careers</a>\n\s+<a href="#">Contact</a>\n\s+</div>'
    footer_replacement = '''<div class="footer-col" style="flex: 1;">
                <h4>Product</h4>
                <a href="?page=features" target="_self">Features</a>
                <a href="?page=api" target="_self">API Documentation</a>
                <a href="?page=pricing" target="_self">Pricing</a>
            </div>
            <div class="footer-col" style="flex: 1;">
                <h4>Resources</h4>
                <a href="?page=tutorials" target="_self">Tutorials</a>
                <a href="?page=news" target="_self">Market News</a>
                <a href="?page=support" target="_self">Support</a>
            </div>
            <div class="footer-col" style="flex: 1;">
                <h4>Company</h4>
                <a href="?page=about" target="_self">About Us</a>
                <a href="?page=careers" target="_self">Careers</a>
                <a href="?page=contact" target="_self">Contact</a>
            </div>'''
    content = re.sub(footer_pattern, footer_replacement, content)

    # 3. Insert the 9 page functions before render_footer
    pages_code = '''
# --- STATIC PAGES ---
def render_back_button():
    if st.button("🏠 Back to Home", type="primary"):
        st.session_state.page = "home"
        st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)

def render_features():
    st.title("🌟 Features")
    render_back_button()
    st.markdown("""
    <div class="dash-card">
        <h3>1. Real-Time Analytics</h3>
        <p>Track live asset prices and order book data with microsecond precision using WebSocket integrations with major exchanges.</p>
    </div><br>
    <div class="dash-card">
        <h3>2. Advanced AI Modeling</h3>
        <p>Leverage ensemble models combining LSTM, XGBoost, and Random Forests to predict market volatility and identify entry/exit signals.</p>
    </div><br>
    <div class="dash-card">
        <h3>3. NLP Sentiment Engines</h3>
        <p>Analyze thousands of financial news articles and social media posts every minute using specialized FinBERT language models.</p>
    </div>
    """, unsafe_allow_html=True)

def render_api_docs():
    st.title("💻 API Documentation")
    render_back_button()
    st.markdown("""
    <div class="dash-card">
        <h3>REST API Access</h3>
        <p>Integrate our predictive models directly into your custom trading scripts. Authenticate via Bearer tokens.</p>
        <pre><code class="language-python">
import requests

url = "https://api.tradeai.platform/v1/predict"
headers = {"Authorization": "Bearer YOUR_TOKEN"}
data = {"ticker": "AAPL", "timeframe": "1h"}
response = requests.post(url, headers=headers, json=data)
print(response.json())
        </code></pre>
    </div>
    """, unsafe_allow_html=True)

def render_pricing():
    st.title("💳 Pricing")
    render_back_button()
    st.markdown("""
    <div style="display:flex; gap:2rem;">
        <div class="dash-card" style="flex:1; text-align:center;">
            <h3>Basic</h3>
            <h1 style="color:#8b5cf6;">$0<span style="font-size:1rem;color:#9ca3af;">/mo</span></h1>
            <p>End-of-day predictions</p>
            <p>3 tracked assets</p>
            <p>Community Support</p>
        </div>
        <div class="dash-card" style="flex:1; text-align:center; border-color:#3b82f6;">
            <h3>Pro</h3>
            <h1 style="color:#3b82f6;">$49<span style="font-size:1rem;color:#9ca3af;">/mo</span></h1>
            <p>15-minute intervals</p>
            <p>Unlimited assets</p>
            <p>API Access</p>
        </div>
        <div class="dash-card" style="flex:1; text-align:center;">
            <h3>Enterprise</h3>
            <h1 style="color:#10b981;">Custom</h1>
            <p>Tick-level analytics</p>
            <p>Dedicated infrastructure</p>
            <p>24/7 Phone Support</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_tutorials():
    st.title("📚 Tutorials")
    render_back_button()
    st.markdown("""
    <div class="dash-card">
        <h3>Getting Started with TradeAI</h3>
        <p>Learn how to connect your brokerage account and configure your first automated paper trading strategy.</p>
        <a href="#">Read Guide →</a>
    </div><br>
    <div class="dash-card">
        <h3>Understanding AI Confidence Scores</h3>
        <p>A deep dive into how our models calculate confidence intervals and how to use them for position sizing.</p>
        <a href="#">Read Guide →</a>
    </div>
    """, unsafe_allow_html=True)

def render_market_news():
    st.title("📰 Market News")
    render_back_button()
    st.markdown("""
    <div class="dash-card">
        <h4>Fed Announces New Rate Decision</h4>
        <p style="color:#9ca3af;">Markets react as the Federal Reserve announces a surprise 25bps cut to the benchmark interest rate...</p>
        <span style="color:#10b981; font-weight:bold;">Sentiment: Positive (0.78)</span>
    </div><br>
    <div class="dash-card">
        <h4>Tech Giants Report Earnings</h4>
        <p style="color:#9ca3af;">Major technology companies posted mixed results for Q3, leading to increased volatility in the Nasdaq...</p>
        <span style="color:#f59e0b; font-weight:bold;">Sentiment: Neutral (0.12)</span>
    </div>
    """, unsafe_allow_html=True)

def render_support():
    st.title("🛟 Support")
    render_back_button()
    st.markdown("""
    <div class="dash-card">
        <h3>How can we help?</h3>
        <p>Search our knowledge base or open a ticket with our support engineers.</p>
    </div>
    """, unsafe_allow_html=True)
    st.text_input("Search Knowledge Base...")
    if st.button("Open Support Ticket"):
        st.success("Our support portal is currently being upgraded. Please email support@tradeai.platform.")

def render_about_us():
    st.title("🏢 About Us")
    render_back_button()
    st.markdown("""
    <div class="dash-card">
        <h3>Our Mission</h3>
        <p>We believe institutional-grade AI trading tools should be accessible to retail investors. Our team of quantitative analysts and machine learning engineers have spent years building a robust platform that democratizes algorithmic trading.</p>
    </div>
    """, unsafe_allow_html=True)

def render_careers():
    st.title("💼 Careers")
    render_back_button()
    st.markdown("""
    <div class="dash-card">
        <h3>Open Positions</h3>
        <ul>
            <li><strong>Senior Quantitative Analyst</strong> - New York, NY (Hybrid)</li>
            <li><strong>Machine Learning Engineer (Time Series)</strong> - Remote</li>
            <li><strong>Frontend Developer (React/Streamlit)</strong> - London, UK</li>
        </ul>
        <p>Email your resume to careers@tradeai.platform</p>
    </div>
    """, unsafe_allow_html=True)

def render_contact():
    st.title("✉️ Contact")
    render_back_button()
    st.markdown("""
    <div class="dash-card">
        <h3>Get in Touch</h3>
        <p><strong>Email:</strong> hello@tradeai.platform</p>
        <p><strong>Phone:</strong> +1 (800) 555-0199</p>
        <p><strong>Address:</strong> 100 Financial District Blvd, Suite 400, New York, NY 10005</p>
    </div>
    """, unsafe_allow_html=True)

def render_footer():'''
    content = re.sub(r'def render_footer\(\):', pages_code, content)

    # 4. Update the routing engine at the end of the file
    routing_pattern = r'# --- ROUTING LOGIC ---.*?elif st\.session_state\.page == "dashboard":'
    routing_replacement = '''# --- ROUTING LOGIC ---
if st.session_state.page == "home":
    render_home()
    render_footer()
elif st.session_state.page == "features": render_features(); render_footer()
elif st.session_state.page == "api": render_api_docs(); render_footer()
elif st.session_state.page == "pricing": render_pricing(); render_footer()
elif st.session_state.page == "tutorials": render_tutorials(); render_footer()
elif st.session_state.page == "news": render_market_news(); render_footer()
elif st.session_state.page == "support": render_support(); render_footer()
elif st.session_state.page == "about": render_about_us(); render_footer()
elif st.session_state.page == "careers": render_careers(); render_footer()
elif st.session_state.page == "contact": render_contact(); render_footer()
elif st.session_state.page == "dashboard":'''
    content = re.sub(routing_pattern, routing_replacement, content, flags=re.DOTALL)

    with open(file_path, "w") as f:
        f.write(content)

if __name__ == "__main__":
    main()
