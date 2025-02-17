import { Link } from "react-router-dom";
import { useState } from "react";
import "../index.css";

function PracticeMode() {
  const [selectedMode, setSelectedMode] = useState("");

  const handleModeSelection = (mode) => {
    setSelectedMode(mode);
  };

  return (
    <div className="practice-mode">
      <h1>Choose your practice mode</h1>
      <div className="mode">
        <button onClick={() => handleModeSelection("history")}>
          Practice History
        </button>
        <button onClick={() => handleModeSelection("diagnosis")}>
          Practice Diagnosis
        </button>
      </div>

      {selectedMode && (
        <div className="next-mode">
          <Link to={`/practice/${selectedMode}`}>
            <button>Next</button>
          </Link>
        </div>
      )}
    </div>
  );
}

export default PracticeMode;
