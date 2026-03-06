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
    st.markdown("본인의 Gemini API Key가 필요합니다.  \n[🔑 여기서 무료 키를 발급받으세요 (Google AI Studio)](https://aistudio.google.com/app/apikey)")
    
    saved_key = cookie_manager.get("gemini_api_key") or ""
    
    if "gemini_api_key" not in st.session_state:
        st.session_state.gemini_api_key = saved_key
        
    api_key_input = st.text_input("Gemini API Key", value=st.session_state.gemini_api_key, type="password", placeholder="AIzaSy...")
    if api_key_input and api_key_input != saved_key:
        st.session_state.gemini_api_key = api_key_input
        cookie_manager.set("gemini_api_key", api_key_input)

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
당신은 '국립국어원 한글 맞춤법'과 다음 '서울광염교회 글쓰기 규정'을 완벽하게 숙지한 전문 교정가입니다.

[서울광염교회 주요 글쓰기 규정]
1. 존칭: '시', '께서' 등의 존칭 선어말 어미와 겸양어는 하나님, 예수님, 성령님께만 사용합니다. 사람에게는 쓰지 않습니다. (예: 목사님이 하셨습니다(X) -> 목사님이 했습니다(O)) 직분 뒤에만 '님'을 씁니다.
2. 주어 생략/반복: 반복되는 주어는 생략을 원칙으로 하며, 부득이 반복할 경우 '이름'은 빼고 '성+직분'(예: 홍 목사)으로 쓰거나, 성별 무관하게 대명사 '그'를 씁니다. (그녀, 그분 사용 금지).
3. 띄어쓰기: 숫자, 화폐 단위, 명수는 띄어쓰지 않고 모두 무조건 붙여 씁니다. (예: 3억원, 1만5천명, 1000만원대). 복합어(다음세대 등)도 붙여 씁니다.
4. 문체: 한 글(또는 문단) 안에서 문장 종결 표현(해라체/하십시오체)이 혼용되지 않도록 일관성 있게 하나로 통일하여 교정하세요. 다수 쓰인 문체로 전체를 통일합니다.

[기본 문법 및 시제 규정]
5. 문장 성분 호응: 주어, 목적어, 서술어가 논리적으로 명확하게 호응하는지 확인하고 교정하세요. (예: 내가 바라는 것은 네가 잘 되기를 바란다(X) -> 내가 바라는 것은 네가 잘 되는 것이다(O))
6. 시제 일치 (국립국어원 원칙): 국어시제법과 국립국어원 원칙에 맞게 선어말어미(았/었/겠 등)와 관형사형 어미(ㄴ/는/ㄹ)를 사용하여 과거, 현재, 미래 등 문맥 구조에 맞게 완벽한 시제 조화(시제 일치)를 이루도록 교정하세요.

**가장 중요한 원칙**: 사용자가 쓴 원래의 글의 색채 및 뉘앙스는 절대로 임의로 바꾸지 않되, 문체(해라체/하십시오체)가 섞여 있다면 일관되게 통일하고, 맞춤법이나 규정에 어긋난 부분을 교정해야 합니다.

사용자의 글을 분석하여 찾은 모든 오류를 반드시 아래의 순수 JSON 배열 형식으로만 반환하세요.
형식: [{"original": "틀린부분", "correction": "수정제안", "reason": "이유(규정 명시)"}, ...]
에러가 없으면 반드시 빈 배열 `[]`만 반환하세요.
**[주의]** 절대로 설명, 요약, 앞뒤 인사말, 추가 텍스트를 붙이지 마세요. 오직 JSON 배열만 출력해야 프로그램이 에러 없이 작동합니다.
"""

def analyze_text(text):
    from google import genai
    from google.genai import types
    
    if not st.session_state.gemini_api_key:
        return None

    try:
        client = genai.Client(api_key=st.session_state.gemini_api_key)
        response = client.models.generate_content(
            model='gemini-1.5-flash-latest',
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
    st.markdown("### 🔍 교정 제안 (원하시는 교정 항목만 체크해주세요)")
    
    if len(st.session_state.suggestions) == 0:
        st.success("발견된 오류가 없습니다! 훌륭한 글입니다.")
    else:
        selected_suggestions = []
        for i, sug in enumerate(st.session_state.suggestions):
            label_text = f"**수정 전**: `{sug.get('original', '')}` ➡️ **수정 후**: `{sug.get('correction', '')}`  \n*(이유: {sug.get('reason', '')})*"
            if sug.get('alternative'):
                label_text += f"  \n💡 **추천 표현**: *{sug.get('alternative')}*"
            
            checked = st.checkbox(
                label_text,
                value=True,
                key=f"chk_{i}"
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
                    사용자가 작성한 <원본 글>에 대하여 사용자가 <승인한 수정 및 추천 표현들> 목록을 제공합니다.
                    당신은 이 승인된 내용만을 원본 글에 정확히 반영하여 <완성된 글>을 작성해야 합니다.
                    **중요 원칙**: 승인되지 않은 변경 사항은 절대 임의로 적용하지 마세요. 사용자의 톤과 글의 다른 색채를 100% 그대로 유지해야 합니다.
                    단, 문체(해라체/하십시오체)가 혼용된 경우, 전체 글의 문장이 일관되게 통일되도록 마지막 맺음말을 자연스럽게 조정하세요.
                    오직 승인된 부분만 교체하고, 문체 통일 외의 문장은 절대 임의로 바꾸지 마세요.
                    완성된 글 텍스트만 출력하세요. 다른 설명은 덧붙이지 마세요.
                    """
                    
                    user_content = f"<원본 글>\n{st.session_state.original_text}\n\n<승인한 수정 및 추천 표현들>\n"
                    for s in selected_suggestions:
                        replacement = s.get('alternative') if s.get('alternative') else s.get('correction')
                        user_content += f"- '{s.get('original', '')}' -> '{replacement}'\n"
                    
                    from google import genai
                    from google.genai import types
                    
                    try:
                        client = genai.Client(api_key=st.session_state.gemini_api_key)
                        apply_resp = client.models.generate_content(
                            model='gemini-1.5-flash-latest',
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
