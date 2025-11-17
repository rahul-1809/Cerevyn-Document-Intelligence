import React, { useState } from 'react';
import './ChatInput.css';

function ChatInput({ onSendMessage, disabled }) {
  const [message, setMessage] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim() && !disabled) {
      onSendMessage(message);
      setMessage('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="chat-input">
      <input
        type="text"
        className="chat-input__field"
        placeholder="Ask a question about your documents..."
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyPress={handleKeyPress}
        disabled={disabled}
      />
      <button
        type="submit"
        className="chat-input__button"
        disabled={disabled || !message.trim()}
        onClick={handleSubmit}
      >
        Send
      </button>
    </div>
  );
}

export default ChatInput;
