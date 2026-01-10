# agents.py
from textwrap import dedent
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Initialize OpenAI client with API key
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
        # Updated for new SDK: access content via .content
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"⚠️ OpenAI Error: {e}"


# -------- AGENTS --------
def assessment_agent(background, concerns, goals, coping_mechanisms,
                     sleep_quality, physical_activity, social_support):
    prompt = dedent(f"""
    You are MindMesh — Assessment Agent.

    Create:
    - SUMMARY (2–3 sentences)
    - AREAS TO EXPLORE (3–6 bullet points)
    - RISK CHECK (supportive tone)

    BACKGROUND: {background}
    CONCERNS: {concerns}
    GOALS: {goals}
    COPING: {coping_mechanisms}
    SLEEP: {sleep_quality}
    ACTIVITY: {physical_activity}
    SUPPORT: {social_support}
    """)
    return call_openai(prompt)


def action_agent(assessment_text, sleep_quality, physical_activity, social_support):
    prompt = dedent(f"""
    You are MindMesh — Action Agent.
    Create a simple 4-week plan.

    Include:
    1) Weekly focus
    2) Daily micro-actions
    3) Self-checkpoints

    ASSESSMENT: {assessment_text}
    """)
    return call_openai(prompt)


def followup_agent(assessment_text, action_plan_text):
    prompt = dedent(f"""
    You are MindMesh — Follow-Up Agent.

    Create a warm 7-day check-in message with:
    - Short check-in
    - Encouragement
    - Reflective question

    ASSESSMENT: {assessment_text}
    ACTION PLAN: {action_plan_text}
    """)
    return call_openai(prompt)


# -------- PARALLEL EXECUTION --------
def run_agents_parallel(background, concerns, goals, coping_mechanisms,
                        sleep_quality, physical_activity, social_support):

    results = {"assessment": "", "action": "", "follow": ""}

    with ThreadPoolExecutor(max_workers=3) as executor:

        future_assessment = executor.submit(
            assessment_agent,
            background, concerns, goals, coping_mechanisms,
            sleep_quality, physical_activity, social_support
        )

        # Wait for assessment to finish first
        assessment_text = future_assessment.result()
        results["assessment"] = assessment_text

        futures = {
            executor.submit(action_agent, assessment_text, sleep_quality, physical_activity, social_support): "action",
            executor.submit(followup_agent, assessment_text, ""): "follow"
        }

        for future in as_completed(futures):
            key = futures[future]
            results[key] = future.result()

    return results
