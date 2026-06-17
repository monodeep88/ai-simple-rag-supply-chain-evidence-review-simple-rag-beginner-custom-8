from .vector_store import SearchResult


class LocalAnswerModel:
    """Deterministic local answer model for development and tests."""

    def invoke(self, question: str, context: list[SearchResult], reasoning: str) -> str:
        context_text = " ".join(item.text for item in context[:2])
        if not context_text:
            context_text = "No matching context was found."
        return (
            f"Based on the retrieved project documents: {context_text} "
            f"Reasoning summary: {reasoning} "
            f"Direct answer: {question.strip()}"
        )


def get_answer_model():
    try:
        from app.config import OPENAI_API_KEY, OPENAI_MODEL
        if not OPENAI_API_KEY:
            return LocalAnswerModel()
        from langchain_openai import ChatOpenAI

        class LangChainAnswerModel:
            def __init__(self) -> None:
                self.llm = ChatOpenAI(model=OPENAI_MODEL, temperature=0.2)

            def invoke(self, question: str, context: list[SearchResult], reasoning: str) -> str:
                context_text = "\n\n".join(f"Source: {item.title}\n{item.text}" for item in context)
                prompt = (
                    "Answer the user using only the context. Include practical next steps.\n\n"
                    f"Context:\n{context_text}\n\nReasoning:\n{reasoning}\n\nQuestion: {question}"
                )
                return self.llm.invoke(prompt).content

        return LangChainAnswerModel()
    except Exception:
        return LocalAnswerModel()
