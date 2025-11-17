import React from 'react';
import './UploadedFiles.css';

function formatBytes(bytes) {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
}

export default function UploadedFiles({ files, selected, onSelect, onRefresh, onDelete }) {
  return (
    <div className="uploaded-files">
      <div className="uploaded-files__header">
        <h3>Uploaded PDFs</h3>
        <button className="uploaded-files__refresh" onClick={onRefresh} title="Refresh list">⟲</button>
      </div>
      {(!files || files.length === 0) ? (
        <div className="uploaded-files__empty">No PDFs uploaded yet.</div>
      ) : (
        <ul className="uploaded-files__list">
          {files.map((f) => (
            <li
              key={f.name}
              className={['uploaded-files__item', selected === f.name ? 'is-active' : ''].join(' ')}
              title={f.name}
            >
              <button className="uploaded-files__row" onClick={() => onSelect?.(f)}>
                <span className="uploaded-files__icon">📄</span>
                <span className="uploaded-files__name">{f.name}</span>
                <span className="uploaded-files__meta">{formatBytes(f.size_bytes)}</span>
              </button>
              <button
                className="uploaded-files__delete"
                title="Delete PDF"
                onClick={(e) => { e.stopPropagation(); onDelete?.(f); }}
              >
                🗑️
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
