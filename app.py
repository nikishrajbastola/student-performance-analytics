import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="📊",
    layout="wide"
)

# -----------------------------------
# CUSTOM CSS
# -----------------------------------
st.markdown("""
<style>
.main {
    background-color: #f7f9fc;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.dashboard-title {
    font-size: 42px;
    font-weight: 800;
    color: #111827;
}

.subtitle {
    font-size: 18px;
    color: #4b5563;
    margin-bottom: 30px;
}

.metric-card {
    background: white;
    padding: 24px;
    border-radius: 18px;
    box-shadow: 0px 4px 18px rgba(0,0,0,0.08);
    text-align: center;
    margin-bottom: 15px;
}

.metric-value {
    font-size: 32px;
    font-weight: 800;
    color: #2563eb;
}

.metric-label {
    font-size: 14px;
    color: #6b7280;
}

.insight-box {
    background: #eef6ff;
    border-left: 5px solid #2563eb;
    padding: 15px;
    border-radius: 10px;
    margin-top: 10px;
    margin-bottom: 25px;
    color: #1f2937;
}

.section-header {
    font-size: 28px;
    font-weight: 700;
    margin-top: 20px;
    margin-bottom: 20px;
    color: #111827;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------
# LOAD DATA
# -----------------------------------
@st.cache_data
def load_data():

    df = pd.read_csv("student_data.csv")

    # Feature Engineering
    df["avg_grade"] = (df["G1"] + df["G2"] + df["G3"]) / 3
    df["grade_change"] = df["G3"] - df["G1"]
    df["total_alcohol"] = df["Dalc"] + df["Walc"]

    # Performance Band
    def performance_band(grade):
        if grade < 10:
            return "Low"
        elif grade <= 13:
            return "Moderate"
        elif grade <= 16:
            return "Good"
        else:
            return "High"

    df["performance_band"] = df["G3"].apply(performance_band)

    # High Absence Flag
    threshold = df["absences"].quantile(0.75)
    df["is_high_absence"] = df["absences"] > threshold

    return df

df = load_data()

# -----------------------------------
# HEADER
# -----------------------------------
st.markdown(
    '<div class="dashboard-title">📊 Student Performance & Academic Analytics</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Interactive dashboard exploring academic trajectory, attendance, study habits, and student risk factors.</div>',
    unsafe_allow_html=True
)

# -----------------------------------
# SIDEBAR FILTERS
# -----------------------------------
st.sidebar.header("🔎 Filters")

study_time = st.sidebar.slider(
    "Study Time",
    int(df["studytime"].min()),
    int(df["studytime"].max()),
    (1, 4)
)

failures = st.sidebar.slider(
    "Past Failures",
    int(df["failures"].min()),
    int(df["failures"].max()),
    (0, 3)
)

sex_filter = st.sidebar.multiselect(
    "Sex",
    options=sorted(df["sex"].unique()),
    default=sorted(df["sex"].unique())
)

internet_filter = st.sidebar.multiselect(
    "Internet Access",
    options=sorted(df["internet"].unique()),
    default=sorted(df["internet"].unique())
)

performance_filter = st.sidebar.multiselect(
    "Performance Band",
    options=["Low", "Moderate", "Good", "High"],
    default=["Low", "Moderate", "Good", "High"]
)

# -----------------------------------
# FILTER DATA
# -----------------------------------
filtered_df = df[
    (df["studytime"] >= study_time[0]) &
    (df["studytime"] <= study_time[1]) &
    (df["failures"] >= failures[0]) &
    (df["failures"] <= failures[1]) &
    (df["sex"].isin(sex_filter)) &
    (df["internet"].isin(internet_filter)) &
    (df["performance_band"].isin(performance_filter))
]

# -----------------------------------
# EMPTY CHECK
# -----------------------------------
if filtered_df.empty:
    st.warning("No data matches selected filters.")
    st.stop()

# -----------------------------------
# KPI METRICS
# -----------------------------------
st.markdown('<div class="section-header">📌 Dashboard Overview</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{len(filtered_df)}</div>
        <div class="metric-label">Students</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{filtered_df["G3"].mean():.2f}</div>
        <div class="metric-label">Average Final Grade</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{filtered_df["absences"].mean():.2f}</div>
        <div class="metric-label">Average Absences</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    pass_rate = (filtered_df["G3"] >= 10).mean() * 100

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{pass_rate:.1f}%</div>
        <div class="metric-label">Pass Rate</div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------
# TABS
# -----------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📘 Academic Overview",
    "⚠️ Risk Factors",
    "🧠 Behavioral & Demographic",
    "🔍 Key Findings"
])

# ===================================
# TAB 1 — ACADEMIC OVERVIEW
# ===================================
with tab1:

    st.markdown('<div class="section-header">Academic Performance Overview</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # Histogram
    with col1:

        fig_hist = px.histogram(
            filtered_df,
            x="G3",
            nbins=20,
            title="Distribution of Final Grades",
            marginal="box"
        )

        st.plotly_chart(fig_hist, use_container_width=True)

        st.markdown("""
        <div class="insight-box">
        <strong>Insight:</strong> Most students scored within the moderate performance range, with fewer students at the extreme high and low ends.
        </div>
        """, unsafe_allow_html=True)

    # Boxplot
    with col2:

        fig_box = px.box(
            filtered_df,
            y="G3",
            title="Final Grade Spread"
        )

        st.plotly_chart(fig_box, use_container_width=True)

        st.markdown("""
        <div class="insight-box">
        <strong>Insight:</strong> The boxplot summarizes the spread, median, and potential outliers in final grade distributions.
        </div>
        """, unsafe_allow_html=True)

    # Heatmap
    st.subheader("Correlation Heatmap")

    numeric_cols = [
        "G1", "G2", "G3",
        "avg_grade", "grade_change",
        "studytime", "failures",
        "absences", "total_alcohol",
        "Medu", "Fedu", "goout"
    ]

    corr = filtered_df[numeric_cols].corr()

    fig_heatmap = px.imshow(
        corr,
        text_auto=".2f",
        aspect="auto",
        title="Correlation Heatmap"
    )

    st.plotly_chart(fig_heatmap, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
    <strong>Insight:</strong> Earlier grades, especially G2, show the strongest relationship with final academic performance.
    </div>
    """, unsafe_allow_html=True)

