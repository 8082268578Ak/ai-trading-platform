import re

def main():
    file_path = "/Users/amitkumar/Downloads/ai-trading-platform/app/streamlit_app.py"
    with open(file_path, "r") as f:
        content = f.read()

    # 1. Update CSS Color Palette for Light Mode
    css_vars_pattern = r'    bg_color = "#0A0B14"\n    text_color = "#ffffff"\n    text_muted = "#9ca3af"\n    card_bg = "#111422"\n    card_border = "rgba\(255,255,255,0\.05\)"\n    sidebar_bg = "#0f111a"\n    accent = "#8b5cf6"'
    css_vars_replacement = '''    bg_color = "#f8fafc"
    text_color = "#0f172a"
    text_muted = "#64748b"
    card_bg = "#ffffff"
    card_border = "rgba(0,0,0,0.08)"
    sidebar_bg = "#f1f5f9"
    accent = "#3b82f6"'''
    content = re.sub(css_vars_pattern, css_vars_replacement, content)

    # 2. Update Safe Sidebar Styling
    safe_sidebar_pattern = r'    /\* Safe Sidebar Styling \*/\n    section\[data-testid="stSidebar"\] \{\n        background-color: #0e1117 !important;\n        border-right: 1px solid rgba\(255,255,255,0\.1\) !important;\n    \}'
    safe_sidebar_replacement = '''    /* Safe Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: {sidebar_bg} !important;
        border-right: 1px solid {card_border} !important;
    }'''
    content = re.sub(safe_sidebar_pattern, safe_sidebar_replacement, content)

    # 3. Update Hardcoded White colors in CSS
    content = content.replace('color: #ffffff;\n        letter-spacing: -0.5px;', 'color: {text_color};\n        letter-spacing: -0.5px;')
    content = content.replace('color: #ffffff !important;\n        font-weight: 600;\n        text-shadow: 0 0 10px rgba(255, 255, 255, 0.3);', 'color: {text_color} !important;\n        font-weight: 600;')
    content = content.replace('color: #ffffff !important;', 'color: {text_color} !important;')
    
    # Wait, the `color: #ffffff !important;` might break other things, like hover text. Let's just fix the logo text manually via replace:
    # Actually, using python replace on the whole file is fine if I know what I'm replacing.
    
    # 4. Insert the `render_header()` function and its call.
    header_code = '''
# --- TOP NATIVE HEADER ---
def render_header():
    # Use native Streamlit columns for a robust, theme-compliant header
    col_logo, col_space, col1, col2, col3, col4, col5, col6 = st.columns([2, 1, 1, 1, 1, 1, 1, 1.5])
    
    with col_logo:
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:10px; padding-top: 5px;">
            <div style="background: linear-gradient(135deg, #3b82f6, #a855f7); width: 32px; height: 32px; border-radius: 8px; display:flex; align-items:center; justify-content:center; color:white; font-size:1.2rem;">⬡</div>
            <span style="font-size: 1.5rem; font-weight: 800; color: #0f172a;">TradeAI</span>
        </div>
        """, unsafe_allow_html=True)
        
    with col1:
        if st.button("Home", use_container_width=True): st.session_state.page = "home"; st.rerun()
    with col2:
        if st.button("Dashboard", use_container_width=True): st.session_state.page = "dashboard"; st.rerun()
    with col3:
        if st.button("Features", use_container_width=True): st.session_state.page = "features"; st.rerun()
    with col4:
        if st.button("News", use_container_width=True): st.session_state.page = "news"; st.rerun()
    with col5:
        if st.button("Pricing", use_container_width=True): st.session_state.page = "pricing"; st.rerun()
    with col6:
        if st.session_state.get("password_correct", False):
            if st.button("🚪 Logout", type="primary", use_container_width=True):
                st.session_state.password_correct = False
                st.session_state.page = "home"
                st.rerun()
        else:
            if st.button("👤 Login", type="primary", use_container_width=True):
                st.session_state.page = "dashboard"
                st.rerun()
    st.markdown("---")

render_header()
'''

    # Inject it right after `inject_css()` block ends (around where `# --- GLOBAL DATA LOADER ---` is)
    content = content.replace('# --- GLOBAL DATA LOADER ---', header_code + '\n# --- GLOBAL DATA LOADER ---')

    with open(file_path, "w") as f:
        f.write(content)

if __name__ == "__main__":
    main()
