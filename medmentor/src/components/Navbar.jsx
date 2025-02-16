import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav>
      <ul className="top_nav">
        <li>
          <Link to="/">Home</Link>
        </li>
        <li>
          <Link to="/app">Practice</Link>
        </li>
      </ul>
    </nav>
  );
}

export default Navbar;
