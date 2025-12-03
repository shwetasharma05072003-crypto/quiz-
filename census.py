import streamlit as st
import random
from datetime import datetime

st.set_page_config(page_title="SSC JE — GS Quiz", layout="wide")

TOTAL_TIME_SECONDS = 50 * 60  # 50 minutes
NEGATIVE_MARK = 0.3
POSITIVE_MARK = 1.0

# -----------------------
# SESSION STATE INIT
# -----------------------
if "start_time" not in st.session_state:
    st.session_state.start_time = datetime.now()
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "auto_submitted" not in st.session_state:
    st.session_state.auto_submitted = False
if "shuffled_questions" not in st.session_state:
    st.session_state.shuffled_questions = None
if "responses" not in st.session_state:
    st.session_state.responses = {}

# -----------------------
# QUESTIONS DATA
# -----------------------
census_questions = [
    {"question": "When was the first synchronous Census conducted in India?",
     "options": ["1871", "1881", "1901", "1921"], "answer": "1881"},

    {"question": "Who is known as the Father of the Indian Census?",
     "options": ["H.H. Risley", "W.C. Plowden", "J. Martineau", "A. Mitra"], "answer": "W.C. Plowden"},

    {"question": "How often is the Census conducted in India?",
     "options": ["5 years", "10 years", "8 years", "12 years"], "answer": "10 years"},

    {"question": "The latest completed Census in India was conducted in:",
     "options": ["2001", "2011", "2021", "2023"], "answer": "2011"},

    {"question": "Which Ministry conducts the Census of India?",
     "options": ["Ministry of Statistics", "Ministry of Home Affairs", "NITI Aayog", "Ministry of Rural Development"],
     "answer": "Ministry of Home Affairs"},

    {"question": "Who conducts the Census in India?",
     "options": ["National Sample Survey Office", "CSO", "Registrar General of India", "NITI Aayog"],
     "answer": "Registrar General of India"},

    {"question": "India's population in Census 2011 was:",
     "options": ["102 crore", "110 crore", "121 crore", "132 crore"], "answer": "121 crore"},

    {"question": "Which state recorded the highest population in 2011?",
     "options": ["Maharashtra", "Bihar", "Uttar Pradesh", "West Bengal"], "answer": "Uttar Pradesh"},

    {"question": "Which state recorded the lowest population in 2011?",
     "options": ["Goa", "Sikkim", "Nagaland", "Arunachal Pradesh"], "answer": "Sikkim"},

    {"question": "Which UT has the highest population (2011)?",
     "options": ["Delhi", "Chandigarh", "Puducherry", "Lakshadweep"], "answer": "Delhi"},

    {"question": "Which UT has the lowest population (2011)?",
     "options": ["Dadra & Nagar Haveli", "Lakshadweep", "Chandigarh", "Daman & Diu"],
     "answer": "Lakshadweep"},

    {"question": "Sex ratio of India in Census 2011 is:",
     "options": ["933", "940", "943", "950"], "answer": "943"},

    {"question": "Which state has the highest sex ratio (2011)?",
     "options": ["Kerala", "Tamil Nadu", "Odisha", "Andhra Pradesh"], "answer": "Kerala"},

    {"question": "Which state has the lowest sex ratio (2011)?",
     "options": ["Punjab", "Haryana", "Bihar", "Gujarat"], "answer": "Haryana"},

    {"question": "What is India’s literacy rate (2011)?",
     "options": ["67.8%", "72.98%", "74.04%", "76.6%"], "answer": "74.04%"},

    {"question": "Which state has the highest literacy rate (2011)?",
     "options": ["Kerala", "Mizoram", "Goa", "Delhi"], "answer": "Kerala"},

    {"question": "Which state has the lowest literacy rate (2011)?",
     "options": ["Uttar Pradesh", "Jharkhand", "Bihar", "Rajasthan"], "answer": "Bihar"},

    {"question": "Which decade recorded the highest population growth?",
     "options": ["1951–61", "1961–71", "1971–81", "1981–91"], "answer": "1961–71"},

    {"question": "Which decade showed negative population growth?",
     "options": ["1901–11", "1911–21", "1921–31", "1941–51"], "answer": "1911–21"},

    {"question": "Population density of India in 2011 was:",
     "options": ["324", "352", "382", "412"], "answer": "382"},

    {"question": "Which state has the highest population density?",
     "options": ["Uttar Pradesh", "Bihar", "West Bengal", "Kerala"], "answer": "Bihar"},

    {"question": "Which state has the lowest population density?",
     "options": ["Sikkim", "Nagaland", "Mizoram", "Arunachal Pradesh"], "answer": "Arunachal Pradesh"},

    {"question": "Which state recorded highest decadal growth (2001–11)?",
     "options": ["Bihar", "Rajasthan", "Meghalaya", "Haryana"], "answer": "Meghalaya"},

    {"question": "Which state recorded negative decadal growth (2001–11)?",
     "options": ["Goa", "Nagaland", "Sikkim", "Tripura"], "answer": "Nagaland"},

    {"question": "Average household size in India (2011) is:",
     "options": ["4.3", "4.5", "4.8", "5.1"], "answer": "4.8"},

    {"question": "Census 2011 was which number census of India?",
     "options": ["14th", "15th", "16th", "17th"], "answer": "15th"},

    {"question": "Census 2011 was which number after independence?",
     "options": ["5th", "6th", "7th", "8th"], "answer": "7th"},

    {"question": "Child sex ratio (0–6 years) in Census 2011 is:",
     "options": ["914", "918", "920", "926"], "answer": "914"},

    {"question": "Which state has highest child sex ratio?",
     "options": ["Nagaland", "Mizoram", "Kerala", "Goa"], "answer": "Mizoram"},

    {"question": "Which state has lowest child sex ratio?",
     "options": ["Punjab", "Haryana", "Gujarat", "Rajasthan"], "answer": "Haryana"},
]

