from langchain.tools import tool
from typing import Dict, List

@tool
def analyze_symptoms(symptoms: Dict) -> Dict:
    """
    Analyse les symptômes pour détecter les red flags.
    """
    red_flags = [
        "difficulté respiratoire", "douleur thoracique",
        "confusion", "fièvre élevée", "perte de conscience"
    ]
    
    detected_red_flags = []
    for red_flag in red_flags:
        if red_flag in str(symptoms).lower():
            detected_red_flags.append(red_flag)
    
    return {
        "severity": "urgent" if detected_red_flags else "normal",
        "red_flags": detected_red_flags,
        "recommendation": "Consultation urgente recommandée" if detected_red_flags else "Suivi standard"
    }

@tool
def format_medical_report(data: Dict) -> str:
    """
    Formate les données médicales en rapport structuré.
    """
    report = f"""
    RAPPORT MEDICAL - ORIENTATION CLINIQUE
    ========================================
    
    Motif de consultation: {data.get('initial_case', 'Non spécifié')}
    
    Analyse clinique préliminaire:
    {data.get('diagnostic_summary', 'Non disponible')}
    
    Recommandation intermédiaire:
    {data.get('interim_care', 'Non disponible')}
    
    Conduite à tenir (avis médical):
    {data.get('physician_treatment', 'Non disponible')}
    
    ---
    Ce système ne remplace pas une consultation médicale.
    En cas d'urgence, contactez les services d'urgence.
    """
    
    return report