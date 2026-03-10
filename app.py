import streamlit as st
import asyncio
import json
import time
import extra_streamlit_components as stx
import html
from google import genai
from google.genai import types

cookie_manager = stx.CookieManager(key="cookie_manager")

try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

    asyncio.set_event_loop(asyncio.new_event_loop())

st.set_page_config(page_title="서울광염교회 글쓰기 교정", page_icon="✨", layout="centered", initial_sidebar_state="collapsed")

def inject_custom_css():
    st.markdown("""
        <style>
        @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.8/dist/web/variable/pretendardvariable.css');
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&display=swap');
        
        /* Global Background and Font */
        .stApp {
            background-color: #FAF9F6;
            font-family: 'Pretendard Variable', Pretendard, -apple-system, BlinkMacSystemFont, system-ui, Roboto, 'Helvetica Neue', 'Segoe UI', 'Apple SD Gothic Neo', 'Noto Sans KR', 'Malgun Gothic', 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', sans-serif;
            color: #333333;
        }
        
        /* Typography overrides */
        h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            font-family: 'Playfair Display', serif !important;
            color: #1a1a1a;
        }
        
        /* Hide Default Streamlit Elements (Toolbar, Footer, Deploy button, Cloud Viewer Badge, Action Buttons) */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden !important;}
        [data-testid="stToolbar"] {visibility: hidden !important;}
        [data-testid="stAppDeployButton"] {display: none !important;}
        .stDeployButton {display: none !important;}
        .viewerBadge_container {display: none !important;}
        .viewerBadge_link {display: none !important;}
        [data-testid="stViewerBadge"] {display: none !important;}
        .stActionButton {display: none !important;}
        [data-testid="manage-app-button"] {display: none !important;}
        
        /* Ensure specific header area where toggle sidebar sits remains visible but background transparent */
        header[data-testid="stHeader"] {
            background-color: transparent !important;
            background: transparent !important;
            opacity: 1 !important;
            visibility: visible !important;
            pointer-events: none !important;
        }
        header[data-testid="stHeader"] * {
            pointer-events: auto !important;
            visibility: visible !important;
        }
        
        /* Aggressively Force Sidebar Toggle Button to be Always Visible */
        [data-testid="collapsedControl"], 
        [data-testid="stSidebarCollapsedControl"],
        button[kind="header"] {
            display: block !important;
            opacity: 1 !important;
            visibility: visible !important;
            color: #8c7b5f !important;
            background-color: transparent !important;
            transform: scale(1.3) translate(8px, 8px) !important;
            transition: none !important;
            z-index: 9999999 !important;
            pointer-events: auto !important;
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            border: none !important;
            box-shadow: none !important;
        }
        [data-testid="collapsedControl"] svg,
        [data-testid="stSidebarCollapsedControl"] svg,
        button[kind="header"] svg {
            fill: #8c7b5f !important;
            color: #8c7b5f !important;
            width: 2.2rem !important;
            height: 2.2rem !important;
            display: block !important;
            visibility: visible !important;
            opacity: 1 !important;
        }
        [data-testid="collapsedControl"]:hover *,
        [data-testid="stSidebarCollapsedControl"]:hover *,
        button[kind="header"]:hover * {
            fill: #5a4b32 !important;
            color: #5a4b32 !important;
        }
        
        /* Hide Default Sidebar Navigation Menu (app, main pages) */
        [data-testid="stSidebarNav"] {
            display: none !important;
            visibility: hidden !important;
            height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Override Streamlit's hover-to-show wrapper for header buttons */
        header[data-testid="stHeader"] > div,
        header[data-testid="stHeader"] .st-emotion-cache-1avcm0n, 
        header[data-testid="stHeader"] .st-emotion-cache-15ecox0,
        .st-emotion-cache-18ni7ap {
            opacity: 1 !important;
            visibility: visible !important;
            pointer-events: auto !important;
            display: block !important;
        }
        
        div:has(> [data-testid="collapsedControl"]),
        div:has(> [data-testid="stSidebarCollapsedControl"]) {
            opacity: 1 !important;
            visibility: visible !important;
            display: block !important;
            pointer-events: auto !important;
        }
        
        /* Background Blobs Setup */
        .blob-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: 0;
            overflow: hidden;
            pointer-events: none;
        }
        
        .blob1 {
            position: absolute;
            top: 15%;
            left: 20%;
            width: 50vw;
            height: 50vw;
            max-width: 600px;
            max-height: 600px;
            background: radial-gradient(circle, rgba(220,210,240,0.85) 0%, rgba(220,210,240,0) 70%);
            border-radius: 50%;
            filter: blur(40px);
            animation: float 10s ease-in-out infinite;
        }
        
        .blob2 {
            position: absolute;
            top: 45%;
            right: 10%;
            width: 30vw;
            height: 30vw;
            max-width: 400px;
            max-height: 400px;
            background: radial-gradient(circle, rgba(235,230,215,0.9) 0%, rgba(235,230,215,0) 70%);
            border-radius: 50%;
            filter: blur(30px);
            animation: float 12s ease-in-out infinite reverse;
        }
        
        .blob3 {
            position: absolute;
            top: 25%;
            left: 10%;
            width: 15vw;
            height: 15vw;
            max-width: 200px;
            max-height: 200px;
            background: radial-gradient(circle, rgba(200,180,220,0.9) 0%, rgba(200,180,220,0) 70%);
            border-radius: 50%;
            filter: blur(20px);
            animation: float 8s ease-in-out infinite;
        }

        @keyframes float {
            0% { transform: translate(0, 0); }
            50% { transform: translate(15px, 20px); }
            100% { transform: translate(0, 0); }
        }

        /* Custom Title Area */
        .custom-title-container {
            text-align: center;
            margin-top: 3rem;
            margin-bottom: 2rem;
            position: relative;
            z-index: 10;
        }
        .custom-title {
            font-family: 'Playfair Display', serif;
            font-size: clamp(3rem, 5vw, 5.5rem);
            font-weight: 400;
            margin-bottom: 0px;
            color: #A89574; /* Beige color requested */
            letter-spacing: -3.5px;
        }
        .custom-subtitle {
            font-family: 'Playfair Display', serif;
            font-size: clamp(1.5rem, 2.5vw, 2.2rem);
            font-style: italic;
            color: #4a4a4a;
            margin-bottom: 2rem;
            font-weight: 400;
        }
        .custom-desc {
            font-family: 'Pretendard Variable', Pretendard, sans-serif;
            font-size: 1.05rem;
            color: #666666; /* K60 color matching logo */
            max-width: 700px;
            margin: 0 auto;
            line-height: 1.7;
        }
        
        /* Streamlit specific label overrides */
        .stTextArea label p {
            color: #666666 !important; /* K60 color */
            font-family: 'Pretendard Variable', Pretendard, sans-serif !important;
            font-size: 1.05rem !important;
            display: none; /* Hide label as per request, use placeholder instead */
        }
        
        /* Custom Diamond Logo styles */
        .logo-container {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-bottom: 0.5rem;
        }
        .logo-container a {
            display: inline-block;
            transition: transform 0.2s ease;
        }
        .logo-container a:hover {
            transform: scale(1.05);
        }
        
        /* Make content relatively positioned so it sits above blobs */
        .block-container {
            position: relative;
            z-index: 10;
        }

        /* Hide default Streamlit status */
        [data-testid="stStatusWidget"] {
            visibility: hidden;
        }
        
        /* Pencil Animation */
        .pencil-anim {
            display: inline-block;
            width: 24px;
            height: 24px;
            background-image: url('data:image/svg+xml;utf8,<svg width="24" height="24" viewBox="0 0 24 24" fill="%238a8a8a" xmlns="http://www.w3.org/2000/svg"><path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/></svg>');
            background-repeat: no-repeat;
            background-position: center;
            background-size: contain;
            animation: pencil-write 1s infinite alternate;
            vertical-align: middle;
            margin-left: 8px;
        }

        @keyframes pencil-write {
            0% { transform: translate(0, 0) rotate(0deg); }
            50% { transform: translate(4px, -4px) rotate(15deg); }
            100% { transform: translate(8px, 0) rotate(0deg); }
        }
        </style>
        
        <div class="blob-bg">
            <div class="blob1"></div>
            <div class="blob2"></div>
            <div class="blob3"></div>
        </div>
    """, unsafe_allow_html=True)
    # Logic moved to global scope

