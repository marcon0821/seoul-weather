import streamlit as st
import pandas as pd

# 1. 화면 제목 및 설명
st.title("🌡️ 서울의 100년 기온 변화")
st.write("이 앱은 서울의 과거 기온 데이터를 바탕으로 **연도별 평균 기온**이 어떻게 변해왔는지 시각화합니다. 데이터 출처: 기상청 (모두의 데이터 분석 제공)")

# 2. 데이터 불러오기 함수 (캐싱하여 속도 향상)
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/seoul.csv"
    
    # 인코딩 에러 해결을 위해 utf-8 사용 (오류 발생 시 cp949 대비)
    try:
        df = pd.read_csv(url, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(url, encoding='cp949')
        
    # 열 이름 통일 (혹시 모를 공백이나 특수기호 방지)
    df.columns = ['날짜', '지점', '평균기온', '최저기온', '최고기온']
    
    # 결측치(비어있는 데이터) 제거
    df = df.dropna()
    
    # '날짜' 열을 문자열에서 날짜(datetime) 형식으로 변환 후 연도만 추출
    df['날짜'] = pd.to_datetime(df['날짜'])
    df['연도'] = df['날짜'].dt.year
    
    # 연도별 평균 기온 계산
    yearly_mean = df.groupby('연도')['평균기온'].mean().reset_index()
    
    return yearly_mean

# 3. 데이터 처리 및 화면 출력
try:
    data = load_data()
    
    # 스트림릿 내장 라인 차트 사용
    st.line_chart(data=data, x='연도', y='평균기온')
    
    # 데이터프레임 원본도 확인하고 싶다면 아래 주석을 해제하세요.
    # st.dataframe(data)

except Exception as e:
    st.error(f"데이터를 처리하는 중 문제가 발생했습니다: {e}")