# ===================================
# TAB 2 — RISK FACTORS
# ===================================
with tab2:

    st.markdown('<div class="section-header">Academic Risk Factors</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # Failures Chart
    with col1:

        failures_avg = (
            filtered_df.groupby("failures", as_index=False)["G3"]
            .mean()
        )

        fig_failures = px.bar(
            failures_avg,
            x="failures",
            y="G3",
            title="Past Failures vs Average Final Grade",
            text_auto=".2f"
        )

        st.plotly_chart(fig_failures, use_container_width=True)

        st.markdown("""
        <div class="insight-box">
        <strong>Insight:</strong> Students with more past failures consistently achieved lower average final grades.
        </div>
        """, unsafe_allow_html=True)

    # Absence Scatter
    with col2:

        fig_abs = px.scatter(
            filtered_df,
            x="absences",
            y="G3",
            color="performance_band",
            hover_data=["studytime", "failures"],
            title="Absences vs Final Grade"
        )

        st.plotly_chart(fig_abs, use_container_width=True)

        st.markdown("""
        <div class="insight-box">
        <strong>Insight:</strong> Higher absence counts are generally associated with weaker academic performance.
        </div>
        """, unsafe_allow_html=True)

    # Absence by Performance
    fig_abs_box = px.box(
        filtered_df,
        x="performance_band",
        y="absences",
        title="Absence Distribution by Performance Band"
    )

    st.plotly_chart(fig_abs_box, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
    <strong>Insight:</strong> Lower-performing students show wider absence distributions and more extreme attendance patterns.
    </div>
    """, unsafe_allow_html=True)

# ===================================
# TAB 3 — BEHAVIORAL FACTORS
# ===================================
with tab3:

    st.markdown('<div class="section-header">Behavioral & Demographic Analysis</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # Studytime
    with col1:

        fig_study = px.box(
            filtered_df,
            x="studytime",
            y="G3",
            color="performance_band",
            title="Study Time vs Final Grade"
        )

        st.plotly_chart(fig_study, use_container_width=True)

        st.markdown("""
        <div class="insight-box">
        <strong>Insight:</strong> Higher study-time categories generally correspond to stronger academic performance.
        </div>
        """, unsafe_allow_html=True)

    # Internet Access
    with col2:

        internet_avg = (
            filtered_df.groupby("internet", as_index=False)["G3"]
            .mean()
        )

        fig_internet = px.bar(
            internet_avg,
            x="internet",
            y="G3",
            title="Internet Access vs Average Final Grade",
            text_auto=".2f"
        )

        st.plotly_chart(fig_internet, use_container_width=True)

        st.markdown("""
        <div class="insight-box">
        <strong>Insight:</strong> Students with internet access achieved slightly higher average grades, although this relationship is not necessarily causal.
        </div>
        """, unsafe_allow_html=True)

    # Gender Boxplot
    fig_gender = px.box(
        filtered_df,
        x="sex",
        y="G3",
        title="Final Grade Distribution by Sex"
    )

    st.plotly_chart(fig_gender, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
    <strong>Insight:</strong> Academic and behavioral variables appear more informative than broad demographic differences.
    </div>
    """, unsafe_allow_html=True)

# ===================================
# TAB 4 — KEY FINDINGS
# ===================================
with tab4:

    st.markdown('<div class="section-header">🔍  Key Findings</div>', unsafe_allow_html=True)

    st.markdown("""
    ### Main Findings

    1. **Academic trajectory matters most** — earlier grades strongly track with final performance.

    2. **Past failures are a major warning signal** — students with more failures consistently perform worse academically.

    3. **Attendance matters** — higher absences are associated with weaker outcomes.

    4. **Study habits matter, but not alone** — study time helps, although performance variation still exists.

    5. **Demographic differences appear weaker** than academic and behavioral indicators.

    6. **Correlation does not imply causation** — these findings represent associations, not guaranteed causal relationships.
    """)

    st.info("""
    Non-obvious insight: Some support-related variables may appear weak because students receiving support were already academically at risk before intervention.
    """)

    st.success("""
    Overall takeaway: Academic trajectory, past failures, and attendance patterns appear to be the strongest indicators of student academic risk in this dataset.
    """)

# -----------------------------------
# DATA PREVIEW
# -----------------------------------
with st.expander("📄 View Filtered Dataset"):
    st.dataframe(filtered_df)