from langchain.tools import tool
from typing import Dict, List
import json

@tool
def ask_patient_question(question: str, question_number: int) -> Dict:
    """
    Pose une question au patient et attend sa réponse.
    Cet outil est utilisé pour collecter les informations du patient.
    """
    return {
        "question": question,
        "question_number": question_number,
        "status": "waiting_for_response"
    }

@tool
def record_patient_response(question: str, answer: str, question_number: int) -> Dict:
    """
    Enregistre la réponse du patient.
    """
    return {
        "question": question,
        "answer": answer,
        "question_number": question_number,
        "recorded": True
    }

@tool
def generate_interim_care(symptoms_summary: str) -> str:
    """
    Génère une recommandation intermédiaire basée sur les symptômes.
    """
    recommendations = {
        "respiratory": "Repos, hydratation abondante, surveillance de la température. Consultez si aggravation ou difficultés respiratoires.",
        "digestive": "Hydratation, alimentation légère, repos digestif. Consultez si vomissements répétés ou déshydratation.",
        "generic": "Repos, hydratation, surveillance des symptômes. Consultez un médecin si les symptômes persistent ou s'aggravent."
    }
    
    for key, rec in recommendations.items():
        if key in symptoms_summary.lower():
            return rec
    
    return recommendations["generic"]