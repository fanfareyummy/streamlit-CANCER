import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import urllib.request

# --- 1. 티니핑 마법 페이지 설정 (완전 핑크·글리터 테마) ---
st.set_page_config(
    page_title="캐치! 티니핑 마법 건강 진단", 
    page_icon="💖", 
    layout="wide"
)

# [초필살기] 나눔고딕 폰트를 온라인에서 강제로 다운로드하여 Matplotlib에 주입!
@st.cache_data
def load_font():
    font_url = "https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Regular.ttf"
    font_path = "NanumGothic.ttf"
    urllib.request.urlretrieve(font_url, font_path)
    return font_path

try:
    font_path = load_font()
    font_prop = fm.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()
except Exception as e:
    plt.rcParams['font.family'] = ['Malgun Gothic', 'AppleGothic', 'sans-serif']

plt.rcParams['axes.unicode_minus'] = False

# --- 2. 웹페이지 전체에 귀여운 폰트 및 스타일 적용 (CSS 마법) ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Gamja+Flower&family=Nanum+Gothic+Coding&display=swap');
    
    html, body, [data-testid="stWidgetLabel"], .stMarkdown p {
        font-family: 'Gamja Flower', 'Malgun Gothic', sans-serif !important;
        font-size: 1.15rem !important;
    }
    h1, h2, h3 {
        font-family: 'Gamja Flower', 'Malgun Gothic', sans-serif !important;
        font-weight: bold !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- 3. 가상 데이터셋 (세션 상태 유지) ---
if 'df' not in st.session_state:
    np.random.seed(42)
    st.session_state.df = pd.DataFrame({
        '음주 횟수': np.concatenate([np.random.normal(1, 0.8, 50), np.random.normal(5, 1.2, 50), np.random.normal(8, 1.0, 50)]),
        '흡연 횟수': np.concatenate([np.random.normal(2, 1.5, 50), np.random.normal(10, 2.0, 50), np.random.normal(17, 1.5, 50)]),
        'cluster': np.concatenate([np.zeros(50), np.ones(50), np.ones(50)*2])
    })
    st.session_state.df['음주 횟수'] = st.session_state.df['음주 횟수'].clip(0, 10)
    st.session_state.df['흡연 횟수'] = st.session_state.df['흡연 횟수'].clip(0, 20)
    st.session_state.df['cluster'] = st.session_state.df['cluster'].astype(int)

df = st.session_state.df

# --- 4. 이미지 에셋 로드 (티니핑 공식 이미지) ---
teenieping_logo = "https://shopby-images.cdn-nhncommerce.com/20251210/193406.74593594/%EC%BA%90%EC%B9%98%ED%8B%B0%EB%8B%88%ED%95%91.png"
hachuping_img = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT0yx11nxnIhf6fFOJHWlXaUsJZA0YqVEXzcA&s"
joaping_img = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQeQj23ZRAGlZtuCcTMShhj1k8KeUvSLUy8VQ&s"
banglping_img = "https://cimg.cowave.kr/image/vendor_inventory/8590/4fe3c32147424c16a4d8dd8b5de5529afe5168d35115abfffaeadc6bf453.jpg"

# --- 5. 티니핑 공식 웹사이트 스타일 헤더 ---
st.markdown(
    f"""
    <div style='text-align: center; background-color: #fff0f5; padding: 25px; border-radius: 20px; border: 3px solid #ffb6c1; box-shadow: 0 4px 15px rgba(255,182,193,0.5);'>
        <img src='{teenieping_logo}' width='280'><br>
        <h1 style='color: #ff1493; margin-top: 15px; font-size: 2.5rem;'>💖 반짝반짝! 나의 건강 핑 찾기 💖</h1>
        <p style='color: #ff69b4; font-size: 1.4rem; font-weight: bold;'>마법 슬라이더를 움직여봐핑! AI 친구들이 환자분의 비밀 포지션을 찾아줄 거야핑! ٩(♥ε♥)۶</p>
    </div>
    <hr style='border: 2px dashed #ffb6c1;'>
    """, 
    unsafe_allow_html=True
)

# --- 6. 2단 레이아웃 (좌측: 입력 및 결과 / 우측: 실시간 대시보드) ---
left_col, right_col = st.columns([1, 1.2], gap="large")

with left_col:
    st.markdown("<h2 style='color: #ff1493; text-align: center;'>🎛️ 마법의 라이프 지표</h2>", unsafe_allow_html=True)
    
    st.markdown("<p style='color: #ff69b4; font-weight: bold; font-size: 1.2rem;'>나이핑 (세)</p>", unsafe_allow_html=True)
    age = st.slider("내 나이핑", min_value=10, max_value=100, value=25, step=1, label_visibility="collapsed")
    
    st.markdown("<br><p style='color: #ff69b4; font-weight: bold; font-size: 1.2rem;'>주당 흡연 횟수 (번 ☁️)</p>", unsafe_allow_html=True)
    smoke = st.slider("흡연핑", min_value=0, max_value=20, value=4, step=1, label_visibility="collapsed")
    
    st.markdown("<br><p style='color: #ff69b4; font-weight: bold; font-size: 1.2rem;'>주당 음주 횟수 (번 🥂)</p>", unsafe_allow_html=True)
    alcohol = st.slider("음주핑", min_value=0, max_value=10, value=2, step=1, label_visibility="collapsed")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 입력값에 기반한 실시간 가상 군집 계산
    if smoke + alcohol > 19:
        predicted_cluster = 2
        cluster_desc = "삐뽀삐뽀! 방글핑이 경고해핑! 조심해야 할 '🚨 위험핑' 군집이다핑!"
        alert_style = "background-color: #ffe4e1; border: 3px solid #ff4500; color: #ff0000;"
        ping_img = banglping_img
    elif smoke + alcohol > 8:
        predicted_cluster = 1
        cluster_desc = "토닥토닥.. 조아핑이 응원해핑! 관리가 필요한 '💛 조아핑' 군집이다핑!"
        alert_style = "background-color: #fffff0; border: 3px solid #ffd700; color: #daa520;"
        ping_img = joaping_img
    else:
        predicted_cluster = 0
        cluster_desc = "참 잘했어요핑! 하츄핑이 사랑해핑! 건강한 '👑 사랑핑' 군집이다핑!"
        alert_style = "background-color: #f0fff0; border: 3px solid #32cd32; color: #008000;"
        ping_img = hachuping_img
        
    # 실시간 분석 결과 피드백 카드 (티니핑 사진 크기 대폭 상향: 100px -> 160px)
    st.markdown("<h2 style='color: #ff1493;'>🔍 마법의 AI 분석 결과핑!</h2>", unsafe_allow_html=True)
    
    st.markdown(
        f"""
        <div style='{alert_style} padding: 20px; border-radius: 20px; font-weight: bold; box-shadow: 0 4px 10px rgba(0,0,0,0.1); display: flex; align-items: center;'>
            <img src='{ping_img}' width='160' style='border-radius: 20px; margin-right: 20px; border: 3px solid white; object-fit: cover; height: 140px;'>
            <div>
                <span style='font-size: 1.4rem; color:#333;'>🎈 {age}세 환자분의 진단:</span><br><br>
                <span style='font-size: 1.3rem; line-height: 1.5;'>현재 <br><span style='font-size: 1.4rem; text-decoration: underline;'>[{cluster_desc}]</span><br> 에 퐁당 속해있습니다핑!</span>
            </div>
        </div>
        """, 
        unsafe_allow_html=True
    )

# --- 7. 우측 칼럼: 실시간 포지셔닝 그래프 ---
with right_col:
    st.markdown("<h2 style='color: #ff1493; text-align: center;'>📍 환자 군집 내 실시간 포지셔닝핑</h2>", unsafe_allow_html=True)
    
    fig, ax = plt.subplots(figsize=(6, 4.3), dpi=100)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#fffafa') 
    
    # 전체 데이터 플롯
    colors = ['#ff69b4', '#ffd700', '#ff4500']
    for i in range(3):
        cls_data = df[df['cluster'] == i]
        ax.scatter(cls_data['음주 횟수'], cls_data['흡연 횟수'], c=colors[i], alpha=0.5, s=50, edgecolors='none', zorder=2)
    
    # 사용자의 현재 위치 마커 (커다란 하트 별!)
    ax.scatter(alcohol, smoke, c='#ff1493', s=450, marker='*', label='💖 나의 위치핑!', edgecolor='#ffffff', linewidth=3, zorder=10)
    
    # 디자인 데코레이션
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#ffb6c1')
    ax.spines['bottom'].set_color('#ffb6c1')
    
    ax.set_xlabel('주당 음주 횟수핑 (번 🥂)', color='#ff1493', fontsize=12, fontweight='bold')
    ax.set_ylabel('주당 흡연 횟수핑 (번 ☁️)', color='#ff1493', fontsize=12, fontweight='bold')
    ax.tick_params(colors='#ff69b4', labelsize=10)
    ax.grid(True, color='#ffe4e1', linestyle='--', alpha=0.6, zorder=1)
    
    legend = ax.legend(facecolor='#ffffff', edgecolor='#ffb6c1', loc='upper right', fontsize=10)
    plt.setp(legend.get_texts(), color='#ff1493', fontweight='bold') 
    
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-1, 21)
    
    st.pyplot(fig, use_container_width=True)

