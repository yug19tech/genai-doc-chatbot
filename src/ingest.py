import os
import sys
from importlib import import_module
PdfReader = import_module("pypdf").PdfReader

chromadb = import_module("chromadb")

DATA_DIR = "data"
DB_DIR="chroma_db"


def load_pdf(path):
    reader = PdfReader(path)
    pages=[]
    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()
        if text and text.strip():
            page.append({"page":page_number, "text":text})
    return pages


def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        if end >= len(text):
            break
        start = end - overlap
    return chunks


def ingest(chunk_size=500, overlap=50):
    client = chromadb.PersistentClient(path=DB_DIR)

    try:
        client.delete_collectio("docs")
    except Exception:
        pass
    collection = client.create_collection("docs")

    ids, documents, metadatas  = [], [], []
    for filename in os.listdir(DATA_DIR):
        if not filename.lower().endswith(".pdf"):
            continue
        pages = load_pdf(os.path.join(DATA_DIR, filename))
        for page in pages:
            for i, chunk in enumerate(chunk_text(page["text"], chunk_size, overlap)):
                ids.append(f"{filename}-p{page['page']}-c{i}")
                documents.append(chunk)
                metadatas.append({"source":filename, "page": page["page"]})

    batch = 500
    for i in range(0, len(ids), batch):
        collection.add(
            ids=ids[i:i + batch],
            documents=documents[i:i + batch],
            metadatas=metadatas[i:i + batch],
        )

    print(f"Done. Stored {len(ids)} chunks (chunk_size={chunk_size}, overlap={overlap}).")

if __name__ == "__main__":
    size = int(sys.argv[1]) if len(sys.argv) > 1 else 500
    ov  = int(sys.argv[2]) if len(sys.argv) > 2 else 50
    ingest(size, ov)
