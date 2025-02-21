import { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import "../index.css";

function Scenario() {
  const location = useLocation();
  const navigate = useNavigate();
  const { medicalQuestion, generatedCase, mode } = location.state || {};

  const [differentialDiagnosis, setDifferentialDiagnosis] = useState("");

  useEffect(() => {
    if (!medicalQuestion || !generatedCase) {
      navigate("/");
    }
  }, [medicalQuestion, generatedCase, navigate]);

  return (
    <div className="osce-container">
      <div className="station-details">
        <h3>
          {medicalQuestion} OSCE Station{" "}
          {/* {mode === "history" ? "History Taking" : "Diagnosis"} */}
        </h3>
      </div>

      <div className="scenario-content">
        <h3>📝 Case Prompt</h3>
        <p>{generatedCase}</p>
        <div className="input-section">
          <h3>Enter Your Initial Diagnosis</h3>
          <p className="text-gray-600">
            Based on the case prompt, enter a diagnosis you think it might be.
            As you gather more information from the patient, you can modify or
            refine your diagnosis.
          </p>
          <input
            type="text"
            placeholder="Enter your initial diagnosis..."
            value={differentialDiagnosis}
            onChange={(e) => setDifferentialDiagnosis(e.target.value)}
          />
        </div>
      </div>

      <div className="button-group">
        <button onClick={() => navigate("/app/chatbot")}>Practice</button>
      </div>
    </div>
  );
}

export default Scenario;
