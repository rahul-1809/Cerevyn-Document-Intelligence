# Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Step 1: Backend Setup (2 minutes)

```bash
cd backend
./setup.sh
```

Edit `.env` file and add your Groq API key:
```
GROQ_API_KEY=gsk_your_actual_key_here
```

Start the backend:
```bash
source venv/bin/activate
python main.py
```

✓ Backend running at http://localhost:8000

### Step 2: Frontend Setup (2 minutes)

Open a new terminal:
```bash
cd frontend
./setup.sh
npm run dev
```

✓ Frontend running at http://localhost:3000

### Step 3: Use the App (1 minute)

1. Open http://localhost:3000
2. Click "Select PDF Files" in the sidebar
3. Choose PDF files and click "Upload"
4. Wait for processing to complete
5. Ask questions in the chat!

## 🎯 Example Questions

- "What is the main topic of this document?"
- "Summarize the key points from section 3"
- "What does the document say about [specific topic]?"

## 📝 Important Notes

- PDF files are stored temporarily in `backend/uploads/`
- Vector embeddings are persisted in `backend/chroma_db/`
- The app uses Groq's Mixtral model for fast inference
- Every answer includes source citations with page numbers

## 🔧 Troubleshooting

**Backend won't start:**
- Check if Groq API key is set in `.env`
- Ensure Python 3.9+ is installed
- Try: `pip install -r requirements.txt`

**Frontend won't connect:**
- Verify backend is running at http://localhost:8000
- Check CORS settings in `backend/main.py`
- Clear browser cache

**No answers from chat:**
- Make sure documents are uploaded first
- Check backend console for errors
- Verify ChromaDB is populated

## 📚 API Testing

Test the backend directly:

```bash
# Health check
curl http://localhost:8000/

# Upload a file
curl -X POST http://localhost:8000/upload \
  -F "files=@path/to/document.pdf"

# Send a chat message
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is this about?"}'
```

## 🎨 Customization

**Change the LLM model:**
Edit `backend/graph_nodes.py`, line ~115:
```python
model="llama-3.1-70b-versatile"  # or other Groq models
```

**Adjust chunk size:**
Edit `backend/upload_handler.py`, line ~32:
```python
chunk_size=1000,  # Increase for more context
chunk_overlap=200,  # Increase to preserve more context
```

**Change number of retrieved documents:**
Edit `backend/graph_nodes.py`, line ~49:
```python
k=5  # Retrieve top 5 chunks
```

## 📊 Monitoring

Backend logs show:
- File processing status
- Document chunking progress
- Query execution flow
- Error messages

Frontend console shows:
- API request/response details
- State updates
- Component lifecycle events

## 🔐 Security Notes

- Never commit `.env` files
- Keep your Groq API key secure
- Validate file uploads (size, type)
- Consider rate limiting for production

## 📖 Further Reading

- [LangGraph Documentation](https://python.langchain.com/docs/langgraph)
- [FastAPI Guide](https://fastapi.tiangolo.com/)
- [Groq Documentation](https://console.groq.com/docs)
- [ChromaDB Documentation](https://docs.trychroma.com/)
