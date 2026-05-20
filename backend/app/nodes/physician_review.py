def physician_review(state):

    print("\n===== REVUE MEDECIN =====")

    print("\nSynthèse clinique :")
    print(state.get("diagnostic_summary"))

    print("\nRecommandation intermédiaire :")
    print(state.get("interim_care"))

    treatment = input("\nTraitement proposé par le médecin : ")

    return {

        "physician_treatment": treatment
    }