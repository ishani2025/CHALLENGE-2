# CHALLENGE-2
Technical Troubleshooting Guide
Dual-Agent Local LLM System for Enterprise IT Support

Problem Statement
Enterprise IT teams handle extremely large error logs (10,000+ lines) filled with repeated stack traces and noise. Engineers manually scan logs, search forums, and escalate issues, leading to high Mean Time to Resolution (MTTR).

There is a need for an automated system that can:

Compress verbose logs

Identify recurring error patterns

Retrieve similar past issues

Generate step-by-step solutions

Escalate low-confidence cases automatically

Solution Overview
We built a dual-agent troubleshooting system that combines:

ScaleDown API for log compression

Local LLM (Ollama + Mistral) for reasoning

Embedding-based similarity search

Confidence-driven escalation workflow

Optional Jira ticket automation

The system reduces log noise, retrieves relevant fixes, and automates escalation decisions.

Workflow (Flowchart Format)
User Uploads Large Error Log
            │
            ▼
     ScaleDown API
  (Compress 10k+ lines)
            │
            ▼
 Agent 1 – Log Analyst
  - Extract primary error
  - Identify recurring issues
  - Categorize failure type
            │
            ▼
  Embedding Similarity Search
  - Search KB (StackOverflow,
    GitHub, Runbooks)
  - Retrieve Top Matches
            │
            ▼
 Agent 2 – Solution Engineer
  - Generate root cause
  - Provide step-by-step fix
  - Compute confidence score
            │
            ▼
     Decision Controller
     ┌───────────────┬───────────────┬───────────────┐
     │ High          │ Medium        │ Low           │
     │ Confidence    │ Confidence    │ Confidence    │
     │               │               │               │
     ▼               ▼               ▼
 Auto Resolve   Suggest Review   Escalate → Jira
                                     Ticket
How to Run
1. Install Dependencies
pip install -r requirements.txt
2. Install and Start Ollama
ollama pull mistral
ollama run mistral
3. Set Environment Variables
SCALEDOWN_API_KEY=your_key
SCALEDOWN_BASE_URL=your_url
JIRA_API_KEY=your_jira_key
4. Run the Application
CLI:

python app.py
Web UI:

streamlit run ui/web_app.py
Key Benefits
Compresses logs by up to 85%

Reduces manual troubleshooting effort

Retrieves historically proven fixes

Intelligent confidence-based escalation

Processes sensitive logs locally

Simulated 50% reduction in MTTR

Limitations
Dependent on knowledge base quality

Similarity search may miss novel issues

Confidence scoring requires tuning

Relies on ScaleDown API availability

Not a full ITSM replacement

Conclusion
This system demonstrates a practical enterprise troubleshooting pipeline using dual-agent AI, semantic retrieval, controlled escalation, and real-world workflow integration.

