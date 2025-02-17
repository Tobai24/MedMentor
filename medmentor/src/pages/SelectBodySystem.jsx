import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import "../index.css";

function SelectBodySystem() {
  const { mode } = useParams();
  const [selectedSystem, setSelectedSystem] = useState("");
  const [medicalCondition, setMedicalCondition] = useState("");
  const navigate = useNavigate();

  const handleSystemSelection = (system) => {
    setSelectedSystem(system);
  };

  const handleConditionInput = (event) => {
    setMedicalCondition(event.target.value);
  };

  const handleStartSimulation = () => {
    if (!selectedSystem) {
      alert("Please select a body system before starting the simulation.");
      return;
    }
    navigate("/scenario");
  };

  const handleRandomSelection = () => {
    const systems = [
      "Cardiovascular",
      "Respiratory",
      "Neurological",
      "Musculoskeletal",
      "Digestive",
      "Endocrine",
      "Urinary",
      "Reproductive",
      "Integumentary",
      "Immune",
    ];
    const randomSystem = systems[Math.floor(Math.random() * systems.length)];
    setSelectedSystem(randomSystem);
  };

  return (
    <div className="select-body-system">
      {/* <h1>{mode === "history" ? "Practice History" : "Practice Diagnosis"}</h1> */}
      <h2>Please Select a Body System</h2>
      <div className="system">
        {[
          "Cardiovascular",
          "Respiratory",
          "Neurological",
          "Musculoskeletal",
          "Digestive",
          "Endocrine",
          "Urinary",
          "Reproductive",
          "Integumentary",
          "Immune",
        ].map((system) => (
          <div
            key={system}
            className={`system-item ${
              selectedSystem === system ? "selected" : ""
            }`}
            onClick={() => handleSystemSelection(system)}
          >
            {system}
          </div>
        ))}
        <button className="random-system" onClick={handleRandomSelection}>
          Random Body System
        </button>
      </div>

      {mode === "history" && (
        <div>
          <h2>Input Medical Condition (if applicable)</h2>
          <input
            type="text"
            value={medicalCondition}
            onChange={handleConditionInput}
            placeholder="Enter condition"
          />
        </div>
      )}

      <div className="button-group">
        <button disabled={!selectedSystem} onClick={handleStartSimulation}>
          Start Simulation
        </button>
      </div>
    </div>
  );
}

export default SelectBodySystem;
