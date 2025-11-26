import streamlit as st
import random
import io
import csv
from datetime import datetime

st.set_page_config(page_title="SSC JE — GS Quiz", layout="wide")

# -----------------------

# CONFIG

# -----------------------

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

# RAW QUESTION BANK (45 Questions)

# -----------------------

RAW_QUESTIONS = [
# Constitution Articles (30)
{"q": "Article 1 of the Constitution deals with:",
"options": ["A. Fundamental Duties", "B. Name and territory of India", "C. Citizenship", "D. Official languages"],
"ans": "B. Name and territory of India"},
{"q": "“India, that is Bharat, shall be a Union of States” is stated in:",
"options": ["A. Article 2", "B. Article 4", "C. Article 1", "D. Article 5"],
"ans": "C. Article 1"},
{"q": "Citizenship at the commencement of the Constitution is covered under:",
"options": ["A. Article 10", "B. Article 7", "C. Article 5", "D. Article 11"],
"ans": "C. Article 5"},
{"q": "Right to Equality is ensured by Articles:",
"options": ["A. 14–18", "B. 19–22", "C. 23–24", "D. 25–28"],
"ans": "A. 14–18"},
{"q": "Article 14 ensures:",
"options": ["A. Freedom of speech", "B. Equality before law", "C. Right to education", "D. Right to life"],
"ans": "B. Equality before law"},
{"q": "Prohibition of discrimination is mentioned in:",
"options": ["A. Article 14", "B. Article 15", "C. Article 19", "D. Article 20"],
"ans": "B. Article 15"},
{"q": "Untouchability is abolished under:",
"options": ["A. Article 16", "B. Article 17", "C. Article 18", "D. Article 15"],
"ans": "B. Article 17"},
{"q": "Article 19 contains:",
"options": ["A. 4 freedoms", "B. 5 freedoms", "C. 6 freedoms", "D. 7 freedoms"],
"ans": "C. 6 freedoms"},
{"q": "Protection in respect of conviction for offenses is under:",
"options": ["A. Article 20", "B. Article 21", "C. Article 22", "D. Article 23"],
"ans": "A. Article 20"},
{"q": "“Right to Life and Personal Liberty” is guaranteed by:",
"options": ["A. Article 19", "B. Article 21", "C. Article 22", "D. Article 24"],
"ans": "B. Article 21"},
{"q": "Right to Education is a Fundamental Right under:",
"options": ["A. Article 21A", "B. Article 29", "C. Article 45", "D. Article 14"],
"ans": "A. Article 21A"},
{"q": "Article 22 deals with:",
"options": ["A. Freedom of religion", "B. Protection against arrest and detention", "C. Cultural rights", "D. Right to constitutional remedies"],
"ans": "B. Protection against arrest and detention"},
{"q": "Prohibition of traffic in human beings is under:",
"options": ["A. Article 20", "B. Article 21", "C. Article 23", "D. Article 24"],
"ans": "C. Article 23"},
{"q": "Prohibition of child labour in factories is in:",
"options": ["A. Article 23", "B. Article 24", "C. Article 21", "D. Article 19"],
"ans": "B. Article 24"},
{"q": "Freedom of religion begins from Article:",
"options": ["A. 19", "B. 21", "C. 25", "D. 32"],
"ans": "C. 25"},
{"q": "Article 32 is related to:",
"options": ["A. Impeachment", "B. Election of President", "C. Writs", "D. Finance Commission"],
"ans": "C. Writs"},
{"q": "“Heart & Soul of the Constitution” refers to:",
"options": ["A. Article 32", "B. Article 21", "C. Article 368", "D. Article 3"],
"ans": "A. Article 32"},
{"q": "Article 40 relates to:",
"options": ["A. Panchayats", "B. Free legal aid", "C. Uniform Civil Code", "D. Alcohol prohibition"],
"ans": "A. Panchayats"},
{"q": "Article 44 deals with:",
"options": ["A. DPSPs", "B. UCC (Uniform Civil Code)", "C. Fundamental Duties", "D. Cooperative societies"],
"ans": "B. UCC (Uniform Civil Code)"},
{"q": "Fundamental Duties are in:",
"options": ["A. Article 48A", "B. Article 51A", "C. Article 50", "D. Article 60"],
"ans": "B. Article 51A"},
{"q": "The President of India takes oath under:",
"options": ["A. Article 52", "B. Article 53", "C. Article 60", "D. Article 61"],
"ans": "C. Article 60"},
{"q": "Procedure for impeachment of the President is in:",
"options": ["A. Article 61", "B. Article 62", "C. Article 63", "D. Article 64"],
"ans": "A. Article 61"},
{"q": "Vice-President’s resignation is stated in:",
"options": ["A. Article 65", "B. Article 66", "C. Article 67", "D. Article 68"],
"ans": "C. Article 67"},
{"q": "Article 72 deals with:",
"options": ["A. Pardoning power of President", "B. Pardoning power of Governor", "C. Election Commission", "D. Comptroller and Auditor General"],
"ans": "A. Pardoning power of President"},
{"q": "Governor’s pardoning power is under:",
"options": ["A. Article 72", "B. Article 161", "C. Article 163", "D. Article 170"],
"ans": "B. Article 161"},
{"q": "Article 239A is related to:",
"options": ["A. Panchayati Raj", "B. Union Territories", "C. Finance Commission", "D. Cooperative Societies"],
"ans": "B. Union Territories"},
{"q": "Article 243G is related to:",
"options": ["A. Municipalities", "B. Panchayats", "C. Anti-defection", "D. Language"],
"ans": "B. Panchayats"},
{"q": "Article 280 deals with:",
"options": ["A. Finance Commission", "B. CAG", "C. UPSC", "D. NITI Aayog"],
"ans": "A. Finance Commission"},
{"q": "Article 300A guarantees:",
"options": ["A. Right to Equality", "B. Right to Property (legal right)", "C. Right to Education", "D. Right to Worship"],
"ans": "B. Right to Property (legal right)"},
{"q": "Constitution Amendment Procedure is described in:",
"options": ["A. Article 352", "B. Article 356", "C. Article 360", "D. Article 368"],
"ans": "D. Article 368"},

```
# Dam Questions (10)
{"q": "Bhakra Nangal Dam is built on which river?",
 "options": ["a) Yamuna", "b) Sutlej", "c) Ganga", "d) Godavari"],
 "ans": "b) Sutlej"},
{"q": "Hirakud Dam is located in which state?",
 "options": ["a) Maharashtra", "b) Odisha", "c) Chhattisgarh", "d) Jharkhand"],
 "ans": "b) Odisha"},
{"q": "Tehri Dam is built on which river?",
 "options": ["a) Bhagirathi", "b) Ganga", "c) Yamuna", "d) Chenab"],
 "ans": "a) Bhagirathi"},
{"q": "Sardar Sarovar Dam is built on which river?",
 "options": ["a) Tapi", "b) Narmada", "c) Krishna", "d) Mahanadi"],
 "ans": "b) Narmada"},
{"q": "Nagarjuna Sagar Dam is on which river?",
 "options": ["a) Krishna", "b) Godavari", "c) Mahanadi", "d) Cauvery"],
 "ans": "a) Krishna"},
{"q": "Koyna Dam is located in which state?",
 "options": ["a) Kerala", "b) Maharashtra", "c) Karnataka", "d) Andhra Pradesh"],
 "ans": "b) Maharashtra"},
{"q": "Idukki Dam is located in which state?",
 "options": ["a) Tamil Nadu", "b) Kerala", "c) Karnataka", "d) Andhra Pradesh"],
 "ans": "b) Kerala"},
{"q": "Mettur Dam is built on which river?",
 "options": ["a) Cauvery", "b) Krishna", "c) Godavari", "d) Tapi"],
 "ans": "a) Cauvery"},
{"q": "Which is the tallest dam in India?",
 "options": ["a) Bhakra Nangal", "b) Tehri", "c) Hirakud", "d) Sardar Sarovar"],
 "ans": "b) Tehri"},
{"q": "Which dam is primarily used for hydroelectric power in Maharashtra?",
 "options": ["a) Bhakra Nangal", "b) Koyna", "c) Tehri", "d) Hirakud"],
 "ans": "b) Koyna"},

# Nobel Prize 2025 (5)
{"q": "Who won the 2025 Nobel Prize in Physics?",
 "options": ["a) Susumu Kitagawa, Richard Robson & Omar Yaghi",
             "b) Mary E. Brunkow, Fred Ramsdell & Shimon Sakaguchi",
             "c) John Clarke, Michel H. Devoret & John M. Martinis",
             "d) László Krasznahorkai"],
 "ans": "c) John Clarke, Michel H. Devoret & John M. Martinis"},
{"q": "For what contribution was the 2025 Physics Prize awarded?",
 "options": ["a) Discovery of penicillin",
             "b) Quantum‑mechanical tunneling & energy quantisation in electric circuits",
             "c) Discovery of DNA structure",
             "d) Metal‑organic frameworks"],
 "ans": "b) Quantum‑mechanical tunneling & energy quantisation in electric circuits"},
{"q": "Who won the 2025 Nobel Prize in Chemistry?",
 "options": ["a) John Clarke, Michel H. Devoret & John M. Martinis",
             "b) Mary E. Brunkow, Fred Ramsdell & Shimon Sakaguchi",
             "c) Susumu Kitagawa, Richard Robson & Omar M. Yaghi",
             "d) Joel Mokyr, Philippe Aghion & Peter Howitt"],
 "ans": "c) Susumu Kitagawa, Richard Robson & Omar M. Yaghi"},
{"q": "Who won the 2025 Nobel Prize in Physiology or Medicine?",
 "options": ["a) John Clarke, Michel H. Devoret & John M. Martinis",
             "b) Susumu Kitagawa, Richard Robson & Omar M. Yaghi",
             "c) Mary E. Brunkow, Fred Ramsdell & Shimon Sakaguchi",
             "d) László Krasznahorkai"],
 "ans": "c) Mary E. Brunkow, Fred Ramsdell & Shimon Sakaguchi"},
{"q": "Who won the 2025 Nobel Peace Prize?",
 "options": ["a) A scientific team",
             "b) A novelist",
             "c) María Corina Machado",
             "d) An economist"],
 "ans": "c) María Corina Machado"}
```

]

