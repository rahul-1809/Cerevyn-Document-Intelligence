import React, { useEffect, useState, useCallback } from 'react';
import Layout from './components/Layout';
import FileUpload from './components/FileUpload';
import ChatWindow from './components/ChatWindow';
import ChatInput from './components/ChatInput';
import { uploadDocuments, sendChatMessage, getUploadedFiles, deleteUploadedFile } from './api/api';
import UploadedFiles from './components/UploadedFiles';
import PdfViewer from './components/PdfViewer';
import './App.css';

function App() {
  // State management
  const [chatHistory, setChatHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [fileUploadStatus, setFileUploadStatus] = useState('idle'); // 'idle', 'uploading', 'success', 'error'
  const [uploadMessage, setUploadMessage] = useState('');
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [selectedPdf, setSelectedPdf] = useState(null);

  const refreshUploadedFiles = useCallback(async () => {
    try {
      const { files } = await getUploadedFiles();
      setUploadedFiles(files);
      // Keep selection valid
      if (selectedPdf && !files.find(f => f.name === selectedPdf.name)) {
        setSelectedPdf(null);
      }
    } catch (e) {
      // ignore for now
    }
  }, [selectedPdf]);

  useEffect(() => {
    refreshUploadedFiles();
  }, [refreshUploadedFiles]);

  /**
   * Handle file upload
   * @param {File[]} files - Selected PDF files
   */
  const handleFileUpload = async (files) => {
    if (!files || files.length === 0) {
      return;
    }

    setFileUploadStatus('uploading');
    setUploadMessage('Processing files...');

    try {
      const response = await uploadDocuments(files);
      setFileUploadStatus('success');
      setUploadMessage(response.message || `Successfully processed ${response.files_processed} file(s)`);
      // Refresh uploaded files list
      await refreshUploadedFiles();
      
      // Reset status after 3 seconds
      setTimeout(() => {
        setFileUploadStatus('idle');
        setUploadMessage('');
      }, 3000);
    } catch (error) {
      setFileUploadStatus('error');
      setUploadMessage(error.response?.data?.detail || 'Failed to upload files');
      
      // Reset status after 5 seconds
      setTimeout(() => {
        setFileUploadStatus('idle');
        setUploadMessage('');
      }, 5000);
    }
  };

  /**
   * Handle sending a chat message
   * @param {string} message - User's question
   */
  const handleSendMessage = async (message) => {
    if (!message.trim()) {
      return;
    }

    // Add user message to chat history immediately
    const userMessage = {
      role: 'user',
      content: message,
      timestamp: new Date().toISOString(),
    };
    setChatHistory((prev) => [...prev, userMessage]);

    // Set loading state
    setIsLoading(true);

    try {
      // Send question to backend
      const response = await sendChatMessage(message);

      // Add AI response to chat history
      const aiMessage = {
        role: 'ai',
        content: response.answer,
        sources: response.sources, // Array of {doc, page}
        timestamp: new Date().toISOString(),
      };
      setChatHistory((prev) => [...prev, aiMessage]);
    } catch (error) {
      // Add error message to chat
      const errorMessage = {
        role: 'ai',
        content: 'Sorry, I encountered an error processing your question. Please try again.',
        sources: [],
        timestamp: new Date().toISOString(),
      };
      setChatHistory((prev) => [...prev, errorMessage]);
      console.error('Chat error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDeleteFile = async (file) => {
    if (!file) return;
    const confirmDelete = window.confirm(`Delete \"${file.name}\"? This will also remove it from search.`);
    if (!confirmDelete) return;
    try {
      await deleteUploadedFile(file.name);
      if (selectedPdf?.name === file.name) setSelectedPdf(null);
      await refreshUploadedFiles();
    } catch (e) {
      alert('Failed to delete file. Check backend logs.');
    }
  };

  return (
    <Layout
      sidebar={
        <>
          <FileUpload
            onUpload={handleFileUpload}
            status={fileUploadStatus}
            message={uploadMessage}
          />
          <UploadedFiles
            files={uploadedFiles}
            selected={selectedPdf?.name}
            onSelect={(f) => setSelectedPdf(f)}
            onRefresh={refreshUploadedFiles}
            onDelete={handleDeleteFile}
          />
        </>
      }
      main={
        <>
          {selectedPdf && (
            <PdfViewer file={selectedPdf} onClose={() => setSelectedPdf(null)} />
          )}
          <ChatWindow
            chatHistory={chatHistory}
            isLoading={isLoading}
          />
          <ChatInput
            onSendMessage={handleSendMessage}
            disabled={isLoading}
          />
        </>
      }
    />
  );
}

export default App;
