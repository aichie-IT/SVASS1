import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- LOAD DATA ---
url = 'https://raw.githubusercontent.com/aichie-IT/SVASS1/refs/heads/main/student_dataset.csv'
df = pd.read_csv(url)

col1, col2, col3, col4 = st.columns(4)
   
col1.metric(label="PLO 2", value=f"3.3", help="PLO 2: Cognitive Skill", border=True)
col2.metric(label="PLO 3", value=f"3.5", help="PLO 3: Digital Skill", border=True)
col3.metric(label="PLO 4", value=f"4.0", help="PLO 4: Interpersonal Skill", border=True)
col4.metric(label="PLO 5", value=f"4.3", help="PLO 5: Communication Skill", border=True)

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Student Data Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Fill missing values
df['Challenges_Faced'].fillna('No Response', inplace=True)
df['Suggestions_for_Improvement'].fillna('No Response', inplace=True)

# --- SIDEBAR ---
st.sidebar.header("📊 Dashboard Controls")
show_raw = st.sidebar.checkbox("Show Raw Data")
if show_raw:
    st.dataframe(df, use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.info("Select sections below to explore insights.")

# --- HEADER ---
st.title("🎓 Student Survey Dashboard")
st.markdown("This dashboard provides insights into students’ online learning experiences and satisfaction levels.")

# --- COLOR TEMPLATE ---
color_theme = px.colors.sequential.Viridis

# --- ROW 1: Gender Distribution ---
col1, col2 = st.columns(2)

with col1:
    gender_counts = df['Gender'].value_counts().reset_index()
    gender_counts.columns = ['Gender', 'Count']
    fig_gender_pie = px.pie(
        gender_counts,
        names='Gender',
        values='Count',
        title='Gender Distribution (%)',
        color_discrete_sequence=color_theme,
        hole=0.3
    )
    fig_gender_pie.update_traces(textinfo='percent+label')
    st.plotly_chart(fig_gender_pie, use_container_width=True)

with col2:
    fig_gender_bar = px.bar(
        gender_counts,
        x='Gender',
        y='Count',
        title='Gender Distribution Count',
        text='Count',
        color='Gender',
        color_discrete_sequence=color_theme
    )
    fig_gender_bar.update_traces(textposition='outside')
    st.plotly_chart(fig_gender_bar, use_container_width=True)

# --- ROW 2: Gender vs Online Tool ---
st.subheader("💻 Online Tools Used by Gender")
gender_tool = df.groupby(['Gender', 'Online_Tool_Used']).size().reset_index(name='Count')
fig_gender_tool = px.bar(
    gender_tool,
    x='Gender',
    y='Count',
    color='Online_Tool_Used',
    barmode='group',
    title='Online Tools Used by Gender',
    color_discrete_sequence=color_theme
)
st.plotly_chart(fig_gender_tool, use_container_width=True)

# --- ROW 3: Impact and Satisfaction ---
col3, col4 = st.columns(2)

with col3:
    fig_impact = px.histogram(
        df,
        x='Impact_on_Learning',
        nbins=10,
        title='Distribution of Impact on Learning',
        color_discrete_sequence=color_theme
    )
    fig_impact.update_layout(xaxis_title='Impact Score', yaxis_title='Frequency')
    st.plotly_chart(fig_impact, use_container_width=True)

with col4:
    fig_satisfaction = px.histogram(
        df,
        x='Satisfaction_Score',
        nbins=10,
        title='Distribution of Satisfaction Scores',
        color_discrete_sequence=color_theme
    )
    fig_satisfaction.update_layout(xaxis_title='Satisfaction Score', yaxis_title='Frequency')
    st.plotly_chart(fig_satisfaction, use_container_width=True)

# --- ROW 4: Satisfaction by Year ---
st.subheader("📅 Satisfaction Score by Year of Study")
fig_box = px.box(
    df,
    x='Year_of_Study',
    y='Satisfaction_Score',
    color='Year_of_Study',
    color_discrete_sequence=color_theme,
    title='Satisfaction Score Distribution by Year'
)
st.plotly_chart(fig_box, use_container_width=True)

# --- ROW 5: Distribution by Major ---
col5, col6 = st.columns([1.3, 1])

with col5:
    major_counts = df['Major'].value_counts().reset_index()
    major_counts.columns = ['Major', 'Count']  # ✅ rename columns properly
    fig_major = px.bar(
        major_counts,
        x='Count',
        y='Major',
        orientation='h',
        title='Student Distribution by Major',
        color='Count',
        color_continuous_scale=color_theme
    )
    fig_major.update_layout(xaxis_title='Count', yaxis_title='Major')
    st.plotly_chart(fig_major, use_container_width=True)

with col6:
    usage_counts = df['Usage_Frequency'].value_counts().reset_index()
    usage_counts.columns = ['Usage_Frequency', 'Count']  # ✅ rename columns properly
    fig_usage = px.bar(
        usage_counts,
        x='Usage_Frequency',
        y='Count',
        title='Usage Frequency of Online Tools',
        color='Count',
        color_continuous_scale=color_theme
    )
    fig_usage.update_layout(xaxis_title='Usage Frequency', yaxis_title='Count')
    st.plotly_chart(fig_usage, use_container_width=True)

# --- ROW 6: Challenges Faced ---
st.subheader("🚧 Challenges Faced by Students")
challenge_counts = df['Challenges_Faced'].value_counts().reset_index()
challenge_counts.columns = ['Challenges_Faced', 'Count']  # ✅ rename columns properly
fig_challenges = px.bar(
    challenge_counts,
    x='Count',
    y='Challenges_Faced',
    orientation='h',
    title='Challenges Faced by Students',
    color='Count',
    color_continuous_scale=color_theme
)
fig_challenges.update_layout(xaxis_title='Count', yaxis_title='Challenges')
st.plotly_chart(fig_challenges, use_container_width=True)


# --- FOOTER ---
st.markdown("---")
st.caption("© 2025 Student Dashboard | Designed with ❤️ using Streamlit & Plotly")