def render_custom_header():
    st.markdown("""
        <div class="custom-title-container">
            <div class="logo-container">
                <a href="https://www.sls.or.kr/_bbs/" target="_blank" title="서울광염교회 홈페이지">
                    <svg width="60" height="60" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <polygon points="20,0 40,20 20,40 0,20" fill="#666666" />
                        <line x1="20" y1="0" x2="20" y2="40" stroke="#FAF9F6" stroke-width="2" />
                        <line x1="0" y1="20" x2="40" y2="20" stroke="#FAF9F6" stroke-width="2" />
                        <rect x="19" y="19" width="2" height="2" fill="#666666" />
                    </svg>
                </a>
            </div>
            <div class="custom-title">Writing Correction</div>
            <div class="custom-desc" style="margin-top: 2rem;">
                <strong>[ 교정 원칙 ]</strong><br>
                1. 서울광염교회 글쓰기 규정 중심적용<br>
                2. 국립국어원 표준어 규정 일반적용
            </div>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# Authentication & Sidebar Logic
# ==========================================

# Define Master Key for Creator (e.g., Pastor's specific access code)
MASTER_KEY = "admin777!" # Change this to the desired master key

saved_key = cookie_manager.get("gemini_api_key") or ""
global_key = ""
try:
    global_key = st.secrets.get("GEMINI_API_KEY", "")
except FileNotFoundError:
    pass

if "gemini_api_key" not in st.session_state:
    st.session_state.gemini_api_key = global_key or saved_key

current_input = st.session_state.gemini_api_key

is_admin = False
is_valid_key = False

if current_input:
    if current_input == MASTER_KEY:
        is_admin = True
        is_valid_key = True # Admin also needs app access 
        # For admin, we use the global key if available, otherwise they MUST have configured it previously
        if global_key:
            st.session_state.gemini_api_key_actual = global_key
    elif current_input.startswith("AIza"):
        is_valid_key = True
        st.session_state.gemini_api_key_actual = current_input

# Fallback: if somehow the global key is there and they just entered a general password?
if not getattr(st.session_state, "gemini_api_key_actual", None) and global_key and is_valid_key:
    st.session_state.gemini_api_key_actual = global_key

# Optional query param backdoor
if not is_admin and "admin" in st.query_params and st.query_params["admin"] == "true":
    is_admin = True
    
if not is_admin:
    # Hide sidebar completely for non-admins
    st.markdown("""
        <style>
        [data-testid="collapsedControl"], 
        [data-testid="stSidebarCollapsedControl"],
        [data-testid="stSidebarNav"],
        header[data-testid="stHeader"],
        button[kind="header"] {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;
            width: 0 !important;
            height: 0 !important;
        }
        div:has(> [data-testid="collapsedControl"]),
        div:has(> [data-testid="stSidebarCollapsedControl"]) {
            display: none !important;
        }
        </style>
    """, unsafe_allow_html=True)

inject_custom_css()
render_custom_header()

# ==========================================
# Main Header & Auth Area
# ==========================================

# Use Session State extensively for auth
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

# Top Right Auth UI Container
auth_placeholder = st.container()
with auth_placeholder:
    st.markdown('<div id="auth-anchor"></div>', unsafe_allow_html=True)
    
    st.markdown("""
        <style>
        /* Modern minimal text input styling */
        [data-testid="stTextInput"] div[data-baseweb="input"] {
            border-radius: 20px !important;
            background-color: rgba(255,255,255,0.7) !important;
            border: 1px solid #e0dcd5 !important;
            padding: 0 12px !important;
            backdrop-filter: blur(5px);
            transition: all 0.2s;
        }
        [data-testid="stTextInput"] div[data-baseweb="input"]:focus-within {
            border-color: #A89574 !important;
            background-color: rgba(255,255,255,0.95) !important;
            box-shadow: 0 0 0 1px #A89574 !important;
        }
        [data-testid="stTextInput"] input {
            font-family: 'Pretendard Variable', Pretendard, sans-serif !important;
            color: #666666 !important;
            font-size: 0.85rem !important;
            height: 32px !important;
        }
        [data-testid="stTextInput"] input::placeholder {
            color: #b0ada8 !important;
        }
        .key-link {
            text-align: right;
            margin-top: 5px;
            margin-right: 8px;
        }
        .key-link a {
            color: #A89574;
            text-decoration: none;
            font-family: 'Pretendard Variable', Pretendard, sans-serif !important;
            font-weight: 500;
            font-size: 0.75rem;
            transition: color 0.2s;
        }
        .key-link a:hover {
            color: #8c7b5f;
        }
        
        /* Error text style */
        .stAlert {
            padding: 0.5rem !important;
            margin-top: 0.5rem !important;
        }
        .stAlert p {
            font-size: 0.8rem !important;
            font-family: 'Pretendard Variable', Pretendard, sans-serif !important;
            margin-bottom: 0 !important;
        }
        
        /* Make Streamlit's container for the auth elements transparent and right-aligned */
        #auth-anchor {
            display: none;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Callback triggered immediately when Enter is pressed in text_input
    def handle_login_submit():
        val = st.session_state.get("api_key_widget_main", "").strip()
        if val:
            # Save the key into session state and cookie
            st.session_state.gemini_api_key = val
            cookie_manager.set("gemini_api_key", val)
            
            # Re-evaluate authentication immediately
            if val == MASTER_KEY:
                st.session_state.authenticated = True
                st.session_state.is_admin = True
                
                # Setup global key for admin if available
                global_key = ""
                try:
                    global_key = st.secrets.get("GEMINI_API_KEY", "")
                except FileNotFoundError:
                    pass
                if global_key:
                    st.session_state.gemini_api_key_actual = global_key
                st.rerun()
                    
            elif val.startswith("AIza"):
                st.session_state.authenticated = True
                st.session_state.is_admin = False
                st.session_state.gemini_api_key_actual = val
                st.rerun()
            else:
                st.session_state.authenticated = False
                st.session_state.is_admin = False

    # Also automatically evaluate saved_key on mount if unauthenticated
    if not st.session_state.get("authenticated", False):
        if saved_key == MASTER_KEY:
            st.session_state.authenticated = True
            st.session_state.is_admin = True
            global_key = ""
            try:
                global_key = st.secrets.get("GEMINI_API_KEY", "")
            except FileNotFoundError:
                pass
            if global_key:
                st.session_state.gemini_api_key_actual = global_key
        elif saved_key and saved_key.startswith("AIza"):
            st.session_state.authenticated = True
            st.session_state.is_admin = False
            st.session_state.gemini_api_key_actual = saved_key

    # Render UI conditionally
    if st.session_state.get("authenticated", False):
        badge_text = "제작자 모드" if st.session_state.get("is_admin", False) else "인증 완료"
        badge_color = "#A89574" if st.session_state.get("is_admin", False) else "#4a8b5b"
        st.markdown(f"""
            <div style="background-color: rgba(255,255,255,0.8); padding: 4px 12px; border-radius: 20px; border: 1px solid #e0dcd5; backdrop-filter: blur(5px);">
                <span style="color: {badge_color}; font-family: 'Pretendard Variable', Pretendard, sans-serif; font-size: 0.85rem; font-weight: 600;">✅ {badge_text}</span>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.text_input("Key", value=st.session_state.get("gemini_api_key", ""), type="password", placeholder="API 또는 마스터키 (Enter)", label_visibility="collapsed", key="api_key_widget_main", on_change=handle_login_submit)
        
        st.markdown("""
        <div class="key-link" style="margin-bottom: 4px;">
            <span style="color: #A89574; font-family: 'Pretendard Variable', Pretendard, sans-serif; font-size: 0.8rem; font-weight: 600;">API 키를 인증해주세요</span>
        </div>
        <div class="key-link" style="margin-top: 0; margin-bottom: 2px;">
            <a href="https://aistudio.google.com/app/apikey" target="_blank">🔑 무료 API 키 발급 바로가기</a>
        </div>
        <div style="font-family: 'Pretendard Variable', Pretendard, sans-serif; font-size: 0.75rem; color: #8a8178; line-height: 1.7; margin-top: 4px; padding-left: 2px;">
            <div>① 위 링크 클릭 → 구글 계정으로 로그인</div>
            <div>② <b style="color:#A89574;">Create API key</b> 버튼 클릭</div>
            <div>③ 생성된 키(<code style="font-size:0.72rem; background:#f5f0eb; padding:0 3px; border-radius:3px;">AIza...</code>)를 복사</div>
            <div>④ 위 입력창에 붙여넣기 후 <b style="color:#A89574;">Enter</b></div>
        </div>
        """, unsafe_allow_html=True)

        # Display validation error check using session state val
        val_check = st.session_state.get("gemini_api_key", "")
        if val_check and not (val_check.startswith("AIza") or val_check == MASTER_KEY) and not st.session_state.get("authenticated", False):
            st.error("❌ 잘못된 인증키")

    # Always position the auth container at top-right (works for both badge and input)
    st.components.v1.html("""
        <script>
            const positionAuthContainer = () => {
                const anchor = window.parent.document.getElementById('auth-anchor');
                if (anchor) {
                    const container = anchor.closest('[data-testid="stVerticalBlock"]');
                    if (container) {
                        container.style.position = 'absolute';
                        container.style.top = '3.5rem';
                        container.style.right = '2rem';
                        container.style.width = '240px';
                        container.style.zIndex = '999999';
                        container.style.background = 'transparent';
                        container.style.boxShadow = 'none';
                        container.style.border = 'none';
                    }
                }
            };
            positionAuthContainer();
            setTimeout(positionAuthContainer, 300);

            // Auto submit from LocalStorage
            const anchor = window.parent.document.getElementById('auth-anchor');
            const savedKey = window.localStorage.getItem('gemini_api_key_local');
            if (anchor && savedKey) {
                const container = anchor.closest('[data-testid="stVerticalBlock"]');
                if(container) {
                    const inputs = container.querySelectorAll('input[type="password"]');
                    for (let input of inputs) {
                        if (!input.value && savedKey.length > 0) {
                            let setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
                            setter.call(input, savedKey);
                            input.dispatchEvent(new Event('input', { bubbles: true }));
                            setTimeout(() => {
                                input.blur();
                                const enterEvent = new window.parent.KeyboardEvent('keydown', {
                                    key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true, cancelable: true
                                });
                                input.dispatchEvent(enterEvent);
                            }, 300);
                        }
                    }
                }
            }

            // Track manual entry into LocalStorage
            if (anchor) {
                const container = anchor.closest('[data-testid="stVerticalBlock"]');
                if(container) {
                    const inputs = container.querySelectorAll('input[type="password"]');
                    for (let input of inputs) {
                        if (!input.dataset.enterBound) {
                            input.dataset.enterBound = "true";
                            input.addEventListener('keydown', function(event) {
                                if (event.key === 'Enter') {
                                    if (this.value) {
                                        window.localStorage.setItem('gemini_api_key_local', this.value);
                                    }
                                }
                            });
                        }
                    }
                }
            }
        </script>
    """, height=0)


# Sidebar layout (Only shown for Admin per CSS logic above)
with st.sidebar:
    st.markdown("""
        <div id="my-custom-profile" style="margin-top: 3rem; display: flex; align-items: center; padding-bottom: 20px; margin-bottom: 20px; border-bottom: 1px solid rgba(168, 149, 116, 0.2); cursor: pointer; transition: opacity 0.2s;" onmouseover="this.style.opacity='0.7'" onmouseout="this.style.opacity='1'">
            <div style="width: 36px; height: 36px; border-radius: 50%; background-color: #A89574; display: flex; align-items: center; justify-content: center; margin-right: 12px;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
            </div>
            <div style="color: #A89574; font-weight: 600; font-family: 'Pretendard Variable', Pretendard, sans-serif; font-size: 1.05rem;">Manage Cloud</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.components.v1.html("""
        <script>
            const initCloudCleaner = () => {
                const parent = window.parent.document;
                
                // Aggressive element hider
                const cleanDOM = () => {
                    const selectors = [
                        '.viewerBadge_container', '[id*="viewerBadge"]', '[data-testid="manage-app-button"]', 
                        '[data-testid="stViewerBadge"]', '[class*="viewerBadge"]', '#creatorBadge', 
                        'a[href*="streamlit.io/cloud"]'
                    ];
                    
                    const profileBtn = parent.querySelector(selectors.join(', '));
                    if (profileBtn) {
                        window._streamlitProfileBtn = profileBtn; 
                    }

                    const allCloudElements = parent.querySelectorAll(selectors.join(', '));
                    allCloudElements.forEach(el => {
                        el.style.setProperty("display", "none", "important");
                        el.style.setProperty("visibility", "hidden", "important");
                        el.style.setProperty("opacity", "0", "important");
                        el.style.setProperty("pointer-events", "none", "important");
                        
                        if(el.parentElement && el.parentElement.tagName === 'DIV' && el.parentElement !== parent.body) {
                            el.parentElement.style.setProperty("display", "none", "important");
                            el.parentElement.style.setProperty("opacity", "0", "important");
                        }
                    });
                    
                    const allDivs = parent.querySelectorAll('div');
                    allDivs.forEach(div => {
                        const style = window.getComputedStyle(div);
                        if (style.position === 'fixed' || style.position === 'absolute') {
                             const bottom = parseInt(style.bottom);
                             const right = parseInt(style.right);
                             const zIndex = parseInt(style.zIndex);
                             if (!isNaN(bottom) && bottom <= 50 && !isNaN(right) && right <= 50 && !isNaN(zIndex) && zIndex > 10) {
                                 div.style.setProperty("display", "none", "important");
                                 div.style.setProperty("opacity", "0", "important");
                                 div.style.setProperty("pointer-events", "none", "important");
                                 if(!window._streamlitProfileBtn) {
                                     window._streamlitProfileBtn = div.querySelector('button') || div.querySelector('a') || div;
                                 }
                             }
                        }
                    });
                    
                    const actionElems = parent.querySelectorAll('[data-testid="stActionElements"], .stActionButton, [data-testid="stAppDeployButton"]');
                    actionElems.forEach(el => {
                        if (!el.querySelector('[data-testid="collapsedControl"]') && !el.closest('[data-testid="collapsedControl"]')) {
                            el.style.setProperty("display", "none", "important");
                            el.style.setProperty("visibility", "hidden", "important");
                            el.style.setProperty("opacity", "0", "important");
                            el.style.setProperty("pointer-events", "none", "important");
                        }
                    });
                    
                    const toolbar = parent.querySelector('[data-testid="stToolbar"]');
                    if (toolbar) {
                        toolbar.style.setProperty("visibility", "hidden", "important");
                    }
                };
                
                setInterval(cleanDOM, 500);
                cleanDOM();
                
                const myProfile = document.getElementById("my-custom-profile");
                if (myProfile && !myProfile.dataset.bound) {
                    myProfile.dataset.bound = "true";
                    myProfile.addEventListener("click", () => {
                         if (window._streamlitProfileBtn) {
                             const btn = window._streamlitProfileBtn.querySelector('button') || 
                                         window._streamlitProfileBtn.querySelector('a') || 
                                         window._streamlitProfileBtn;
                             if(btn && typeof btn.click === 'function') {
                                 btn.click();
                             } else {
                                 alert("프로필 또는 클라우드 메뉴를 열 수 없습니다.");
                             }
                         } else {
                             alert("클라우드 설정에 연결할 수 없습니다. Streamlit 커뮤니티 클라우드 환경에서만 동작합니다.");
                         }
                    });
                }
            };
            if(document.readyState === 'complete') initCloudCleaner();
            else window.addEventListener('load', initCloudCleaner);
        </script>
    """, height=0)
    
    st.markdown("<h3 style='margin-bottom: 15px; color: #A89574;'>Menu</h3>", unsafe_allow_html=True)
    st.markdown("""
    <style>
    .custom-sidebar-link {
        display: flex;
        align-items: center;
        padding: 12px 15px;
        color: #A89574 !important;
        text-decoration: none;
        font-weight: 500;
        border-radius: 8px;
        margin-bottom: 5px;
        transition: all 0.2s;
        font-family: 'Pretendard Variable', Pretendard, sans-serif;
        font-size: 0.95rem;
    }
    .custom-sidebar-link:hover {
        background-color: rgba(168, 149, 116, 0.1);
        text-decoration: none;
    }
    .custom-sidebar-icon {
        margin-right: 12px;
        width: 18px;
        height: 18px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .custom-sidebar-icon svg {
        width: 100%;
        height: 100%;
        stroke: currentColor;
        stroke-width: 2;
        stroke-linecap: round;
        stroke-linejoin: round;
        fill: none;
    }
    </style>
    <a href="#" onclick="navigator.clipboard.writeText(window.location.href); alert('현재 앱의 URL이 복사되었습니다!'); return false;" class="custom-sidebar-link">
        <span class="custom-sidebar-icon"><svg viewBox="0 0 24 24"><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><polyline points="16 6 12 2 8 6"/><line x1="12" y1="2" x2="12" y2="15"/></svg></span>
        Share
    </a>
    <a href="https://github.com/skimbo777/skimbo777-Writing-Correction/stargazers" target="_blank" class="custom-sidebar-link">
        <span class="custom-sidebar-icon"><svg viewBox="0 0 24 24"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg></span>
        Star
    </a>
    <a href="https://github.com/skimbo777/skimbo777-Writing-Correction/edit/main/app.py" target="_blank" class="custom-sidebar-link">
        <span class="custom-sidebar-icon"><svg viewBox="0 0 24 24"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg></span>
        Edit
    </a>
    <a href="https://github.com/skimbo777/skimbo777-Writing-Correction" target="_blank" class="custom-sidebar-link">
        <span class="custom-sidebar-icon"><svg viewBox="0 0 24 24"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/></svg></span>
        GitHub
    </a>
    <a href="https://github.com/skimbo777/skimbo777-Writing-Correction/fork" target="_blank" class="custom-sidebar-link">
        <span class="custom-sidebar-icon"><svg viewBox="0 0 24 24"><line x1="6" y1="3" x2="6" y2="15"/><circle cx="18" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M18 9a9 9 0 0 1-9 9"/></svg></span>
        Fork
    </a>
    <div style="margin-top: 15px;"></div>
    <a href="https://streamlit.io/" target="_blank" class="custom-sidebar-link" style="border-top: 1px solid rgba(168, 149, 116, 0.2); padding-top: 18px; border-radius: 0;">
        <span class="custom-sidebar-icon"><svg viewBox="0 0 24 24"><path d="M2 22h20"/><path d="M12 2l4 8 6-4-3 14H5L2 6l6 4z"/></svg></span>
        Streamlit
    </a>
    <a href="https://share.streamlit.io/" target="_blank" class="custom-sidebar-link">
        <span class="custom-sidebar-icon"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg></span>
        Manage app
    </a>
    """, unsafe_allow_html=True)

# Session state initialization
if "suggestions" not in st.session_state:
    st.session_state.suggestions = None
if "original_text" not in st.session_state:
    st.session_state.original_text = ""
if "final_text" not in st.session_state:
    st.session_state.final_text = ""
    
if "show_success" not in st.session_state:
    st.session_state.show_success = False

if "main_text_input" not in st.session_state:
    st.session_state.main_text_input = ""

if "do_analyze" not in st.session_state:
    st.session_state.do_analyze = False

if "input_error" not in st.session_state:
    st.session_state.input_error = None

def trigger_analysis():
    st.session_state.do_analyze = True
    st.session_state.input_error = None

loading_placeholder_top = st.empty()

if st.session_state.suggestions is None:
    if st.session_state.show_success:
        st.markdown('<div class="custom-desc" style="text-align: center; padding: 1rem; border-radius: 0.5rem; background-color: rgba(74, 139, 91, 0.1); color: #2b5937; margin-bottom: 1rem; border: 1px solid rgba(74, 139, 91, 0.2);">✨ 교정이 완료되어 아래 텍스트 창에 완성본이 반영되었습니다!</div>', unsafe_allow_html=True)
        st.toast("교정이 완료되었습니다!", icon="🎉")
        st.session_state.show_success = False
        
    with loading_placeholder_top.container():
        col_btn, col_msg = st.columns([2, 8])
        with col_btn:
            if not st.session_state.do_analyze:
                st.button("교정하기", type="primary", on_click=trigger_analysis, use_container_width=True)
            else:
                # During analysis, analyze_text will populate this container via loading_placeholder_top
                pass
        with col_msg:
            if st.session_state.input_error:
                st.markdown(f'<div style="background-color: rgba(255, 243, 205, 0.6); color: #856404; padding: 0.5rem 1rem; border-radius: 0.5rem; border: 1px solid rgba(255, 243, 205, 1); font-size: 0.85rem; display: flex; align-items: center; min-height: 42px;">{st.session_state.input_error}</div>', unsafe_allow_html=True)
        
    user_text = st.text_area("main_input", height=450, placeholder="교정할 글을 입력해주세요... (단축키: Cmd/Ctrl + Enter 로 즉시 교정)", label_visibility="collapsed", key="main_text_input")

    # Clear Input Button
    c1, c2, _ = st.columns([2, 2, 6])
    with c1:
        if st.button("입력창 초기화", use_container_width=True):
            st.session_state.main_text_input = ""
            st.session_state.input_error = None
            st.rerun()

    # Shortcut script for Cmd/Ctrl + Enter
    st.components.v1.html("""
        <script>
            const parent = window.parent.document;
            // Find textareas and bind
            const bindShortcuts = () => {
                const textareas = parent.querySelectorAll('textarea');
                textareas.forEach(ta => {
                    if (!ta.dataset.shortcutBound) {
                        ta.dataset.shortcutBound = "true";
                        ta.addEventListener('keydown', function(e) {
                            if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
                                e.preventDefault(); // prevent new line
                                e.stopPropagation(); // prevent React from eating the event
                                
                                // Force Streamlit to sync the typed text by blurring
                                ta.blur(); 
                                
                                setTimeout(() => {
                                    // Find '교정하기' button
                                    const buttons = Array.from(parent.querySelectorAll('button'));
                                    const correctBtn = buttons.find(b => b.textContent && b.textContent.includes('교정하기'));
                                    if (correctBtn && !correctBtn.disabled) {
                                        correctBtn.click();
                                    }
                                }, 300); // 300ms is safe enough for Streamlit to sync text
                                
                                // Return focus after click
                                setTimeout(() => {
                                    ta.focus();
                                }, 600);
                            }
                        }, { capture: true }); // Use capture phase to intercept before Streamlit binds
                    }
                });
            };
            // Retry a few times in case the DOM isn't fully ready
            setTimeout(bindShortcuts, 500);
            setTimeout(bindShortcuts, 1500);
            setInterval(bindShortcuts, 3000);
        </script>
    """, height=0)

SYSTEM_PROMPT = """
당신은 완벽한 전문 교정가입니다.

[가장 중요한 원칙 - 문장 및 양식 보존]
**AI가 문장 전체를 새로 쓰거나 치환, 구조를 변경하는 것을 절대 금지합니다.** 사용자의 고유한 문체와 문장 구조뿐만 아니라, 원문에 포함된 **줄바꿈(엔터), 문단 나누기, 띄어쓰기 간격 등 모든 서식과 양식을 100% 그대로 유지**하는 것이 최우선입니다. 오류가 있는 부분만 최소한으로 단어 단위로 고치세요.

[서울광염교회 주요 글쓰기 규정 ("type": "correction")]
1. 존칭: '시', '께서' 등의 존칭 선어말 어미와 겸양어는 하나님, 예수님, 성령님께만 사용합니다. 사람에게는 쓰지 않습니다. (예: 목사님이 하셨습니다(X) -> 목사님이 했습니다(O)) 직분 뒤에만 '님'을 씁니다.
2. 주어 생략/반복: 반복되는 주어는 생략을 원칙으로 하며, 부득이 반복할 경우 '이름'은 빼고 '성+직분'(예: 홍 목사)으로 쓰거나, 성별 무관하게 대명사 '그'를 씁니다. (그녀, 그분 사용 금지).
3. 띄어쓰기: 숫자, 화폐 단위, 명수는 띄어쓰지 않고 무조건 붙여 씁니다. (예: 3억원, 1만5천명). 그 외의 일반적인 한글 맞춤법 띄어쓰기 오류도 모두 꼼꼼하게 교정하세요.
4. 문체: 한 글 안에서 해라체/하십시오체가 혼용되지 않도록 일관성 있게 하나로 통일.
5. 호응 및 시제: 주어와 서술어 호응, 국어시제법 완벽 일치.

[단어 단위 추천 - 문학적 어휘 제안 ("type": "suggestion")]
문장에 쓰인 단어 중, 문맥상 더 아름다운 시적 표현이나 상황에 적합한 서정적/문학적 단어가 있다면 그 단어만 선별하여 리스트로 추천해 주세요. (예: 'original': '은혜가 큽니다', 'correction': ['무궁합니다', '지극합니다']). 이런 문학적 어휘 제안은 "type": "suggestion" 으로 분류합니다.

사용자의 글을 분석하여 찾은 모든 오류 및 문학적 어휘 제안을 반드시 아래의 순수 JSON 배열 형식으로만 반환하세요.
형식: [{"type": "correction" 또는 "suggestion", "original": "해당 단어나 문구", "correction": ["수정제안1", "수정제안2"], "reason": "교정 이유 또는 추천 사유"}, ...]
반드시 "correction" 필드는 대괄호 `[]`를 사용하여 배열(리스트) 형태로 여러 개의 후보를 제안하세요. (후보가 하나라도 배열로 반환하세요.)
에러나 제안이 없으면 반드시 빈 배열 `[]`만 반환하세요. 앞뒤 추가 설명 없이 오직 JSON 배열만 출력해야 합니다.
"""

@st.cache_data(show_spinner=False, ttl=600)
def _get_cached_analysis(text, api_key_to_use, system_prompt):
    client = genai.Client(api_key=api_key_to_use)
    safety_settings = [
        types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_HARASSMENT, threshold=types.HarmBlockThreshold.BLOCK_NONE),
        types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH, threshold=types.HarmBlockThreshold.BLOCK_NONE),
        types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, threshold=types.HarmBlockThreshold.BLOCK_NONE),
        types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, threshold=types.HarmBlockThreshold.BLOCK_NONE),
    ]
    prompt = f"{system_prompt}\n\n[사용자 입력 글]\n{text}"
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=prompt,
        config=types.GenerateContentConfig(safety_settings=safety_settings)
    )
    return response.text.strip()