# --- 8. 하단 데코레이션 (티니핑 아이콘들 크기 상향: 50px -> 110px) ---
st.markdown("<hr style='border: 2px dashed #ffb6c1;'>", unsafe_allow_html=True)
st.markdown(
    f"""
    <div style='text-align: center; padding-bottom: 20px;'>
        <p style='color: #ff69b4; font-weight: bold; font-size: 1.3rem; margin-bottom: 15px;'>💖 우리 귀여운 티니핑 친구들을 모아봐핑! 💖</p>
        <img src='{hachuping_img}' width='110' style='margin: 0 15px; border-radius: 15px; border: 2px solid #ffb6c1; box-shadow: 0 4px 8px rgba(0,0,0,0.1);'>
        <img src='{joaping_img}' width='110' style='margin: 0 15px; border-radius: 15px; border: 2px solid #ffb6c1; box-shadow: 0 4px 8px rgba(0,0,0,0.1);'>
        <img src='{banglping_img}' width='110' style='margin: 0 15px; border-radius: 15px; border: 2px solid #ffb6c1; box-shadow: 0 4px 8px rgba(0,0,0,0.1);'>
        <br><br>
        <p style='color: #ffb6c1; font-size: 0.9rem;'>© SAMG Entertainment. All pings reserved.</p>
    </div>
    """, 
    unsafe_allow_html=True
)
