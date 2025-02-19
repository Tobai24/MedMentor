import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import axios from "axios";

function SelectBodySystem() {
  const { mode } = useParams(); // Get mode from the URL
  const [medicalQuestion, setMedicalQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (!mode) {
      navigate("/practice");
    }
  }, [mode, navigate]);

  const handleQuestionInput = (e) => {
    setMedicalQuestion(e.target.value);
    setError(null);
  };
  const handleGenerateCase = async () => {
    if (!medicalQuestion.trim()) {
      setError("Please enter a medical question.");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const requestData = { question: medicalQuestion };
      console.log("Sending request:", requestData);

      const response = await axios.post(
        "http://127.0.0.1:8000/generate-case",
        requestData,
        {
          headers: { "Content-Type": "application/json" },
          responseType: "text",
        }
      );

      console.log("Response received:", response.data);

      if (response.data) {
        navigate("/scenario", {
          state: {
            medicalQuestion,
            generatedCase: response.data,
            mode: location.state?.mode,
          },
        });
      } else {
        throw new Error("Invalid response from server");
      }
    } catch (error) {
      console.error("Error:", error);
      setError("Failed to generate case. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="select-body-system p-4 max-w-2xl mx-auto">
      <p className="text-2xl font-bold mb-4">
        {mode === "history" ? "History Taking" : "Diagnosis"} Practice
      </p>

      <input
        type="text"
        value={medicalQuestion}
        onChange={handleQuestionInput}
        placeholder="Enter a medical condition or a body system"
        className="w-full p-2 border rounded mb-4"
      />

      {error && <div className="text-red-500 mb-4">{error}</div>}

      <div className="button-group">
        <button
          onClick={handleGenerateCase}
          disabled={loading}
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:bg-gray-400"
        >
          {loading ? "Generating..." : "Generate Case"}
        </button>
      </div>
    </div>
  );
}

export default SelectBodySystem;
