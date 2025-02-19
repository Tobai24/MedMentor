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
      navigate("/"); // Using navigate instead of window.location for better routing
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
          <h3>Enter Differential Diagnoses</h3>
          <input
            type="text"
            placeholder={
              mode === "history"
                ? "Enter history questions..."
                : "Enter possible diagnoses..."
            }
            value={differentialDiagnosis}
            onChange={(e) => setDifferentialDiagnosis(e.target.value)}
          />
        </div>
      </div>

      <div className="button-group">
        <button onClick={() => navigate("/practice")}>Practice</button>
      </div>
    </div>
  );
}

export default Scenario;
