from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.config import ALLOWED_ORIGINS, PROJECT_SUBJECT, PROJECT_TYPE
from app.db import AgentRun, SessionLocal, init_db
from app.schemas import AskRequest, AskResponse
from app.services.pipeline import run_pipeline

app = FastAPI(title=f"{PROJECT_SUBJECT} API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in ALLOWED_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "project_type": PROJECT_TYPE, "subject": PROJECT_SUBJECT}


@app.post("/api/ask", response_model=AskResponse)
def ask(payload: AskRequest) -> AskResponse:
    try:
        response = run_pipeline(payload.question)
        db = SessionLocal()
        try:
            db.add(AgentRun(question=payload.question, project_type=PROJECT_TYPE))
            db.commit()
        finally:
            db.close()
        return response
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
