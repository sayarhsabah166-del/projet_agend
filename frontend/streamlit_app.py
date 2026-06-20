import streamlit as st
import requests
import json
from datetime import datetime
import time

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Système d'Orientation Clinique",
    page_icon="🏥",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1.5rem;
    border-radius: 15px;
    margin-bottom: 2rem;
    text-align: center;
}
.main-header h1 {
    color: white;
    margin: 0;
    font-size: 2rem;
}
.main-header p {
    color: rgba(255,255,255,0.9);
    margin: 0.5rem 0 0 0;
}
.disclaimer {
    background-color: #fff3cd;
    border-left: 4px solid #ffc107;
    padding: 1rem;
    margin: 1rem 0;
    border-radius: 10px;
    font-size: 0.9rem;
}
.report-box {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    padding: 1.5rem;
    border-radius: 15px;
    border: 1px solid #dee2e6;
    font-family: 'Courier New', monospace;
    font-size: 0.9rem;
    white-space: pre-wrap;
}
.question-box {
    background-color: #e3f2fd;
    padding: 1rem;
    border-radius: 10px;
    border-left: 4px solid #2196f3;
    margin: 1rem 0;
}
.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    padding: 0.5rem 2rem;
    font-weight: bold;
}
.stButton > button:hover {
    transform: translateY(-2px);
    transition: 0.3s;
}
</style>
""", unsafe_allow_html=True)

# ============================================
# INITIALISATION DES SESSIONS
# ============================================
if "step" not in st.session_state:
    st.session_state.step = "start"
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None
if "question_index" not in st.session_state:
    st.session_state.question_index = 0
if "initial_case" not in st.session_state:
    st.session_state.initial_case = ""
if "patient_responses" not in st.session_state:
    st.session_state.patient_responses = []

# ============================================
# HEADER
# ============================================
st.markdown("""
<div class="main-header">
    <h1>🏥 Système d'Orientation Clinique</h1>
    <p>Assistant médical multi-agents basé sur LangGraph</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="disclaimer">
