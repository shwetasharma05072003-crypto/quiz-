import streamlit as st
import random
import io
import csv
from datetime import datetime, timedelta

st.set_page_config(page_title="SSC JE — GS Quiz (Science + Current Affairs)", layout="wide")

# -----------------------
# CONFIG
# -----------------------
TOTAL_TIME_SECONDS = 40 * 60  # 40 minutes
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
# RAW QUESTION BANK
# -----------------------
RAW_QUESTIONS = [
    {"q": "Which of the following is the SI unit of electric charge?",
     "options": ["Coulomb", "Volt", "Ampere", "Ohm"],
     "ans": "Coulomb"},
    {"q": "Which gas is produced during photosynthesis?",
     "options": ["Oxygen", "Carbon dioxide", "Nitrogen", "Hydrogen"],
     "ans": "Oxygen"},
    {"q": "The atomic number of an element is equal to the number of:",
     "options": ["Protons in the nucleus", "Neutrons in the nucleus", "Electrons in valence shell", "Protons plus neutrons"],
     "ans": "Protons in the nucleus"},
    {"q": "What is the main function of red blood cells (RBCs)?",
     "options": ["Transport oxygen", "Fight infection", "Clot blood", "Store nutrients"],
     "ans": "Transport oxygen"},
    {"q": "Which wave has the longest wavelength?",
     "options": ["Radio waves", "Infrared rays", "Visible light", "Ultraviolet rays"],
     "ans": "Radio waves"},
    {"q": "pH of a neutral aqueous solution at 25°C is approximately:",
     "options": ["7", "0", "14", "1"],
     "ans": "7"},
    {"q": "Who proposed the three laws of motion?",
     "options": ["Isaac Newton", "Albert Einstein", "James Clerk Maxwell", "Galileo Galilei"],
     "ans": "Isaac Newton"},
    {"q": "Which vitamin is primarily produced in human skin on exposure to sunlight?",
     "options": ["Vitamin D", "Vitamin C", "Vitamin A", "Vitamin K"],
     "ans": "Vitamin D"},
    {"q": "Catalysts function by:",
     "options": ["Lowering activation energy", "Raising activation energy", "Changing equilibrium constant", "Being consumed in reaction"],
     "ans": "Lowering activation energy"},
    {"q": "Which organelle is known as the powerhouse of the cell?",
     "options": ["Mitochondrion", "Nucleus", "Ribosome", "Golgi apparatus"],
     "ans": "Mitochondrion"},
    {"q": "Bohr model of hydrogen explains the emission spectrum by stating that electrons:",
     "options": ["Jump between fixed energy levels", "Move in random orbits", "Are stationary", "Continuously lose energy"],
     "ans": "Jump between fixed energy levels"},
    {"q": "What is the chemical formula of table salt?",
     "options": ["NaCl", "KCl", "Na2CO3", "CaCl2"],
     "ans": "NaCl"},
    {"q": "Which blood group is known as the universal donor?",
     "options": ["O negative", "AB positive", "A positive", "B negative"],
     "ans": "O negative"},
    {"q": "Which law states that pressure of a gas is inversely proportional to its volume at constant temperature?",
     "options": ["Boyle's Law", "Charles's Law", "Avogadro's Law", "Gay-Lussac's Law"],
     "ans": "Boyle's Law"},
    {"q": "Which of these is NOT a macronutrient?",
     "options": ["Vitamin C", "Proteins", "Carbohydrates", "Fats"],
     "ans": "Vitamin C"},
    {"q": "What type of bond is formed when electrons are shared between atoms?",
     "options": ["Covalent bond", "Ionic bond", "Hydrogen bond", "Metallic bond"],
     "ans": "Covalent bond"},
    {"q": "Which gas primarily causes global warming?",
     "options": ["Carbon dioxide (CO2)", "Oxygen (O2)", "Nitrogen (N2)", "Argon (Ar)"],
     "ans": "Carbon dioxide (CO2)"},
    {"q": "Which immune cells are primarily responsible for producing antibodies?",
     "options": ["B lymphocytes (B cells)", "T lymphocytes (T cells)", "Macrophages", "Neutrophils"],
     "ans": "B lymphocytes (B cells)"},
    {"q": "Which property of sound determines pitch?",
     "options": ["Frequency", "Amplitude", "Speed", "Wavelength"],
     "ans": "Frequency"},
    {"q": "Which element has the highest electronegativity?",
     "options": ["Fluorine", "Oxygen", "Chlorine", "Nitrogen"],
     "ans": "Fluorine"},
    {"q": "What is the term for a solution with pH < 7?",
     "options": ["Acidic", "Basic", "Neutral", "Alkaline"],
     "ans": "Acidic"},
    {"q": "Which device converts chemical energy into electrical energy?",
     "options": ["Battery (cell)", "Transformer", "Resistor", "Capacitor"],
     "ans": "Battery (cell)"},
    {"q": "The bending of light when it passes from one medium to another is called:",
     "options": ["Refraction", "Reflection", "Diffraction", "Interference"],
     "ans": "Refraction"},
    {"q": "Which of the following is an example of a biodegradable polymer?",
     "options": ["Polylactic acid (PLA)", "Polyethylene (PE)", "Polystyrene (PS)", "Polyvinyl chloride (PVC)"],
     "ans": "Polylactic acid (PLA)"},
    {"q": "Which law describes the relation between current, voltage and resistance?",
     "options": ["Ohm's Law", "Faraday's Law", "Kirchhoff's Law", "Newton's Law"],
     "ans": "Ohm's Law"},

    # Current Affairs
    {"q": "G20 Summit 2025 will be hosted by which country?",
     "options": ["Brazil", "Italy", "India", "Australia"],
     "ans": "Italy"},
    {"q": "What is the theme of the G20 Summit 2025?",
     "options": ["One Earth, One Family", "People, Planet, Prosperity", "Global Stability & Sustainability", "Green Growth for All"],
     "ans": "Global Stability & Sustainability"},
    {"q": "Who hosted the G20 Summit in 2024?",
     "options": ["India", "Indonesia", "Brazil", "UAE"],
     "ans": "Brazil"},
    {"q": "India hosted the G20 Summit in which year?",
     "options": ["2021", "2022", "2023", "2024"],
     "ans": "2023"},
    {"q": "BRICS Summit 2025 will be held in—",
     "options": ["China", "Russia", "South Africa", "India"],
     "ans": "Russia"},
    {"q": "BRICS Summit 2024 was hosted by—",
     "options": ["UAE", "South Africa", "China", "India"],
     "ans": "South Africa"},
    {"q": "After expansion, BRICS consists of how many member countries?",
     "options": ["7", "9", "10", "11"],
     "ans": "11"},
    {"q": "SCO Summit 2025 will be held in—",
     "options": ["Uzbekistan", "India", "Kazakhstan", "Russia"],
     "ans": "Kazakhstan"},
    {"q": "India chaired the SCO Summit (Virtual) in which year?",
     "options": ["2022", "2023", "2024", "2025"],
     "ans": "2023"},
    {"q": "SCO was established in—",
     "options": ["1995", "1998", "2001", "2003"],
     "ans": "2001"},
    {"q": "COP29 was hosted by—",
     "options": ["UAE", "Azerbaijan", "Qatar", "Oman"],
     "ans": "Azerbaijan"},
    {"q": "The proposed International Climate Finance Bank was discussed during—",
     "options": ["G20 2025", "BRICS 2025", "COP29", "SCO 2025"],
     "ans": "COP29"},
    {"q": "India signed the “Strategic Technology Partnership 2025” with—",
     "options": ["Japan", "USA", "UK", "Canada"],
     "ans": "USA"},
    {"q": "India–EU Clean Energy Dialogue 2025 focused on—",
     "options": ["Solar power", "Biofuels", "Green hydrogen", "All of the above"],
     "ans": "All of the above"},
    {"q": "India’s 2025 Carbon Capture collaboration is with—",
     "options": ["Norway", "Sweden", "Germany", "Denmark"],
     "ans": "Norway"},
    {"q": "The ‘Global Green Partnership 2025’ was launched between India and—",
     "options": ["USA", "Japan", "France", "Germany"],
     "ans": "Japan"},
    {"q": "Which country hosted the World Economic Forum 2025?",
     "options": ["USA", "Switzerland", "France", "UAE"],
     "ans": "Switzerland"},
    {"q": "The BRICS bank is also known as—",
     "options": ["New Development Bank", "Global Growth Bank", "Asia Infrastructure Bank", "BRICS Monetary Fund"],
     "ans": "New Development Bank"},
    {"q": "ASEAN Summit 2025 was chaired by—",
     "options": ["Malaysia", "Laos", "Myanmar", "Indonesia"],
     "ans": "Laos"},
    {"q": "BIMSTEC Summit 2025 was hosted by—",
     "options": ["Sri Lanka", "Bhutan", "India", "Nepal"],
     "ans": "Sri Lanka"},
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
# CIRCULAR COUNTDOWN TIMER
# -----------------------
if not st.session_state.submitted:

    mins, secs = divmod(remaining, 60)

    # BLINKING RED WHEN < 5 MIN
    blink_class = "blink" if remaining < 300 else ""

    timer_html = f"""
    <style>
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
        to {{
            visibility: hidden;
        }}
    }}
    </style>

    <div class="timer-box {blink_class}">
        {mins:02d}:{secs:02d}
    </div>

    <script>
        setTimeout(() => {{
            window.location.reload();
        }}, 1000);
    </script>
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
st.title("SSC JE — GS Quiz (Science + Current Affairs)")
st.markdown(f"**Total Questions:** {NUM_Q}  •  **Time:** 40 minutes  •  **Marks:** +1 / −0.3")
st.write("---")

# -----------------------
# Quiz area
# -----------------------
if not st.session_state.submitted:
    st.write("Answer the questions below. Select **Not Attempted** if you want to skip a question.")

    for i, q in enumerate(QUESTIONS):
        default = st.session_state.responses.get(i, None)
        choice = st.radio(
            f"Q{i+1}. {q['q']}",
            q["options"],
            index=q["options"].index(default) if default in q["options"] else None,
            key=f"q_{i}"
        )
        st.session_state.responses[i] = choice

    if st.button("Submit Now"):
        st.session_state.submitted = True
        st.session_state.auto_submitted = False
        st.stop()

# -----------------------
# RESULTS
# -----------------------
if st.session_state.submitted:

    st.header("Result Summary")
    total_score = 0.0
    correct = wrong = not_attempted = 0

    rows = []

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
            "Your Answer": user_ans,
            "Correct Answer": correct_ans,
            "Outcome": outcome,
            "Marks": mark
        })

        # Show feedback
        if outcome == "Correct":
            st.success(f"Q{i+1}. {q['q']}\n- ✅ Your answer: **{user_ans}**  •  +{POSITIVE_MARK}")
        elif outcome == "Wrong":
            st.error(f"Q{i+1}. {q['q']}\n- ❌ Your answer: **{user_ans}**  •  Correct: **{correct_ans}**  •  −{NEGATIVE_MARK}")
        else:
            st.info(f"Q{i+1}. {q['q']}\n- ⚪ Not Attempted. Correct: **{correct_ans}**")

    st.write("---")
    st.markdown(f"### ✅ Correct : **{correct}**   •   ❌ Wrong : **{wrong}**   •   ⚪ Not Attempted : **{not_attempted}**")
    st.markdown(f"### 🟦 Final Score : **{total_score:.2f} / {NUM_Q}**")

    csv_buffer = io.StringIO()
    writer = csv.DictWriter(
        csv_buffer,
        fieldnames=["Q_no", "Question", "Your Answer", "Correct Answer", "Outcome", "Marks"]
    )
    writer.writeheader()
    for r in rows:
        writer.writerow(r)

    csv_bytes = csv_buffer.getvalue().encode("utf-8")

    st.download_button(
        "Download detailed result (CSV)",
        data=csv_bytes,
        file_name=f"ssc_je_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

    st.write("---")
    st.caption("Note: Questions & options are shuffled each session. To retake, refresh the page and start again.")


