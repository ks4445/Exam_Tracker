import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Mission AFCAT Tracker", layout="wide")
st.title("✈️ Mission AFCAT: Interactive Diary & Analytics")
st.caption("Target Date: September 1st | Aim High")

# Persistent database simulation using Session State
if "afcat_data" not in st.session_state:
    st.session_state.afcat_data = pd.DataFrame(columns=["Date", "Math_Pct", "Reasoning_Pct", "English_Pct", "Defense_GA_Pct", "Mock_Score"])

# Sidebar for inputs
st.sidebar.header("🎯 Log Daily Performance")
log_date = st.sidebar.date_input("Select Date", datetime.date.today())

st.sidebar.subheader("How much did you complete? (0-100%)")
m_val = st.sidebar.slider("Numerical Ability / Math", 0, 100, 50, step=10)
r_val = st.sidebar.slider("Reasoning & Military Aptitude", 0, 100, 50, step=10)
e_val = st.sidebar.slider("English Comprehension/Vocab", 0, 100, 50, step=10)
g_val = st.sidebar.slider("Defense GA & Static Facts", 0, 100, 50, step=10)

st.sidebar.subheader("🏆 Weekly Mock Log")
is_mock_day = st.sidebar.checkbox("Did you take an AFCAT Mock today?")
mock_score = st.sidebar.number_input("Enter Full Mock Score (Max 300)", 0, 300, 0) if is_mock_day else None

if st.sidebar.button("Save Entry to App History"):
    new_row = {
        "Date": log_date, "Math_Pct": m_val, "Reasoning_Pct": r_val, 
        "English_Pct": e_val, "Defense_GA_Pct": g_val, "Mock_Score": mock_score
    }
    df = st.session_state.afcat_data
    if log_date in df["Date"].values:
        df = df[df["Date"] != log_date]
    st.session_state.afcat_data = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True).sort_values("Date")
    st.sidebar.success(f"Data saved for {log_date}!")

# Main Layout
tab1, tab2 = st.tabs(["📅 Daily Diary Checklist", "📊 Weekend Metrics & Charts"])

with tab1:
    st.header(f"Today's List: {datetime.date.today().strftime('%A, %B %d')}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.checkbox("Numerical Ability: Completed daily target tasks", key="m_check")
        st.checkbox("Reasoning & Aptitude: Completed visual / spatial tasks", key="r_check")
    with col2:
        st.checkbox("English: Covered reading speed and vocabulary targets", key="e_check")
        st.checkbox("AFCAT Core GA: Completed Defense facts / Air Force commands", key="g_check")

with tab2:
    st.header("📈 Weekly Progress & Performance Metrics")
    df = st.session_state.afcat_data
    
    if df.empty:
        st.warning("No data logged yet. Fill out the sidebar entry to generate weekend graphs.")
    else:
        st.subheader("Logged History")
        st.dataframe(df.set_index("Date"), use_container_width=True)
        
        # 1. Bar Chart: Daily Study Output
        st.subheader("💡 Study Execution Volume per Subject (%)")
        chart_data = df.set_index("Date")[["Math_Pct", "Reasoning_Pct", "English_Pct", "Defense_GA_Pct"]]
        st.bar_chart(chart_data)
        
        # 2. Line Chart: Mock Performance
        st.subheader("🎯 Mock Test Tracking")
        mock_df = df.dropna(subset=["Mock_Score"])
        if not mock_df.empty:
            st.line_chart(mock_df.set_index("Date")["Mock_Score"])
        else:
            st.info("No Mock entries logged yet. Check 'Did you take an AFCAT Mock today?' in the sidebar to plot line tracking.")
