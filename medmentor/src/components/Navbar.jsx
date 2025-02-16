import { Link } from "react-router-dom";
import "../index.css";

function Navbar() {
  return (
    <nav>
      <ul className="top_nav">
        <li>
          <Link to="/">Home</Link>
        </li>
        <li>
          <Link to="/scenario">Scenario</Link>
        </li>
        <li>
          <Link to="/app/chatbot">Chat</Link>
        </li>
      </ul>
    </nav>
  );
}

export default Navbar;
