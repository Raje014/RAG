import os

from dotenv import load_dotenv
from groq import Groq

from retriever import search_documents

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

groq_client = Groq(
    api_key=GROQ_API_KEY
)

MODEL_NAME = "openai/gpt-oss-20b"


def is_greeting(question: str):

    greetings = {
        "hi",
        "hello",
        "hey",
        "hii",
        "hai",
        "good morning",
        "good afternoon",
        "good evening",
        "how are you",
        "thanks",
        "thank you",
        "bye"
    }

    question = question.lower().strip()

    return question in greetings


def greeting_response(question: str):

    question = question.lower().strip()

    if question in ["hi", "hello", "hey", "hii", "hai"]:
        return "Hello! 👋 How can I help you with the documents?"

    if question == "good morning":
        return "Good morning! ☀️ How can I help you?"

    if question == "good afternoon":
        return "Good afternoon! 😊 How can I help you?"

    if question == "good evening":
        return "Good evening! 🌙 How can I help you?"

    if question == "how are you":
        return "I'm doing great! 😊 Ask me anything about the documents."

    if question in ["thanks", "thank you"]:
        return "You're welcome! 😊"

    if question == "bye":
        return "Goodbye! 👋"

    return "Hello! How can I help you?"


def generate_answer(question: str):

    # Handle normal conversation first
    if is_greeting(question):
        return {
            "answer": greeting_response(question),
            "sources": []
        }

    # Retrieve relevant chunks
    results = search_documents(
        question,
        limit=3
    )

    # No documents found
    if not results:
        return {
            "answer": "I couldn't find relevant information in the documents.",
            "sources": []
        }

    # Prepare context
    context_parts = []

    sources = []

    for result in results:

        text = result.payload.get("text", "")

        if text:
            context_parts.append(text)

            sources.append({
                "score": round(float(result.score), 3),
                "text": text[:180]
            })

    context = "\n\n---\n\n".join(context_parts)

    prompt = f"""
You are a document-based AI assistant.

Answer the user's question using ONLY the provided document context.

If the answer is not present in the context, say:
"I couldn't find that information in the provided documents."

Do not invent facts.

Keep simple questions concise.
For detailed questions, explain clearly.

DOCUMENT CONTEXT:

{context}

USER QUESTION:

{question}
"""

    response = groq_client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful document question-answering assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_completion_tokens=500
    )

    answer = response.choices[0].message.content

    return {
        "answer": answer,
        "sources": sources
    }