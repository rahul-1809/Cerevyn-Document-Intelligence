import axios from 'axios';

// Base API URL - change this if backend runs on different port
const API_BASE_URL = 'http://localhost:8000';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Upload PDF files to the backend
 * @param {File[]} files - Array of PDF files to upload
 * @returns {Promise} - Response with upload status
 */
export const uploadDocuments = async (files) => {
  const formData = new FormData();
  
  // Append each file to FormData
  files.forEach((file) => {
    formData.append('files', file);
  });
  
  // Use different headers for multipart/form-data
  const response = await api.post('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

/**
 * Send a chat message to the backend
 * @param {string} question - User's question
 * @returns {Promise} - Response with answer and sources
 */
export const sendChatMessage = async (question) => {
  const response = await api.post('/chat', { question });
  return response.data;
};

/**
 * List uploaded PDF files from the backend
 * @returns {Promise<{files: Array<{name: string, url: string, size_bytes: number, modified_at: number}>}>}
 */
export const getUploadedFiles = async () => {
  const response = await api.get('/api/uploads');
  // Build absolute URLs for convenience
  const host = API_BASE_URL.replace(/\/$/, '');
  const files = (response.data.files || []).map((f) => ({
    ...f,
    absoluteUrl: `${host}${f.url}`,
  }));
  return { files };
};

/**
 * Delete an uploaded PDF by filename
 * @param {string} name - PDF file name
 */
export const deleteUploadedFile = async (name) => {
  const response = await api.delete(`/api/uploads/${encodeURIComponent(name)}`);
  return response.data;
};

/**
 * Health check endpoint
 * @returns {Promise} - Server status
 */
export const checkHealth = async () => {
  const response = await api.get('/');
  return response.data;
};

export default api;
