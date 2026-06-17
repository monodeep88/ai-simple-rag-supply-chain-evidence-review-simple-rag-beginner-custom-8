import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Document:
    title: str
    text: str


@dataclass(frozen=True)
class Chunk:
    title: str
    text: str
    index: int


def load_documents(data_dir: Path) -> list[Document]:
    documents: list[Document] = []
    for path in sorted(data_dir.glob("*")):
        if path.suffix.lower() not in {".txt", ".md", ".csv"}:
            continue
        documents.append(Document(title=path.name, text=path.read_text(encoding="utf-8")))
    if not documents:
        raise FileNotFoundError(f"No sample documents found in {data_dir}")
    return documents


def split_text(text: str, chunk_size: int = 650, overlap: int = 100) -> list[str]:
    cleaned = re.sub(r"\s+", " ", text).strip()
    if not cleaned:
        return []
    chunks: list[str] = []
    start = 0
    while start < len(cleaned):
        end = min(start + chunk_size, len(cleaned))
        chunks.append(cleaned[start:end])
        if end == len(cleaned):
            break
        start = max(0, end - overlap)
    return chunks


def chunk_documents(documents: list[Document]) -> list[Chunk]:
    chunks: list[Chunk] = []
    for document in documents:
        for index, text in enumerate(split_text(document.text)):
            chunks.append(Chunk(title=document.title, text=text, index=index))
    return chunks
