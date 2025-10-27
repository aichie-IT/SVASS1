import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(page_title="Student Dashboard", layout="wide")

# --- LOAD DATA ---
df = pd.read_csv("student_dataset.csv")  # <-- replace with your actual file path

# Handle NaN values safely
df['Challenges_Faced'] = df['Challenges_Faced'].fillna('No Response')
df['Suggestions_for_Improvement'] = df['Suggestions_for_Improvement'].fillna('No Response')

# --- PAGE TITLE ---
st.title("🎓 Student Dashboard")

# --- DATA SUMMARY BOX ---
st.markdown("### 📊 Dataset Summary")

# Compute dataset stats
num_rows = df.shape[0]
num_cols = df.shape[1]
missing_values = df.isnull().sum().sum()
unique_majors = df['Major'].nunique() if 'Major' in df.columns else 0
unique_years = df['Year_of_Study'].nunique() if 'Year_of_Study' in df.columns else 0

# Show summary as clean metric boxes
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Rows", f"{num_rows}")
col2.metric("Total Columns", f"{num_cols}")
col3.metric("Missing Values", f"{missing_values}")
col4.metric("Unique Majors", f"{unique_majors}")
col5.metric("Study Years", f"{unique_years}")

st.markdown("---")

# --- COLOR THEME ---
color_theme = px.colors.sequential.Tealgrn

# --- ROW 5: Distribution by Major ---
col5, col6 = st.columns([1.3, 1])

with col5:
    fig_major = px.bar(
        df['Major'].value_counts().reset_index(),
        x='count',
        y='index',
        orientation='h',
        title='Student Distribution by Major',
        color_discrete_sequence=color_theme
    )
    fig_major.update_layout(xaxis_title='Count', yaxis_title='Major')
    st.plotly_chart(fig_major, use_container_width=True)

with col6:
    fig_usage = px.bar(
        df['Usage_Frequency'].value_counts().reset_index(),
        x='index',
        y='count',
        title='Usage Frequency of Online Tools',
        color_discrete_sequence=color_theme
    )
    fig_usage.update_layout(xaxis_title='Usage Frequency', yaxis_title='Count')
    st.plotly_chart(fig_usage, use_container_width=True)

# --- ROW 6: Challenges Faced ---
st.subheader("🚧 Challenges Faced by Students")
fig_challenges = px.bar(
    df['Challenges_Faced'].value_counts().reset_index(),
    x='count',
    y='index',
    orientation='h',
    title='Challenges Faced by Students',
    color_discrete_sequence=color_theme
)
fig_challenges.update_layout(xaxis_title='Count', yaxis_title='Challenges')
st.plotly_chart(fig_challenges, use_container_width=True)

# --- FOOTER ---
st.markdown("---")
st.caption("© 2025 Student Dashboard | Designed with ❤️ using Streamlit & Plotly")
