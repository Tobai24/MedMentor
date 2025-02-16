import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Scenario from "./components/Scenario";
import Chat from "./components/Chat";
import Navbar from "./components/Navbar";

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/scenario" element={<Scenario />} />
        <Route path="/app/chatbot" element={<Chat />} />
      </Routes>
    </Router>
  );
}

export default App;
