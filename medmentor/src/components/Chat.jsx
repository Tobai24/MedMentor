import { useState } from "react";

function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (input.trim() === "") return;

    const userMessage = { role: "user", text: input };
    setMessages([...messages, userMessage]);

    setTimeout(() => {
      const botMessage = {
        role: "bot",
        text: "Doctor, I've been feeling very dizzy and tired lately.",
      };
      setMessages((prev) => [...prev, botMessage]);
    }, 1000);

    setInput("");
  };

  return (
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
  );
}

export default Chat;
