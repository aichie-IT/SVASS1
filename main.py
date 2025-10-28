import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Setup ---
st.set_page_config(
    page_title="Student Dashboard",
    page_icon="🎓",
    layout="wide"
)

# --- Theme Colors ---
color_theme = px.colors.sequential.Viridis

# --- Load Dataset ---
url = "https://raw.githubusercontent.com/aichie-IT/SVASS1/refs/heads/main/student_dataset.csv"
df = pd.read_csv(url)

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filter Data")

year_options = df["Year_of_Study"].dropna().unique()
major_options = df["Major"].dropna().unique()

selected_year = st.sidebar.multiselect(
    "Select Year of Study:",
    options=sorted(year_options),
    default=year_options
)

selected_major = st.sidebar.multiselect(
    "Select Major:",
    options=sorted(major_options),
    default=major_options
)

# --- Filter the Data ---
filtered_df = df[
    (df["Year_of_Study"].isin(selected_year)) &
    (df["Major"].isin(selected_major))
]

# --- MAIN TITLE ---
st.title("🎓 Student Insights Dashboard")
st.markdown("Explore student learning experiences, satisfaction, and skill outcomes after COVID-19.")

# --- STYLED SUMMARY BOX ---
st.markdown("""
<style>
.summary-box {
    background: linear-gradient(135deg, #1e3c72, #2a5298);
    color: white;
    padding: 25px;
    border-radius: 15px;
    margin-bottom: 25px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.15);
}
.metric-title {
    font-size: 16px;
    font-weight: 600;
    color: #d1e3ff;
}
.metric-value {
    font-size: 26px;
    font-weight: 700;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# --- COMBINED SUMMARY METRICS ---
with st.container():
    st.markdown('<div class="summary-box">', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-title">👩‍🎓 Total Students</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{len(filtered_df):,}</div>', unsafe_allow_html=True)

    with col2:
        avg_satisfaction = filtered_df["Satisfaction_Score"].mean()
        st.markdown('<div class="metric-title">😊 Avg. Satisfaction</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{avg_satisfaction:.2f}</div>', unsafe_allow_html=True)

    with col3:
        avg_impact = filtered_df["Impact_on_Learning"].mean()
        st.markdown('<div class="metric-title">📘 Avg. Learning Impact</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{avg_impact:.2f}</div>', unsafe_allow_html=True)

    with col4:
        unique_tools = filtered_df["Online_Tool_Used"].nunique()
        st.markdown('<div class="metric-title">💻 Online Tools Used</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{unique_tools}</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# --- PLO METRICS SECTION ---
st.markdown('<div class="summary-box">', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

col1.metric(label="PLO 2 — Cognitive Skill", value="3.3", help="Average cognitive skill level")
col2.metric(label="PLO 3 — Digital Skill", value="3.5", help="Average digital skill level")
col3.metric(label="PLO 4 — Interpersonal Skill", value="4.0", help="Average interpersonal skill level")
col4.metric(label="PLO 5 — Communication Skill", value="4.3", help="Average communication skill level")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# --- TABS ---
tab1, tab2, tab3 = st.tabs(["📊 Overview", "📈 Scores", "🚧 Challenges"])

# --- TAB 1: OVERVIEW ---
with tab1:
    st.subheader("👥 Demographics Overview")

    col1, col2 = st.columns(2)
    # Gender distribution
    with col1:
        gender_counts = filtered_df["Gender"].value_counts().reset_index()
        gender_counts.columns = ["Gender", "Count"]
        fig_gender_pie = px.pie(
            gender_counts,
            values="Count",
            names="Gender",
            title="Gender Distribution",
            color_discrete_sequence=color_theme
        )
        st.plotly_chart(fig_gender_pie, use_container_width=True)

    # Online tool usage by gender
    with col2:
        gender_tool = filtered_df.groupby("Gender")["Online_Tool_Used"].value_counts().reset_index(name="Count")
        fig_gender_tool = px.bar(
            gender_tool,
            x="Gender",
            y="Count",
            color="Online_Tool_Used",
            barmode="group",
            title="Online Tools Used by Gender",
            color_discrete_sequence=color_theme
        )
        fig_gender_tool.update_layout(xaxis_title="Gender", yaxis_title="Count")
        st.plotly_chart(fig_gender_tool, use_container_width=True)

    # Major and usage frequency
    col3, col4 = st.columns([1.3, 1])
    with col3:
        major_counts = filtered_df["Major"].value_counts().reset_index()
        major_counts.columns = ["Major", "Count"]
        fig_major = px.bar(
            major_counts,
            x="Count",
            y="Major",
            orientation="h",
            title="Student Distribution by Major",
            color="Count",
            color_continuous_scale=color_theme
        )
        fig_major.update_layout(xaxis_title="Count", yaxis_title="Major")
        st.plotly_chart(fig_major, use_container_width=True)

    with col4:
        usage_counts = filtered_df["Usage_Frequency"].value_counts().reset_index()
        usage_counts.columns = ["Usage_Frequency", "Count"]
        fig_usage = px.bar(
            usage_counts,
            x="Usage_Frequency",
            y="Count",
            title="Usage Frequency of Online Tools",
            color="Count",
            color_continuous_scale=color_theme
        )
        fig_usage.update_layout(xaxis_title="Usage Frequency", yaxis_title="Count")
        st.plotly_chart(fig_usage, use_container_width=True)

# --- TAB 2: SCORES ---
with tab2:
    st.subheader("📈 Learning and Satisfaction Scores")

    col1, col2 = st.columns(2)
    with col1:
        fig_impact = px.histogram(
            filtered_df,
            x="Impact_on_Learning",
            nbins=10,
            title="Distribution of Impact on Learning Score",
            color_discrete_sequence=color_theme
        )
        fig_impact.update_layout(xaxis_title="Impact on Learning", yaxis_title="Frequency")
        st.plotly_chart(fig_impact, use_container_width=True)

    with col2:
        fig_satisfaction = px.histogram(
            filtered_df,
            x="Satisfaction_Score",
            nbins=10,
            title="Distribution of Satisfaction Scores",
            color_discrete_sequence=color_theme
        )
        fig_satisfaction.update_layout(xaxis_title="Satisfaction Score", yaxis_title="Frequency")
        st.plotly_chart(fig_satisfaction, use_container_width=True)

    # Satisfaction by year
    st.subheader("Satisfaction Score by Year of Study")
    fig_box = px.box(
        filtered_df,
        x="Year_of_Study",
        y="Satisfaction_Score",
        color="Year_of_Study",
        title="Satisfaction Distribution by Year of Study",
        color_discrete_sequence=color_theme
    )
    fig_box.update_layout(xaxis_title="Year of Study", yaxis_title="Satisfaction Score")
    st.plotly_chart(fig_box, use_container_width=True)

# --- TAB 3: CHALLENGES ---
with tab3:
    st.subheader("🚧 Challenges Faced by Students")
    challenge_counts = filtered_df["Challenges_Faced"].value_counts().reset_index()
    challenge_counts.columns = ["Challenges_Faced", "Count"]
    fig_challenges = px.bar(
        challenge_counts,
        x="Count",
        y="Challenges_Faced",
        orientation="h",
        title="Top Challenges in Online Learning",
        color="Count",
        color_continuous_scale=color_theme
    )
    fig_challenges.update_layout(xaxis_title="Count", yaxis_title="Challenges")
    st.plotly_chart(fig_challenges, use_container_width=True)

# --- Footer ---
st.markdown("---")
st.caption("© 2025 Student Dashboard | Designed with ❤️ using Streamlit & Plotly")
