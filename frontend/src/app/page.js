'use client'; // This is necessary for Next.js to treat this as a Client Component
import { useState, useRef } from 'react';

export default function Home() {
  const [file, setFile] = useState(null);
  const [isUploaded, setIsUploaded] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messageEndRef = useRef(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append('file', file);
    setIsLoading(true);
    try {
      const response = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData,
      });
      if (response.ok) {
        setIsUploaded(true);
        setMessages([...messages, { sender: 'system', text: `Document "${file.name}" uploaded successfully! Ask me anything about it.` }]);
      }
    } catch (error) {
      console.error('Upload failed:', error);
    }
    setIsLoading(false);
  };

  const handleSend = async () => {
    if (!input.trim() || !isUploaded) return;
    const userMessage = { sender: 'user', text: input };
    setMessages([...messages, userMessage]);
    setInput('');
    setIsLoading(true);
    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: input }),
      });
      const data = await response.json();
      setMessages(messages => [...messages, userMessage, { sender: 'ai', text: data.answer }]);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(messages => [...messages, userMessage, { sender: 'ai', text: "Sorry, I couldn't process your request." }]);
    }
    setIsLoading(false);
  };

  return (
    <div className="container">
      <h1>DocuChat</h1>
      <p>Upload a PDF and chat with it.</p>
      
      <div className="upload-section">
        <input type="file" accept=".pdf" onChange={handleFileChange} disabled={isUploaded} />
        <button onClick={handleUpload} disabled={!file || isUploaded || isLoading}>
          {isLoading ? 'Processing...' : 'Upload & Process'}
        </button>
      </div>

      <div className="chat-section">
        <div className="chat-messages">
          {messages.map((msg, index) => (
            <div key={index} className={`message ${msg.sender}`}>
              {msg.text}
            </div>
          ))}
          <div ref={messageEndRef} />
        </div>
        <div className="chat-input">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            placeholder={isUploaded ? "Ask a question about the document..." : "Please upload a document first."}
            disabled={!isUploaded || isLoading}
          />
          <button onClick={handleSend} disabled={!isUploaded || isLoading || !input.trim()}>
            Send
          </button>
        </div>
      </div>
    </div>
  );
}