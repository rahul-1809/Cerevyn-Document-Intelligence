import React, { useState, useRef } from 'react';
import './FileUpload.css';

function FileUpload({ onUpload, status, message }) {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const fileInputRef = useRef(null);

  const handleFileSelect = (e) => {
    const files = Array.from(e.target.files);
    const pdfFiles = files.filter(file => file.name.endsWith('.pdf'));
    setSelectedFiles(pdfFiles);
  };

  const handleUploadClick = () => {
    if (selectedFiles.length > 0) {
      onUpload(selectedFiles);
      // Clear selection after upload
      setSelectedFiles([]);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  const handleButtonClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="file-upload">
      <h2 className="file-upload__title">Upload Documents</h2>
      <p className="file-upload__description">
        Upload PDF files to build your knowledge base
      </p>

      <input
        ref={fileInputRef}
        type="file"
        multiple
        accept=".pdf"
        onChange={handleFileSelect}
        className="file-upload__input"
      />

      <button
        onClick={handleButtonClick}
        className="file-upload__button"
        disabled={status === 'uploading'}
      >
        Select PDF Files
      </button>

      {selectedFiles.length > 0 && (
        <div className="file-upload__selected">
          <p className="file-upload__count">
            {selectedFiles.length} file(s) selected
          </p>
          <ul className="file-upload__list">
            {selectedFiles.map((file, index) => (
              <li key={index} className="file-upload__file">
                {file.name}
              </li>
            ))}
          </ul>
          <button
            onClick={handleUploadClick}
            className="file-upload__button"
            disabled={status === 'uploading'}
          >
            {status === 'uploading' ? 'Uploading...' : 'Upload'}
          </button>
        </div>
      )}

      {message && (
        <div className={`file-upload__status file-upload__status--${status}`}>
          {message}
        </div>
      )}
    </div>
  );
}

export default FileUpload;
