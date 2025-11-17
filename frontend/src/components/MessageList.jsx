import React from 'react';
import Message from './Message';
import './MessageList.css';

function MessageList({ messages }) {
  return (
    <div className="message-list">
      {messages.map((message, index) => (
        <Message
          key={index}
          role={message.role}
          content={message.content}
          sources={message.sources}
          timestamp={message.timestamp}
        />
      ))}
    </div>
  );
}

export default MessageList;
