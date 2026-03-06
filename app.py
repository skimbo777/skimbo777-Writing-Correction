import streamlit as st
import asyncio
import json
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
        }
        
        /* Aggressively Force Sidebar Toggle Button to be Always Visible */
        [data-testid="collapsedControl"], 
        [data-testid="stSidebarCollapsedControl"] {
            display: flex !important;
            opacity: 1 !important;
            visibility: visible !important;
            color: #A89574 !important;
            background-color: transparent !important;
            transform: scale(1.5) translate(5px, 5px) !important;
            transition: none !important;
            z-index: 999999 !important;
            pointer-events: auto !important;
        }
        [data-testid="collapsedControl"] svg,
        [data-testid="stSidebarCollapsedControl"] svg {
            fill: #A89574 !important;
            color: #A89574 !important;
            width: 1.5rem !important;
            height: 1.5rem !important;
        }
        [data-testid="collapsedControl"]:hover *,
        [data-testid="stSidebarCollapsedControl"]:hover * {
            fill: #8c7b5f !important;
            color: #8c7b5f !important;
        }
        
        /* Override Streamlit's hover-to-show wrapper for header buttons */
        header[data-testid="stHeader"] > div,
        header[data-testid="stHeader"] .st-emotion-cache-1avcm0n, 
        header[data-testid="stHeader"] .st-emotion-cache-15ecox0 {
            opacity: 1 !important;
            visibility: visible !important;
            pointer-events: auto !important;
            display: flex !important;
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
            margin-bottom: 4rem;
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

inject_custom_css()
render_custom_header()

# Sidebar for Gemini API Key
with st.sidebar:
    st.markdown("""
        <div id="my-custom-profile" style="display: flex; align-items: center; padding-bottom: 20px; margin-bottom: 20px; border-bottom: 1px solid rgba(168, 149, 116, 0.2); cursor: pointer; transition: opacity 0.2s;" onmouseover="this.style.opacity='0.7'" onmouseout="this.style.opacity='1'">
            <div style="width: 36px; height: 36px; border-radius: 50%; background-color: #A89574; display: flex; align-items: center; justify-content: center; margin-right: 12px;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
            </div>
            <div style="color: #A89574; font-weight: 600; font-family: 'Pretendard Variable', Pretendard, sans-serif; font-size: 1.05rem;">My Profile</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.components.v1.html("""
        <script>
            const initCloudCleaner = () => {
                const parent = window.parent.document;
                
                // Aggressive element hider
                const cleanDOM = () => {
                    // Find profile button specifically (usually inside viewerBadge or managed-app-badge or Deploy)
                    const profileBtn = parent.querySelector('.viewerBadge_container, [id^="viewerBadge"], [data-testid="manage-app-button"], [data-testid="stViewerBadge"]');
                    if (profileBtn) {
                        // Hide it instead of removing so we can simulate a click on it
                        profileBtn.style.setProperty("display", "none", "important");
                        profileBtn.style.setProperty("visibility", "hidden", "important");
                        profileBtn.style.setProperty("opacity", "0", "important");
                        window._streamlitProfileBtn = profileBtn; 
                    }
                    
                    // Top right action buttons (Fork, GitHub, Share)
                    const actionElems = parent.querySelectorAll('[data-testid="stActionElements"], .stActionButton, [data-testid="stAppDeployButton"], [data-testid="stToolbar"]');
                    actionElems.forEach(el => {
                        el.style.setProperty("display", "none", "important");
                        el.style.setProperty("visibility", "hidden", "important");
                        el.style.setProperty("opacity", "0", "important");
                        el.style.setProperty("pointer-events", "none", "important");
                    });
                };
                
                setInterval(cleanDOM, 500); // Run aggressively
                cleanDOM();
                
                // Bind profile click
                const myProfile = document.getElementById("my-custom-profile");
                if (myProfile) {
                    myProfile.addEventListener("click", () => {
                         let profileTarget = parent.querySelector('.viewerBadge_container, [id^="viewerBadge"], [data-testid="manage-app-button"], [data-testid="stViewerBadge"]');
                         if (profileTarget) {
                             // Some times the actual clickable is the child button
                             const btn = profileTarget.querySelector('button') || profileTarget;
                             btn.click();
                         } else {
                             alert("클라우드 설정에 연결할 수 없습니다. Streamlit 커뮤니티 클라우드 환경에서만 동작합니다.");
                         }
                    });
                }
            };
            // Wait for parent DOM
            if(document.readyState === 'complete') initCloudCleaner();
            else window.addEventListener('load', initCloudCleaner);
        </script>
    """, height=0)
    
    st.markdown("### ⚙️ Settings")
    
    saved_key = cookie_manager.get("gemini_api_key") or ""
    
    if "gemini_api_key" not in st.session_state:
        st.session_state.gemini_api_key = saved_key
        
    is_valid_key = st.session_state.gemini_api_key and st.session_state.gemini_api_key.startswith("AIza")
    
    if is_valid_key:
        st.markdown("""
            <div style="background-color: #eef7f0; padding: 20px; border-radius: 10px; border: 1px solid #d4ebd9; text-align: center; margin-bottom: 20px;">
                <h3 style="color: #4a8b5b; margin-top: 0; margin-bottom: 0; font-family: 'Pretendard Variable', Pretendard, sans-serif; font-size: 1.25rem;">API키 인증: Complete</h3>
            </div>
        """, unsafe_allow_html=True)
            
        # JS to remove focus from any element to prevent yellow outline, and check if we should prompt to save
        st.components.v1.html("""
            <script>
                // Remove focus
                Array.from(window.parent.document.querySelectorAll('input')).forEach(i => i.blur()); 
                if(window.parent.document.activeElement) window.parent.document.activeElement.blur();
                
                // Ask to save if not already saved and just entered
                const currentKey = '""" + st.session_state.gemini_api_key + """';
                const savedKey = window.localStorage.getItem('gemini_api_key_local');
                if (currentKey && currentKey !== savedKey) {
                    // Slight delay to ensure React/Streamlit renders the Complete UI first
                    setTimeout(() => {
                        if (window.confirm("이 API 키를 저장할까요?")) {
                            window.localStorage.setItem('gemini_api_key_local', currentKey);
                        } else {
                            // If they say no, make sure we don't ask again for this specific key during this session
                        }
                    }, 500);
                }
            </script>
        """, height=0)
        
        st.markdown("---")
        st.markdown("<h3 style='margin-bottom: 15px; color: #A89574;'>Menu</h3>", unsafe_allow_html=True)
        st.markdown("""
        <style>
        .custom-sidebar-link {
            display: flex;
            align-items: center;
            padding: 12px 15px;
            color: #A89574 !important; /* Logo matching beige color */
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
        
        <a href="#" class="custom-sidebar-link">
            <span class="custom-sidebar-icon"><svg viewBox="0 0 24 24"><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><polyline points="16 6 12 2 8 6"/><line x1="12" y1="2" x2="12" y2="15"/></svg></span>
            Share
        </a>
        <a href="#" class="custom-sidebar-link">
            <span class="custom-sidebar-icon"><svg viewBox="0 0 24 24"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg></span>
            Star
        </a>
        <a href="#" class="custom-sidebar-link">
            <span class="custom-sidebar-icon"><svg viewBox="0 0 24 24"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg></span>
            Edit
        </a>
        <a href="#" class="custom-sidebar-link">
            <span class="custom-sidebar-icon"><svg viewBox="0 0 24 24"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/></svg></span>
            GitHub
        </a>
        <a href="#" class="custom-sidebar-link">
            <span class="custom-sidebar-icon"><svg viewBox="0 0 24 24"><line x1="6" y1="3" x2="6" y2="15"/><circle cx="18" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M18 9a9 9 0 0 1-9 9"/></svg></span>
            Fork
        </a>
        <div style="margin-top: 15px;"></div>
        <a href="#" class="custom-sidebar-link" style="border-top: 1px solid rgba(168, 149, 116, 0.2); padding-top: 18px; border-radius: 0;">
            <span class="custom-sidebar-icon"><svg viewBox="0 0 24 24"><path d="M2 22h20"/><path d="M12 2l4 8 6-4-3 14H5L2 6l6 4z"/></svg></span>
            Streamlit
        </a>
        <a href="#" class="custom-sidebar-link">
            <span class="custom-sidebar-icon"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg></span>
            Manage app
        </a>
        """, unsafe_allow_html=True)
        
    else:
        st.markdown("본인의 Gemini API Key가 필요합니다.  \n[🔑 여기서 무료 키를 발급받으세요 (Google AI Studio)](https://aistudio.google.com/app/apikey)")
        api_key_input = st.text_input("Gemini API Key", value=st.session_state.gemini_api_key, type="password", placeholder="AIzaSy...", key="api_key_widget")
        
        # JS to retrieve from local storage on initial load
        st.components.v1.html("""
            <script>
                const savedKey = window.localStorage.getItem('gemini_api_key_local');
                const p = window.parent;
                if (savedKey && savedKey.startsWith('AIza')) {
                    const inputs = p.document.querySelectorAll('input[type="password"]');
                    for (let input of inputs) {
                        if (!input.value) {
                            // We need to simulate React events to actually trigger a change in Streamlit
                            let nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
                            nativeInputValueSetter.call(input, savedKey);
                            input.dispatchEvent(new Event('input', { bubbles: true }));
                            // Fake enter keypress
                            input.dispatchEvent(new KeyboardEvent('keydown', {'key': 'Enter'}));
                        }
                    }
                }
            </script>
        """, height=0)
        
        if api_key_input != saved_key and api_key_input != st.session_state.gemini_api_key:
            st.session_state.gemini_api_key = api_key_input
            cookie_manager.set("gemini_api_key", api_key_input)
            if api_key_input.startswith("AIza"):
                st.rerun()
                
        if api_key_input and not api_key_input.startswith("AIza"):
            st.markdown("""
                <div style="background-color: #fdf3f4; padding: 15px; border-radius: 8px; border: 1px solid #fadce0; margin-top: 10px;">
                    <p style="color: #d15663; margin: 0; font-size: 0.95em;">❌ API 키를 확인해주세요.</p>
                </div>
            """, unsafe_allow_html=True)

# Session state initialization
if "suggestions" not in st.session_state:
    st.session_state.suggestions = None
if "original_text" not in st.session_state:
    st.session_state.original_text = ""
if "final_text" not in st.session_state:
    st.session_state.final_text = ""

# Main Text Input
user_text = st.text_area("main_input", height=500, placeholder="교정할 글을 입력해주세요...", label_visibility="collapsed")

SYSTEM_PROMPT = """
당신은 완벽한 전문 교정가입니다.

[가장 중요한 원칙 - 문장 및 양식 보존]
**AI가 문장 전체를 새로 쓰거나 치환, 구조를 변경하는 것을 절대 금지합니다.** 사용자의 고유한 문체와 문장 구조뿐만 아니라, 원문에 포함된 **줄바꿈(엔터), 문단 나누기, 띄어쓰기 간격 등 모든 서식과 양식을 100% 그대로 유지**하는 것이 최우선입니다. 오류가 있는 부분만 최소한으로 단어 단위로 고치세요.

[서울광염교회 주요 글쓰기 규정 ("type": "correction")]
1. 존칭: '시', '께서' 등의 존칭 선어말 어미와 겸양어는 하나님, 예수님, 성령님께만 사용합니다. 사람에게는 쓰지 않습니다. (예: 목사님이 하셨습니다(X) -> 목사님이 했습니다(O)) 직분 뒤에만 '님'을 씁니다.
2. 주어 생략/반복: 반복되는 주어는 생략을 원칙으로 하며, 부득이 반복할 경우 '이름'은 빼고 '성+직분'(예: 홍 목사)으로 쓰거나, 성별 무관하게 대명사 '그'를 씁니다. (그녀, 그분 사용 금지).
3. 띄어쓰기: 숫자, 화폐 단위, 명수는 띄어쓰지 않고 무조건 붙여 씁니다. (예: 3억원, 1만5천명).
4. 문체: 한 글 안에서 해라체/하십시오체가 혼용되지 않도록 일관성 있게 하나로 통일.
5. 호응 및 시제: 주어와 서술어 호응, 국어시제법 완벽 일치.

[단어 단위 추천 - 문학적 어휘 제안 ("type": "suggestion")]
문장에 쓰인 단어 중, 문맥상 더 아름다운 시적 표현이나 상황에 적합한 서정적/문학적 단어가 있다면 그 단어만 선별하여 리스트로 추천해 주세요. (예: 'original': '은혜가 큽니다', 'correction': '무궁합니다, 지극합니다'). 이런 문학적 어휘 제안은 "type": "suggestion" 으로 분류합니다.

사용자의 글을 분석하여 찾은 모든 오류 및 문학적 어휘 제안을 반드시 아래의 순수 JSON 배열 형식으로만 반환하세요.
형식: [{"type": "correction" 또는 "suggestion", "original": "해당 단어나 문구", "correction": "수정제안 단어 또는 추천단어들", "reason": "교정 이유 또는 추천 사유"}, ...]
에러나 제안이 없으면 반드시 빈 배열 `[]`만 반환하세요. 앞뒤 추가 설명 없이 오직 JSON 배열만 출력해야 합니다.
"""

def analyze_text(text):
    if not st.session_state.gemini_api_key:
        return None

    try:
        client = genai.Client(api_key=st.session_state.gemini_api_key)
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=text,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.0,
                response_mime_type="application/json",
            ),
        )
        content = response.text.strip()
        
        start_idx = content.find('[')
        end_idx = content.rfind(']')
        
        if start_idx != -1 and end_idx != -1 and end_idx >= start_idx:
            json_str = content[start_idx:end_idx+1]
            return json.loads(json_str)
        else:
            raise ValueError("Invalid JSON format from Gemini.")
    except Exception as e:
        st.error(f"AI 분석 실패. API 키가 정확한지 확인하시거나 잠시 후 다시 시도해주세요. 에러: {e}")
        return None

if st.button("교정하기", type="primary"):
    if not st.session_state.gemini_api_key.strip():
        st.warning("사이드바에 Gemini API Key를 입력해주세요.")
    elif not user_text.strip():
        st.warning("교정할 글을 입력해주세요.")
    else:
        # Reset state upon new analysis
        st.session_state.suggestions = None
        st.session_state.final_text = ""
        st.session_state.original_text = ""
        
        loading_placeholder = st.empty()
        with loading_placeholder.container():
            col1, col2 = st.columns([1, 4])
            with col1:
                st.button("Stop 🛑", key="stop_analyze")
            with col2:
                st.markdown("<div style='font-size:1.05rem; color:#444; margin-top: 5px;'>교정된 글을 분석하고 있습니다... (5~15초 소요될 수 있습니다) <span class='pencil-anim'></span></div>", unsafe_allow_html=True)
                
        st.session_state.original_text = user_text
        suggestions = analyze_text(user_text)
        loading_placeholder.empty()
        
        if suggestions is not None:
            st.session_state.suggestions = suggestions
                
if st.session_state.suggestions is not None:
    # Render interactive text area replacement
    st.markdown("### 📝 분석된 원문 (틀린 단어 위에 마우스를 올리면 교정 내용이 보입니다)")
    
    annotated_text = html.escape(st.session_state.original_text)
    
    corrections = [s for s in st.session_state.suggestions if s.get("type", "correction") != "suggestion"]
    literary_suggestions = [s for s in st.session_state.suggestions if s.get("type") == "suggestion"]
    all_sugs = corrections + literary_suggestions
    
    st.markdown("""
    <style>
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
        .highlight-word:hover::after, .highlight-word:active::after {
            content: attr(data-tooltip);
            position: absolute;
            bottom: 125%;
            left: 50%;
            transform: translateX(-50%);
            background: #fff;
            color: #333;
            padding: 12px;
            border-radius: 8px;
            white-space: pre-wrap;
            font-size: 0.95rem;
            z-index: 9999;
            width: max-content;
            max-width: 320px;
            line-height: 1.5;
            box-shadow: 0 4px 15px rgba(0,0,0,0.15);
            border: 1px solid #eee;
            text-align: left;
            pointer-events: none;
        }
        .highlight-word:hover::before, .highlight-word:active::before {
            content: '';
            position: absolute;
            bottom: 100%;
            left: 50%;
            margin-left: -8px;
            border-width: 8px;
            border-style: solid;
            border-color: #fff transparent transparent transparent;
            z-index: 10000;
        }
    </style>
    """, unsafe_allow_html=True)
    
    for i, sug in enumerate(all_sugs):
        orig = html.escape(sug.get('original', ''))
        corr = html.escape(sug.get('correction', ''))
        reason = html.escape(sug.get('reason', ''))
        sug_type = sug.get('type', 'correction')
        
        if sug_type == 'suggestion':
            tooltip_text = f"✨ 어휘 추천\\n💡 {corr}\\n({reason})"
        else:
            tooltip_text = f"🔍 수정 제안\\n❌ {orig}\\n✅ {corr}\\n({reason})"
            
        if orig and orig in annotated_text:
            span_html = f'<span class="highlight-word" data-tooltip="{tooltip_text}">{orig}</span>'
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
        margin-bottom: 20px;
    ">{annotated_text}</div>
    '''
    st.markdown(pseudo_textarea_html, unsafe_allow_html=True)
    
    col_reset, col_apply = st.columns([3, 7])
    with col_reset:
        if st.button("새로운 글 작성하기 (초기화)"):
            st.session_state.suggestions = None
            st.session_state.original_text = ""
            st.session_state.final_text = ""
            st.rerun()
            
    with col_apply:
        gen_btn_col, gen_stop_col = st.columns([6, 4])
        with gen_btn_col:
            generate_clicked = st.button("모든 교정 제안을 적용하여 완성하기", type="primary")
        with gen_stop_col:
            gen_stop_placeholder = st.empty()
            
        if generate_clicked:
            selected_suggestions = all_sugs
            
            with gen_stop_placeholder.container():
                st.button("Stop", type="primary", key="stop_gen")
                
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
                client = genai.Client(api_key=st.session_state.gemini_api_key)
                apply_resp = client.models.generate_content(
                    model='gemini-2.0-flash',
                    contents=user_content,
                    config=types.GenerateContentConfig(
                        system_instruction=APPLY_PROMPT,
                        temperature=0.0
                    )
                )
                st.session_state.final_text = apply_resp.text.strip()
            except Exception as e:
                st.session_state.final_text = f"글 생성에 실패했습니다. API 키 오류 또는 서버 문제일 수 있습니다. 에러: {e}"
                
            loading_placeholder2.empty()

if st.session_state.final_text:
    st.markdown("### ✨ 완성된 글 <span class='pencil-anim'></span>", unsafe_allow_html=True)
    st.text_area("아래 텍스트를 복사하여 사용하세요:", value=st.session_state.final_text, height=300, key="final")
