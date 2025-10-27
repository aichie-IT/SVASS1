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

# --- Main Title ---
st.title("🎓 Student Insights Dashboard")
st.markdown("Explore patterns in student learning experiences and online tool usage after COVID-19.")

st.markdown("---")

# --- Row 1: Gender Distribution ---
col1, col2 = st.columns(2)

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

with col2:
    fig_gender_bar = px.bar(
        gender_counts,
        x="Gender",
        y="Count",
        title="Gender Count by Category",
        color="Count",
        color_continuous_scale=color_theme
    )
    fig_gender_bar.update_layout(xaxis_title="Gender", yaxis_title="Count")
    st.plotly_chart(fig_gender_bar, use_container_width=True)

# --- Row 2: Online Tool Usage by Gender ---
st.subheader("💻 Online Tool Usage by Gender")
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

# --- Row 3: Impact and Satisfaction Scores ---
col3, col4 = st.columns(2)

with col3:
    fig_impact = px.histogram(
        filtered_df,
        x="Impact_on_Learning",
        nbins=10,
        title="Distribution of Impact on Learning Score",
        color_discrete_sequence=color_theme
    )
    fig_impact.update_layout(xaxis_title="Impact on Learning Score", yaxis_title="Frequency")
    st.plotly_chart(fig_impact, use_container_width=True)

with col4:
    fig_satisfaction = px.histogram(
        filtered_df,
        x="Satisfaction_Score",
        nbins=10,
        title="Distribution of Satisfaction Scores",
        color_discrete_sequence=color_theme
    )
    fig_satisfaction.update_layout(xaxis_title="Satisfaction Score", yaxis_title="Frequency")
    st.plotly_chart(fig_satisfaction, use_container_width=True)

# --- Row 4: Satisfaction by Year of Study ---
st.subheader("📊 Satisfaction Score by Year of Study")
fig_box = px.box(
    filtered_df,
    x="Year_of_Study",
    y="Satisfaction_Score",
    color="Year_of_Study",
    title="Distribution of Satisfaction Scores by Year of Study",
    color_discrete_sequence=color_theme
)
fig_box.update_layout(xaxis_title="Year of Study", yaxis_title="Satisfaction Score")
st.plotly_chart(fig_box, use_container_width=True)

# --- Row 5: Major & Usage Frequency ---
col5, col6 = st.columns([1.3, 1])

with col5:
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

with col6:
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

# --- Row 6: Challenges Faced ---
st.subheader("🚧 Challenges Faced by Students")
challenge_counts = filtered_df["Challenges_Faced"].value_counts().reset_index()
challenge_counts.columns = ["Challenges_Faced", "Count"]
fig_challenges = px.bar(
    challenge_counts,
    x="Count",
    y="Challenges_Faced",
    orientation="h",
    title="Challenges Faced by Students",
    color="Count",
    color_continuous_scale=color_theme
)
fig_challenges.update_layout(xaxis_title="Count", yaxis_title="Challenges")
st.plotly_chart(fig_challenges, use_container_width=True)

# --- Footer ---
st.markdown("---")
st.caption("© 2025 Student Dashboard | Designed with ❤️ using Streamlit & Plotly")
