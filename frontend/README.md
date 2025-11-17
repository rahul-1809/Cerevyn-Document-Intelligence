# Cerevyn Document Intelligence - Frontend

React-based frontend for the Document Intelligence application with file upload, uploaded PDFs list, inline PDF viewer, delete action, and chat interface.

## Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm run dev
```

The app will be available at `http://localhost:3000`

## Features

- **File Upload**: Upload multiple PDF files to build your knowledge base
- **Uploaded PDFs List**: See all PDFs you’ve uploaded (backed by `GET /api/uploads`)
- **Inline PDF Viewer**: Click a file to view it in-app (served from `/uploads/{filename}`)
- **Delete PDF**: Remove a PDF and its vectors (via `DELETE /api/uploads/{filename}`)
- **Real-time Chat**: Ask questions about your documents
- **Source Citations**: Responses include references to specific document pages
- **Responsive UI**: Clean, modern interface with sidebar and main chat area

## Component Structure

- `App.jsx` - Main component managing application state
- `Layout.jsx` - Overall page structure with sidebar and main content
- `FileUpload.jsx` - File selection and upload interface
- `ChatWindow.jsx` - Main chat display area
- `MessageList.jsx` - Container for chat messages
- `Message.jsx` - Individual message bubble with source citations
- `ChatInput.jsx` - Text input for user questions

## API Integration

The frontend connects to the FastAPI backend at `http://localhost:8000`:

- `POST /upload` - Upload PDF files
- `POST /chat` - Send questions and receive answers with sources
- `GET /api/uploads` - List uploaded PDFs with URLs
- Static: `/uploads/{filename}` - Serve PDFs for viewing
- `DELETE /api/uploads/{filename}` - Delete a PDF and remove vectors

## State Management

The `App` component manages:
- `chatHistory` - Array of user and AI messages
- `isLoading` - Loading state during API calls
- `fileUploadStatus` - Status of file uploads ('idle', 'uploading', 'success', 'error')
- `uploadMessage` - User feedback messages
- `uploadedFiles` - Files from `/api/uploads`
- `selectedPdf` - Currently viewed PDF

## Build for Production

```bash
npm run build
```

Output will be in the `dist/` directory.
