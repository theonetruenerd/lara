import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import './App.css'

function App() {
  const [messages, setMessages] = useState([])
  const [inputMessage, setInputMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const sendMessage = async (message) => {
  try {
    const response = await fetch('http://localhost:8000/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify({ message: message }),
    })
    
    if (!response.ok) {
      throw new Error('Network response was not ok')
    }
    
    const data = await response.json()
    return data.response
  } catch (error) {
    console.error('Error:', error)
    return 'Sorry, there was an error processing your message.'
  }
}

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (inputMessage.trim() && !isLoading) {
      // Add user message
      const userMessage = {
        text: inputMessage,
        isUser: true,
        id: Date.now()
      }
      setMessages(prevMessages => [...prevMessages, userMessage])
      setInputMessage('')
      setIsLoading(true)

      // Get bot response
      const botResponse = await sendMessage(inputMessage)
      setMessages(prevMessages => [...prevMessages, {
        text: botResponse,
        isUser: false,
        id: Date.now()
      }])
      setIsLoading(false)
    }
  }

  return (
    <div className="chat-container">
      <div className="chat-messages">
        {messages.map(message => (
          <div
            key={message.id}
            className={`message ${message.isUser ? 'user-message' : 'bot-message'}`}
          >
            {message.isUser ? (
                 message.text
               ) : (
                 /* Use ReactMarkdown to render Markdown content */
                 <ReactMarkdown>{message.text}</ReactMarkdown>
               )}
             </div>
        ))}
        {isLoading && (
          <div className="message bot-message loading">
            Thinking...
          </div>
        )}
      </div>
      <form onSubmit={handleSubmit} className="chat-input-form">
        <input
          type="text"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          placeholder="Type your message..."
          className="chat-input"
          disabled={isLoading}
        />
        <button 
          type="submit" 
          className="chat-submit"
          disabled={isLoading}
        >
          Send
        </button>
      </form>
    </div>
  )
}

export default App