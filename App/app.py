import streamlit as st
import pickle
import pandas as pd
import numpy as np
from scipy.stats import norm
import os

@st.cache_data
def load_data():
    data_path = os.path.join("..", "Data", "Dataset_Student_performance.csv")
    return pd.read_csv(data_path)

df = load_data()

action_vars = ["Hours_Studied", "Attendance", "Tutoring_Sessions", "Sleep_Hours", "Physical_Activity"]

def get_reference_stats(df, target, band=5):
    upper = target + band
    mask = (df["Exam_Score"] >= target) & (df["Exam_Score"] < upper)
    ref = df.loc[mask, action_vars]

    if len(ref) < 30:
        mask = (df["Exam_Score"] >= target) & (df["Exam_Score"] < target + 10)
        ref = df.loc[mask, action_vars]

    stats = {
        "n": len(ref),
        "mean": ref.mean(numeric_only=True),
        "median": ref.median(numeric_only=True)
    }
    return stats


model_path = os.path.join("..", "Models", "model.pkl")
rmse_path = os.path.join("..", "Models", "rmse.pkl")

with open(model_path, "rb") as f:
    model = pickle.load(f)

with open(rmse_path, "rb") as f:
    rmse = pickle.load(f)

if "show_results" not in st.session_state:
    st.session_state.show_results = False

def reset_results():
    st.session_state.show_results = False

st.title("Simulateur de performance académique")

st.subheader("Renseignez votre profil")

Hours_Studied = st.slider("Heures d'étude par semaine", 1, 40, 20, on_change=reset_results)
Attendance = st.slider("Taux de présence (%)", 60, 100, 80, on_change=reset_results)
Sleep_Hours = st.slider("Heures de sommeil par nuit", 4, 10, 7, on_change=reset_results)
Previous_Scores = st.slider("Score académique précédent", 50, 100, 75, on_change=reset_results)
Tutoring_Sessions = st.slider("Séances de tutorat par semaine", 0, 8, 1, on_change=reset_results)
Physical_Activity = st.slider("Heures d'activité physique par semaine", 0, 6, 3, on_change=reset_results)

Parental_Involvement = st.selectbox("Implication parentale", ["Low", "Medium", "High"], on_change=reset_results)
Access_to_Resources = st.selectbox("Accès aux ressources", ["Low", "Medium", "High"], on_change=reset_results)
Extracurricular_Activities = st.selectbox("Activités extrascolaires", ["Yes", "No"], on_change=reset_results)
Motivation_Level = st.selectbox("Niveau de motivation", ["Low", "Medium", "High"], on_change=reset_results)
Internet_Access = st.selectbox("Accès à Internet", ["Yes", "No"], on_change=reset_results)
Family_Income = st.selectbox("Revenu familial", ["Low", "Medium", "High"], on_change=reset_results)
Teacher_Quality = st.selectbox("Qualité des enseignants", ["Low", "Medium", "High"], on_change=reset_results)
School_Type = st.selectbox("Type d'école", ["Public", "Private"], on_change=reset_results)
Peer_Influence = st.selectbox("Influence des pairs", ["Negative", "Neutral", "Positive"], on_change=reset_results)
Learning_Disabilities = st.selectbox("Troubles d'apprentissage", ["Yes", "No"], on_change=reset_results)
Parental_Education_Level = st.selectbox("Niveau d'éducation des parents", ["High School", "College", "Postgraduate"], on_change=reset_results)
Distance_from_Home = st.selectbox("Distance domicile-école", ["Near", "Moderate", "Far"], on_change=reset_results)
Gender = st.selectbox("Genre", ["Male", "Female"], on_change=reset_results)

target = st.selectbox("Score visé", [55, 60, 65, 70, 75], on_change=reset_results)

if st.button("Calculer mes chances"):
    st.session_state.show_results = True

