# Document Intelligence RAG Assistant

An AI-powered document question-answering system built using
Retrieval-Augmented Generation (RAG).

## Features

- PDF document processing
- Text chunking
- Semantic embeddings
- Qdrant vector database
- Similarity-based retrieval
- Groq LLM
- Grounded question answering
- Conversational greetings
- Web-based chatbot interface
- Flask REST API

## Architecture

User
↓
Frontend
↓
Flask API
↓
RAG Pipeline
↓
Embedding Model
↓
Qdrant
↓
Retrieved Context
↓
Groq LLM
↓
Answer

## Tech Stack

- Python
- Flask
- LangChain
- Sentence Transformers
- Qdrant
- Groq
- HTML
- CSS
- JavaScript

## Run Locally

Create virtual environment:

python -m venv venv

Activate:

Windows:

venv\Scripts\activate

Install dependencies:

pip install -r backend/requirements.txt

Create `.env` and add:

GROQ_API_KEY=your_key
QDRANT_URL=your_url
QDRANT_API_KEY=your_key

Run:

python backend/app.py

Open:

http://127.0.0.1:5000