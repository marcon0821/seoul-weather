import streamlit as st
import pandas as pd

# 앱 페이지 기본 설정
st.set_page_config(page_title="서울 기온 변화", page_icon="🌡️", layout="centered")

# 메인 타이틀 및 설명
st.title("🌡️ 서울의 100년 기온 변화")
st.markdown("""
이 앱은 서울의 과거 기온 데이터를 바탕으로 **연도별 평균 기온**이 어떻게 변해왔는지 시각화합니다.
데이터 출처: 기상청 (모두의 데이터 분석 제공)
""")

@st.cache_data
def load_data():
    """CSV 데이터를 불러오고 캐싱하여 앱 속도를 높입니다."""
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/seoul.csv"
    # 한국 공공데이터에서 자주 쓰이는 cp949 인코딩 사용
    df = pd.read_csv(url, encoding='cp949')
    return df

try:
    # 1. 데이터 불러오기
    df = load_data()
    
    # 2. 데이터 전처리
    # 평균기온 열의 결측치(빈 데이터) 제거
    df = df.dropna(subset=['평균기온(℃)'])
    
    # '날짜' 컬럼을 문자열에서 날짜(datetime) 타입으로 변환
    df['날짜'] = pd.to_datetime(df['날짜'], format='%Y-%m-%d', errors='coerce')
    
    # 변환 과정에서 문제가 생긴(NaT) 행 제거
    df = df.dropna(subset=['날짜'])
    
    # 날짜에서 '연도'만 추출하여 새로운 열 생성
    df['연도'] = df['날짜'].dt.year
    
    # 연도별 평균기온의 평균을 계산
    yearly_mean = df.groupby('연도')['평균기온(℃)'].mean()
    
    st.subheader("📈 연도별 평균 기온 추이 (단위: ℃)")
    
    # 스트림릿 내장 라인 차트를 사용하여 그래프 그리기
    # 인덱스(연도)가 X축, 값(평균기온)이 Y축이 됩니다.
    st.line_chart(yearly_mean)
    
    st.info("💡 그래프 위에 마우스를 올리면 정확한 연도와 기온 수치를 확인할 수 있습니다.")
    
    st.divider() # 구분선
    st.subheader("📊 데이터 확인하기")
    
    # 사용자가 원할 때만 원본/연도별 데이터를 볼 수 있도록 체크박스 사용
    if st.checkbox("연도별 평균 기온 데이터 표 보기"):
        st.dataframe(yearly_mean.reset_index(), use_container_width=True)
        
    if st.checkbox("원본 데이터 보기"):
        st.dataframe(df, use_container_width=True)

except Exception as e:
    # 에러 발생 시 사용자에게 친절하게 안내
    st.error(f"데이터를 처리하는 중 문제가 발생했습니다: {e}")