import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="MCQ Exam", layout="wide")

# ---------------- TIMER ----------------
TOTAL_TIME = 20 * 60  # 20 minutes

if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

def get_time_left():
    elapsed = time.time() - st.session_state.start_time
    return max(TOTAL_TIME - elapsed, 0)


# -------- FIXED-TOP CIRCULAR TIMER CSS ---------
st.markdown("""
<style>
#timer-circle {
    position: fixed;
    top: 20px;
    right: 20px;
    background: #222;
    color: white;
    border-radius: 50%;
    width: 120px;
    height: 120px;
    font-size: 28px;
    font-weight: bold;
    display: flex;
    justify-content: center;
    align-items: center;
    border: 6px solid #00c3ff;
    animation: pulse 1s infinite;
    z-index: 9999;
}

@keyframes pulse {
    0% { box-shadow: 0 0 10px #00c3ff; }
    50% { box-shadow: 0 0 25px #00c3ff; }
    100% { box-shadow: 0 0 10px #00c3ff; }
}

.red-blink {
    border-color: red !important;
    animation: blink 1s infinite !important;
}

@keyframes blink {
    0% { color: white; }
    50% { color: red; }
    100% { color: white; }
}
</style>
""", unsafe_allow_html=True)


# ---------------- 50 MCQs ----------------
questions = [
    {
        "q": "Who is the President of India in 2025?",
        "options": ["Droupadi Murmu", "Narendra Modi", "Amit Shah", "Rajnath Singh"],
        "answer": "Droupadi Murmu"
    },
    {
        "q": "Which country hosted the 2025 BRICS Summit?",
        "options": ["India", "Russia", "Brazil", "South Africa"],
        "answer": "Russia"
    },
    {
        "q": "Nobel Peace Prize 2024 was awarded to:",
        "options": ["Narges Mohammadi", "Maria Ressa", "UNHCR", "World Food Programme"],
        "answer": "Narges Mohammadi"
    },
]

# Add remaining MCQs (auto-generated)
for i in range(4, 51):
    questions.append({
        "q": f"Sample Question {i}: Which option is correct?",
        "options": [f"Option A{i}", f"Option B{i}", f"Option C{i}", f"Option D{i}"],
        "answer": f"Option A{i}"
    })


# ---------------- TIMER DISPLAY ----------------
time_left = get_time_left()
minutes = int(time_left // 60)
seconds = int(time_left % 60)

timer_class = "red-blink" if time_left < 300 else ""

st.markdown(
    f'<div id="timer-circle" class="{timer_class}">{minutes:02d}:{seconds:02d}</div>',
    unsafe_allow_html=True
)

if time_left == 0:
    st.session_state.submit = True


# ---------------- FORM ----------------
if "responses" not in st.session_state:
    st.session_state.responses = {}

st.title("📘 Full-Length MCQ Test (50 Questions)")
st.write("All questions appear below. Answer before timer ends.")

with st.form("exam_form"):
    for idx, q in enumerate(questions):
        st.session_state.responses[idx] = st.radio(
            f"**Q{idx+1}. {q['q']}**",
            q["options"],
            index=None,
            key=f"q_{idx}"
        )

    submitted = st.form_submit_button("Submit")

    if submitted:
        st.session_state.submit = True
        st.session_state.time_taken = TOTAL_TIME - time_left


# ---------------- RESULT ----------------
if st.session_state.get("submit", False):

    st.subheader("📊 Final Score")

    score = 0
    detailed = []

    for idx, q in enumerate(questions):
        user_ans = st.session_state.responses.get(idx)
        correct = q["answer"]

        if user_ans == correct:
            score += 1
            marks = "+1"
        elif user_ans is None:
            marks = "0"
        else:
            score -= 0.3
            marks = "-0.3"

        detailed.append([
            idx + 1,
            q["q"],
            user_ans if user_ans else "Not Answered",
            correct,
            marks
        ])

    st.write(f"### ✅ Your Score: **{score} / 50**")
    st.write(
        f"### ⏳ Time Taken: {int(st.session_state.time_taken//60)} min "
        f"{int(st.session_state.time_taken%60)} sec"
    )

    st.subheader("📘 Detailed Answers")

    df = pd.DataFrame(
        detailed, 
        columns=["Q.No", "Question", "Your Answer", "Correct Answer", "Marks"]
    )

    st.dataframe(df, use_container_width=True)



