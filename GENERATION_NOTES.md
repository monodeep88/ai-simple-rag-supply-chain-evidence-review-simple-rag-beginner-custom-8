# Generation Notes

Mode: ai

Model: groq / llama-3.1-8b-instant

Fallback reason: OpenAI limit reached. Automatically switched to Groq.

Architecture: PDF FAQ Knowledge Bot

Template path: templates/simple-rag/pdf-faq-knowledge-bot

Short description:

A beginner-friendly RAG project for reviewing supply chain evidence

Architecture notes:

- Use Docker to containerize services for easy deployment and management
- Implement API Gateway to handle incoming requests and route them to respective services
- Use PostgreSQL as the database to store and manage data

Project planner agent workflow:

- Architecture Agent: Define app boundaries, data flow, runtime stack, and integration points. Outputs: Use Docker to containerize services for easy deployment and management; Implement API Gateway to handle incoming requests and route them to respective services; Use PostgreSQL as the database to store and manage data
- Backend Agent: Design FastAPI modules, service contracts, validation, and error handling. Outputs: Data Ingestion Module (FastAPI); Data Processing Module (Python); Data Visualization Module (React)
- Frontend Agent: Design React screens, state flow, controls, and user feedback states. Outputs: User-friendly interface for data visualization; Filtering and sorting capabilities for evidence review; RAG system for categorizing evidence
- Database Agent: Design persistence models, sample data, indexes, and audit records. Outputs: Run history; Source document metadata; Generated workflow audit records
- Testing Agent: Define contract tests, smoke tests, and generated project validation. Outputs: Unit testing and integration testing using Pytest and Jest
- DevOps Agent: Define environment variables, Docker workflow, and repository packaging. Outputs: Docker-ready project; Environment sample file; GitHub repository upload
- Reviewer Agent: Review the generated plan for completeness, security, and portfolio quality. Outputs: Data ingestion and processing; Evidence categorization using RAG system; Data visualization and analysis
