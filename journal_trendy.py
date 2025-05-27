import streamlit as st
import json
import os
from datetime import date, datetime
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="🌸 My Career Journal", layout="centered")

st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #fff8fb !important;
        color: #333 !important;
    }
    textarea, input, .stTextInput>div>div>input {
        background-color: white !important;
        color: black !important;
        border-radius: 8px;
    }
    section[data-testid="stSidebar"] {
        background-color: #e0f0ff !important;
    }
    h1, h2 {
        color: #ee5fa1;
    }
    .stButton>button {
        background-color: #eeaeca;
        color: white;
        border-radius: 10px;
    }
    .stButton>button:hover {
        background-color: #f084ac;
    }
</style>
""", unsafe_allow_html=True)

JOURNAL_FILE = "journal_data.json"

if os.path.exists(JOURNAL_FILE):
    with open(JOURNAL_FILE, "r") as f:
        journal_data = json.load(f)
else:
    journal_data = {}

st.title("🌸 Career-Focused Daily Journal")
st.caption("Reflect, track, and grow daily 🌱")

mode = st.sidebar.radio("Choose Mode", ["📝 Write Journal", "📖 View Entries + Progress"])

if mode == "📝 Write Journal":
    st.header("🧘 Log Today's Work and Learning")
    journal_date = str(st.date_input("Date", date.today()))
    sections = {}

    sections["internship"] = st.text_area("💼 Internship Task")
    sections["python"] = st.text_area("🐍 Python Practice")
    sections["sql"] = st.text_area("🗃️ SQL Practice")
    sections["ml_dl"] = st.text_area("🤖 ML/DL Work")
    sections["llms"] = st.text_area("🧠 LLM Learning or Projects")
    sections["resume"] = st.text_area("📄 Resume / Job Hunt")
    sections["part_time"] = st.text_area("💼 Part-time Apps")

    mood = st.selectbox("🎭 Mood", ["😄", "🙂", "😐", "😩", "😠"])
    energy = st.slider("⚡ Energy Level", 1, 5, 3)
    satisfaction = st.selectbox("📊 Progress Satisfaction", ["✅ Yes", "😐 Meh", "❌ No"])
    tomorrow = st.text_area("🔮 Tomorrow's Focus")

    if st.button("Save Entry"):
        journal_data[journal_date] = {
            "sections": sections,
            "mood": mood,
            "energy": energy,
            "satisfaction": satisfaction,
            "tomorrow": tomorrow
        }
        with open(JOURNAL_FILE, "w") as f:
            json.dump(journal_data, f, indent=4)
        st.success("✨ Entry saved!")

elif mode == "📖 View Entries + Progress":
    st.header("📅 Your Journal and Progress")

    def show_progress_grid(data):
        today = datetime.today()
        dates = []
        values = []
        for i in range(30):
            day = (today - pd.Timedelta(days=i)).strftime('%Y-%m-%d')
            dates.append(day)
            val = data.get(day, {}).get("satisfaction", None)
            if val == "✅ Yes":
                values.append(2)
            elif val == "😐 Meh":
                values.append(1)
            elif val == "❌ No":
                values.append(0)
            else:
                values.append(None)

        dates.reverse()
        values.reverse()
        colors = {0: "#FF6B6B", 1: "#FFD93D", 2: "#6BCB77", None: "#E0E0E0"}

        fig, ax = plt.subplots(figsize=(8, 1))
        ax.bar(range(30), [1]*30, color=[colors[v] for v in values], edgecolor="white")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title("Progress Over Last 30 Days", fontsize=12, color="#555")
        st.pyplot(fig)

    show_progress_grid(journal_data)

    if journal_data:
        selected_date = st.selectbox("Select a date", sorted(journal_data.keys(), reverse=True))
        entry = journal_data[selected_date]
        sections = entry["sections"]

        st.markdown(f"### 🗓️ Entry for **{selected_date}**")
        for key, label in [
            ("internship", "💼 Internship"),
            ("python", "🐍 Python"),
            ("sql", "🗃️ SQL"),
            ("ml_dl", "🤖 ML/DL"),
            ("llms", "🧠 LLMs"),
            ("resume", "📄 Resume / Jobs"),
            ("part_time", "💼 Part-time Apps")
        ]:
            st.markdown(f"**{label}:** {sections.get(key, '*No input*')}")

        st.markdown(f"**🎭 Mood:** {entry['mood']}")
        st.markdown(f"**⚡ Energy:** {entry['energy']}/5")
        st.markdown(f"**📊 Satisfaction:** {entry['satisfaction']}")
        st.markdown(f"**🔮 Tomorrow's Plan:** {entry['tomorrow']}")
    else:
        st.info("No entries found yet. Start writing today!")

