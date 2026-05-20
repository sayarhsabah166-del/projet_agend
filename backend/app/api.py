from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.graph import graph

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------

conversation_state = {
    "patient_case": "",
    "patient_answers": [],
    "question_count": 0
}

# -------------------------

class ConsultationRequest(BaseModel):
    patient_case: str

class AnswerRequest(BaseModel):
    answer: str

# -------------------------

@app.post("/consultation/start")
def start_consultation(data: ConsultationRequest):

    global conversation_state

    conversation_state = {
        "patient_case": data.patient_case,
        "patient_answers": [],
        "question_count": 0
    }

    result = graph.invoke(conversation_state)

    return result

# -------------------------

@app.post("/consultation/answer")
def answer_question(data: AnswerRequest):

    global conversation_state

    question_count = len(conversation_state["patient_answers"])

    questions = [
        "Depuis quand avez-vous les symptômes ?",
        "Avez-vous de la fièvre ?",
        "Avez-vous des douleurs thoraciques ?",
        "Avez-vous des difficultés respiratoires ?",
        "Avez-vous des antécédents médicaux ?"
    ]

    conversation_state["patient_answers"].append({
        "question": questions[question_count],
        "answer": data.answer
    })

    result = graph.invoke(conversation_state)

    conversation_state.update(result)

    return result