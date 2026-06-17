# Architecture

Selected architecture: PDF FAQ Knowledge Bot

Template path: templates/simple-rag/pdf-faq-knowledge-bot

## Pipeline

User Request -> Architecture Selection -> Topic Selection -> AI Blueprint Generation -> Template Selection -> Code Customization -> Project Validation -> GitHub Repository Creation -> GitHub Push

## Project Type Satisfaction Map

This generated project satisfies **Simple RAG** through the runtime path below. The implementation is not only a README claim: the files listed after the diagram are generated in the repository and validated before GitHub push.

```text
[User]
  |
  | question / task details / tone / constraints
  v
[React Frontend]
  |
  | POST /api/ask
  v
[FastAPI Backend]
  |
  +--> [Vector Store / Sample Docs]
  |        |
  |        +-- retrieved context / cited sources
  |
  v
[Retriever]
  |
  v
[Citation Answer Builder]
  |
  v
[Final Answer Builder]
  |
  | answer + sources + timeline steps
  v
[React Frontend]
  |
  v
[User sees final output + agent timeline]
```

Runtime proof points:

- `frontend/src/App.jsx` renders the user workspace, starter prompts, answer panel, cited sources, and timeline.
- `backend/app/main.py` exposes `POST /api/ask` and returns the final answer, sources, timeline steps, and project type.
- `backend/app/services/pipeline.py` orchestrates the project-type flow: Retriever, Citation Answer Builder.
- `backend/app/services/vector_store.py` loads sample documents and retrieves relevant cited context.
- `backend/app/domain.py` contains the generated topic-specific workflow steps, business rules, tools, persona, and starter questions.
- `backend/app/db.py` stores each run so the generated app behaves like a real workflow tool instead of a static prompt demo.
- `backend/tests/test_project_contract.py` validates the API contract and project-type behavior.

Type-specific behavior:

- Flow style: User question -> load documents -> split chunks -> embed -> Chroma similarity search -> answer with citations.
- Visible output: final answer, cited sources, timeline steps, and project type.
- Validation gate: pytest, frontend build, Docker Compose config, and Docker build before repository upload.

## Specialist Agents

- **Architecture Agent**: Define app boundaries, data flow, runtime stack, and integration points.
- **Backend Agent**: Design FastAPI modules, service contracts, validation, and error handling.
- **Frontend Agent**: Design React screens, state flow, controls, and user feedback states.
- **Database Agent**: Design persistence models, sample data, indexes, and audit records.
- **Testing Agent**: Define contract tests, smoke tests, and generated project validation.
- **DevOps Agent**: Define environment variables, Docker workflow, and repository packaging.
- **Reviewer Agent**: Review the generated plan for completeness, security, and portfolio quality.

## Validation

The source is expected to pass pytest, frontend build, Docker Compose config, and Docker build before publication.

## Portfolio Proof

This repository includes:

- `WHY_THIS_PROJECT.md` for project-type fit.
- `DEPLOYMENT.md` for hosting options.
- `docs/screenshots/app-preview.svg` for a preview image.
- `backend/tests/test_project_contract.py` for automated validation.
