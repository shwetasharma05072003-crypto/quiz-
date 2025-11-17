# quiz.py
import streamlit as st
import random
import pandas as pd
from datetime import datetime
from pathlib import Path

st.set_page_config(page_title="Stable MCQ Quiz", layout="wide")

# -------------------------
# Put your questions here
# -------------------------
questions = [
    {"q": "Which of the following is a fat‐soluble vitamin?", "options": ["Vitamin B6", "Vitamin C", "Vitamin A", "Vitamin B12"], "answer": "Vitamin A"},
    {"q": "The chemical name of Vitamin D is:", "options": ["Retinol", "Calciferol", "Tocopherol", "Ascorbic acid"], "answer": "Calciferol"},
    {"q": "Which vitamin deficiency causes bleeding gums?", "options": ["Vitamin A", "Vitamin D", "Vitamin C", "Vitamin K"], "answer": "Vitamin C"},
    {"q": "Which vitamin is not stored significantly in the human body?", "options": ["Vitamin A", "Vitamin D", "Vitamin C", "Vitamin E"], "answer": "Vitamin C"},
    {"q": "Riboflavin is also known as:", "options": ["Vitamin B1", "Vitamin B2", "Vitamin B3", "Vitamin B6"], "answer": "Vitamin B2"},
    {"q": "Which vitamin increases the absorption of iron from the gut?", "options": ["Vitamin B1", "Vitamin C", "Vitamin D", "Vitamin K"], "answer": "Vitamin C"},
    {"q": "Niacin is the scientific name of which vitamin?", "options": ["Vitamin B1", "Vitamin B2", "Vitamin B3", "Vitamin B6"], "answer": "Vitamin B3"},
    {"q": "Which vitamin has the scientific name Phytonadione?", "options": ["Vitamin K", "Vitamin E", "Vitamin A", "Vitamin C"], "answer": "Vitamin K"},
    {"q": "Pernicious anemia results from deficiency of:", "options": ["Vitamin B9", "Vitamin B12", "Vitamin B6", "Vitamin C"], "answer": "Vitamin B12"},
    {"q": "Rickets in children results from deficiency of:", "options": ["Vitamin D", "Vitamin B12", "Vitamin C", "Vitamin A"], "answer": "Vitamin D"},
    {"q": "Pellagra, with dermatitis, diarrhea, and dementia, is caused by deficiency of:", "options": ["Vitamin B1", "Vitamin B2", "Vitamin B3", "Vitamin B6"], "answer": "Vitamin B3"},
    {"q": "Which phylum includes animals with segmented bodies?", "options": ["Mollusca", "Annelida", "Arthropoda", "Nematoda"], "answer": "Annelida"},
    {"q": "Bilateral symmetry is characteristic of:", "options": ["Cnidaria", "Platyhelminthes", "Porifera", "Echinodermata"], "answer": "Platyhelminthes"},
    {"q": "Cnidocytes (stinging cells) are characteristic of:", "options": ["Ctenophora", "Cnidaria", "Platyhelminthes", "Porifera"], "answer": "Cnidaria"},
    {"q": "Which phylum has a complete digestive system but no circulatory system?", "options": ["Platyhelminthes", "Nematoda", "Annelida", "Arthropoda"], "answer": "Nematoda"},
    {"q": "Hermaphroditism is commonly found in:", "options": ["Earthworm", "Ascaris", "Cockroach", "Starfish"], "answer": "Earthworm"},
    {"q": "Flame cells (protonephridia) are excretory structures of:", "options": ["Annelida", "Platyhelminthes", "Nematoda", "Mollusca"], "answer": "Platyhelminthes"},
    {"q": "The term ‘cell’ was first used by:", "options": ["Schleiden", "Schwann", "Robert Hooke", "Leeuwenhoek"], "answer": "Robert Hooke"},
    {"q": "Who discovered the nucleus?", "options": ["Robert Brown", "Robert Hooke", "Virchow", "Schleiden"], "answer": "Robert Brown"},
    {"q": "‘All cells arise from pre-existing cells’ was stated by:", "options": ["Darwin", "Schleiden", "Schwann", "Virchow"], "answer": "Virchow"},
    {"q": "The cell theory was proposed by:", "options": ["Schleiden & Schwann", "Watson & Crick", "Whittaker", "Lamarck"], "answer": "Schleiden & Schwann"},
    {"q": "Which of the following is present in plant cells but absent in animal cells?", "options": ["Mitochondria", "Ribosomes", "Cell wall", "Lysosomes"], "answer": "Cell wall"},
    {"q": "Powerhouse of the cell is:", "options": ["Ribosome", "Mitochondria", "Golgi body", "Nucleus"], "answer": "Mitochondria"},
    {"q": "Ribosomes are involved in:", "options": ["Respiration", "Protein synthesis", "Lipid synthesis", "Cell division"], "answer": "Protein synthesis"},
    {"q": "Which is the site of photosynthesis?", "options": ["Mitochondria", "Golgi body", "Chloroplasts", "Nucleus"], "answer": "Chloroplasts"},
    {"q": "The fluid part of the cell is called:", "options": ["Cytosol", "Cytoplasm", "Matrix", "Stroma"], "answer": "Cytoplasm"},
    {"q": "Which structure regulates entry/exit of materials?", "options": ["Nucleus", "Cell membrane", "Ribosome", "Vacuole"], "answer": "Cell membrane"},
    {"q": "Which is a single-membrane organelle?", "options": ["Mitochondria", "Chloroplast", "Lysosome", "Nucleus"], "answer": "Lysosome"},
    {"q": "Chromosomes are present in:", "options": ["Cytoplasm", "Nucleus", "Cell wall", "Golgi body"], "answer": "Nucleus"},
    {"q": "Plant cells store food in:", "options": ["Cell wall", "Vacuoles", "Lysosomes", "Ribosomes"], "answer": "Vacuoles"},
    {"q": "The organelle for packaging and secretion is:", "options": ["Ribosomes", "Golgi apparatus", "Mitochondria", "Centrioles"], "answer": "Golgi apparatus"},
    {"q": "The longest cell in the human body is:", "options": ["Blood cell", "Liver cell", "Neuron", "Muscle cell"], "answer": "Neuron"},
    {"q": "The longest bone in the human body is:", "options": ["Tibia", "Fibula", "Femur", "Humerus"], "answer": "Femur"},
    {"q": "The smallest bone in the human body is:", "options": ["Incus", "Malleus", "Stapes", "Hyoid"], "answer": "Stapes"},
    {"q": "Which organ is known as the ‘master gland’?", "options": ["Thyroid", "Pituitary gland", "Adrenal gland", "Pancreas"], "answer": "Pituitary gland"},
    {"q": "The functional unit of the kidney is:", "options": ["Nephron", "Alveolus", "Neuron", "Glomerulus"], "answer": "Nephron"},
    {"q": "Number of chromosomes in a human somatic cell:", "options": ["23", "44", "23 pairs (46)", "92"], "answer": "23 pairs (46)"},
    {"q": "The largest internal organ is:", "options": ["Kidney", "Lungs", "Liver", "Heart"], "answer": "Liver"},
    {"q": "Strongest muscle in the human body:", "options": ["Heart", "Masseter", "Biceps", "Diaphragm"], "answer": "Masseter"},
    {"q": "Red color of blood is due to:", "options": ["Myosin", "Pepsin", "Hemoglobin", "Fibrin"], "answer": "Hemoglobin"},
    {"q": "Which vitamin is synthesized by sunlight?", "options": ["Vitamin A", "Vitamin C", "Vitamin D", "Vitamin K"], "answer": "Vitamin D"},
    {"q": "Bone protecting the brain is called:", "options": ["Femur", "Cranium", "Sternum", "Atlas"], "answer": "Cranium"},
    {"q": "Which blood cells help in clotting?", "options": ["RBC", "WBC", "Platelets", "Plasma"], "answer": "Platelets"},
    {"q": "Which tissue connects muscle to bone?", "options": ["Ligaments", "Tendons", "Cartilage", "Areolar tissue"], "answer": "Tendons"},
    {"q": "Pacemaker of the heart:", "options": ["AV Node", "SA Node", "Purkinje fibres", "Bundle of His"], "answer": "SA Node"},
    {"q": "Organ controlling balance and posture:", "options": ["Cerebrum", "Cerebellum", "Medulla", "Pons"], "answer": "Cerebellum"},
    {"q": "The voice box is known as:", "options": ["Pharynx", "Trachea", "Larynx", "Epiglottis"], "answer": "Larynx"},
    {"q": "Breathing is controlled by:", "options": ["Cerebrum", "Medulla oblongata", "Cerebellum", "Hypothalamus"], "answer": "Medulla oblongata"},
    {"q": "Universal donor blood group:", "options": ["A", "B", "O negative", "AB positive"], "answer": "O negative"},
    {"q": "Which organ secretes insulin?", "options": ["Thyroid", "Pituitary", "Pancreas", "Adrenal"], "answer": "Pancreas"},
    {"q": "Which enzyme is present in saliva?", "options": ["Pepsin", "Trypsin", "Ptyalin", "Lipase"], "answer": "Ptyalin"},
    {"q": "Normal blood pressure is:", "options": ["80/40 mmHg", "100/60 mmHg", "120/80 mmHg", "140/90 mmHg"], "answer": "120/80 mmHg"},
    {"q": "Adam’s Apple becomes prominent due to increased levels of which hormone?", "options": ["Estrogen", "Progesterone", "Testosterone", "Oxytocin"], "answer": "Testosterone"},
]

