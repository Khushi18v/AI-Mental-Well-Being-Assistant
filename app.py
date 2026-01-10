import streamlit as st
from dotenv import load_dotenv
import os
from textwrap import dedent

# Agents + UI Modules
from agents import run_agents_parallel
from tools_ui import journal_ui, relaxation_ui, recommendations_ui, safety_ui

# Storage + Sentiment
from storage import load_json, save_json
from sentiment import sentiment_score

# Load environment variables
load_dotenv()

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="MindMesh - AI Mental Wellbeing Assistant",
    page_icon="🧠",
    layout="wide"
)

# ---------------- CSS LOADER ----------------
def load_local_css(file_name):
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(file_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_local_css("styles.css")

# ---------------- SIDEBAR ----------------
st.sidebar.title("MindMesh Tools")
tool = st.sidebar.radio(
    "Choose a section:",
    ["Main Assistant", "Journal", "Relaxation", "Recommendations", "Safety"]
)

#                           MAIN ASSISTANT
if tool == "Main Assistant":

    left, right = st.columns([2, 1])
    with left:
        st.markdown(
            """
            <h1>MindMesh</h1>
            <div class='muted'>
                MindMesh combines multiple intelligent agents into a single workspace,
                helping you reflect, plan, and explore your thoughts with clarity.
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown('<div class="glass" style="margin-top:10px">', unsafe_allow_html=True)
    st.subheader("Share what's on your mind")

    # ---------------- FIRST ROW ----------------
    col1, col2 = st.columns([2.3, 1], gap="medium")

    with col1:
        background = st.text_area("Background", height=140)
        concerns = st.text_area("Concerns", height=140)
        goals = st.text_area("Goals", height=140)
        coping_mechanisms = st.text_area(
            "Coping Mechanisms (e.g., exercise, talking to friends, avoidance)",
            height=140
        )

    with col2:
        st.markdown("<div class='section-title'>Support Level</div>", unsafe_allow_html=True)
        support_level = st.radio("", ["Reflective", "Structured", "Crisis"], index=1)

        st.markdown("<div class='section-title'>Physical Activity</div>", unsafe_allow_html=True)
        physical_activity = st.radio(" ", ["Daily", "Weekly", "Rarely", "Never"])

    # ---------------- SECOND ROW ----------------
    sq1, sq2, sq3 = st.columns(3, gap="medium")

    with sq1:
        st.markdown("<div class='section-title'>Sleep Quality</div>", unsafe_allow_html=True)
        sleep_quality = st.radio(" ", ["Good", "Average", "Poor"])

    with sq2:
        st.markdown("<div class='section-title'>Mood Status</div>", unsafe_allow_html=True)
        mood_status = st.radio(" ", ["Happy", "Neutral", "Low", "Depressed"])

    with sq3:
        st.markdown("<div class='section-title'>Social Support</div>", unsafe_allow_html=True)
        social_support = st.radio(" ", ["Strong", "Somewhat strong", "Weak", "No support"])

    # ---------------- GENERATE BUTTON ----------------
    generate = st.button("✨ Generate Plan")

    for key in ["assessment", "action", "follow"]:
        if key not in st.session_state:
            st.session_state[key] = ""

    if generate:
        if not (background.strip() and concerns.strip() and goals.strip()):
            st.error("Please fill all fields.")
        else:
            with st.spinner("Generating Plan..."):
                results = run_agents_parallel(
                    background, concerns, goals, coping_mechanisms,
                    sleep_quality, physical_activity, social_support
                )

                st.session_state.assessment = results["assessment"]
                st.session_state.action = results["action"]
                st.session_state.follow = results["follow"]

            st.success("Done!")

    # ---------------- RESULTS ----------------
    st.markdown('<div class="glass" style="margin-top:20px">', unsafe_allow_html=True)
    st.subheader("Results")

    st.markdown("### 📝 Assessment")
    st.markdown(st.session_state.assessment or "No assessment yet.")

    st.markdown("### ✅ Action Plan")
    st.markdown(st.session_state.action or "")

    st.markdown("### 💬 Follow-Up")
    st.markdown(st.session_state.follow or "")

    st.markdown('</div>', unsafe_allow_html=True)


#OTHER SECTIONS

elif tool == "Journal":
    journal_ui()

elif tool == "Relaxation":
    relaxation_ui()

elif tool == "Recommendations":
    recommendations_ui()

elif tool == "Safety":
    safety_ui()

# ---------------- FOOTER ----------------
st.markdown(
    """
    <div class='footer'>MindMesh • Built with care</div>
    """,
    unsafe_allow_html=True
)