# -----------------------

# SHUFFLE QUESTIONS + OPTIONS

# -----------------------

def build_shuffled():
shuffled = []
for item in RAW_QUESTIONS:
opts = item["options"].copy()
opts_with_skip = opts + ["Not Attempted"]
random.shuffle(opts_with_skip)
shuffled.append({
"q": item["q"],
"options": opts_with_skip,
"correct_text": item["ans"]
})
random.shuffle(shuffled)
return shuffled

if st.session_state.shuffled_questions is None:
st.session_state.shuffled_questions = build_shuffled()

QUESTIONS = st.session_state.shuffled_questions
NUM_Q = len(QUESTIONS)

# -----------------------

# TIME HANDLING

# -----------------------

elapsed = (datetime.now() - st.session_state.start_time).total_seconds()
remaining = int(max(0, TOTAL_TIME_SECONDS - elapsed))

if remaining == 0 and not st.session_state.submitted:
st.session_state.submitted = True
st.session_state.auto_submitted = True

# -----------------------

# TIMER

# -----------------------

if not st.session_state.submitted:
mins, secs = divmod(remaining, 60)
blink_class = "blink" if remaining < 300 else ""
timer_html = f""" <style>
.timer-box {{
position: fixed;
top: 10px;
right: 20px;
z-index: 9999;
background-color: white;
padding: 15px;
border-radius: 50%;
border: 6px solid #ff4d4d;
width: 110px;
height: 110px;
display: flex;
justify-content: center;
align-items: center;
font-size: 22px;
font-weight: 700;
color: #b30000;
box-shadow: 0px 0px 12px rgba(255,0,0,0.4);
}}
.blink {{
animation: blink-animation 1s steps(5, start) infinite;
color: red !important;
}}
@keyframes blink-animation {{
to {{ visibility: hidden; }}
}} </style> <div class="timer-box {blink_class}">
{mins:02d}:{secs:02d} </div> <script>
setTimeout(() => {{
window.location.reload();
}}, 1000); </script>
"""
st.markdown(timer_html, unsafe_allow_html=True)
else:
if st.session_state.auto_submitted:
st.warning("⏱ Time's up — test auto-submitted.")
else:
st.info("✅ Test submitted.")

# -----------------------

# MAIN PAGE

# -----------------------

st.title("SSC JE — GS Quiz (Constitution + Dams + Nobel 2025)")
st.markdown(f"**Total Questions:** {NUM_Q}  •  **Time:** 50 minutes  •  **Marks:** +1 / −0.3")
st.write("---")

# -----------------------

# QUIZ AREA

# -----------------------

if not st.session_state.submitted:
st.write("Answer the questions below. Select **Not Attempted** if you want to skip a question.")
for i, q in enumerate(QUESTIONS):
default = st.session_state.responses.get(i, None)
choice = st.radio(
f"Q{i+1}. {q['q']}",
q["options"],
index=q["options"].index(default) if default in q["options"] else 0,
key=f"q_{i}"
)
st.session_state.responses[i] = choice

```
if st.button("Submit Now"):
    st.session_state.submitted = True
    st.session_state.auto_submitted = False
    st.stop()
```

# -----------------------

# RESULTS

# -----------------------

if st.session_state.submitted:
st.header("Result Summary")
total_score = 0.0
correct = wrong = not_attempted = 0
rows = []

```
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
        outcome = "Wrong"

    rows.append({
        "Q_no": i + 1,
        "Question": q["q"],
        "
```