# -----------------------
# SHUFFLE QUESTIONS
# -----------------------
def build_shuffled():
    shuffled = []
    for item in census_questions:
        opts = item["options"].copy()
        opts_with_skip = opts + ["Not Attempted"]
        random.shuffle(opts_with_skip)

        shuffled.append({
            "q": item["question"],
            "options": opts_with_skip,
            "correct_text": item["answer"]
        })

    random.shuffle(shuffled)
    return shuffled


if st.session_state.shuffled_questions is None:
    st.session_state.shuffled_questions = build_shuffled()

QUESTIONS = st.session_state.shuffled_questions
NUM_Q = len(QUESTIONS)

# -----------------------
# TIMER
# -----------------------
elapsed = (datetime.now() - st.session_state.start_time).total_seconds()
remaining = int(max(0, TOTAL_TIME_SECONDS - elapsed))

if remaining == 0 and not st.session_state.submitted:
    st.session_state.submitted = True
    st.session_state.auto_submitted = True

if not st.session_state.submitted:
    mins, secs = divmod(remaining, 60)
    st.markdown(f"⏰ **Time Left:** {mins:02d}:{secs:02d}")

# -----------------------
# QUIZ
# -----------------------
if not st.session_state.submitted:
    st.write("Answer all questions below. Select 'Not Attempted' if skipping.")

    for i, q in enumerate(QUESTIONS):
        choice = st.radio(
            f"Q{i+1}. {q['q']}",
            q["options"],
            index=len(q["options"]) - 1,
            key=f"q_{i}"
        )
        st.session_state.responses[i] = choice

    if st.button("Submit Now", type="primary"):
        st.session_state.submitted = True
        st.session_state.auto_submitted = False
        st.stop()

# -----------------------
# RESULT SUMMARY
# -----------------------
if st.session_state.submitted:
    st.header("Result Summary")
    total_score = 0.0
    correct = wrong = not_attempted = 0

    for i, q in enumerate(QUESTIONS):
        user_ans = st.session_state.responses.get(i, "Not Attempted")
        correct_ans = q["correct_text"]

        if user_ans == "Not Attempted" or user_ans is None:
            mark = 0.0
            not_attempted += 1
            outcome = "Not Attempted"

        elif user_ans == correct_ans:
            mark = POSITIVE_MARK
            total_score += mark
            correct += 1
            outcome = "Correct"

        else:
            mark = -NEGATIVE_MARK
            total_score += mark
            wrong += 1
            outcome = f"Wrong (−{NEGATIVE_MARK})"

        st.write(f"Q{i+1}. {q['q']}")
        st.write(f"Your Answer: {user_ans} | Correct Answer: {correct_ans} | Result: {outcome}\n")

    st.markdown(f"### **Total Score: {total_score} / {NUM_Q}**")
    st.markdown(f"✅ Correct: {correct} | ❌ Wrong: {wrong} | ⏸️ Not Attempted: {not_attempted}")
