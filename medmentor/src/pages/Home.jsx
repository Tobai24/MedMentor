import { Link } from "react-router-dom";
import "../index.css";

function Home() {
  return (
    <div className="home">
      <h1>Welcome to MedMentor</h1>
      <p>Your AI-powered study companion for OSCE exams.</p>
      <Link to="/app">
        <button>Start Practicing</button>
      </Link>
    </div>
  );
}

export default Home;
