import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------
# Load Data
# -----------------------
df = pd.read_csv("student_data.csv")

# Feature engineering (same as your notebook)
df["avg_grade"] = (df["G1"] + df["G2"] + df["G3"]) / 3
df["grade_change"] = df["G3"] - df["G1"]
df["total_alcohol"] = df["Dalc"] + df["Walc"]

# -----------------------
# App Title
# -----------------------
st.title("📊 Student Performance Dashboard")

st.markdown("""
This dashboard explores how study habits, attendance, and lifestyle factors impact student performance.
""")

# -----------------------
# Sidebar Filters
# -----------------------
st.sidebar.header("Filters")

study_time = st.sidebar.slider("Study Time", int(df["studytime"].min()), int(df["studytime"].max()), (1,4))
failures = st.sidebar.slider("Past Failures", int(df["failures"].min()), int(df["failures"].max()), (0,3))

filtered_df = df[
    (df["studytime"] >= study_time[0]) &
    (df["studytime"] <= study_time[1]) &
    (df["failures"] >= failures[0]) &
    (df["failures"] <= failures[1])
]

# -----------------------
# Chart 1: Study Time vs Final Grade
# -----------------------
st.subheader("📈 Study Time vs Final Grade")

fig1 = px.box(
    filtered_df,
    x="studytime",
    y="G3",
    title="Study Time Impact on Final Grades"
)

st.plotly_chart(fig1)

st.markdown("""
**Insight:** Students with higher study time generally achieve better final grades.
""")

# -----------------------
# Chart 2: Absences vs Grade
# -----------------------
st.subheader("📉 Absences vs Final Grade")

fig2 = px.scatter(
    filtered_df,
    x="absences",
    y="G3",
    color="failures",
    title="Absences Impact on Performance"
)

st.plotly_chart(fig2)

st.markdown("""
**Insight:** Higher absences are associated with lower grades.
""")

# -----------------------
# Chart 3: Alcohol vs Performance
# -----------------------
st.subheader("🍺 Alcohol Consumption vs Performance")

fig3 = px.box(
    filtered_df,
    x="total_alcohol",
    y="G3",
    title="Alcohol Consumption Impact"
)

st.plotly_chart(fig3)

# -----------------------
# Key Takeaways
# -----------------------
st.subheader("🔍 Key Findings")

st.markdown("""
- Study time positively impacts performance  
- Past failures strongly predict lower grades  
- High absences correlate with poor outcomes  
- Lifestyle factors (like alcohol use) show moderate impact  
""")