# -------------------------
# Initialize session-state once per user session
# -------------------------
if "initialized" not in st.session_state:
    # shuffle questions once and store
    shuffled = random.sample(questions, k=len(questions))
    # For each question store a shuffled option order (persisted)
    for i, q in enumerate(shuffled):
        q_copy = q.copy()
        opts = q_copy["options"][:]
        random.shuffle(opts)
        shuffled[i] = {"q": q_copy["q"], "options": opts, "answer": q_copy["answer"]}
    st.session_state["shuffled_questions"] = shuffled
    # initialize answer keys to None so nothing is preselected
    for i in range(len(shuffled)):
        key = f"answer_{i}"
        if key not in st.session_state:
            st.session_state[key] = None
    st.session_state["initialized"] = True

st.title("📘 Stable MCQ Quiz")
st.write("Enter your name and select answers. Nothing will be pre-selected.")

name = st.text_input("Your name", key="student_name")

# Use a form so submit is atomic and we don't re-run while selecting
with st.form("quiz_form"):
    shuffled = st.session_state["shuffled_questions"]
    for i, q in enumerate(shuffled):
        st.write(f"**{i+1}. {q['q']}**")
        # radio uses a stable key so selections persist; index=None ensures no default selection
        st.radio(
            label="",
            options=q["options"],
            key=f"answer_{i}",
            index=None
        )
        st.markdown("---")

    submitted = st.form_submit_button("Submit")

