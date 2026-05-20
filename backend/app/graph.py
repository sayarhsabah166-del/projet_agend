from langgraph.graph import StateGraph, END

from app.state import MedicalState

from app.nodes.supervisor import supervisor
from app.nodes.diagnostic_agent import diagnostic_agent
from app.nodes.physician_review import physician_review
from app.nodes.report_agent import report_agent


# Création du workflow
workflow = StateGraph(MedicalState)


# Ajouter les nodes
workflow.add_node("supervisor", supervisor)

workflow.add_node("diagnostic_agent", diagnostic_agent)

workflow.add_node("physician_review", physician_review)

workflow.add_node("report_agent", report_agent)


# Point de départ
workflow.set_entry_point("supervisor")


# Transitions depuis supervisor
workflow.add_conditional_edges(

    "supervisor",

    lambda state: state["next"],

    {

        "diagnostic_agent": "diagnostic_agent",

        "physician_review": "physician_review",

        "report_agent": "report_agent",

        "FINISH": END
    }
)


# Retour au supervisor
workflow.add_edge("diagnostic_agent", "supervisor")

workflow.add_edge("physician_review", "supervisor")

workflow.add_edge("report_agent", "supervisor")


# Compiler le graph
graph = workflow.compile()