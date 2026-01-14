import streamlit as st
import pandas as pd
import plotly.express as px

# ======================
# PAGE CONFIG
# ======================
st.set_page_config(
    page_title="NFSU House Distribution",
    layout="wide"
)

# ======================
# HELPERS
# ======================
def semester_to_year(sem):
    try:
        sem = int(sem)
        if sem in [1, 2]:
            return "First Year"
        elif sem in [3, 4]:
            return "Second Year"
        elif sem in [5, 6]:
            return "Third Year"
        elif sem in [7, 8]:
            return "Fourth Year"
    except:
        return None

# ======================
# LOAD DATA
# ======================
DATA_FILE = "students_with_houses1.xlsx"
df = pd.read_excel(DATA_FILE)

# Basic cleaning
df["Program"] = df["Program"].astype(str).str.strip()
df["Gender"] = df["Gender"].astype(str).str.upper().str.strip()
df["House"] = df["House"].astype(str).str.strip()
df["Semester"] = df["Semester"].astype(str).str.strip()

# Create Academic Year column
df["Year"] = df["Semester"].apply(semester_to_year)

# ======================
# TITLE
# ======================
st.title("🏠 NFSU Goa – Student House Distribution Dashboard (Year-wise)")

# ======================
# SIDEBAR FILTERS
# ======================
st.sidebar.header("🔎 Filters")

programs = ["All"] + sorted(df["Program"].dropna().unique().tolist())
years = ["All"] + sorted(df["Year"].dropna().unique().tolist())
genders = ["All"] + sorted(df["Gender"].dropna().unique().tolist())
houses = ["All"] + sorted(df["House"].dropna().unique().tolist())

sel_program = st.sidebar.selectbox("🎓 Program / Stream", programs)
sel_year = st.sidebar.selectbox("📘 Academic Year", years)
sel_gender = st.sidebar.selectbox("⚧️ Gender", genders)
sel_house = st.sidebar.selectbox("🏠 House", houses)

# ======================
# APPLY FILTERS
# ======================
filtered = df.copy()

if sel_program != "All":
    filtered = filtered[filtered["Program"] == sel_program]

if sel_year != "All":
    filtered = filtered[filtered["Year"] == sel_year]

if sel_gender != "All":
    filtered = filtered[filtered["Gender"] == sel_gender]

if sel_house != "All":
    filtered = filtered[filtered["House"] == sel_house]

# ======================
# SUMMARY CARDS
# ======================
c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Students", len(filtered))
c2.metric("Male Students", len(filtered[filtered["Gender"] == "M"]))
c3.metric("Female Students", len(filtered[filtered["Gender"] == "F"]))
c4.metric("Total Houses", filtered["House"].nunique())

# ======================
# SUMMARY TABLE
# ======================


# ======================
# BAR CHART – HOUSE vs PROGRAM
# ======================
st.subheader("📈 House Distribution Across Programs")

fig1 = px.bar(
    filtered.groupby(["House", "Program"])
    .size()
    .reset_index(name="Count"),
    x="House",
    y="Count",
    color="Program",
    barmode="group",
    title="House-wise Student Distribution by Program"
)

st.plotly_chart(fig1, use_container_width=True)

# ======================
# BAR CHART – HOUSE vs YEAR
# ======================
st.subheader("📈 House Distribution Across Academic Years")

fig2 = px.bar(
    filtered.groupby(["House", "Year"])
    .size()
    .reset_index(name="Count"),
    x="House",
    y="Count",
    color="Year",
    barmode="group",
    title="House-wise Student Distribution by Academic Year"
)

st.plotly_chart(fig2, use_container_width=True)

# ======================
# PIE CHART – GENDER
# ======================
st.subheader("📊 Gender Distribution (Filtered View)")

fig3 = px.pie(
    filtered,
    names="Gender",
    color="Gender",
    color_discrete_map={"M": "#1f77b4", "F": "#ff69b4"},
    title="Gender Distribution"
)

st.plotly_chart(fig3, use_container_width=True)

# ======================
# STUDENT LIST (LIMITED COLUMNS)
# ======================
st.subheader("📋 Student List with House Assigned")

display_cols = [
    "Enrollment No",
    "Program",
    "Year",
    "Student Name",
    "Gender",
    "House"
]

display_cols = [c for c in display_cols if c in filtered.columns]

# ----------------------
# Add House Badge Column
# ----------------------
def house_badge(house):
    colors = {
        "A": "#1976d2",  # Blue
        "B": "#2e7d32",  # Green
        "C": "#ef6c00",  # Orange
        "D": "#c2185b",  # Pink
    }
    return f"""
    <span style="
        background-color:{colors.get(house,'#777')};
        color:white;
        padding:4px 10px;
        border-radius:12px;
        font-weight:600;
        font-size:0.85rem;
        display:inline-block;
        min-width:28px;
        text-align:center;
    ">
        {house}
    </span>
    """

table_df = filtered[display_cols].copy()
table_df["House"] = table_df["House"].apply(house_badge)

# ----------------------
# Render as HTML table
# ----------------------
st.markdown(
    table_df.to_html(escape=False, index=False),
    unsafe_allow_html=True
)
