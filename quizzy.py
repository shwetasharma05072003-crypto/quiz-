import streamlit as st
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="SSC JE GS Test", layout="wide")

# ----------------------------
# TIMER SETTINGS
# ----------------------------

TOTAL_TIME = 40 * 60  # 40 minutes in seconds

if "start_time" not in st.session_state:
    st.session_state.start_time = datetime.now()

if "submitted" not in st.session_state:
    st.session_state.submitted = False

# Calculate remaining time
elapsed = (datetime.now() - st.session_state.start_time).total_seconds()
remaining = TOTAL_TIME - elapsed

# Auto submit when time ends
if remaining <= 0 and not st.session_state.submitted:
    st.session_state.submitted = True

# Display timer
if not st.session_state.submitted:
    mins, secs = divmod(int(remaining), 60)
    st.markdown(f"### ⏳ Time Left: **{mins:02d}:{secs:02d}**")

# Force rerun every second for timer
if not st.session_state.submitted:
    st.experimental_rerun()


# ----------------------------
# QUESTION BANK (example)
# ----------------------------

questions = [
    {
        "q": "Which law states that energy can neither be created nor destroyed?",
        "options": ["Newton's First Law", "Law of Conservation of Energy", "Law of Gravitation", "Coulomb’s Law"],
        "ans": "Law of Conservation of Energy"
    },
    {
        "q": "Which metal is liquid at room temperature?",
        "options": ["Sodium", "Mercury", "Gold", "Aluminum"],
        "ans": "Mercury"
    },
    # Add all 50 questions here …
]

# Shuffle questions once
if "shuffled_questions" not in st.session_state:
    st.session_state.shuffled_questions = random.sample(questions, len(questions))

questions = st.session_state.shuffled_questions

responses = {}

st.title("📝 SSC JE General Studies Test")

# ----------------------------
# INPUT ANSWERS
# ----------------------------
if not st.session_state.submitted:
    st.write("### Select the correct answers:")

    for i, q in enumerate(questions):
        responses[i] = st.radio(f"**Q{i+1}. {q['q']}**", q["options"], index=None, key=f"q{i}")

    if st.button("Submit Test"):
        st.session_state.submitted = True
        st.experimental_rerun()


# ----------------------------
# RESULT AREA
# ----------------------------
if st.session_state.submitted:
    score = 0
    wrong = 0
    correct = 0

    st.subheader("📘 Result Analysis")

    for i, q in enumerate(questions):
        user_ans = st.session_state.get(f"q{i}")

        if user_ans == q["ans"]:
            score += 1
            correct += 1
            st.success(f"Q{i+1}. ✔ Correct | Your answer: {user_ans}")
        else:
            score -= 0.3
            wrong += 1

            st.error(
                f"Q{i+1}. ❌ Wrong | Your answer: {user_ans} | Correct: {q['ans']}"
            )

    st.write("---")
    st.write(f"### ✅ **Final Score: {score} / {len(questions)}**")
    st.write(f"### ✔ Correct: {correct}")
    st.write(f"### ✘ Wrong: {wrong} (–0.3 each)")
