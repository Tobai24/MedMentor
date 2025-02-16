import { useState } from "react";
import { Link } from "react-router-dom";
import "../index.css";

function Scenario() {
  const scenarios = [
    {
      instructions:
        "You are a final-year medical student in an OSCE examination. You are about to see a simulated patient in a clinical station. Read the scenario below carefully before proceeding.",
      stationTitle: "Respiratory OSCE Station - Chronic Cough",
      patient: {
        name: "John Edwards",
        age: 55,
        gender: "Male",
        occupation: "Retired mechanic",
      },
      complaint:
        "I have been having trouble breathing and a cough that won't go away.",
      background: {
        medicalHistory: [
          "Chronic Obstructive Pulmonary Disease (COPD) for 5 years",
          "Hypertension, managed with medication",
        ],
        familyHistory: ["Father had lung cancer", "Mother had heart disease"],
        riskFactors: [
          "Smoker, approximately 20 pack-years",
          "Occasional alcohol consumption",
        ],
      },
      candidateTasks: [
        "Take a focused history from the patient.",
        "Identify three likely differential diagnoses.",
        "List three key investigations you would order.",
        "Explain the most appropriate initial management plan.",
      ],
    },
    {
      instructions:
        "You are a final-year medical student in an OSCE examination. You are about to see a simulated patient in a clinical station. Read the scenario below carefully before proceeding.",
      stationTitle: "Neurology OSCE Station - Altered Mental Status",
      patient: {
        name: "James Carter",
        age: 70,
        gender: "Male",
        occupation: "Retired teacher",
      },
      complaint:
        "I feel confused sometimes, and my daughter says I've been acting differently.",
      background: {
        medicalHistory: [
          "Type 2 Diabetes (10 years)",
          "Mild cognitive impairment",
        ],
        familyHistory: ["Brother had Alzheimer's disease"],
        riskFactors: [
          "High sugar intake",
          "History of poorly controlled diabetes",
        ],
      },
      candidateTasks: [
        "Obtain a structured history from the patient or relative.",
        "State three possible diagnoses.",
        "Mention three bedside tests or investigations you would perform.",
        "Outline a brief management plan.",
      ],
    },
  ];

  const [scenario, setScenario] = useState(
    scenarios[Math.floor(Math.random() * scenarios.length)]
  );

  const [showHistory, setShowHistory] = useState(false);

  return (
    <div className="osce-container">
      <div className="instructions">
        <p>
          <strong>Instructions to Candidate:</strong>
        </p>
        <p>{scenario.instructions}</p>
      </div>

      <div className="station-details">
        <h3> {scenario.stationTitle}</h3>
      </div>

      <div className="scenario-content">
        <h3>👤 Patient Details</h3>
        <ul>
          <li>
            <strong>Name:</strong> {scenario.patient.name}
          </li>
          <li>
            <strong>Age:</strong> {scenario.patient.age}
          </li>
          <li>
            <strong>Gender:</strong> {scenario.patient.gender}
          </li>
          <li>
            <strong>Occupation:</strong> {scenario.patient.occupation}
          </li>
        </ul>

        <h3>🩹 Presenting Complaint</h3>
        <p>💬 "{scenario.complaint}"</p>

        <button
          className="hint-btn"
          onClick={() => setShowHistory(!showHistory)}
        >
          {showHistory ? "Hide History" : "Show Hint 🔍"}
        </button>

        {showHistory && (
          <div className="background-context fade-in">
            <h3>📜 Background Context:</h3>
            <ul>
              <li>
                <strong>Medical History:</strong>
                <ul>
                  {scenario.background.medicalHistory.map((item, index) => (
                    <li key={index}>✅ {item}</li>
                  ))}
                </ul>
              </li>
              <li>
                <strong>Family History:</strong>
                <ul>
                  {scenario.background.familyHistory.map((item, index) => (
                    <li key={index}>👨‍👩‍👦 {item}</li>
                  ))}
                </ul>
              </li>
              <li>
                <strong>Risk Factors:</strong>
                <ul>
                  {scenario.background.riskFactors.map((item, index) => (
                    <li key={index}>⚠️ {item}</li>
                  ))}
                </ul>
              </li>
            </ul>
          </div>
        )}
      </div>

      <div className="tasks">
        <h3>📑 Candidate Tasks:</h3>
        <ul>
          {scenario.candidateTasks.map((task, index) => (
            <li key={index}>📝 {task}</li>
          ))}
        </ul>
      </div>

      <Link to="/app/chatbot">
        <button className="proceed-btn">Proceed to Patient Interaction</button>
      </Link>
    </div>
  );
}

export default Scenario;
