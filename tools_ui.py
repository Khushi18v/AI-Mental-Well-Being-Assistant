import streamlit as st
from datetime import datetime
from storage import load_json, save_json
from sentiment import sentiment_score
import time

# -------- IMPORT YOUR OPENAI AGENT HELPERS --------
from openai import OpenAI
from textwrap import dedent
import os
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed

# Load .env
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# -------- OPENAI HELPER --------

def call_openai(prompt: str):
    """Send a prompt to OpenAI and return clean text output."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ OpenAI Error: {e}"

# AI TOOL FUNCTIONS

def ai_reflection(text):
    prompt = f"""
    Provide a gentle reflection for this journal entry:
    - 2 sentences supportive tone
    - 1 compassionate suggestion
    ENTRY: {text}
    """
    return call_openai(prompt)


def ai_relaxation_suggestion(state):
    prompt = f"""
    User emotional state: {state}
    Suggest the most suitable relaxation technique from:
    - Box Breathing
    - 4-7-8 Breathing
    - Progressive Muscle Relaxation
    - Safe Place Visualization
    - Thought Labeling
    - Cognitive Defusion
    Return:
    1) Name of technique
    2) 1–2 sentence explanation
    """
    return call_openai(prompt)


def ai_daily_suggestion():
    prompt = """
    Give one personalized wellbeing suggestion.
    Keep it calm, friendly, 1–2 sentences.
    """
    return call_openai(prompt)


def ai_supportive_message(text):
    prompt = f"""
    User message: {text}
    Respond with:
    - Empathy (2–3 sentences)
    - Validation
    - Gentle encouragement for seeking support if needed
    Avoid medical language.
    """
    return call_openai(prompt)

# -------------- AI JOURNAL SECTION -----------------

def journal_ui():
    st.markdown("## 🧾 Safe-Space Journal")
    entries = load_json("journal.json")
    text = st.text_area("Write freely...", height=150)

    if st.button("Save Entry"):
        if text.strip():
            reflection = ai_reflection(text)

            entry = {
                "text": text,
                "sentiment": sentiment_score(text),
                "ai_reflection": reflection,
                "timestamp": datetime.now().strftime("%d %b %Y, %I:%M %p")
            }
            entries.append(entry)
            save_json("journal.json", entries)
            st.success("Saved.")
            st.info(reflection)

    st.markdown("### Past Entries")
    for e in reversed(entries[-20:]):
        st.markdown(
            f"""
            <div class="glass" style="margin-bottom:10px">
                <strong>{e['timestamp']}</strong><br>
                {e['text']}<br>
                <small>Sentiment: {e['sentiment']}</small><br>
                <em style="opacity:0.7;">AI Reflection: {e.get('ai_reflection', '')}</em>
            </div>
            """,
            unsafe_allow_html=True
        )

# -------------- AI RELAXATION SECTION --------------

def relaxation_ui():
    st.markdown("## 🌬️ Relaxation Hub — Breathe, Release, Reset")

    # --- AI Suggestion Added ---
    st.markdown("### 🤖 AI-Based Relaxation Suggestion")
    user_state = st.text_input("How are you feeling right now? (optional)")
    if st.button("Get AI Suggestion"):
        if user_state.strip():
            st.info(ai_relaxation_suggestion(user_state))

    tab1, tab2 = st.tabs(["🌬️ Breathing Exercises", "🧘 Mind Relaxation"])

    # ----- Breathing Tab -----
    with tab1:
        st.markdown(
            """
            <div class="glass" style="padding:15px;">
                <h3>🌬️ Guided Breathing Techniques</h3>
                <p>Controlled breathing helps calm the nervous system and restore balance.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        modes = {
            "Box Breathing (4-in / 4-hold / 4-out / 4-hold)": (4, 4, 4, 4),
            "4–7–8 Relaxation Breath": (4, 7, 8, 0),
            "Pursed-Lip Breathing (4-in / 6-out)": (4, 0, 6, 0),
            "Coherence Breathing (5.5-in / 5.5-out)": (5.5, 0, 5.5, 0),
            "Triangle Breathing (4-in / 4-hold / 6-out)": (4, 4, 6, 0),
        }

        choice = st.selectbox("Choose a breathing technique:", list(modes.keys()))
        inhale, hold, exhale, hold2 = modes[choice]

        st.markdown('<div class="breathing-circle"></div>', unsafe_allow_html=True)

        if st.button("Start Breathing Exercise"):
            placeholder = st.empty()

            for cycle in range(3):
                placeholder.markdown(
                    f"<h3 class='breathing-text'>Breathe in… ({inhale}s)</h3>",
                    unsafe_allow_html=True
                )
                time.sleep(inhale)

                if hold > 0:
                    placeholder.markdown(
                        f"<h3 class='breathing-text'>Hold… ({hold}s)</h3>",
                        unsafe_allow_html=True
                    )
                    time.sleep(hold)

                placeholder.markdown(
                    f"<h3 class='breathing-text'>Breathe out… ({exhale}s)</h3>",
                    unsafe_allow_html=True
                )
                time.sleep(exhale)

                if hold2 > 0:
                    placeholder.markdown(
                        f"<h3 class='breathing-text'>Hold… ({hold2}s)</h3>",
                        unsafe_allow_html=True
                    )
                    time.sleep(hold2)

            placeholder.markdown("<h3 class='breathing-text'>Complete ✨</h3>", unsafe_allow_html=True)
            st.success("Your breathing exercise is complete. Notice how your body feels now.")

    # ----- Mind Relaxation Tab -----
    with tab2:
        st.markdown("### 🧘 Mind Relaxation Exercises")

        relax_type = st.selectbox(
            "Choose an exercise:",
            [
                "Progressive Muscle Relaxation",
                "Safe Place Visualization",
                "Cognitive Defusion (Unhooking)",
                "Thought Labeling",
                "5-Breath Reset",
                "Color Tracing Exercise",
            ]
        )

        if relax_type == "Progressive Muscle Relaxation":
            st.markdown(
                """
                <div class="glass">
                <h4>🧘 Progressive Muscle Relaxation</h4>
                Slowly tense each muscle group for 4 seconds, then release:<br><br>
                • Hands → clench and let go<br>
                • Shoulders → raise, then drop<br>
                • Face → tighten, then soften<br>
                • Stomach → tighten, then relax<br>
                • Legs → press down, then release<br><br>
                Notice the warmth and heaviness.
                </div>
                """, unsafe_allow_html=True)

        elif relax_type == "Safe Place Visualization":
            st.markdown(
                """
                <div class="glass">
                <h4>🏝 Safe Place Visualization</h4>
                Imagine a peaceful space:<br><br>
                • Quiet forest<br>
                • Warm beach<br>
                • Soft room<br><br>
                Add sensory details and stay there for 20–30 seconds.
                </div>
                """, unsafe_allow_html=True)

        elif relax_type == "Cognitive Defusion (Unhooking)":
            st.markdown(
                """
                <div class="glass">
                <h4>🌿 Cognitive Defusion</h4>
                When a difficult thought appears, say:<br><br>
                “I am noticing the thought that…”<br><br>
                Let it drift by gently.
                </div>
                """, unsafe_allow_html=True)

        elif relax_type == "Thought Labeling":
            st.markdown(
                """
                <div class="glass">
                <h4>🔎 Thought Labeling</h4>
                Label thoughts as they appear:<br><br>
                • “This is worry.”<br>
                • “This is planning.”<br>
                • “This is imagining.”<br>
                • “This is fear.”<br><br>
                Label → observe → release.
                </div>
                """, unsafe_allow_html=True)

        elif relax_type == "5-Breath Reset":
            st.markdown(
                """
                <div class="glass">
                <h4>🌬️ 5-Breath Reset</h4>
                With each breath release tension:<br><br>
                1 — Shoulders<br>
                2 — Jaw<br>
                3 — Hands<br>
                4 — Stomach<br>
                5 — Ground feet
                </div>
                """, unsafe_allow_html=True)

        elif relax_type == "Color Tracing Exercise":
            st.markdown(
                """
                <div class="glass">
                <h4>🎨 Color Tracing Exercise</h4>
                Pick a color around you.<br><br>
                Notice 5 objects in that color and observe their textures and shapes.
                </div>
                """, unsafe_allow_html=True)




