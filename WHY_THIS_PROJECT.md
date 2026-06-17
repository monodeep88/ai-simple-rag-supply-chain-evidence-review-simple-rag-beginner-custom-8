# Why This Project Satisfies Simple RAG

## Portfolio Claim

**Supply Chain Evidence Review Simple RAG** is not a static prompt demo. It is a runnable full-stack AI application for **Supply Chain Evidence Review Simple RAG - Beginner Custom 8** that demonstrates the core expectations of a **Simple RAG** project at **Beginner** difficulty.

## What A Reviewer Can Verify

- A real React interface accepts user questions and shows final answers, cited sources, and timeline steps.
- A real FastAPI backend exposes `POST /api/ask`.
- A service pipeline runs the expected project flow: Retriever, Citation Answer Builder.
- Sample domain documents are stored in `backend/app/data/sample_docs`.
- The vector/search layer retrieves cited context instead of returning a generic answer.
- The run log database stores each request so the project behaves like an application workflow.
- Tests verify metadata, pipeline output, tool behavior, and full-stack file presence.

## Type Fit

User question -> load documents -> split chunks -> embed -> Chroma similarity search -> answer with citations.

## Recruiter / Interview Talking Points

- Explain why this project type was chosen for the domain.
- Walk through how the backend converts a user request into timeline steps.
- Show how cited sources reduce hallucination risk.
- Discuss how Docker, tests, and environment variables make the repo runnable by someone else.
- Describe one production upgrade: authentication, file upload, richer vector DB, background jobs, or deployment.
