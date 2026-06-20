from typing import Annotated, Literal, Optional, List
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field

class PatientQuestion(BaseModel):
    question: str
    answer: Optional[str] = None
    order: int

class MedicalState(TypedDict, total=False):
    # Messages pour la communication
    messages: Annotated[list, add_messages]
    
    # État du workflow
    next: Literal[
        "diagnostic_agent",
        "physician_review",
        "report_agent",
        "FINISH"
    ]
    
    # Données patient
    patient_initial_case: str
    patient_responses: List[dict]
    question_count: int
    
    # Résultats cliniques
    diagnostic_summary: str
    interim_care: str
    physician_treatment: str
    physician_notes: str
    final_report: str
    
    # Métadonnées
    thread_id: str
    error: Optional[str]

class ConsultationResponse(BaseModel):
    thread_id: str
    status: str
    current_step: str
    data: dict

class FinalReport(BaseModel):
    thread_id: str
    patient_initial_case: str
    patient_responses: List[dict]
    diagnostic_summary: str
    interim_care: str
    physician_treatment: str
    final_report: str
    disclaimer: str = "Ce système ne remplace pas une consultation médicale."