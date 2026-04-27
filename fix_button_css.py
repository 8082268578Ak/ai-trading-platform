import re

def main():
    file_path = "/Users/amitkumar/Downloads/ai-trading-platform/app/streamlit_app.py"
    with open(file_path, "r") as f:
        content = f.read()

    # 1. Add Secondary Button CSS to fix visibility in light mode
    css_addition = """
    /* Fix Button Text Color in Light Mode */
    button[data-testid="baseButton-secondary"] {
        color: #0f172a !important;
        background-color: transparent !important;
        border: 1px solid rgba(0,0,0,0.15) !important;
    }
    button[data-testid="baseButton-secondary"] p {
        color: #0f172a !important;
        font-weight: 500;
    }
    button[data-testid="baseButton-secondary"]:hover {
        border-color: #3b82f6 !important;
        background-color: rgba(59, 130, 246, 0.05) !important;
    }
    button[data-testid="baseButton-secondary"]:hover p {
        color: #3b82f6 !important;
    }
    """
    
    # Insert it right before the </style> tag in inject_css()
    content = content.replace("    </style>", css_addition + "\n    </style>")

    # 2. Add emojis to the header buttons to provide context
    content = content.replace('st.button("Home",', 'st.button("🏠 Home",')
    content = content.replace('st.button("Dashboard",', 'st.button("📊 Dashboard",')
    content = content.replace('st.button("Features",', 'st.button("🌟 Features",')
    content = content.replace('st.button("News",', 'st.button("📰 News",')
    content = content.replace('st.button("Pricing",', 'st.button("💳 Pricing",')

    with open(file_path, "w") as f:
        f.write(content)

if __name__ == "__main__":
    main()
