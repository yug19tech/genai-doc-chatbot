import os
import importlib
try:
    load_dotenv = importlib.import_module("dotenv").load_dotenv
except ModuleNotFoundError as exc:
    if exc.name == "dotenv":
        raise ModuleNotFoundError(
            "python-dotenv is required. Install it with: python -m pip install python-dotenv"
        ) from exc
    raise
try:
    Groq = importlib.import_module("groq").Groq
except ModuleNotFoundError as exc:
    if exc.name == "groq":
        raise ModuleNotFoundError(
            "groq is required. Install it with: python -m pip install groq"
        ) from exc
    raise

load_dotenv()

MODEL = "llama-3.3-70b-versatile"  # if Groq says it's retired, pick a current model from console.groq.com/docs/models

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
try:
    chromadb = importlib.import_module("chromadb")
except ModuleNotFoundError as exc:
    if exc.name == "chromadb":
        raise ModuleNotFoundError(
            "chromadb is required. Install it with: python -m pip install chromadb"
        ) from exc
    raise
db = chromadb.PersistentClient(path="chroma_db")
collection = db.get_collection("docs")


def retrieve(question, k=4):
    """Find the k most relevant chunks for the question."""
    results = collection.query(query_texts=[question], n_results=k)
    chunks = []
    for text, meta in zip(results["documents"][0], results["metadatas"][0]):
        chunks.append({"text": text, "source": meta["source"], "page": meta["page"]})
    return chunks


def answer_question(question, k=4):
    """Return (answer, chunks_used)."""
    chunks = retrieve(question, k)

    context = "\n\n".join(
        f"[Source: {c['source']}, page {c['page']}]\n{c['text']}" for c in chunks
    )

    system_prompt = (
        "You are a helpful assistant that answers questions about the provided documents. "
        "Answer ONLY using the context given. "
        "If the answer is not in the context, say exactly: "
        "\"I couldn't find this in the documents.\" "
        "Always mention the source file and page number you used."
    )
    user_prompt = f"Context:\n{context}\n\nQuestion: {question}"

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0,
    )
    return response.choices[0].message.content, chunks


if __name__ == "__main__":
    q = input("Ask a question: ")
    answer, used = answer_question(q)
    print("\nANSWER:\n", answer)
    print("\nSOURCES:")
    for c in used:
        print(f"- {c['source']} (page {c['page']})")