import { useState, useEffect, useRef } from 'react';
import AnimatedText from './AnimatedText';
import LaraAvatar from './LaraAvatar';

export default function ChatPanel() {
  const [messages, setMessages] = useState([
    { from: 'lara', text: "Welcome to the lab. What experiment are we running today?" }
  ]);
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(scrollToBottom, [messages]);

  const sendMessage = () => {
    if (!input.trim()) return;
    setMessages(prev => [...prev, { from: 'user', text: input }]);
    setInput('');
    // Fake Lara response for demo:
    setTimeout(() => {
      setMessages(prev => [...prev, { from: 'lara', text: "Processing your input..." }]);
    }, 800);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <main className="flex-1 bg-inkyBlack p-6 flex flex-col relative">
      <div className="absolute top-4 right-4">
        <LaraAvatar />
      </div>
      <div className="flex-1 overflow-y-auto space-y-4 mb-4 scrollbar-thin scrollbar-thumb-verdigris scrollbar-track-oxidizedCopper p-2 rounded bg-oxidizedCopper bg-opacity-20">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`max-w-3/4 ${msg.from === 'lara' ? 'self-start' : 'self-end'} 
              bg-${msg.from === 'lara' ? 'verdigris bg-opacity-40' : 'burgundy bg-opacity-60'}
              rounded-lg p-3 font-terminal relative`}
          >
            {msg.from === 'lara' ? (
              <AnimatedText text={msg.text} />
            ) : (
              <div className="font-typewriter whitespace-pre-wrap">{msg.text}</div>
            )}
            {/* Speech bubble tail */}
            <span
              className={`absolute bottom-0 ${msg.from === 'lara' ? 'left-0' : 'right-0'} w-0 h-0 border-t-8 border-t-transparent
              border-b-8 border-b-transparent
              ${msg.from === 'lara' ? 'border-r-8 border-r-verdigris bg-opacity-40' : 'border-l-8 border-l-burgundy bg-opacity-60'}`}
              style={{ filter: 'drop-shadow(0 0 1px black)' }}
            />
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Input area */}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          sendMessage();
        }}
        className="flex space-x-3 items-center"
      >
        <textarea
          className="flex-1 bg-pumice bg-opacity-20 text-inkBlack font-typewriter rounded p-3 resize-none border border-bronze focus:outline-none focus:ring-2 focus:ring-neonTurquoise"
          rows={2}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Write your message or command..."
        />
        <button
          type="submit"
          className="bg-neonTurquoise text-inkyBlack font-bold px-4 py-2 rounded hover:bg-neonTurquoise/90 transition"
          aria-label="Send message"
        >
          ➤
        </button>
      </form>
    </main>
  );
}
