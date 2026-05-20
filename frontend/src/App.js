import { useState } from "react";

function App() {

  const [patientCase, setPatientCase] = useState("");

  const [question, setQuestion] = useState("");

  const [answer, setAnswer] = useState("");

  const [report, setReport] = useState("");

  // ---------------------

  const startConsultation = async () => {

    const response = await fetch(
      "http://localhost:8000/consultation/start",
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify({
          patient_case: patientCase,
        }),
      }
    );

    const data = await response.json();

    setQuestion(data.current_question);
  };

  // ---------------------

  const sendAnswer = async () => {

    const response = await fetch(
      "http://localhost:8000/consultation/answer",
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify({
          answer: answer,
        }),
      }
    );

    const data = await response.json();

    setAnswer("");

    // Nouvelle question
    if (data.current_question) {

      setQuestion(data.current_question);

    } else {

      setQuestion("");

      setReport(`
${data.diagnostic_summary}

${data.interim_care}
      `);
    }
  };

  // ---------------------

  return (

    <div style={{ padding: "40px" }}>

      <h1>Système Médical Multi-Agents</h1>

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

        <div>

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

        <div>

          <h2>Synthèse Clinique</h2>

          <pre>{report}</pre>

        </div>
      )}

    </div>
  );
}

export default App;
