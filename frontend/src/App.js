import { useState } from 'react';

function App() {
  const [messages, setMessages] = useState([
    { text: "Hey Bestie 💖", sender: "bot" },
  ]);
  const [input, setInput] = useState('');

  const handleSend = async () => {
    if (!input.trim()) return;

    // Append user message
    const newMessages = [...messages, { text: input, sender: 'user' }];
    setMessages(newMessages);
    setInput('');

    try {
      const response = await fetch("https://srainapark-cbt-chat-app.hf.space/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          messages: [
            { role: "user", content: input }
          ]
        })
      });
      

      if (!response.ok) {
        throw new Error(`Server returned ${response.status}`);
      }

      const data = await response.json();
      const botMessage = data.reply || "Hmm... no reply received.";

      // Append bot message
      setMessages(prev => [...prev, { text: botMessage, sender: 'bot' }]);
    } catch (err) {
      console.error("Agent error:", err);
      setMessages(prev => [
        ...prev,
        { text: "Oops! Bestie backend is sleeping 😴", sender: 'bot' }
      ]);
    }
  };

  return (
    <div className="bg-pink-50 min-h-screen flex flex-col items-center p-4">
      <h1 className="text-2xl font-bold mb-4">Bestie</h1>

      <div className="w-full max-w-md bg-white shadow rounded-xl p-4 flex-1 overflow-y-auto mb-4 space-y-2">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`rounded-xl px-4 py-2 w-fit max-w-[75%] whitespace-pre-wrap ${
              msg.sender === 'user'
                ? 'ml-auto bg-pink-200 text-black'
                : 'mr-auto bg-white text-black border'
            }`}
          >
            {msg.text}
          </div>
        ))}
      </div>

      <div className="w-full max-w-md flex gap-2">
        <input
          className="flex-1 border rounded-full px-4 py-2 text-sm focus:outline-none focus:ring"
          placeholder="Type your thought..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
        />
        <button
          onClick={handleSend}
          className="bg-pink-400 text-white px-4 py-2 rounded-full text-sm"
        >
          Send
        </button>
      </div>
    </div>
  );
}

export default App;
