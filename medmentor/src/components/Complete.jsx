import { useNavigate, useLocation } from "react-router-dom";

function Complete() {
  const navigate = useNavigate();
  const location = useLocation();

  // Retrieve performance data from state (fallback values included)
  const {
    score = 0,
    totalQuestions = 0,
    accuracy = 0,
    timeTaken = "N/A",
  } = location.state || {};

  // Generate feedback based on score
  const getFeedback = () => {
    if (accuracy >= 80) return "Excellent work! 🎉 Keep it up!";
    if (accuracy >= 50) return "Good job! But there's room for improvement.";
    return "Keep practicing! You'll get better. 💪";
  };

  return (
    <div className="complete-page">
      <h1>Session Complete! ✅</h1>
      <h2>Your Performance Summary:</h2>

      <div className="performance-summary">
        <p>
          <strong>Score:</strong> {score} / {totalQuestions}
        </p>
        <p>
          <strong>Accuracy:</strong> {accuracy}%
        </p>
        <p>
          <strong>Time Taken:</strong> {timeTaken} minutes
        </p>
        <p>
          <strong>Feedback:</strong> {getFeedback()}
        </p>
      </div>

      <div className="buttons">
        <button onClick={() => navigate("/")}>Restart</button>
        <button onClick={() => navigate("/report", { state: location.state })}>
          View Report
        </button>
      </div>
    </div>
  );
}

export default Complete;
