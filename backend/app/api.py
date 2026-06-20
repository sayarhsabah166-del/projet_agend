from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sessions = {}

# ===========================
# MODELES
# ===========================

class StartConsultationRequest(BaseModel):
    initial_case: str


class PatientResponseRequest(BaseModel):
    thread_id: str
    answer: str


# ===========================
# QUESTIONS
# ===========================

MEDICAL_QUESTIONS = [
    "Depuis combien de temps ressentez-vous ces symptômes ?",
    "Quelle est l'intensité de vos symptômes sur une échelle de 1 à 10 ?",
    "Avez-vous de la fièvre ? Si oui, quelle température ?",
    "Prenez-vous actuellement des médicaments ?",
    "Avez-vous des antécédents médicaux ?"
]


# ===========================
# START
# ===========================

@app.post("/sessions/start")
async def start_session(request: StartConsultationRequest):

    thread_id = str(uuid.uuid4())

    sessions[thread_id] = {
        "patient_initial_case": request.initial_case,
        "patient_responses": [],
        "question_count": 0,
    }

    return {
        "thread_id": thread_id,
        "status": "question_pending",
        "question": MEDICAL_QUESTIONS[0]
    }


# ===========================
# REPONSES
# ===========================

@app.post("/consultation/respond")
async def respond(request: PatientResponseRequest):
    print("Thread reçu :", request.thread_id)
    print("Sessions :", sessions.keys())
    if request.thread_id not in sessions:
        raise HTTPException(404, "Session introuvable")

    session = sessions[request.thread_id]

    q = session["question_count"]

    session["patient_responses"].append({

        "question": MEDICAL_QUESTIONS[q],

        "answer": request.answer

    })

    session["question_count"] += 1

       # Encore des questions

    if session["question_count"] < len(MEDICAL_QUESTIONS):

        return {
            "status": "question_pending",
            "question": MEDICAL_QUESTIONS[session["question_count"]]
        }

    # ==========================
    # RAPPORT FINAL
    # ==========================

    diagnostic = f"""
Le patient présente :

{session['patient_initial_case']}

Les réponses suggèrent une infection virale bénigne.
"""

    recommandations = """
- Repos
- Hydratation
- Paracétamol si fièvre
- Consulter un médecin si aggravation
"""

    rapport = f"""
==========================
RAPPORT FINAL
==========================

Cas patient :
{session['patient_initial_case']}

QUESTIONS / RÉPONSES
"""

    for rep in session["patient_responses"]:
        rapport += f"""

Question :
{rep['question']}

Réponse :
{rep['answer']}
"""

    rapport += f"""

==========================

SYNTHÈSE

{diagnostic}

==========================

RECOMMANDATIONS

{recommandations}

==========================
"""

    return {
        "status": "completed",
        "final_report": rapport
    }