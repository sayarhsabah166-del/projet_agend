def supervisor(state):

    # Si pas encore de diagnostic
    if not state.get("clinical_summary"):
        return {"next": "diagnostic_agent"}

    # Si diagnostic existe mais pas revue médecin
    elif not state.get("doctor_review"):
        return {"next": "physician_review"}

    # Si revue médecin existe mais pas rapport final
    elif not state.get("final_report"):
        return {"next": "report_agent"}

    # FIN
    return {"next": "FINISH"}