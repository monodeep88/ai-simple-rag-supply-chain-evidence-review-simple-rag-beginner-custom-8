from pathlib import Path

from app.config import DIFFICULTY_LEVEL, PROJECT_SUBJECT, PROJECT_TYPE
from app.domain import BUSINESS_RULES, STARTER_QUESTIONS, WORKFLOW_STEPS
from app.services.pipeline import run_pipeline
from app.services.text import split_text
from app.services.tools import calculate


def test_project_metadata():
    assert PROJECT_TYPE == 'Simple RAG'
    assert PROJECT_SUBJECT == 'Supply Chain Evidence Review Simple RAG - Beginner Custom 8'
    assert DIFFICULTY_LEVEL == 'Beginner'
    assert STARTER_QUESTIONS
    assert WORKFLOW_STEPS
    assert BUSINESS_RULES


def test_text_splitter_creates_chunks():
    chunks = split_text("hello world " * 200, chunk_size=120, overlap=20)
    assert len(chunks) > 1


def test_calculator_tool():
    assert calculate("1 + 2 * 3") == "7"


def test_pipeline_returns_answer_sources_and_steps():
    result = run_pipeline("What is the refund policy?")
    assert result.answer
    assert result.sources
    assert result.steps
    assert result.project_type == 'Simple RAG'


def test_full_stack_files_exist():
    root = Path(__file__).resolve().parents[2]
    assert (root / "frontend" / "src" / "App.jsx").exists()
    assert (root / "backend" / "app" / "main.py").exists()
    assert (root / "backend" / "app" / "domain.py").exists()
    assert (root / "docker-compose.yml").exists()
    assert (root / "WHY_THIS_PROJECT.md").exists()
    assert (root / "DEPLOYMENT.md").exists()
    assert (root / "docs" / "screenshots" / "app-preview.svg").exists()
