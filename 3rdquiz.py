import streamlit as st
import random
import pandas as pd
from datetime import datetime
from pathlib import Path

st.set_page_config(page_title="MCQ Quiz", layout="wide")

# -----------------------------------------
# 50 MCQs
# -----------------------------------------
questions = [
    {"q": "Which gas is mainly responsible for the greenhouse effect?",
     "options": ["Carbon dioxide", "Nitrogen", "Oxygen", "Argon"], "answer": 0},
    {"q": "Who appoints the Chief Justice of India?",
     "options": ["President of India", "Prime Minister", "Lok Sabha Speaker", "Chief Justice himself"], "answer": 0},
    {"q": "What is the SI unit of electric current?",
     "options": ["Volt", "Ampere", "Ohm", "Watt"], "answer": 1},
    {"q": "Which is the largest gland in the human body?",
     "options": ["Thyroid", "Pancreas", "Kidney", "Liver"], "answer": 3},
    {"q": "Which metal is extracted from bauxite ore?",
     "options": ["Copper", "Aluminium", "Zinc", "Iron"], "answer": 1},
    {"q": "GDP stands for:",
     "options": ["Gross Domestic Price", "General Domestic Product", "Gross Domestic Product", "Government Development Plan"], "answer": 2},
    {"q": "Which part of the plant performs photosynthesis?",
     "options": ["Leaf", "Root", "Stem", "Flower"], "answer": 0},
    {"q": "Who was the founder of the Mughal Empire?",
     "options": ["Akbar", "Humayun", "Babur", "Aurangzeb"], "answer": 2},
    {"q": "Which river is known as Dakshin Ganga?",
     "options": ["Krishna", "Godavari", "Cauvery", "Narmada"], "answer": 1},
    {"q": "Shortcut key for Undo in MS Word:",
     "options": ["Ctrl + A", "Ctrl + S", "Ctrl + P", "Ctrl + Z"], "answer": 3},
    {"q": "Which component of blood helps in clotting?",
     "options": ["RBC", "WBC", "Platelets", "Plasma"], "answer": 2},
    {"q": "Fundamental Duties are mentioned under:",
     "options": ["Article 21", "Article 19", "Article 35", "Article 51A"], "answer": 3},
    {"q": "Who discovered the cell?",
     "options": ["Darwin", "Robert Hooke", "Schwann", "Watson"], "answer": 1},
    {"q": "Planning Commission was replaced by NITI Aayog in:",
     "options": ["2015", "2010", "2018", "2020"], "answer": 0},
    {"q": "Barometer is used to measure:",
     "options": ["Temperature", "Humidity", "Wind speed", "Atmospheric pressure"], "answer": 3},
    {"q": "Retinol is another name of:",
     "options": ["Vitamin E", "Vitamin B12", "Vitamin A", "Vitamin D"], "answer": 2},
    {"q": "Tropic of Cancer passes through how many Indian states?",
     "options": ["6", "8", "4", "10"], "answer": 1},
    {"q": "Author of Arthashastra:",
     "options": ["Kalidas", "Banabhatta", "Aryabhatta", "Kautilya"], "answer": 3},
    {"q": "Main component of natural gas is:",
     "options": ["Ethane", "Methane", "Carbon monoxide", "Hydrogen"], "answer": 1},
    {"q": "Speed of light in vacuum is:",
     "options": ["3×10^5 m/s", "3×10^6 m/s", "3×10^8 m/s", "3×10^9 m/s"], "answer": 2},
    {"q": "Which organ produces insulin?",
     "options": ["Liver", "Stomach", "Kidney", "Pancreas"], "answer": 3},
    {"q": "Smallest ocean in the world:",
     "options": ["Arctic Ocean", "Indian Ocean", "Pacific Ocean", "Atlantic Ocean"], "answer": 0},
    {"q": "Do or Die slogan was given during:",
     "options": ["Jallianwala Bagh", "Swadeshi Movement", "Quit India Movement", "Non-Cooperation Movement"], "answer": 2},
    {"q": "Agni-V is a:",
     "options": ["Air-to-air missile", "Ballistic missile", "Cruise missile", "Anti-tank missile"], "answer": 1},
    {"q": "Chemical formula of methane:",
     "options": ["CH₄", "C₂H₆", "CO₂", "NH₃"], "answer": 0},
    {"q": "Largest tea-producing state in India:",
     "options": ["Kerala", "Tamil Nadu", "Assam", "Sikkim"], "answer": 2},
    {"q": "Largest bone in the human body:",
     "options": ["Humerus", "Femur", "Tibia", "Fibula"], "answer": 1},
    {"q": "Universal donor blood group:",
     "options": ["A+", "AB+", "O-", "O+"], "answer": 2},
    {"q": "Main source of water cycle energy:",
     "options": ["Moon", "Sun", "Wind", "Earth's gravity"], "answer": 1},
    {"q": "Nobel Prize 2025 in Physics was awarded for:",
     "options": ["Laser fusion", "Dark matter discovery", "Neutrino research", "Quantum materials"], "answer": 3},
    {"q": "Nobel Peace Prize 2025 was awarded to:",
     "options": ["Global Humanitarian Partnership Initiative", "WHO", "UNICEF", "Doctors Without Borders"], "answer": 0},
    {"q": "Nobel Chemistry Prize 2025 recognized work on:",
     "options": ["Battery chemistry", "Advanced CRISPR editing", "Organic catalysts", "Nanotubes"], "answer": 1},
    {"q": "G20 Summit 2025 was hosted by:",
     "options": ["India", "South Africa", "Brazil", "Italy"], "answer": 2},
    {"q": "India's first Green Hydrogen Valley (2025) is in:",
     "options": ["Gujarat", "Tamil Nadu", "Odisha", "Punjab"], "answer": 0},
    {"q": "Which telecom company launched India's first 6G test network?",
     "options": ["Jio", "Airtel", "BSNL", "Vodafone"], "answer": 1},
    {"q": "Wayanad Wildlife Sanctuary is located in:",
     "options": ["Tamil Nadu", "Karnataka", "Assam", "Kerala"], "answer": 3},
    {"q": "5G stands for:",
     "options": ["Fifth Generation", "Fast Global", "Future Graph", "Fiber Guide"], "answer": 0},
    {"q": "State with highest literacy rate in India (2025):",
     "options": ["Goa", "Sikkim", "Telangana", "Kerala"], "answer": 3},
    {"q": "Powerhouse of the cell:",
     "options": ["Nucleus", "Ribosome", "Mitochondria", "Golgi"], "answer": 2},
    {"q": "Father of Indian Constitution:",
     "options": ["Dr. B.R. Ambedkar", "Rajendra Prasad", "Jawaharlal Nehru", "Gandhi"], "answer": 0},
    {"q": "Narmada river originates from:",
     "options": ["Nasik", "Amarkantak", "Mahabaleshwar", "Bhopal"], "answer": 1},
    {"q": "Gas used in LPG:",
     "options": ["Methane", "Ethane", "Hydrogen", "Propane + Butane"], "answer": 3},
    {"q": "Unit of power:",
     "options": ["Watt", "Henry", "Tesla", "Newton"], "answer": 0},
    {"q": "Minimum age for Lok Sabha elections:",
     "options": ["18", "21", "25", "30"], "answer": 2},
    {"q": "Largest freshwater lake in India:",
     "options": ["Chilika", "Wular", "Sambhar", "Pulicat"], "answer": 1},
    {"q": "Disease caused by Plasmodium:",
     "options": ["Malaria", "Dengue", "Typhoid", "AIDS"], "answer": 0},
    {"q": "Metal liquid at room temperature:",
     "options": ["Zinc", "Iron", "Silver", "Mercury"], "answer": 3},
    {"q": "ISRO’s Satish Dhawan Space Centre is located at:",
     "options": ["Thumba", "Sriharikota", "Bhopal", "Chennai"], "answer": 1},
    {"q": "Hardest substance in human body:",
     "options": ["Bone", "Cartilage", "Enamel", "Dentin"], "answer": 2}
]

# -----------------------------------------
# QUIZ LOGIC
# -----------------------------------------
st.title("📝 MCQ Quiz (50 Questions)")

if "responses" not in st.session_state:
    st.session_state.responses = {}

# Show all questions at once
for i, q in enumerate(questions):
    st.subheader(f"Question {i+1}")
    st.session_state.responses[i] = st.radio(
        q["q"],
        q["options"],
        index=None,   # ✅ THIS FIXES THE AUTO-SELECTION ISSUE
        key=f"q_{i}"
    )

# Submit Button
if st.button("Submit Quiz"):
    score = 0
    total = len(questions)
    negative = 0.3

    st.header("📊 Results")

    for i, q in enumerate(questions):
        selected = q["options"].index(st.session_state.responses[i])
        correct = q["answer"]

        if selected == correct:
            score += 1
            st.success(f"Q{i+1}: Correct ✔️ — {q['q']}")
        else:
            score -= negative
            st.error(f"Q{i+1}: Wrong ❌ — {q['q']}\nCorrect Answer: **{q['options'][correct]}**")

    st.subheader(f"🎯 Final Score: {score} / {total}")
