import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [timeLeft, setTimeLeft] = useState(null);
  const [selectedTime, setSelectedTime] = useState(0);
  const [diagnosis, setDiagnosis] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    if (timeLeft === 0) {
      navigate("/complete");
    }
    if (timeLeft > 0) {
      const timer = setTimeout(() => setTimeLeft(timeLeft - 1), 1000);
      return () => clearTimeout(timer);
    }
  }, [timeLeft, navigate]);

  const startTimer = () => {
    if (selectedTime > 0) {
      setTimeLeft(selectedTime * 60);
    }
  };

  const sendMessage = async () => {
    if (input.trim() === "") return;

    const userMessage = { role: "user", text: input };
    setMessages([...messages, userMessage]);

    setTimeout(() => {
      const botMessage = {
        role: "bot",
        text: "I've been feeling very dizzy and tired lately.",
      };
      setMessages((prev) => [...prev, botMessage]);
    }, 1000);

    setInput("");
  };

  return (
    <div>
      <div className="timer">
        {timeLeft !== null ? (
          <h2>
            Time Left: {Math.floor(timeLeft / 60)}:
            {String(timeLeft % 60).padStart(2, "0")}
          </h2>
        ) : (
          <h2>Select Time to Start</h2>
        )}
      </div>
      <div className="main-container">
        <div className="diagnosis-section">
          <h3>
            Your Differential Diagnosis: Update your DDx throughout the case
          </h3>
          <input
            type="text"
            value={diagnosis}
            onChange={(e) => setDiagnosis(e.target.value)}
            placeholder="Update DDX..."
          />
        </div>

        <div className="time-selection">
          <select
            onChange={(e) => setSelectedTime(Number(e.target.value))}
            value={selectedTime}
          >
            <option value="0">Select time (minutes)</option>
            <option value="1">1 min</option>
            <option value="3">3 min</option>
            <option value="5">5 min</option>
            <option value="8">8 min</option>
          </select>
          <button onClick={startTimer}>Start Timer</button>
        </div>

        <div className="chat-container">
          <div className="chat-box">
            {messages.map((msg, index) => (
              <div key={index} className={`chat-message ${msg.role}`}>
                {msg.text}
              </div>
            ))}
          </div>

          <div className="chat-input">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask a question..."
            />
            <button onClick={sendMessage}>Send</button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Chat;
