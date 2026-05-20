from app.tools.patient_tools import ask_patient
from app.tools.care_tools import recommend_interim_care

def diagnostic_agent(state):

    patient_answers = state.get("patient_answers", [])
    question_count = len(patient_answers)

    # S'il reste des questions
    if question_count < 5:

        question = ask_patient(question_count)

        return {
            "current_question": question,
            "next": "WAIT_PATIENT"
        }

    # Analyse après 5 réponses
    summary = """
    Synthèse clinique préliminaire :
    Symptômes respiratoires simples observés.
    """

    interim = recommend_interim_care()

    return {
        "diagnostic_summary": summary,
        "interim_care": interim
    }