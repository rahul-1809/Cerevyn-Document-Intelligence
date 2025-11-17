import React from 'react';
import './PdfViewer.css';

export default function PdfViewer({ file, onClose }) {
  if (!file) return null;

  return (
    <div className="pdf-viewer">
      <div className="pdf-viewer__header">
        <div className="pdf-viewer__title">{file.name}</div>
        <button className="pdf-viewer__close" onClick={onClose} title="Close">✕</button>
      </div>
      <div className="pdf-viewer__frame">
        <iframe title={file.name} src={file.absoluteUrl} width="100%" height="100%" />
      </div>
    </div>
  );
}