if st.session_state.show_results:
    user_input = pd.DataFrame([{
        "Hours_Studied": Hours_Studied,
        "Attendance": Attendance,
        "Parental_Involvement": Parental_Involvement,
        "Access_to_Resources": Access_to_Resources,
        "Extracurricular_Activities": Extracurricular_Activities,
        "Sleep_Hours": Sleep_Hours,
        "Previous_Scores": Previous_Scores,
        "Motivation_Level": Motivation_Level,
        "Internet_Access": Internet_Access,
        "Tutoring_Sessions": Tutoring_Sessions,
        "Family_Income": Family_Income,
        "Teacher_Quality": Teacher_Quality,
        "School_Type": School_Type,
        "Peer_Influence": Peer_Influence,
        "Physical_Activity": Physical_Activity,
        "Learning_Disabilities": Learning_Disabilities,
        "Parental_Education_Level": Parental_Education_Level,
        "Distance_from_Home": Distance_from_Home,
        "Gender": Gender
    }])

    predicted_score = float(model.predict(user_input)[0])

    pred_min = int(np.floor(predicted_score - rmse))
    pred_max = int(np.ceil(predicted_score + rmse))

    proba = 1 - norm.cdf(target, loc=predicted_score, scale=rmse)

    st.subheader("Résultat")
    st.write(f"Score prédit (fourchette) : {pred_min} à {pred_max}")
    st.write(f"Probabilité d'obtenir au moins {target} : {proba*100:.1f}%")

    ref_stats = get_reference_stats(df, target, band=5)
    ref = ref_stats["median"]

    tolerances = {
        "Hours_Studied": 1,
        "Attendance": 2,
        "Tutoring_Sessions": 0,
        "Sleep_Hours": 0.5,
        "Physical_Activity": 1
    }

    user_vals = {
        "Hours_Studied": Hours_Studied,
        "Attendance": Attendance,
        "Tutoring_Sessions": Tutoring_Sessions,
        "Sleep_Hours": Sleep_Hours,
        "Physical_Activity": Physical_Activity
    }

    labels = {
        "Hours_Studied": "Heures d'étude",
        "Attendance": "Présence",
        "Tutoring_Sessions": "Tutorat / semaine",
        "Sleep_Hours": "Sommeil (h/nuit)",
        "Physical_Activity": "Activité physique (h/semaine)"
    }

    tips_improve = []
    tips_strength = []

    for var in action_vars:
        if pd.isna(ref[var]):
            continue

        gap = float(ref[var]) - float(user_vals[var])

        if gap > tolerances[var]:
            target_value = ref[var]
            if var in ["Hours_Studied", "Attendance", "Tutoring_Sessions", "Physical_Activity"]:
                target_value = int(round(target_value))
            else:
                target_value = round(float(target_value), 1)

            tips_improve.append(
                f"{labels[var]} : viser environ {target_value} (vous êtes à {user_vals[var]})."
            )

        if gap < -tolerances[var]:
            ref_value = ref[var]
            if var in ["Hours_Studied", "Attendance", "Tutoring_Sessions", "Physical_Activity"]:
                ref_value = int(round(ref_value))
            else:
                ref_value = round(float(ref_value), 1)

            tips_strength.append(
                f"{labels[var]} : vous êtes au-dessus de la référence ({user_vals[var]} contre {ref_value} pour les élèves ayant atteint votre objectif)."
            )
        
    if Motivation_Level in ["Low", "Medium"]:
        tips_improve.append(
            f"Motivation : vous avez évalué votre motivation à {Motivation_Level}. "
            "Pour augmenter vos chances, travaillez à l'améliorer (objectifs hebdomadaires, planning fixe, sessions courtes et régulières)."
        )

    if tips_strength:
        st.subheader("Points forts (par rapport aux élèves atteignant votre objectif)")
        st.caption(f"Référence calculée sur {ref_stats['n']} élèves avec un score entre {target} et {target+5}.")
        for t in tips_strength[:3]:
            st.write(f"- {t}")

    if tips_improve:
        st.subheader("Axes d'amélioration (par rapport aux élèves atteignant votre objectif)")
        if not tips_strength:
            st.caption(f"Référence calculée sur {ref_stats['n']} élèves avec un score entre {target} et {target+5}.")
        for t in tips_improve[:3]:
            st.write(f"- {t}")


    if predicted_score >= target:
        st.success("Votre objectif semble atteignable avec votre profil actuel.")
    else:
        st.warning("Des ajustements sont nécessaires pour atteindre votre objectif.")
