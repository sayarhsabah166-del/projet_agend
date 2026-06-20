from ..state import MedicalState
from typing import Dict, Any

class PhysicianReviewNode:
    """Nœud pour la revue du médecin (Human-in-the-Loop)"""
    
    @staticmethod
    async def process(state: MedicalState, physician_input: Dict[str, Any] = None) -> MedicalState:
        """
        Traite l'intervention du médecin.
        Si physician_input est None, le workflow est en attente d'intervention.
        """
        
        if physician_input:
            # Le médecin a fourni ses recommandations
            state["physician_treatment"] = physician_input.get("treatment", "")
            state["physician_notes"] = physician_input.get("notes", "")
            
            # Ajouter un message de confirmation
            from langchain_core.messages import AIMessage
            state["messages"].append(
                AIMessage(content=f"Avis médical enregistré: {state['physician_treatment']}")
            )
            
        return state
    
    @staticmethod
    def needs_intervention(state: MedicalState) -> bool:
        """Vérifie si l'intervention du médecin est nécessaire"""
        return not state.get("physician_treatment")