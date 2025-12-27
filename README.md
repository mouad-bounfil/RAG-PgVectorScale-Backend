# 🤖 AI Chat Assistant with RAG

<div align="center">

![AI Chat](https://img.shields.io/badge/AI-Chat%20Assistant-orange?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-black?style=for-the-badge&logo=flask)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-green?style=for-the-badge&logo=openai)

**An intelligent conversational AI powered by Retrieval-Augmented Generation (RAG)**

*Ask questions, get accurate answers backed by your documents*

[Features](#-features) • [Quick Start](#-quick-start) • [Configuration](#-configuration) • [API](#-api-reference)

</div>

---

## 📋 Overview

AI Chat Assistant is a production-ready chatbot application that combines the power of OpenAI's GPT models with a vector database-backed RAG system. It extracts information from PDF documents, stores them as embeddings in a PostgreSQL database with pgvector/TimescaleDB, and retrieves relevant context to provide accurate, contextual responses.

### ✨ Key Features

- 🧠 **Intelligent Conversations** - Context-aware responses using GPT-4o-mini
- 📚 **Document Understanding** - Extracts and processes PDF documents using Gemini Vision OCR
- 🔍 **Semantic Search** - Vector similarity search for relevant context retrieval
- 💾 **Persistent Memory** - Conversation history maintained across interactions
- 🎨 **Beautiful UI** - Modern, dark-themed interface inspired by shadcn/ui
- ⚡ **Fast & Efficient** - Optimized chunk sizes and embedding strategies
- 🔒 **Secure** - Environment-based configuration and secure API handling

---

## 🏗️ Architecture

```
┌─────────────┐
│   User UI   │
└──────┬──────┘
       │
       ▼
┌─────────────┐      ┌──────────────┐
│ Flask API   │◄────►│   OpenAI     │
└──────┬──────┘      │   GPT-4o     │
       │             └──────────────┘
       ▼
┌─────────────┐      ┌──────────────┐
│   Embeddings│◄────►│   Gemini     │
│   Service   │      │  Vision OCR  │
└──────┬──────┘      └──────────────┘
       │
       ▼
┌─────────────┐
│ PostgreSQL  │
│  + pgvector │
└─────────────┘
```

---

## 🛠️ Tech Stack

### Backend
- **Flask** - Lightweight web framework
- **OpenAI API** - GPT-4o-mini for chat completions
- **Google Gemini** - Vision API for advanced OCR
- **TimescaleDB/PostgreSQL** - Vector database for embeddings
- **LangChain** - Document processing and text splitting

### Frontend
- **HTML5 / JavaScript** - Modern vanilla JS
- **Tailwind CSS** - Utility-first styling
- **Responsive Design** - Mobile-friendly interface

### Document Processing
- **pdf2image** - PDF to image conversion
- **OpenCV** - Image preprocessing
- **RecursiveCharacterTextSplitter** - Smart text chunking

---

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- PostgreSQL with pgvector extension (or TimescaleDB)
- OpenAI API key
- Google Gemini API key
- Poppler (for pdf2image)

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd full-agents-rag
```

2. **Create virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Install Poppler (for PDF processing)**
```bash
# macOS
brew install poppler

# Ubuntu/Debian
sudo apt-get install poppler-utils

# Windows
# Download from: https://github.com/oschwartz10612/poppler-windows/releases/
```

5. **Set up environment variables**

Create a `.env` file in the project root:

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-...your-key-here...

# Gemini Configuration
GEMINI_API_KEY=...your-gemini-key...

# Database Configuration (Railway, Supabase, or local PostgreSQL)
TIMESCALE_SERVICE_URL=postgresql://user:password@host:port/database

# Optional: Custom configuration
FLASK_ENV=development
```

6. **Set up the database**

Make sure your PostgreSQL database has the pgvector extension enabled:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

7. **Process your documents**

Place your PDF files in the `services/` directory and run:

```bash
python services/rag_creation.py
```

This will:
- Extract text from PDFs using Gemini OCR
- Split text into optimized chunks
- Generate embeddings using OpenAI
- Store everything in your vector database

8. **Start the server**

```bash
python server.py
```

The application will be available at `http://localhost:8080`

---

## 📁 Project Structure

```
full-agents-rag/
├── agents/                      # AI agent logic
│   ├── __init__.py
│   ├── index.py                 # Main conversation agent
│   ├── prompt.py                # System prompts
│   └── embeddings.py            # Embedding retrieval
├── controllers/                 # Request handlers
│   └── agents.py
├── routes/                      # API routes
│   └── agents.py
├── services/                    # Core services
│   ├── chunks.py                # PDF processing & chunking
│   └── rag_creation.py          # Embedding generation & storage
├── views/                       # Frontend
│   └── index.html               # Chat interface
├── server.py                    # Flask application
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (create this)
└── README.md                    # You are here!
```

---

## ⚙️ Configuration

### Chunk Size Optimization

The default configuration uses:
- **Chunk size**: 300 characters
- **Chunk overlap**: 50 characters

Adjust in `services/chunks.py`:
```python
splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,      # Increase for longer context
    chunk_overlap=50,    # Increase for more context continuity
)
```

### Embedding Model

Default: `text-embedding-3-small` (1536 dimensions)

To change, update in `services/rag_creation.py`:
```python
model = "text-embedding-3-large"  # Higher quality, more expensive
```

### Chat Model

Default: `gpt-4o-mini`

To change, update in `agents/index.py`:
```python
model = "gpt-4o"  # More capable, higher cost
```

---

## 🔌 API Reference

### POST `/api/agents/conversation`

Send a message to the AI assistant.

**Request:**
```json
{
  "query": "What is artificial intelligence?"
}
```

**Response:**
```json
{
  "response": "Artificial intelligence (AI) is...",
  "status": "success",
  "code": 200
}
```

**Error Response:**
```json
{
  "error": "Error message",
  "status": "error",
  "code": 500
}
```

---

## 🎨 UI Features

### Design System
- **Color Scheme**: Black and Stone (inspired by shadcn/ui)
- **Typography**: System fonts with optimized readability
- **Animations**: Smooth transitions and loading states
- **Responsive**: Works on desktop, tablet, and mobile

### User Experience
- ✅ Real-time typing indicators
- ✅ Smooth message animations
- ✅ Auto-scrolling to latest message
- ✅ Error handling with user-friendly messages
- ✅ Keyboard shortcuts (Enter to send)
- ✅ Disabled state during API calls

---

## 📊 How RAG Works

1. **Document Ingestion**
   - PDFs are converted to images
   - Gemini Vision extracts text via OCR
   - Text is split into semantic chunks

2. **Embedding Generation**
   - Each chunk is embedded using OpenAI's embedding model
   - Embeddings (vectors) are stored in PostgreSQL with metadata

3. **Query Processing**
   - User query is embedded using the same model
   - Vector similarity search finds top-k relevant chunks
   - Retrieved context is added to the conversation

4. **Response Generation**
   - GPT model receives: system prompt + conversation history + retrieved context
   - Generates contextually accurate response
   - Response is stored in conversation history

---

## 🔧 Troubleshooting

### Common Issues

**1. "Extension vectorscale is not available"**
- Solution: Use pgvector instead of TimescaleDB vectorscale
- Run: `CREATE EXTENSION IF NOT EXISTS vector;` in your database

**2. "No module named 'pdf2image'"**
- Solution: Install Poppler (see installation steps)

**3. "API key not found"**
- Solution: Ensure `.env` file exists with correct keys

**4. "Connection refused to database"**
- Solution: Check `TIMESCALE_SERVICE_URL` in `.env`

**5. Slow response times**
- Solution: Reduce chunk_size or limit the number of retrieved embeddings

---

## 🚢 Deployment

### Railway

1. Connect your GitHub repository to Railway
2. Add environment variables in Railway dashboard
3. Deploy automatically on push

### Docker (Optional)

```dockerfile
FROM python:3.13-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8080

CMD ["python", "server.py"]
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- [OpenAI](https://openai.com/) for GPT and embedding models
- [Google Gemini](https://deepmind.google/technologies/gemini/) for Vision OCR
- [shadcn/ui](https://ui.shadcn.com/) for design inspiration
- [LangChain](https://langchain.com/) for document processing utilities
- [TimescaleDB](https://www.timescale.com/) / [pgvector](https://github.com/pgvector/pgvector) for vector storage

---

## 📧 Contact & Support

For questions, issues, or suggestions:
- 🐛 Report bugs via [Issues](../../issues)
- 💡 Request features via [Discussions](../../discussions)
- 📧 Email: your-email@example.com

---

<div align="center">

**Built with ❤️ using Python, Flask, and OpenAI**

⭐ Star this repo if you find it helpful!

</div>