def analyze_text(text, countdown_placeholder=None):
    if not st.session_state.get("authenticated", False):
        st.warning("❌ 우측 상단에서 인증을 먼저 완료해주세요.")
        return None

    api_key_to_use = st.session_state.get("gemini_api_key_actual") or st.session_state.get("api_key_widget_main") or st.session_state.get("gemini_api_key")
    if api_key_to_use == MASTER_KEY or st.session_state.get("is_admin", False):
        try:
            api_key_to_use = st.secrets.get("GEMINI_API_KEY", "")
        except FileNotFoundError:
            pass

    if not api_key_to_use:
        st.error("❌ 유효한 Gemini API 키가 없습니다. 우측 상단에 올바른 키를 입력해주세요.")
        return None

    MAX_RETRIES = 5

    _cd = countdown_placeholder if countdown_placeholder is not None else st.empty()

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            with _cd.container():
                col1, col2 = st.columns([2, 8])
                with col1:
                    if st.button("중지", type="primary", key=f"stop_analyze_{attempt}"):
                        st.session_state.do_analyze = False
                        st.session_state.input_error = None
                        st.rerun()
                with col2:
                    st.markdown("<div style='font-size:1.05rem; color:#444; margin-top: 5px; font-weight:600;'>교정 중입니다... (Processing...) <span class='pencil-anim'></span></div>", unsafe_allow_html=True)
            
            # Using cached helper to avoid redundant API hits for same input
            content = _get_cached_analysis(text, api_key_to_use, SYSTEM_PROMPT)
            
            start_idx = content.find('[')
            end_idx = content.rfind(']')
            if start_idx != -1 and end_idx != -1 and end_idx >= start_idx:
                return json.loads(content[start_idx:end_idx+1])
            else:
                raise ValueError("Invalid JSON format from Gemini.")
        except Exception as e:
            error_msg = str(e).lower()
            full_error = str(e)
            is_quota = "429" in error_msg or "exhaust" in error_msg or "quota" in error_msg or "too many" in error_msg
            is_api_key = "api_key" in error_msg or "api key" in error_msg or "permission" in error_msg or "invalid argument" in error_msg or "api_key_invalid" in error_msg or "unauthorized" in error_msg
            is_safety = "safety" in error_msg or "blocked" in error_msg or "candidate" in error_msg
            is_json = "invalid json format" in error_msg

            # Don't retry on non-transient errors
            if is_api_key or is_safety or is_json:
                _cd.empty()
                if is_api_key:
                    st.session_state.input_error = "❌ API 키가 유효하지 않습니다. 우측 상단에 올바른 API 키를 입력했는지 확인해주세요."
                elif is_safety:
                    st.session_state.input_error = "❌ 구글 안전 정책에 의해 답변 생성이 차단되었습니다. 입력하신 내용을 확인해주세요."
                else:
                    st.session_state.input_error = "❌ AI가 올바른 형식으로 답변하지 못했습니다. 다시 시도해 주세요."
                return None

            if attempt < MAX_RETRIES:
                wait_secs = 30 if is_quota else 10
                for remaining in range(wait_secs, 0, -1):
                    with _cd.container():
                        col1, col2 = st.columns([2, 8])
                        with col1:
                            if st.button("중지", type="primary", key=f"stop_retry_{attempt}_{remaining}"):
                                st.session_state.do_analyze = False
                                st.session_state.input_error = None
                                st.rerun()
                        with col2:
                            st.markdown(
                                f"""<div style='font-size:1.05rem; color:#444; font-weight:600; padding:0.4rem 0; display:flex; align-items:center; gap:0.8rem; flex-wrap:wrap;'>
                                <span>✏️ 교정 중입니다... (Processing...)</span>
                                <span style='background:rgba(255,243,205,0.95); color:#856404; padding:0.2rem 0.8rem; border-radius:0.5rem; border:1px solid rgba(220,190,80,0.6); font-size:0.88rem; font-weight:500; white-space:nowrap;'>
                                ⏳ {remaining}초 후 자동 재시도 ({attempt}/{MAX_RETRIES}회차)
                                </span>
                                </div>""",
                                unsafe_allow_html=True
                            )
                    time.sleep(1)
            else:
                _cd.empty()
                if is_quota:
                    st.session_state.input_error = "❌ 구글 API(무료 티어) 사용량 초과로 5회 재시도 후에도 실패했습니다. 1분 뒤에 다시 시도해 주세요."
                else:
                    st.session_state.input_error = f"❌ 5번 재시도 후에도 오류가 발생했습니다: {full_error}"
                return None
    _cd.empty()
    return None