# ------------ AI RECOMMENDATIONS SECTION -----------

def recommendations_ui():
    st.markdown("## ✨ Personalized Well-Being Recommendations")

    st.markdown(
        """
        <div class="glass" style="padding:15px; border-left:4px solid #6bb4ff;">
            <h4>🌱 Daily Wellness Snapshot</h4>
            Small habits compound over time—choose what resonates today.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 🧘 Guided Mindfulness & Meditation Options")
    st.markdown("""
        - **Box Breathing**  
        - **Body Scan Meditation**  
        - **4–7–8 Breathing**  
        - Mindfulness apps: Headspace, Calm, Insight Timer  
    """)

    st.markdown("---")

    st.markdown("### ✍ Reflective Journaling Prompts")
    st.markdown("""
        - Three things you're grateful for  
        - What brought you peace today?  
        - What challenged you?  
        - One thing you can offer yourself compassion for  
    """)

    st.markdown("---")

    st.markdown("### 🌿 Lifestyle Foundations")
    st.markdown("""
        - 20–30 minutes sunlight  
        - Consistent sleep schedule  
        - Hydrate regularly  
        - 2–5 minute movement breaks  
    """)

    st.markdown("---")

    st.markdown("### 💼 Focus & Productivity")
    st.markdown("""
        - Pomodoro (25/5)  
        - Top 3 priorities  
        - Time-blocking  
        - Monotasking over multitasking  
    """)

    st.markdown("---")

    st.markdown("### 🍎 Nutrition & Mood Support")
    st.markdown("""
        - Omega-3 rich foods  
        - Leafy greens & berries  
        - Regular meal timing  
        - Reduce afternoon caffeine  
    """)

    st.markdown("---")

    st.markdown("### 🎶 Sensory Relaxation")
    st.markdown("""
        - Calm playlists  
        - Nature ambience  
        - Light stretching  
        - Warm drink ritual  
    """)

    st.markdown("---")

    st.markdown("### 🧠 Mental Health Resources")
    st.markdown("""
        - Crisis helplines  
        - Therapy directories  
        - Grounding & breathing tools  
    """)

    st.markdown("---")

    # ------------- AI UPGRADE -------------
    if st.button("🎲 Get a Personalized Suggestion"):
        st.success(ai_daily_suggestion())

# -------------------- AI SAFETY --------------------

def safety_ui():
    st.markdown("## ⚠️ Safety & Support Panel")

    st.markdown(
        """
        <div class="glass" style="padding:15px; border-left:4px solid #ff4b4b;">
            <h4>🛡️ Your Safety Matters</h4>
            MindMesh supports grounding and reflection, but does not replace
            professional mental-health care.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 📞 Emergency & Crisis Support")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🚨 Emergency Services (Local)"):

            st.write("Call your local emergency number: 112 (India) / 911 (US)")
        st.caption("For immediate danger.")

    with col2:
        if st.button("📞 Suicide & Crisis Helpline"):
            st.write("India: 9152987821 (AASRA) | US: 988 (Suicide & Crisis Lifeline)")
        st.caption("24/7 crisis professionals.")

    with col3:
        if st.button("💬 Trusted Contact"):
            st.write("Reach out to a trusted friend, family member, or counselor.")
        st.caption("Talk to someone supportive.")

    st.markdown("---")

    st.markdown("### 🧭 When to Seek Extra Support")
    st.markdown("""
        - Persistent sadness or anxiety  
        - Trouble sleeping or functioning  
        - Panic or intrusive thoughts  
        - Thoughts of harming yourself  
    """)

    st.info("You deserve support. Speaking with a professional can make a difference.")

    st.markdown("---")

    st.markdown("### 🌱 Grounding Resources")
    st.markdown("""
        - 5-4-3-2-1 grounding  
        - Slow breathing  
        - Progressive muscle relaxation  
        - Safe-place visualization  
    """)

    st.caption("If you notice difficult patterns, consider using a relaxation exercise above.")

    # ---------------- AI SUPPORT MESSAGE ----------------
    st.markdown("---")
    st.markdown("### 💬 Want to express how you're feeling?")

    safety_text = st.text_area("Write anything you want. This stays confidential:", height=100)

    if st.button("Get AI Support"):
        if safety_text.strip():
            st.warning(ai_supportive_message(safety_text))