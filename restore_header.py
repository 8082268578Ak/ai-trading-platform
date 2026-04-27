import re

def main():
    file_path = "/Users/amitkumar/Downloads/ai-trading-platform/app/streamlit_app.py"
    with open(file_path, "r") as f:
        content = f.read()

    # The sidebar code to replace
    sidebar_code_pattern = r'# --- PROFESSIONAL SIDEBAR NAVIGATION ---.*?render_sidebar\(\)'
    
    header_code = '''# --- PROFESSIONAL TOP NAVIGATION ---
def render_header():
    col_logo, col_space, col1, col2, col3, col4, col5, col6 = st.columns([2, 1, 1, 1, 1, 1, 1, 1.5])
    
    with col_logo:
        st.markdown("### ⬡ TradeAI")
        
    current_page = st.session_state.page
    
    with col1:
        if st.button("🏠 Home", use_container_width=True, type="primary" if current_page == "home" else "secondary"): 
            st.session_state.page = "home"; st.rerun()
    with col2:
        if st.button("📊 Dashboard", use_container_width=True, type="primary" if current_page == "dashboard" else "secondary"): 
            st.session_state.page = "dashboard"; st.rerun()
    with col3:
        if st.button("🌟 Features", use_container_width=True, type="primary" if current_page == "features" else "secondary"): 
            st.session_state.page = "features"; st.rerun()
    with col4:
        if st.button("📰 News", use_container_width=True, type="primary" if current_page == "news" else "secondary"): 
            st.session_state.page = "news"; st.rerun()
    with col5:
        if st.button("💳 Pricing", use_container_width=True, type="primary" if current_page == "pricing" else "secondary"): 
            st.session_state.page = "pricing"; st.rerun()
    with col6:
        if st.session_state.get("password_correct", False):
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.password_correct = False
                st.session_state.page = "home"
                st.rerun()
        else:
            if st.button("👤 Login", use_container_width=True):
                st.session_state.page = "dashboard"
                st.rerun()
    st.markdown("---")

render_header()'''

    content = re.sub(sidebar_code_pattern, header_code, content, flags=re.DOTALL)

    with open(file_path, "w") as f:
        f.write(content)

if __name__ == "__main__":
    main()
