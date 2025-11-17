import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import './Message.css';

function Message({ role, content, sources, timestamp }) {
  const isUser = role === 'user';

  return (
    <div className={`message message--${isUser ? 'user' : 'ai'}`}>
      <div className="message__content">
        <div className="message__text">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {content}
          </ReactMarkdown>
        </div>
        
        {!isUser && sources && sources.length > 0 && (
          <div className="message__sources">
            <div className="message__sources-title">Sources</div>
            <div className="message__source-list">
              {sources.map((source, index) => (
                <div key={index} className="message__source">
                  <span className="message__source-icon">📄</span>
                  <span>{source.doc}</span>
                  <span style={{opacity: 0.7}}>• Page {source.page}</span>
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
