import streamlit as st
import random
import pandas as pd
from datetime import datetime
from pathlib import Path

st.set_page_config(page_title="MCQ Quiz", layout="wide")

# -----------------------------------------
# 30 MCQs on Constitution Articles (SSC JE Level)
# -----------------------------------------
questions = [
    {"q": "Article 12 defines:",
     "options": ["State", "Citizenship", "Equality", "Rights"], "answer": 0},

    {"q": "Article 14 deals with:",
     "options": ["Freedom of speech", "Equality before law", "Right to life", "Right to property"], "answer": 1},

    {"q": "Article 15 prohibits discrimination on basis of:",
     "options": ["Religion, race, caste, sex, place of birth", "Education", "Wealth", "Occupation"], "answer": 0},

    {"q": "Article 16 provides:",
     "options": ["Equality in education", "Equality of opportunity in public employment", "Right to vote", "Freedom of trade"], "answer": 1},

    {"q": "Article 17 abolishes:",
     "options": ["Slavery", "Untouchability", "Child labour", "Sati"], "answer": 1},

    {"q": "Article 19 guarantees:",
     "options": ["6 freedoms", "Voting rights", "Religious rights", "Emergency powers"], "answer": 0},

    {"q": "Article 21 is related to:",
     "options": ["Right to property", "Right to life and personal liberty", "Right to education", "Right to religion"], "answer": 1},

    {"q": "Article 21A deals with:",
     "options": ["Right to vote", "Right to education", "Right to information", "Right against exploitation"], "answer": 1},

    {"q": "Article 22 provides protection against:",
     "options": ["Taxation", "Arrest and detention", "Property loss", "Unemployment"], "answer": 1},

    {"q": "Article 23 prohibits:",
     "options": ["Untouchability", "Traffic in human beings & forced labour", "Child marriage", "Bonded labour only"], "answer": 1},

    {"q": "Article 24 prohibits:",
     "options": ["Child marriage", "Employment of children in factories", "Forced labour", "Human trafficking"], "answer": 1},

    {"q": "Article 25 guarantees:",
     "options": ["Freedom of speech", "Freedom of religion", "Right to vote", "Right to equality"], "answer": 1},

    {"q": "Article 29 protects:",
     "options": ["Workers", "Minority interests", "Senior citizens", "Women"], "answer": 1},

    {"q": "Article 30 gives minorities the right to:",
     "options": ["Form government", "Establish and administer educational institutions", "Get reservations", "Form political parties"], "answer": 1},

    {"q": "Article 32 is known as:",
     "options": ["Right to equality", "Heart and soul of the Constitution", "Directive principles", "Emergency article"], "answer": 1},

    {"q": "Article 44 deals with:",
     "options": ["Uniform Civil Code", "Right to property", "Election Commission", "Finance Commission"], "answer": 0},

    {"q": "Article 51A contains:",
     "options": ["Fundamental Duties", "Directive Principles", "Preamble", "Schedules"], "answer": 0},

    {"q": "Article 72 grants power to the President to:",
     "options": ["Suspend Constitution", "Grant pardons", "Dismiss PM", "Dissolve Lok Sabha"], "answer": 1},

    {"q": "Article 74 deals with:",
     "options": ["President’s impeachment", "Council of Ministers to aid the President", "Judiciary", "Election Commission"], "answer": 1},

    {"q": "Article 76 establishes the office of:",
     "options": ["CJI", "CAG", "Attorney General", "Advocate General"], "answer": 2},

    {"q": "Article 110 defines:",
     "options": ["Money Bill", "Finance Bill", "Budget", "Tax'], "answer": 0},

    {"q": "Article 112 deals with:",
     "options": ["Budget", "Money Bill", "Finance Commission", "UPSC"], "answer": 0},

    {"q": "Article 123 empowers the President to issue:",
     "options": ["Pardons", "Ordinances", "Warrants", "Bills"], "answer": 1},

    {"q": "Article 148 relates to:",
     "options": ["CJI", "CAG", "CM", "AG"], "answer": 1},

    {"q": "Article 155 deals with appointment of:",
     "options": ["CJI", "Governor", "President", "PM"], "answer": 1},

    {"q": "Article 168 deals with:",
     "options": ["Lok Sabha", "Rajya Sabha", "State Legislatures", "Panchayats"], "answer": 2},

    {"q": "Article 213 gives power to Governors to issue:",
     "options": ["Pardons", "Ordinances", "Orders", "Judgements"], "answer": 1},

    {"q": "Article 226 empowers High Courts to issue:",
     "options": ["Bills", "Writs", "Ordinances", "Judgements"], "answer": 1},

    {"q": "Article 280 establishes the:",
     "options": ["Election Commission", "Finance Commission", "UPSC", "NITI Aayog"], "answer": 1},

    {"q": "Article 300A guarantees:",
     "options": ["Right to vote", "Right to life", "Right to property", "Right to equality"], "answer": 2}
]

# -----------------------------------------
# QUIZ LOGIC
# -----------------------------------------
st.title("📝 MCQ Quiz (30 Questions)")

if "responses" not in st.session_state:
    st.session_state.responses = {}

# Show all questions at once
for i, q in enumerate(questions):
    st.subheader(f"Question {i+1}")
    st.session_state.responses[i] = st.radio(
        q["q"],
        q["options"],
        index=None,
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
