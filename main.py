import streamlit as st
import pandas as pd
import plotly.express as px

col1, col2, col3, col4 = st.columns(4)
   
col1.metric(label="PLO 2", value=f"3.3", help="PLO 2: Cognitive Skill", border=True)
col2.metric(label="PLO 3", value=f"3.5", help="PLO 3: Digital Skill", border=True)
col3.metric(label="PLO 4", value=f"4.0", help="PLO 4: Interpersonal Skill", border=True)
col4.metric(label="PLO 5", value=f"4.3", help="PLO 5: Communication Skill", border=True)

# --- Page Setup ---
st.set_page_config(
    page_title="Student Insights Dashboard",
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

year_options = sorted(df["Year_of_Study"].dropna().unique())
major_options = sorted(df["Major"].dropna().unique())

selected_year = st.sidebar.multiselect(
    "Select Year of Study:",
    options=year_options,
    default=year_options
)

selected_major = st.sidebar.multiselect(
    "Select Major:",
    options=major_options,
    default=major_options
)

# --- Filter Data ---
filtered_df = df[
    (df["Year_of_Study"].isin(selected_year)) &
    (df["Major"].isin(selected_major))
]

# --- Main Header ---
st.title("🎓 Student Insights Dashboard")
st.markdown("Explore patterns in student learning experiences and online tool usage after COVID-19.")

st.markdown("---")

# --- Summary Cards ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("👩‍🎓 Total Students", f"{len(filtered_df):,}")

with col2:
    avg_satisfaction = filtered_df["Satisfaction_Score"].mean()
    st.metric("😊 Avg. Satisfaction", f"{avg_satisfaction:.2f}")

with col3:
    avg_impact = filtered_df["Impact_on_Learning"].mean()
    st.metric("📘 Avg. Learning Impact", f"{avg_impact:.2f}")

with col4:
    unique_tools = filtered_df["Online_Tool_Used"].nunique()
    st.metric("💻 Online Tools Used", f"{unique_tools}")

st.markdown("---")

# --- Tabs ---
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
