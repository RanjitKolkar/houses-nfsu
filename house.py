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
# LOAD DATA (CSV ONLY)
# ======================
DATA_FILE = "exported.csv"
df = pd.read_csv(DATA_FILE)

# ----------------------
# BASIC CLEANING
# ----------------------
df["Program"] = df["Program"].astype(str).str.strip()
df["Gender"] = df["Gender"].astype(str).str.upper().str.strip()
df["House"] = df["House"].astype(str).str.strip()
df["Year"] = df["Year"].astype(str).str.strip()

# ======================
# ROW COLOR FUNCTION
# ======================
def color_house_rows(row):
    house_colors = {
        "M": "background-color: #e3f2fd; color: black;",
        "L": "background-color: #e8f5e9; color: black;",
        "T": "background-color: #fff3e0; color: black;",
        "D": "background-color: #fce4ec; color: black;",
    }
    return [house_colors.get(row["House"], "color: black;")] * len(row)

# ======================
# TITLE
# ======================
st.title("🏠 Student House Distribution 2025")

# ======================
# HOUSE LEGEND
# ======================
st.subheader("🏡 Houses")

house_names = {
    "M": "Majestic Maximus",
    "L": "Ultra Unicorn",
    "T": "Timeless Tigris",
    "D": "Legendary Leo",
}

house_colors = {
    "M": "background-color: #e3f2fd; color: black;",
    "L": "background-color: #e8f5e9; color: black;",
    "T": "background-color: #fff3e0; color: black;",
    "D": "background-color: #fce4ec; color: black;",
}

for key, name in house_names.items():
    st.markdown(
        f"""
        <div style="
            {house_colors[key]}
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 10px;
            font-size: 18px;
            font-weight: 600;
        ">
            {key} – {name}
        </div>
        """,
        unsafe_allow_html=True
    )

# ======================
# SIDEBAR FILTERS
# ======================
st.sidebar.header("🔎 Filters")

programs = ["All"] + sorted(df["Program"].dropna().unique())
years = ["All"] + sorted(df["Year"].dropna().unique())
genders = ["All"] + sorted(df["Gender"].dropna().unique())
houses = ["All"] + sorted(df["House"].dropna().unique())

sel_program = st.sidebar.selectbox("🎓 Program", programs)
sel_year = st.sidebar.selectbox("📘 Year", years)
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
# SUMMARY METRICS
# ======================
c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Students", len(filtered))
c2.metric("Male Students", len(filtered[filtered["Gender"] == "M"]))
c3.metric("Female Students", len(filtered[filtered["Gender"] == "F"]))
c4.metric("Total Houses", filtered["House"].nunique())

# ======================
# STUDENT TABLE (READ ONLY)
# ======================
st.subheader("📋 Student List (Read-Only)")

display_cols = [
    "Sl No",
    "Enrollment No",
    "Program",
    "Year",
    "Student Name",
    "Gender",
    "House"
]

styled_df = (
    filtered[display_cols]
    .style
    .apply(color_house_rows, axis=1)
)

st.dataframe(
    styled_df,
    use_container_width=True,
    height=520
)

# ======================
# BAR CHART – HOUSE vs PROGRAM
# ======================
st.subheader("📈 House Distribution by Program")

fig1 = px.bar(
    filtered.groupby(["House", "Program"])
    .size()
    .reset_index(name="Count"),
    x="House",
    y="Count",
    color="Program",
    barmode="group"
)

st.plotly_chart(fig1, use_container_width=True)

# ======================
# BAR CHART – HOUSE vs YEAR
# ======================
st.subheader("📈 House Distribution by Year")

fig2 = px.bar(
    filtered.groupby(["House", "Year"])
    .size()
    .reset_index(name="Count"),
    x="House",
    y="Count",
    color="Year",
    barmode="group"
)

st.plotly_chart(fig2, use_container_width=True)

# ======================
# PIE CHART – GENDER
# ======================
st.subheader("📊 Gender Distribution")

fig3 = px.pie(
    filtered,
    names="Gender",
    color="Gender",
    color_discrete_map={"M": "#1f77b4", "F": "#ff69b4"}
)

st.plotly_chart(fig3, use_container_width=True)