# On submit evaluate answers and optionally save
if submitted:
    if not name:
        st.warning("Please enter your name before submitting.")
    else:
        shuffled = st.session_state["shuffled_questions"]
        total = len(shuffled)
        score = 0
        results = []
        for i, q in enumerate(shuffled):
            user_choice = st.session_state.get(f"answer_{i}")
            correct = q["answer"]
            is_correct = (user_choice == correct)
            if is_correct:
                score += 1
            results.append({
                "Q_no": i+1,
                "Question": q["q"],
                "Selected": user_choice,
                "Correct": correct,
                "Correct?": is_correct
            })

        st.success(f"{name}, your score is **{score} / {total}**")

        # Show per-question feedback
        for r in results:
            if r["Correct?"]:
                st.write(f"✅ Q{r['Q_no']}: Correct — you chose: **{r['Selected']}**")
            else:
                st.write(f"❌ Q{r['Q_no']}: Wrong — you chose: **{r['Selected']}**; Correct: **{r['Correct']}**")

        # Save to CSV
        out_path = Path("quiz_results.csv")
        row = {"Name": name, "Timestamp": datetime.now(), "Score": score, "Total": total}
        # add selected answers Q1..Qn
        for i, r in enumerate(results, 1):
            row[f"Q{i}"] = r["Selected"]
        # append to existing file
        df_row = pd.DataFrame([row])
        if out_path.exists():
            df = pd.read_csv(out_path)
            df = pd.concat([df, df_row], ignore_index=True)
        else:
            df = df_row
        df.to_csv(out_path, index=False)
        st.info(f"Record saved to {out_path.resolve()}")

