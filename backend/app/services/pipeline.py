from app.config import CHROMA_DIR, DATA_DIR, PROJECT_TYPE
from app.domain import BUSINESS_RULES, DOMAIN_SUMMARY, TOOL_CATALOG, WORKFLOW_STEPS
from app.schemas import AskResponse, Source, TimelineStep
from app.services.llm import get_answer_model
from app.services.text import chunk_documents, load_documents
from app.services.tools import calculate, planning_checklist, summarize_csv
from app.services.vector_store import build_vector_index


FLOW_STYLE = 'Simple RAG'


def _step(name: str, detail: str, status: str = "completed") -> TimelineStep:
    return TimelineStep(step=name, status=status, detail=detail)


def _tool_call(question: str) -> str:
    lowered = question.lower()
    if "calculate:" in lowered:
        return "Calculator result: " + calculate(question.split(":", 1)[1].strip())
    if "csv:" in lowered:
        return "CSV analysis: " + summarize_csv(question.split(":", 1)[1])
    domain_tools = ", ".join(f"{tool['name']}: {tool['description']}" for tool in TOOL_CATALOG[:3])
    return "Checklist: " + " | ".join(planning_checklist(question)[:3]) + f" | Available domain tools: {domain_tools}"


def run_pipeline(question: str) -> AskResponse:
    steps: list[TimelineStep] = []
    documents = load_documents(DATA_DIR)
    steps.append(_step("document_loader", f"Loaded {len(documents)} sample documents."))

    chunks = chunk_documents(documents)
    steps.append(_step("text_splitter", f"Created {len(chunks)} searchable chunks."))

    index = build_vector_index(chunks, CHROMA_DIR)
    steps.append(_step("embedding_and_vector_store", "Indexed chunks with ChromaDB when available, otherwise local embeddings."))

    plan = planning_checklist(question)
    if FLOW_STYLE in {"Agentic RAG", "AI Agent", "Multi-Agent AI", "CrewAI multi-agent", "Pinecone RAG", "LangGraph workflow", "LangChain tool-calling agent"}:
        steps.append(_step("planner", " -> ".join(plan[:3])))
    steps.append(_step("domain_profile", DOMAIN_SUMMARY))
    for rule_number, rule in enumerate(BUSINESS_RULES[:3], start=1):
        steps.append(_step(f"business_rule_{rule_number}", rule))

    results = index.similarity_search(question, k=4)
    steps.append(_step("retriever", f"Retrieved {len(results)} relevant chunks."))
    for workflow_number, workflow_step in enumerate(WORKFLOW_STEPS[:4], start=1):
        steps.append(_step(f"domain_workflow_{workflow_number}", workflow_step))

    if FLOW_STYLE == "Multi-Agent AI":
        steps.append(_step("researcher_agent", "Collected evidence from retrieved documents."))
        steps.append(_step("analyst_agent", "Compared evidence with the user question."))
        steps.append(_step("reviewer_agent", "Checked citations and final answer quality."))
    elif FLOW_STYLE == "CrewAI multi-agent":
        steps.append(_step("crew_manager", "Scoped the task and delegated work to role agents."))
        steps.append(_step("crew_researcher", "Collected evidence from retrieved documents."))
        steps.append(_step("crew_reviewer", "Reviewed delegated outputs and challenged weak evidence."))
    elif FLOW_STYLE == "Pinecone RAG":
        steps.append(_step("pinecone_query", "Built a Pinecone-style embedding query."))
        steps.append(_step("pinecone_metadata_filter", "Applied namespace and metadata filtering before final citation."))
    elif FLOW_STYLE == "LangGraph workflow":
        steps.append(_step("langgraph_plan_node", "Prepared state for retrieval and tool execution."))
        steps.append(_step("langgraph_reason_node", "Updated state with reasoning and source citations."))
    elif FLOW_STYLE == "LangChain tool-calling agent":
        steps.append(_step("langchain_tool_router", "Selected the best local tool for the prompt."))
        steps.append(_step("tool_call", _tool_call(question)))
    elif FLOW_STYLE in {"Agentic RAG", "AI Agent"}:
        steps.append(_step("reasoning", "Reasoned over retrieved context and plan."))
        steps.append(_step("tool_call", _tool_call(question)))

    reasoning = " ".join(step.detail for step in steps[-3:])
    answer = get_answer_model().invoke(question, results, reasoning)
    steps.append(_step("final_answer", "Generated answer with source citations."))

    return AskResponse(
        answer=answer,
        sources=[Source(title=item.title, snippet=item.text[:240], score=item.score) for item in results],
        steps=steps,
        project_type=PROJECT_TYPE,
    )