⚠️ <strong>Disclaimer Médical</strong><br>
Ce système est un <strong>exercice académique</strong> et ne remplace pas une consultation médicale. 
Les informations fournies sont des <strong>suggestions préliminaires</strong>. 
En cas d'urgence, contactez immédiatement les services d'urgence (15/112) ou votre médecin traitant.
</div>
""", unsafe_allow_html=True)

# ============================================
# LISTE DES QUESTIONS
# ============================================
QUESTIONS = [
    "Depuis combien de temps ressentez-vous ces symptômes ?",
    "Quelle est l'intensité de vos symptômes sur une échelle de 1 à 10 ?",
    "Avez-vous de la fièvre ? Si oui, quelle température ?",
    "Prenez-vous actuellement des médicaments ?",
    "Avez-vous des antécédents médicaux pertinents ?"
]

# ============================================
# ÉCRAN 1: DÉMARRAGE
# ============================================
if st.session_state.step == "start":
    st.header("📋 Nouvelle Consultation")
    
    st.markdown("""
    <div style="background-color: #e8f5e9; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
    <strong>📝 Instructions:</strong><br>
    Décrivez les symptômes du patient de manière détaillée.
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("initial_case_form"):
        initial_case = st.text_area(
            "📝 Décrivez les symptômes du patient:",
            placeholder="Exemple: Patient de 35 ans, fièvre 38.5°C, toux sèche, fatigue intense, courbatures",
            height=150
        )
        
        submitted = st.form_submit_button("🚀 Démarrer la Consultation")
        
        if submitted and initial_case:
            with st.spinner("Initialisation de la consultation..."):
                try:
                    response = requests.post(
                        f"{API_URL}/sessions/start",
                        json={"initial_case": initial_case},
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.thread_id = data["thread_id"]
                        st.session_state.initial_case = initial_case
                        st.session_state.step = "questions"
                        st.session_state.question_index = 0
                        st.session_state.patient_responses = []
                        st.success("Consultation démarrée avec succès!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(f"Erreur {response.status_code}: Impossible de démarrer la consultation")
                except requests.exceptions.ConnectionError:
                    st.error("❌ Impossible de se connecter au serveur backend. Vérifiez que le serveur FastAPI est démarré sur http://localhost:8000")
                except Exception as e:
                    st.error(f"❌ Erreur: {str(e)}")
        elif submitted and not initial_case:
            st.warning("Veuillez décrire les symptômes du patient")

# ============================================
# ÉCRAN 2: QUESTIONS/RÉPONSES PATIENT
# ============================================
elif st.session_state.step == "questions":
    st.header("💬 Questionnaire Patient")
    
    current_q = st.session_state.question_index
    
    # Barre de progression
    progress = current_q / 5
    st.progress(progress)
    st.write(f"Progression: {current_q}/5 questions")
    
    # Afficher l'historique
    with st.expander("📜 Historique des questions/réponses", expanded=False):
        if st.session_state.patient_responses:
            for i, resp in enumerate(st.session_state.patient_responses, 1):
                st.markdown(f"**Q{i}:** {resp['question']}")
                st.markdown(f"**R{i}:** {resp['answer']}")
                st.divider()
        else:
            st.info("Aucune réponse enregistrée pour le moment")
    
    # Afficher la question en cours
    if current_q < 5:
        st.markdown(f"""
        <div class="question-box">
            <strong>❓ Question {current_q + 1}/5:</strong><br>
            {QUESTIONS[current_q]}
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("answer_form"):
            answer = st.text_area(
                "✏️ Votre réponse:", 
                placeholder="Saisissez votre réponse ici...",
                height=100
            )
            
            submitted = st.form_submit_button("📤 Envoyer la réponse")
            
            if submitted and answer:
                with st.spinner("Traitement de votre réponse..."):
                    try:
                        # Enregistrer la réponse localement
                        st.session_state.patient_responses.append({
                            "question": QUESTIONS[current_q],
                            "answer": answer
                        })
                        
                        # Envoyer au backend
                        response = requests.post(
                            f"{API_URL}/consultation/respond",
                            json={
                                "thread_id": st.session_state.thread_id,
                                "answer": answer
                            },
                            timeout=30
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            st.session_state.question_index += 1
                            
                            # Vérifier si toutes les questions sont répondues
                            if st.session_state.question_index >= 5:
                                st.session_state.step = "physician"
                                st.success("✅ Questionnaire terminé! Passage à l'avis médical...")
                                st.balloons()
                                time.sleep(2)
                                st.rerun()
                            else:
                                st.success("Réponse enregistrée!")
                                time.sleep(1)
                                st.rerun()
                        else:
                            st.error(f"Erreur {response.status_code}: {response.text}")
                    except Exception as e:
                        st.error(f"❌ Erreur: {str(e)}")
            elif submitted and not answer:
                st.warning("Veuillez saisir une réponse")

# ============================================
# ÉCRAN 3: REVUE MÉDECIN (HUMAN-IN-THE-LOOP)
# ============================================
elif st.session_state.step == "physician":
    st.header("👨‍⚕️ Revue Médicale - Intervention Humaine")
    
    st.info("""
    🔍 **Rôle du médecin traitant:**\n
    En tant que médecin, vous devez analyser la synthèse clinique préliminaire et 
    proposer une conduite à tenir appropriée.
    """)
    
    # Récupérer les données du diagnostic
    try:
        report_response = requests.get(
            f"{API_URL}/consultation/{st.session_state.thread_id}/report",
            timeout=10
        )
        
        if report_response.status_code == 200:
            report_data = report_response.json()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 Synthèse Clinique Préliminaire")
                summary = report_data.get("diagnostic_summary", "Génération en cours...")
                st.markdown(f'<div class="report-box">{summary}</div>', unsafe_allow_html=True)
            
            with col2:
                st.subheader("💊 Recommandation Intermédiaire")
                care = report_data.get("interim_care", "Génération en cours...")
                st.markdown(f'<div class="report-box">{care}</div>', unsafe_allow_html=True)
            
            st.divider()
            
            # Afficher les réponses patient
            with st.expander("📋 Détail des réponses patient", expanded=False):
                patient_responses = report_data.get("patient_responses", [])
                if patient_responses:
                    for i, resp in enumerate(patient_responses, 1):
                        st.markdown(f"**Q{i}:** {resp.get('question', 'N/A')}")
                        st.markdown(f"**R{i}:** {resp.get('answer', 'N/A')}")
                        st.divider()
                else:
                    st.info("Aucune réponse enregistrée")
            
            # Formulaire pour l'avis médical
            st.subheader("📝 Avis et Prescription du Médecin")
            
            with st.form("physician_form"):
                treatment = st.text_area(
                    "💊 Conduite à tenir / Traitement proposé:",
                    placeholder="Exemple: \n- Repos strict pendant 48h\n- Paracétamol 500mg si fièvre >38.5°C (max 3g/jour)\n- Hydratation abondante (1.5L-2L/jour)\n- Consultation médicale si persistance des symptômes >48h\n- Appeler le 15 en cas de difficultés respiratoires",
                    height=150
                )
                
                notes = st.text_area(
                    "📝 Notes supplémentaires (optionnel):",
                    placeholder="Observations complémentaires, recommandations spécifiques...",
                    height=100
                )
                
                submitted = st.form_submit_button("✅ Valider l'avis médical")
                
                if submitted and treatment:
                    with st.spinner("Enregistrement de l'avis médical et génération du rapport final..."):
                        try:
                            response = requests.post(
                                f"{API_URL}/consultation/physician-review",
                                json={
                                    "thread_id": st.session_state.thread_id,
                                    "treatment": treatment,
                                    "notes": notes
                                },
                                timeout=30
                            )
                            
                            if response.status_code == 200:
                                st.success("✅ Avis médical enregistré avec succès!")
                                st.session_state.step = "report"
                                time.sleep(2)
                                st.rerun()
                            else:
                                st.error(f"Erreur {response.status_code}: {response.text}")
                        except Exception as e:
                            st.error(f"❌ Erreur: {str(e)}")
                elif submitted and not treatment:
                    st.warning("Veuillez saisir une conduite à tenir")
    except Exception as e:
        st.error(f"❌ Erreur lors de la récupération des données: {str(e)}")

# ============================================
# ÉCRAN 4: RAPPORT FINAL
# ============================================
elif st.session_state.step == "report":
    st.header("📄 Rapport Médical Final")
    
    try:
        response = requests.get(
            f"{API_URL}/consultation/{st.session_state.thread_id}/report",
            timeout=10
        )
        
        if response.status_code == 200:
            report_data = response.json()
            
            # Afficher le rapport
            final_report = report_data.get("final_report", "Génération du rapport...")
            st.markdown(f'<div class="report-box">{final_report}</div>', unsafe_allow_html=True)
            
            st.divider()
            
            # Boutons d'action
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🆕 Nouvelle Consultation"):
                    # Réinitialiser tout
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]
                    time.sleep(1)
                    st.rerun()
            
            with col2:
                # Télécharger le rapport
                report_json = json.dumps(report_data, indent=2, default=str, ensure_ascii=False)
                st.download_button(
                    label="📥 Télécharger (JSON)",
                    data=report_json,
                    file_name=f"rapport_{st.session_state.thread_id}.json",
                    mime="application/json"
                )
        else:
            st.error("Impossible de récupérer le rapport final")
    except Exception as e:
        st.error(f"❌ Erreur: {str(e)}")

# ============================================
# PIED DE PAGE
# ============================================
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray; font-size: 0.8rem;'>"
    "© 2024 - Système Multi-Agents Médical | Projet Académique | LangGraph + FastAPI + MCP"
    "</p>",
    unsafe_allow_html=True
)