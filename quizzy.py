import streamlit as st
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="SSC JE GS Test", layout="wide")

# -----------------------------------------------------
# TIMER CONFIG
# -----------------------------------------------------
TOTAL_TIME = 40 * 60  # 40 minutes

# Initialize session state variables
if "start_time" not in st.session_state:
    st.session_state.start_time = datetime.now()

if "submitted" not in st.session_state:
    st.session_state.submitted = False

if "answers" not in st.session_state:
    st.session_state.answers = {}

# Compute remaining time
elapsed = (datetime.now() - st.session_state.start_time).total_seconds()
remaining = TOTAL_TIME - elapsed

# Auto submit when time is up
if remaining <= 0 and not st.session_state.submitted:
    st.session_state.submitted = True

# -----------------------------------------------------
# QUESTION BANK
# (I put 3 demo questions. YOU will paste all 45 later)
# -----------------------------------------------------
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
    {
        "q": "What is the SI unit of Force?",
        "options": ["Joule", "Newton", "Pascal", "Watt"],
        "ans": "Newton"
    },
    # 🔥 Add all your 25 Science + 20 Current Affairs questions here
]

# Shuffle only once at start
if "shuffled_questions" not in st.session_state:
    st.session_state.shuffled_questions = random.sample(questions, len(questions))


st.title("📝 SSC JE General Studies Test")

# -----------------------------------------------------
# SHOW TIMER
# -----------------------------------------------------
if not st.session_state.submitted:
    mins, secs = divmod(max(0, int(remaining)), 60)
    st.markdown(f"<h3>⏳ Time Left: <b>{mins:02d}:{secs:02d}</b></h3>", unsafe_allow_html=True)

# The trick: Automatically refresh UI every second
if not st.session_state.submitted:
    st.button("⏳ Refresh Timer (Click Every Minute)", help="Streamlit removed auto-refresh. Click to update timer.")

# -----------------------------------------------------
# TEST INTERFACE
# -----------------------------------------------------
if not st.session_state.submitted:

    st.write("### Select your answers:")

    for i, q in enumerate(st.session_state.shuffled_questions):

        st.session_state.answers[i] = st.radio(
            f"**Q{i+1}. {q['q']}**",
            q["options"],
            index=None,
            key=f"q{i}"
        )

    # Manual submit
    if st.button("Submit Test"):
        st.session_state.submitted = True
        st.experimental_rerun()

# -----------------------------------------------------
# SHOW RESULTS
# -----------------------------------------------------
if st.session_state.submitted:
    st.subheader("📘 Result Analysis")

    score = 0
    correct = 0
    wrong = 0

    for i, q in enumerate(st.session_state.shuffled_questions):

        user_ans = st.session_state.answers.get(i)

        if user_ans == q["ans"]:
            correct += 1
            score += 1
            st.success(f"Q{i+1}. ✔ Correct | Your Answer: {user_ans}")
        else:
            wrong += 1
            score -= 0.3
            st.error(f"Q{i+1}. ❌ Wrong | Your Answer: {user_ans} | Correct: {q['ans']}")

    st.write("---")
    st.write(f"### ✔ Correct: {correct}")
    st.write(f"### ✘ Wrong: {wrong} (−0.3 each)")
    st.write(f"### 🟦 **Final Score: {score} / {len(questions)}**")

