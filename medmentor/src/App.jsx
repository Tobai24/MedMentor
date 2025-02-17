import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import PracticeMode from "./pages/PracticeMode";
import SelectBodySystem from "./pages/SelectBodySystem";
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
        <Route path="/practice" element={<PracticeMode />} />
        <Route path="/practice/:mode" element={<SelectBodySystem />} />
      </Routes>
    </Router>
  );
}

export default App;
