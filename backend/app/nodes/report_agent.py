def report_agent(state):

    report = f"""
==============================
RAPPORT FINAL
==============================

Cas patient :
{state.get("patient_case")}

Questions / Réponses :
{state.get("patient_answers")}

Synthèse clinique :
{state.get("diagnostic_summary")}

Recommandation intermédiaire :
{state.get("interim_care")}

Avis du médecin :
{state.get("physician_treatment")}

IMPORTANT :
Ce système ne remplace pas une consultation médicale.
"""

    return {

        "final_report": report
    }