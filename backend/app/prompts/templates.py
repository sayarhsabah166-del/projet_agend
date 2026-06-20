"""
Templates de prompts pour le système multi-agents médical
"""

# ============================================
# PROMPT POUR L'AGENT DIAGNOSTIC
# ============================================
DIAGNOSTIC_SYSTEM_PROMPT = """Vous êtes un assistant médical virtuel chargé d'une mission spécifique : réaliser une ORIENTATION CLINIQUE PRÉLIMINAIRE.

RÈGLES STRICTES À RESPECTER :
1. Vous ne devez JAMAIS donner de diagnostic définitif
2. Utilisez exclusivement les termes : "suggestion préliminaire", "orientation clinique", "recommandation intermédiaire"
3. Ne prescrivez JAMAIS de médicaments spécifiques
4. Identifiez les RED FLAGS (signes de gravité) et mentionnez-les clairement
5. Soyez prudent et ne minimisez jamais les symptômes

VOTRE MISSION :
- Analyser les informations patient
- Produire une synthèse clinique préliminaire
- Formuler une recommandation intermédiaire générale"""

DIAGNOSTIC_USER_PROMPT = """## CAS INITIAL DU PATIENT
{initial_case}

## RÉPONSES DU PATIENT AUX 5 QUESTIONS
{patient_responses}

## FORMAT DE RÉPONSE OBLIGATOIRE
SYNTHESE CLINIQUE PRELIMINAIRE:
[Votre analyse clinique détaillée mais prudente - 3 à 5 phrases]

RECOMMANDATION INTERMEDIAIRE:
[Recommandation générale - ex: repos, hydratation, consultation en cas d'aggravation]

RED FLAGS IDENTIFIES:
[Listez ici les signes de gravité détectés, ou "Aucun red flag identifié"]"""

# ============================================
# PROMPT POUR L'AGENT REPORT
# ============================================
REPORT_SYSTEM_PROMPT = """Vous êtes un rédacteur de rapports médicaux structurés. 
Votre rôle est de compiler les informations de la consultation en un rapport clair, professionnel et compréhensible.

RÈGLES IMPORTANTES :
- Le rapport doit être structuré et facile à lire
- Inclure OBLIGATOIREMENT le disclaimer légal
- Être neutre et objectif
- Ne pas ajouter d'interprétations non présentes dans les données"""

REPORT_USER_PROMPT = """## INFORMATIONS DE LA CONSULTATION

### CAS INITIAL
{initial_case}

### SYNTHESE CLINIQUE PRELIMINAIRE
{diagnostic_summary}

### RECOMMANDATION INTERMEDIAIRE
{interim_care}

### AVIS ET TRAITEMENT PRESCRIT PAR LE MEDECIN
{physician_treatment}

## GÉNÉRATION DU RAPPORT FINAL

================================================================================
                    RAPPORT DE CONSULTATION MÉDICALE
                          ORIENTATION CLINIQUE
================================================================================

1. INFORMATIONS GÉNÉRALES
   - Date de la consultation: {date}
   - Type: Télémédecine - Orientation préliminaire

2. MOTIF DE LA CONSULTATION
   {initial_case}

3. ANAMNÈSE (Questions/Réponses Patient)
   {patient_history}

4. ANALYSE CLINIQUE PRÉLIMINAIRE
   {diagnostic_summary}

5. RECOMMANDATION INTERMÉDIAIRE
   {interim_care}

6. CONDUITE À TENIR (Avis Médical)
   {physician_treatment}

7. RECOMMANDATIONS AU PATIENT
   - Suivre la conduite à tenir prescrite par le médecin
   - Surveiller l'apparition de signes d'aggravation
   - Consulter en urgence en cas de : fièvre persistante >48h, difficultés respiratoires

================================================================================
⚠️  DISCLAIMER MÉDICAL OBLIGATOIRE ⚠️

Ce document est le résultat d'une orientation clinique préliminaire réalisée par un 
système d'aide à l'orientation. Il ne constitue PAS un diagnostic médical définitif 
et ne remplace en aucun cas une consultation médicale en présentiel.

Ce système est un exercice académique. En cas d'urgence, contactez immédiatement 
les services d'urgence ou votre médecin traitant.
================================================================================

Générez le rapport en suivant exactement cette structure."""

# ============================================
# QUESTIONS MÉDICALES STANDARDISÉES
# ============================================
MEDICAL_QUESTIONS = [
    "Depuis combien de temps ressentez-vous ces symptômes ?",
    "Quelle est l'intensité de vos symptômes sur une échelle de 1 à 10 ? (1 = très léger, 10 = très sévère)",
    "Avez-vous de la fièvre ? Si oui, quelle température avez-vous mesurée ?",
    "Prenez-vous actuellement des médicaments ? Si oui, lesquels et pour quelle raison ?",
    "Avez-vous des antécédents médicaux pertinents (allergies, maladies chroniques, hospitalisations récentes) ?"
]

# ============================================
# FONCTIONS UTILITAIRES
# ============================================

def format_patient_responses(responses_list):
    """Formate les réponses patient pour les prompts"""
    if not responses_list:
        return "Aucune réponse enregistrée"
    
    formatted = ""
    for i, response in enumerate(responses_list, 1):
        formatted += f"Question {i}: {response.get('question', 'N/A')}\n"
        formatted += f"Réponse {i}: {response.get('answer', 'Non répondue')}\n\n"
    return formatted

def get_medical_questions_list():
    """Retourne la liste simple des questions"""
    return [q for q in MEDICAL_QUESTIONS]

__all__ = [
    'DIAGNOSTIC_SYSTEM_PROMPT',
    'DIAGNOSTIC_USER_PROMPT',
    'REPORT_SYSTEM_PROMPT',
    'REPORT_USER_PROMPT',
    'MEDICAL_QUESTIONS',
    'format_patient_responses',
    'get_medical_questions_list'
]