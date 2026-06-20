import { useState } from "react";
import "./App.css";

function App() {

  const [threadId, setThreadId] = useState("");

  const [patientCase, setPatientCase] = useState("");

  const [question, setQuestion] = useState("");

  const [answer, setAnswer] = useState("");

  const [report, setReport] = useState("");

  // ---------------------

  const startConsultation = async () => {

    const response = await fetch(
      "http://localhost:8000/sessions/start",
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

       body: JSON.stringify({
       initial_case: patientCase,
      }) 
      }
    );

    const data = await response.json();

    console.log(data);

    setThreadId(data.thread_id);
    setQuestion(data.question);
  };

  // ---------------------

  const sendAnswer = async () => {

    const response = await fetch(
      "http://localhost:8000/consultation/respond",
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify({
          thread_id: threadId,
          answer: answer,
        }),
      }
    );

    const data = await response.json();
 // 👇 AJOUTE CETTE LIGNE
  console.log("Réponse API :", data);
  setAnswer("");

  // Nouvelle question
if (data.status === "question_pending") {

    setQuestion(data.question);

  }

// Si la consultation est terminee
else if (data.status === "completed") {

    setQuestion("");

    setReport(data.final_report);

    return;
}

// Sinon afficher la question suivante
setQuestion(data.question);
  };

  // ---------------------

  return (

      <div className="container">

      <h1>🏥 Medical Multi-Agent Diagnosis</h1>

      <p className="subtitle">
      Intelligent Clinical Orientation System
      </p>
      {!question && !report && (

        <div>

          <textarea
            rows="5"
            cols="50"
            placeholder="Décrire le cas patient..."
            value={patientCase}
            onChange={(e) => setPatientCase(e.target.value)}
          />

          <br />
          <br />

          <button onClick={startConsultation}>
            Démarrer Consultation
          </button>

        </div>
      )}

      {question && (

        <div className="question-card">

          <h2>Question</h2>

          <p>{question}</p>

          <input
            type="text"
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
          />

          <br />
          <br />

          <button onClick={sendAnswer}>
            Envoyer Réponse
          </button>

        </div>
      )}

      {report && (

        <div className="report">

        <h2>📋 Rapport Final</h2>

          <pre>{report}</pre>

        </div>
      )}

    </div>
  );
}

export default App;
