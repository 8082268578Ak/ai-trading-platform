import re

def main():
    file_path = "/Users/amitkumar/Downloads/ai-trading-platform/app/streamlit_app.py"
    with open(file_path, "r") as f:
        content = f.read()

    # The new footer function with isolated CSS
    footer_code = """

# --- GLOBAL FOOTER ---
def render_footer():
    footer_html = \"\"\"
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
                    <li>GitHub</li>
                    <li>LinkedIn</li>
                    <li>Email</li>
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
    \"\"\"
    st.markdown(footer_html, unsafe_allow_html=True)
"""
    
    # Insert render_footer right before # --- ROUTING LOGIC ---
    content = content.replace('# --- ROUTING LOGIC ---', footer_code + '\n# --- ROUTING LOGIC ---')

    # Add the call to render_footer() at the very end of the file
    content += "\n\n# Render global footer across all pages\nrender_footer()\n"

    with open(file_path, "w") as f:
        f.write(content)

if __name__ == "__main__":
    main()
