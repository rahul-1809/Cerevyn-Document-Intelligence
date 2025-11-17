import React, { useRef, useEffect } from 'react';
import MessageList from './MessageList';
import './ChatWindow.css';

function ChatWindow({ chatHistory, isLoading }) {
  const chatEndRef = useRef(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatHistory, isLoading]);

  return (
    <div className="chat-window">
      {chatHistory.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">📚</div>
          <h2>Welcome to Cerevyn Document Intelligence</h2>
          <p>Upload PDF documents and ask questions about their content.</p>
          <p className="hint">Start by uploading documents using the sidebar.</p>
        </div>
      ) : (
        <MessageList messages={chatHistory} />
      )}
      
      {isLoading && (
        <div className="loading-indicator">
          <div className="typing-dots">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      )}
      
      <div ref={chatEndRef} />
    </div>
  );
}

export default ChatWindow;
