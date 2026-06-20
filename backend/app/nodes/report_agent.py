from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from ..state import MedicalState
from ..prompts.templates import REPORT_SYSTEM_PROMPT, REPORT_USER_PROMPT
from datetime import datetime
import os

class ReportAgentNode:
    """Agent qui génère le rapport final structuré"""
    
    def __init__(self):
        self.llm = ChatOllama(
             model="llama3.2",
             temperature=0.2
          
        )
    
    async def process(self, state: MedicalState) -> MedicalState:
        """Génère le rapport final"""
        
        patient_history = ""
        for i, resp in enumerate(state.get("patient_responses", []), 1):
            patient_history += f"Q{i}: {resp['question']}\nR{i}: {resp['answer']}\n\n"
        
        prompt = REPORT_USER_PROMPT.format(
            initial_case=state["patient_initial_case"],
            diagnostic_summary=state.get("diagnostic_summary", "Non disponible"),
            interim_care=state.get("interim_care", "Non disponible"),
            physician_treatment=state.get("physician_treatment", "Non disponible"),
            date=datetime.now().strftime("%d/%m/%Y à %H:%M"),
            patient_history=patient_history
        )
        
        try:
            response = await self.llm.ainvoke([
                SystemMessage(content=REPORT_SYSTEM_PROMPT),
                HumanMessage(content=prompt)
            ])
            
            state["final_report"] = response.content
            
        except Exception as e:
            state["final_report"] = f"""
            ================================================================================
                                RAPPORT DE CONSULTATION MÉDICALE
                                      ORIENTATION CLINIQUE
            ================================================================================

            1. INFORMATIONS GÉNÉRALES
               Date: {datetime.now().strftime("%d/%m/%Y à %H:%M")}
               Type: Télémédecine - Orientation préliminaire

            2. MOTIF DE LA CONSULTATION
               {state['patient_initial_case']}

            3. ANALYSE CLINIQUE PRÉLIMINAIRE
               {state.get('diagnostic_summary', 'Non disponible')}

            4. RECOMMANDATION INTERMÉDIAIRE
               {state.get('interim_care', 'Non disponible')}

            5. CONDUITE À TENIR (Avis Médical)
               {state.get('physician_treatment', 'Non disponible')}

            ================================================================================
            ⚠️  DISCLAIMER MÉDICAL OBLIGATOIRE ⚠️
            Ce système ne remplace pas une consultation médicale.
            ================================================================================
            """
        
        return state