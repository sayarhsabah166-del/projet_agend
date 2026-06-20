from typing import Literal
from langgraph.graph import StateGraph, END
from ..state import MedicalState

class SupervisorNode:
    """Orchestre le workflow et décide de l'étape suivante"""
    
    @staticmethod
    def should_continue(state: MedicalState) -> Literal["diagnostic_agent", "physician_review", "report_agent", "FINISH"]:
        """Décide quel est le prochain nœud à exécuter"""
        
        # Si erreur, terminer
        if state.get("error"):
            return "FINISH"
        
        # Si pas encore de synthèse diagnostique
        if not state.get("diagnostic_summary"):
            return "diagnostic_agent"
        
        # Si synthèse existe mais pas encore d'avis médecin
        if state.get("diagnostic_summary") and not state.get("physician_treatment"):
            return "physician_review"
        
        # Si avis médecin existe mais pas de rapport final
        if state.get("physician_treatment") and not state.get("final_report"):
            return "report_agent"
        
        # Tout est terminé
        return "FINISH"
    
    @staticmethod
    def route_after_diagnostic(state: MedicalState) -> Literal["physician_review", "diagnostic_agent"]:
        """Route après le diagnostic"""
        if state.get("question_count", 0) >= 5:
            return "physician_review"
        return "diagnostic_agent"