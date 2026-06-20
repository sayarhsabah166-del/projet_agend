from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from ..state import MedicalState
from ..prompts.templates import (
    DIAGNOSTIC_SYSTEM_PROMPT,  # Changé
    DIAGNOSTIC_USER_PROMPT,     # Changé
    MEDICAL_QUESTIONS,          # Changé
    format_patient_responses
)
import os

class DiagnosticAgentNode:
    """Agent de diagnostic qui pose des questions et génère une synthèse"""
    
    def __init__(self):
        self.llm = ChatOllama(
            
            model="llama3.2",
            temperature=0.3
        )
    
    async def process(self, state: MedicalState) -> MedicalState:
        """Processus principal de l'agent diagnostic"""
        
        if "patient_responses" not in state:
            state["patient_responses"] = []
            state["question_count"] = 0
        
        if state["question_count"] < 5:
            next_question = MEDICAL_QUESTIONS[state["question_count"]]
            state["messages"].append(HumanMessage(content=next_question))
            state["question_count"] += 1
            
        elif state["question_count"] == 5 and not state.get("diagnostic_summary"):
            patient_responses_str = format_patient_responses(state["patient_responses"])
            
            prompt = DIAGNOSTIC_USER_PROMPT.format(
                initial_case=state["patient_initial_case"],
                patient_responses=patient_responses_str
            )
            
            try:
                response = await self.llm.ainvoke([
                    SystemMessage(content=DIAGNOSTIC_SYSTEM_PROMPT),
                    HumanMessage(content=prompt)
                ])
                
                content = response.content
                
                if "SYNTHESE CLINIQUE PRELIMINAIRE:" in content:
                    parts = content.split("RECOMMANDATION INTERMEDIAIRE:")
                    if len(parts) >= 2:
                        state["diagnostic_summary"] = parts[0].replace("SYNTHESE CLINIQUE PRELIMINAIRE:", "").strip()
                        state["interim_care"] = parts[1].split("RED FLAGS IDENTIFIES:")[0].strip()
                    else:
                        state["diagnostic_summary"] = content
                        state["interim_care"] = "Repos et hydratation, consultation si aggravation"
                else:
                    state["diagnostic_summary"] = content
                    state["interim_care"] = "Repos et hydratation, consultation si aggravation"
                    
            except Exception as e:
                state["diagnostic_summary"] = f"Synthèse clinique préliminaire basée sur les informations fournies. {state['patient_initial_case']}"
                state["interim_care"] = "Repos, hydratation, surveillance des symptômes. Consulter un médecin en cas d'aggravation."
        
        return state