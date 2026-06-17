import math
import re
from dataclasses import dataclass
from pathlib import Path

from .text import Chunk


def tokenize(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


@dataclass(frozen=True)
class SearchResult:
    title: str
    text: str
    score: float


class LocalVectorIndex:
    """Small deterministic fallback index used when Chroma or API keys are not available."""

    def __init__(self, chunks: list[Chunk]) -> None:
        self.chunks = chunks
        self.chunk_terms = [tokenize(chunk.text) | tokenize(chunk.title) for chunk in chunks]

    def similarity_search(self, query: str, k: int = 4) -> list[SearchResult]:
        query_terms = tokenize(query)
        scored: list[SearchResult] = []
        for chunk, terms in zip(self.chunks, self.chunk_terms):
            overlap = len(query_terms & terms)
            denom = math.sqrt(max(len(query_terms), 1) * max(len(terms), 1))
            score = overlap / denom
            if score > 0:
                scored.append(SearchResult(title=chunk.title, text=chunk.text, score=round(score, 3)))
        scored.sort(key=lambda item: item.score, reverse=True)
        return scored[:k] or [
            SearchResult(title=chunk.title, text=chunk.text, score=0.0)
            for chunk in self.chunks[:k]
        ]


class ChromaVectorIndex:
    """ChromaDB-backed index. Falls back to LocalVectorIndex if Chroma cannot initialize."""

    def __init__(self, chunks: list[Chunk], persist_dir: Path) -> None:
        try:
            import chromadb
            from chromadb.utils import embedding_functions
        except Exception as exc:
            raise RuntimeError("chromadb is not installed") from exc

        persist_dir.mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(path=str(persist_dir))
        self.collection = self.client.get_or_create_collection(
            name="project_docs",
            embedding_function=embedding_functions.DefaultEmbeddingFunction(),
        )
        if self.collection.count() == 0:
            self.collection.add(
                ids=[f"{chunk.title}-{chunk.index}" for chunk in chunks],
                documents=[chunk.text for chunk in chunks],
                metadatas=[{"title": chunk.title, "index": chunk.index} for chunk in chunks],
            )

    def similarity_search(self, query: str, k: int = 4) -> list[SearchResult]:
        result = self.collection.query(query_texts=[query], n_results=k)
        documents = result.get("documents", [[]])[0]
        metadatas = result.get("metadatas", [[]])[0]
        distances = result.get("distances", [[]])[0]
        return [
            SearchResult(
                title=metadata.get("title", "unknown"),
                text=document,
                score=round(1 / (1 + distance), 3),
            )
            for document, metadata, distance in zip(documents, metadatas, distances)
        ]


def build_vector_index(chunks: list[Chunk], persist_dir: Path):
    try:
        return ChromaVectorIndex(chunks, persist_dir)
    except Exception:
        return LocalVectorIndex(chunks)
