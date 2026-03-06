import streamlit as st
import asyncio
import json
import extra_streamlit_components as stx

cookie_manager = stx.CookieManager(key="cookie_manager")

try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

    asyncio.set_event_loop(asyncio.new_event_loop())

st.set_page_config(page_title="서울광염교회 글쓰기 교정", page_icon="✨", layout="centered")

def inject_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500&display=swap');
        
        /* Global Background and Font */
        .stApp {
            background-color: #FAF9F6;
            font-family: 'Inter', sans-serif;
            color: #333333;
        }
        
        /* Typography overrides */
        h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            font-family: 'Playfair Display', serif !important;
            color: #1a1a1a;
        }
        
        /* Hide Default Streamlit Elements */
        #MainMenu {visibility: hidden;}
        header {background-color: transparent !important;}
        footer {visibility: hidden;}
        
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
            font-family: 'Inter', sans-serif;
            font-size: 1.05rem;
            color: #666666; /* K60 color matching logo */
            max-width: 700px;
            margin: 0 auto;
            line-height: 1.7;
        }
        
        /* Streamlit specific label overrides */
        .stTextArea label p {
            color: #666666 !important; /* K60 color */
            font-family: 'Inter', sans-serif !important;
            font-size: 1.05rem !important;
        }
        
        /* Show Streamlit Top Header for mobile sidebar menu */
        [data-testid="stHeader"] {background-color: transparent;}
        
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
    st.markdown("### ⚙️ 설정")
    
    saved_key = cookie_manager.get("gemini_api_key") or ""
    
    if "gemini_api_key" not in st.session_state:
        st.session_state.gemini_api_key = saved_key
        
    is_valid_key = st.session_state.gemini_api_key and st.session_state.gemini_api_key.startswith("AIza")
    
    if is_valid_key:
        st.markdown("""
            <div style="background-color: #eef7f0; padding: 20px; border-radius: 10px; border: 1px solid #d4ebd9; text-align: center; margin-bottom: 20px;">
                <h3 style="color: #4a8b5b; margin-top: 0; margin-bottom: 0; font-family: 'Inter', sans-serif; font-size: 1.25rem;">API키 인증: Complete</h3>
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
                            window.localStorage.setItem('gemini_api_key_declined', currentKey);
                        }
                    }, 500);
                }
            </script>
        """, height=0)
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
user_text = st.text_area("교정할 글을 입력해주세요:", height=300)

SYSTEM_PROMPT = """
당신은 완벽한 전문 교정가입니다.

[가장 중요한 원칙 - 문장 보존]
**AI가 문장 전체를 새로 쓰거나 치환, 구조를 변경하는 것을 절대 금지합니다.** 사용자의 고유한 문체와 문장 구조를 100% 그대로 유지하는 것이 최우선입니다. 오류가 있는 부분만 최소한으로 단어 단위로 고치세요.

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
    from google import genai
    from google.genai import types
    
    if not st.session_state.gemini_api_key:
        return None

    try:
        client = genai.Client(api_key=st.session_state.gemini_api_key)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
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

if st.button("분석하기", type="primary"):
    if not st.session_state.gemini_api_key.strip():
        st.warning("사이드바에 Gemini API Key를 입력해주세요.")
    elif not user_text.strip():
        st.warning("교정할 글을 입력해주세요.")
    else:
        with st.spinner("글을 분석하고 있습니다... (5~15초 소요될 수 있습니다)"):
            st.session_state.original_text = user_text
            suggestions = analyze_text(user_text)
            if suggestions is not None:
                st.session_state.suggestions = suggestions
                
if st.session_state.suggestions is not None:
    corrections = [s for s in st.session_state.suggestions if s.get("type", "correction") != "suggestion"]
    literary_suggestions = [s for s in st.session_state.suggestions if s.get("type") == "suggestion"]
    
    st.markdown("### 🔍 교정 제안 (원하시는 교정 항목만 체크해주세요)")
    
    selected_suggestions = []
    
    if len(corrections) == 0:
        st.success("발견된 오류가 없습니다! 훌륭한 글입니다.")
    else:
        for i, sug in enumerate(corrections):
            label_text = f"**수정 전**: `{sug.get('original', '')}` ➡️ **수정 후**: `{sug.get('correction', '')}`  \n*(이유: {sug.get('reason', '')})*"
            
            checked = st.checkbox(
                label_text,
                value=True,
                key=f"chk_corr_{i}"
            )
            if checked:
                selected_suggestions.append(sug)
                
    if len(literary_suggestions) > 0:
        st.markdown("### ✨ 문학적 어휘 제안")
        for i, sug in enumerate(literary_suggestions):
            label_text = f"**{sug.get('original', '')}** 대신 💡 **{sug.get('correction', '')}**  \n*(추천 사유: {sug.get('reason', '')})*"
            
            checked = st.checkbox(
                label_text,
                value=False,
                key=f"chk_sug_{i}"
            )
            if checked:
                selected_suggestions.append(sug)
        
    if st.button("선택한 교정사항 적용하여 완성하기", type="primary"):
        if not selected_suggestions:
            st.session_state.final_text = st.session_state.original_text
        else:
            with st.spinner("최종 글을 생성하고 있습니다..."):
                APPLY_PROMPT = """
                당신은 전문 교정가입니다. 
                사용자가 작성한 <원본 글>과 <승인한 수정 및 추천 표현들>을 제공받습니다.
                **최우선 원칙**: AI가 문장 전체를 새로 쓰거나 구조를 변경하는 것을 절대 금지합니다. 사용자의 고유한 문체와 문장 구조를 100% 그대로 유지해야 합니다.
                오직 <승인한 목록>에 있는 단어/문구만 그 자리에서 정확히 교체하고, 다른 어휘나 문장 논리는 절대 임의로 바꾸지 마세요.
                (단, 문체가 혼용된 경우에 한해 일관성 있게 마지막 맺음말을 자연스럽게 조정하세요.)
                완성된 글 텍스트만 출력하세요. 다른 설명은 덧붙이지 마세요.
                """
                
                user_content = f"<원본 글>\n{st.session_state.original_text}\n\n<승인한 수정 및 추천 표현들>\n"
                for s in selected_suggestions:
                    user_content += f"- '{s.get('original', '')}' -> '{s.get('correction', '')}'\n"
                    
                    from google import genai
                    from google.genai import types
                    
                    try:
                        client = genai.Client(api_key=st.session_state.gemini_api_key)
                        apply_resp = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=user_content,
                            config=types.GenerateContentConfig(
                                system_instruction=APPLY_PROMPT,
                                temperature=0.0
                            )
                        )
                        st.session_state.final_text = apply_resp.text.strip()
                    except Exception as e:
                        st.session_state.final_text = f"글 생성에 실패했습니다. API 키 오류 또는 서버 문제일 수 있습니다. 에러: {e}"

if st.session_state.final_text:
    st.markdown("### ✨ 완성된 글")
    st.text_area("아래 텍스트를 복사하여 사용하세요:", value=st.session_state.final_text, height=300, key="final")