if st.session_state.do_analyze:
    st.session_state.do_analyze = False # Reset immediately
    
    user_text_val = st.session_state.get("main_text_input", "") 
    if not user_text_val.strip():
        st.session_state.input_error = "교정할 글을 입력해주세요."
        st.rerun()
    else:
        # Reset state upon new analysis
        st.session_state.suggestions = None
        st.session_state.final_text = ""
        st.session_state.original_text = ""
        
        # The button and status will be managed inside analyze_text via loading_placeholder_top
        st.session_state.original_text = user_text_val
        suggestions = analyze_text(user_text_val, countdown_placeholder=loading_placeholder_top)
        loading_placeholder_top.empty()
        
        if suggestions is not None:
            st.session_state.suggestions = suggestions
            st.rerun()
        else:
            # Error stored in input_error — rerun to show it via the persistent error box
            st.rerun()
                
if st.session_state.suggestions is not None:
    # Render interactive text area replacement
    st.markdown('<div class="custom-desc" style="text-align: center; margin-bottom: 10px;">📝 분석된 원문 (틀린 단어 위에 마우스를 올리면 교정 내용이 보입니다)</div>', unsafe_allow_html=True)
    
    corrections = [s for s in st.session_state.suggestions if s.get("type", "correction") != "suggestion"]
    literary_suggestions = [s for s in st.session_state.suggestions if s.get("type") == "suggestion"]
    all_sugs = corrections + literary_suggestions
    
    cmd_col1, cmd_col2, cmd_col3, _ = st.columns([2.5, 4.5, 1.5, 1.5])
    with cmd_col1:
        reset_clicked = st.button("돌아가기 (계속 편집)")
    with cmd_col2:
        generate_clicked = st.button("모든 교정 제안을 적용하여 완성하기", type="primary")
    with cmd_col3:
        gen_stop_placeholder = st.empty()
        
    if reset_clicked:
        st.session_state.main_text_input = st.session_state.original_text
        st.session_state.suggestions = None
        st.session_state.final_text = ""
        st.rerun()
        
    if generate_clicked:
        selected_suggestions = []
        user_choices_str = st.session_state.get("hidden_choices_input", "{}")
        try:
            user_choices = json.loads(user_choices_str)
        except:
            user_choices = {}
            
        for i, sug in enumerate(all_sugs):
            orig = sug.get('original', '')
            choice = user_choices.get(str(i))
            
            if not choice:
                corr_raw = sug.get('correction', [])
                if isinstance(corr_raw, list) and len(corr_raw) > 0:
                    choice = corr_raw[0]
                elif isinstance(corr_raw, str):
                    choice = [c.strip() for c in corr_raw.split(',')][0]
                else:
                    choice = orig

            if choice != orig:
                selected_suggestions.append({
                    'original': orig,
                    'correction': choice
                })
            
        with gen_stop_placeholder.container():
            st.button("중지", type="primary", key="stop_gen")
            
        loading_placeholder2 = st.empty()
        with loading_placeholder2.container():
            st.markdown("<div style='font-size:1.05rem; color:#444; margin-top: 5px;'>교정된 글을 생성하고 있습니다... <span class='pencil-anim'></span></div>", unsafe_allow_html=True)

        APPLY_PROMPT = """
        당신은 전문 교정가입니다. 
        사용자가 작성한 <원본 글>과 <승인한 수정 및 추천 표현들>을 제공받습니다.
        **최우선 원칙**: AI가 문장 전체를 새로 쓰거나 구조를 변경하는 것을 절대 금지합니다. 사용자의 고유한 문체, 문장 구조, 그리고 **줄바꿈(엔터) 처리를 포함한 모든 원문의 단락 구분을 100% 그대로 유지**해야 합니다. 빈 줄(엔터) 하나라도 임의로 삭제하거나 통합하지 마세요.
        오직 <승인한 목록>에 있는 단어/문구만 그 자리에서 정확히 교체하고, 다른 어휘나 문장 논리는 절대 임의로 바꾸지 마세요.
        (단, 문체가 혼용된 경우에 한해 일관성 있게 마지막 맺음말을 자연스럽게 조정하세요.)
        완성된 글 텍스트만 출력하세요. 다른 설명은 덧붙이지 마세요.
        """
            
        user_content = f"<원본 글>\n{st.session_state.original_text}\n\n<승인한 수정 및 추천 표현들>\n"
        for s in selected_suggestions:
            user_content += f"- '{s.get('original', '')}' -> '{s.get('correction', '')}'\n"
            
        try:
            api_key_to_use = st.session_state.get("gemini_api_key_actual") or st.session_state.get("api_key_widget_main") or st.session_state.get("gemini_api_key")
            if api_key_to_use == MASTER_KEY or st.session_state.get("is_admin", False):
                try:
                    api_key_to_use = st.secrets.get("GEMINI_API_KEY", "")
                except FileNotFoundError:
                    pass
            
            client = genai.Client(api_key=api_key_to_use)
            prompt = f"{APPLY_PROMPT}\n\n{user_content}"
            safety_settings = [
                types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_HARASSMENT, threshold=types.HarmBlockThreshold.BLOCK_NONE),
                types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH, threshold=types.HarmBlockThreshold.BLOCK_NONE),
                types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, threshold=types.HarmBlockThreshold.BLOCK_NONE),
                types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, threshold=types.HarmBlockThreshold.BLOCK_NONE),
            ]

            MAX_RETRIES = 5
            apply_resp = None
            apply_countdown = st.empty()
            for attempt in range(1, MAX_RETRIES + 1):
                try:
                    apply_countdown.empty()
                    apply_resp = client.models.generate_content(
                        model='gemini-2.0-flash',
                        contents=prompt,
                        config=types.GenerateContentConfig(safety_settings=safety_settings)
                    )
                    break  # success
                except Exception as inner_e:
                    inner_msg = str(inner_e).lower()
                    is_transient = "429" in inner_msg or "exhaust" in inner_msg or "quota" in inner_msg or "too many" in inner_msg
                    if is_transient and attempt < MAX_RETRIES:
                        wait_secs = 30 if is_transient else 10
                        for remaining in range(wait_secs, 0, -1):
                            apply_countdown.markdown(
                                f"""<div style='text-align:center; padding:0.6rem; border-radius:0.5rem; background:rgba(255,243,205,0.7); color:#856404; border:1px solid rgba(255,238,170,1); font-size:0.9rem; margin-bottom:0.5rem;'>
                                ⏳ 사용량 초과 감지. <b>{remaining}의</b> 후 자동 재시도합니다... ({attempt}/{MAX_RETRIES}회차)
                                </div>""",
                                unsafe_allow_html=True
                            )
                            time.sleep(1)
                    else:
                        apply_countdown.empty()
                        raise  # re-raise for outer except
            apply_countdown.empty()

            if apply_resp is None:
                raise RuntimeError("재시도 후에도 응답없음")

            st.session_state.main_text_input = apply_resp.text.strip()
            st.session_state.suggestions = None
            st.session_state.original_text = ""
            st.session_state.final_text = ""
            st.session_state.show_success = True
            st.rerun()
            
        except Exception as e:
            error_msg = str(e).lower()
            if "429" in error_msg or "exhaust" in error_msg or "quota" in error_msg or "too many" in error_msg:
                st.error("❌ 사용량이 많아 잠시 숨을 고르고 있습니다. 30초 뒤에 다시 완성하기 버튼을 눌러주세요.")
            elif "api_key" in error_msg or "api key" in error_msg or "permission" in error_msg or "invalid argument" in error_msg:
                st.error("❌ API 키가 유효하지 않습니다. 올바른 API 키를 입력해주세요.")
            elif "safety" in error_msg or "blocked" in error_msg or "candidate" in error_msg:
                st.error("❌ 구글 안전 정책에 의해 답변 생성이 차단되었습니다.")
            else:
                st.error(f"❌ 오류가 발생했습니다: {str(e)}\n\n(잠시 후 다시 시도해주세요.)")
            
        loading_placeholder2.empty()

    annotated_text = html.escape(st.session_state.original_text)
    
    st.markdown('<div style="display: none;">', unsafe_allow_html=True)
    st.text_input("hidden_choices", value="{}", key="hidden_choices_input", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <style>
        /* Hide the hidden_choices_input text box entirely */
        div[data-testid="stTextInput"] {
            display: none !important;
        }
        
        /* Force tooltip visibility over container scroll boundaries */
        section[data-testid="stMarkdownContainer"] {
            overflow: visible !important;
        }
        .stMarkdown {
            overflow: visible !important;
        }
        .highlight-word {
            position: relative;
            cursor: pointer;
            background-color: rgba(255, 209, 217, 0.4);
            border-radius: 3px;
            padding: 0 2px;
            border-bottom: 2px dashed #f28b9c;
            color: #b02a46;
            transition: all 0.2s ease;
        }
        .highlight-word:hover, .highlight-word:active {
            background-color: rgba(255, 209, 217, 1);
        }
        .word-hover-tooltip {
            position: absolute;
            background: #fff;
            color: #333;
            padding: 12px;
            border-radius: 8px;
            white-space: pre-wrap;
            font-size: 0.95rem;
            z-index: 10000;
            width: max-content;
            max-width: 320px;
            line-height: 1.5;
            box-shadow: 0 4px 15px rgba(0,0,0,0.15);
            border: 1px solid #eee;
            text-align: left;
            pointer-events: none;
            font-family: inherit;
            transform: translateX(-50%);
        }
        .word-hover-tooltip::after {
            content: '';
            position: absolute;
            top: 100%;
            left: 50%;
            margin-left: -8px;
            border-width: 8px;
            border-style: solid;
            border-color: #fff transparent transparent transparent;
        }
        .highlight-word.resolved {
            background-color: rgba(74, 139, 91, 0.2);
            border-bottom: 2px solid #4a8b5b;
            color: #2b5937;
        }
        .word-popup {
            position: absolute;
            background: #fff;
            border: 1px solid #ccc;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            border-radius: 8px;
            z-index: 10001;
            padding: 5px;
            display: flex;
            flex-direction: column;
            min-width: 140px;
            font-family: inherit;
        }
        .word-popup-option {
            padding: 8px 12px;
            cursor: pointer;
            border-radius: 4px;
            font-size: 0.95rem;
            color: #333;
        }
        .word-popup-option:hover {
            background-color: #f0f0f0;
        }
    </style>
    """, unsafe_allow_html=True)
    
    user_choices_str = st.session_state.get("hidden_choices_input", "{}")
    try:
        user_choices = json.loads(user_choices_str)
    except:
        user_choices = {}
        
    for i, sug in enumerate(all_sugs):
        raw_orig = sug.get('original', '')
        orig = html.escape(raw_orig)
        
        corr_raw = sug.get('correction', [])
        if isinstance(corr_raw, str):
            options = [c.strip() for c in corr_raw.split(',')]
        else:
            options = corr_raw
        options = list(dict.fromkeys(options))
        
        reason = html.escape(sug.get('reason', ''))
        sug_type = sug.get('type', 'correction')
        
        corr_display = ", ".join(options)
        
        if sug_type == 'suggestion':
            tooltip_text = f"✨ 어휘 추천\\n💡 {corr_display}\\n({reason})\\n👉 클릭하여 단어 선택"
        else:
            tooltip_text = f"🔍 수정 제안\\n❌ {orig}\\n✅ {corr_display}\\n({reason})\\n👉 클릭하여 단어 선택"
            
        options_json = html.escape(json.dumps(options).replace("'", "\\'"))
        
        raw_choice = user_choices.get(str(i))
        if not raw_choice:
            raw_choice = raw_orig
            
        display_text = html.escape(raw_choice)
        resolved_class = " resolved" if raw_choice != raw_orig else ""
        
        if orig and orig in annotated_text:
            span_html = f'<span class="highlight-word{resolved_class}" data-index="{i}" data-orig="{orig}" data-options=\'{options_json}\' data-tooltip="{tooltip_text}">{display_text}</span>'
            annotated_text = annotated_text.replace(orig, span_html, 1)
            
    pseudo_textarea_html = f'''
    <div id="original-text-display" style="
        white-space: pre-wrap; 
        background-color: #fff; 
        border: 1px solid #ccc; 
        padding: 1.5rem; 
        border-radius: 8px; 
        min-height: 500px; 
        max-height: 800px; 
        overflow-y: auto; 
        font-size: 1.05rem; 
        line-height: 1.8;
        color: #333;
        font-family: inherit;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.05);
        margin-top: -1.2rem;
        margin-bottom: 20px;
    ">{annotated_text}</div>
    '''
    st.markdown(pseudo_textarea_html, unsafe_allow_html=True)
    
    st.components.v1.html("""
        <script>
            const parent = window.parent.document;
            let currentPopup = null;
            let currentHoverTooltip = null;
            
            const closePopup = () => {
                if (currentPopup && currentPopup.parentNode) {
                    currentPopup.parentNode.removeChild(currentPopup);
                }
                currentPopup = null;
            };
            
            const closeHoverTooltip = () => {
                if (currentHoverTooltip && currentHoverTooltip.parentNode) {
                    currentHoverTooltip.parentNode.removeChild(currentHoverTooltip);
                }
                currentHoverTooltip = null;
            };
            
            parent.addEventListener('click', (e) => {
                if (!e.target.classList.contains('highlight-word') && !e.target.classList.contains('word-popup-option')) {
                    closePopup();
                }
            });
            
            const updateHiddenInput = (index, chosenText) => {
                const input = parent.querySelector('input[aria-label="hidden_choices"]');
                if (input) {
                    let currentData = {};
                    try {
                        if (input.value) currentData = JSON.parse(input.value);
                    } catch(e) {}
                    
                    currentData[index] = chosenText;
                    
                    let setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
                    setter.call(input, JSON.stringify(currentData));
                    input.dispatchEvent(new Event('input', { bubbles: true }));
                }
            };
            
            const bindHighlights = () => {
                const highlights = parent.querySelectorAll('.highlight-word:not([data-bound])');
                highlights.forEach(span => {
                    span.dataset.bound = "true";
                    
                    span.addEventListener('mouseenter', (e) => {
                        if (currentPopup) return; // Don't show hover tooltip if a popup menu is already open
                        const text = span.dataset.tooltip;
                        if (!text) return;
                        
                        closeHoverTooltip();
                        
                        const tooltip = parent.createElement('div');
                        tooltip.className = 'word-hover-tooltip';
                        tooltip.innerHTML = text.replace(/\\n/g, '<br>');
                        
                        parent.body.appendChild(tooltip);
                        
                        // Measure and position it relative to the page viewport absolute top
                        const rect = span.getBoundingClientRect();
                        requestAnimationFrame(() => {
                            const tooltipRect = tooltip.getBoundingClientRect();
                            tooltip.style.top = (rect.top + parent.defaultView.scrollY - tooltipRect.height - 10) + 'px';
                            tooltip.style.left = (rect.left + parent.defaultView.scrollX + (rect.width / 2)) + 'px';
                        });
                        
                        currentHoverTooltip = tooltip;
                    });
                    
                    span.addEventListener('mouseleave', () => {
                        closeHoverTooltip();
                    });
                    span.addEventListener('click', (e) => {
                        e.stopPropagation();
                        closePopup();
                        
                        const optionsStr = span.dataset.options;
                        const orig = span.dataset.orig;
                        const index = span.dataset.index;
                        let options = [];
                        try {
                            options = JSON.parse(optionsStr);
                        } catch(err) {}
                        
                        const popup = parent.createElement('div');
                        popup.className = 'word-popup';
                        
                        const rect = span.getBoundingClientRect();
                        popup.style.top = (rect.bottom + parent.defaultView.scrollY + 5) + 'px';
                        popup.style.left = (rect.left + parent.defaultView.scrollX) + 'px';
                        
                        const addOption = (text, isOrig) => {
                            const opt = parent.createElement('div');
                            opt.className = 'word-popup-option';
                            opt.innerHTML = isOrig ? `<span style="color:#888;">원본 유지:</span> ${text}` : `✨ ${text}`;
                            
                            opt.addEventListener('click', (ev) => {
                                ev.stopPropagation();
                                span.textContent = text;
                                if (isOrig) {
                                    span.classList.remove('resolved');
                                } else {
                                    span.classList.add('resolved');
                                }
                                updateHiddenInput(index, text);
                                closePopup();
                            });
                            popup.appendChild(opt);
                        };
                        
                        options.forEach(optText => {
                            if (optText !== orig) addOption(optText, false);
                        });
                        addOption(orig, true);
                        
                        parent.body.appendChild(popup);
                        currentPopup = popup;
                    });
                });
            };
            
            setInterval(bindHighlights, 500);
        </script>
    """, height=0)
    
