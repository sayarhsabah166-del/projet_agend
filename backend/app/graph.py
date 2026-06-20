from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver  # Changement ici
from .state import MedicalState
from .nodes.supervisor import SupervisorNode
from .nodes.diagnostic_agent import DiagnosticAgentNode
from .nodes.physician_review import PhysicianReviewNode
from .nodes.report_agent import ReportAgentNode
from typing import Literal

class MedicalGraph:
    """Workflow principal du système médical"""
    
    def __init__(self):
        self.supervisor = SupervisorNode()
        self.diagnostic_agent = DiagnosticAgentNode()
        self.physician_review = PhysicianReviewNode()
        self.report_agent = ReportAgentNode()
        
        # Créer le graphe
        self.workflow = StateGraph(MedicalState)
        
        # Ajouter les nœuds
        self.workflow.add_node("supervisor", self.supervisor_route)
        self.workflow.add_node("diagnostic_agent", self.diagnostic_agent.process)
        self.workflow.add_node("physician_review", self.physician_review.process)
        self.workflow.add_node("report_agent", self.report_agent.process)
        
        # Définir le point d'entrée
        self.workflow.set_entry_point("supervisor")
        
        # Ajouter les edges conditionnels
        self.workflow.add_conditional_edges(
            "supervisor",
            self.supervisor.should_continue,
            {
                "diagnostic_agent": "diagnostic_agent",
                "physician_review": "physician_review",
                "report_agent": "report_agent",
                "FINISH": END
            }
        )
        
        # Retour du diagnostic_agent vers supervisor
        self.workflow.add_edge("diagnostic_agent", "supervisor")
        
        # Retour du physician_review vers supervisor
        self.workflow.add_edge("physician_review", "supervisor")
        
        # Retour du report_agent vers supervisor
        self.workflow.add_edge("report_agent", "supervisor")
        
        # Compiler le graphe avec mémoire
        self.memory = MemorySaver()
        self.app = self.workflow.compile(checkpointer=self.memory)
    
    async def supervisor_route(self, state: MedicalState) -> MedicalState:
        """Nœud supervisor pour le routage"""
        return state
    
    def get_graph(self):
        """Retourne le graphe pour LangGraph Studio"""
        return self.app