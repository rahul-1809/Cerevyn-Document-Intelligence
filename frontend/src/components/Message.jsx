import React from 'react';
import './Message.css';

function Message({ role, content, sources, timestamp }) {
  const isUser = role === 'user';

  return (
    <div className={`message ${isUser ? 'message-user' : 'message-ai'}`}>
      <div className="message-content">
        <div className="message-bubble">
          <p className="message-text">{content}</p>
        </div>
        
        {!isUser && sources && sources.length > 0 && (
          <div className="message-sources">
            <div className="sources-header">
              <span className="sources-icon">📄</span>
              <span className="sources-title">Sources:</span>
            </div>
            <div className="sources-list">
              {sources.map((source, index) => (
                <div key={index} className="source-item">
                  <span className="source-doc">{source.doc}</span>
                  <span className="source-page">Page {source.page}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Message;
