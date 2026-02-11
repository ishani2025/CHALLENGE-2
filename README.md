Technical Troubleshooting Guide
Dual-agent AI system for enterprise IT troubleshooting using ScaleDown, local LLM (Ollama), semantic retrieval, and automated escalation.

Problem
Enterprise logs often exceed 10,000+ lines and contain repetitive stack traces and noise. Engineers manually analyze logs, search forums, and escalate unresolved issues, increasing Mean Time to Resolution (MTTR).

Solution
This system automates enterprise troubleshooting by:

Compressing large logs using ScaleDown API

Extracting dominant errors with a local LLM

Retrieving similar historical issues using embeddings

Generating step-by-step solutions

Computing confidence scores

Escalating low-confidence cases to Jira

Architecture Workflow
Large Log
   ↓
ScaleDown API (Compression)
   ↓
Agent 1 – Log Analysis
   ↓
Similarity Search (Knowledge Base)
   ↓
Agent 2 – Solution + Confidence
   ↓
Decision Engine
   ├── Auto Resolve
   ├── Suggest Review
   └── Escalate → Jira Ticket
Features
Dual-agent reasoning architecture

Local LLM processing (Ollama + Mistral)

Embedding-based similarity search

Confidence-driven escalation workflow

Optional Slack & Jira integration

MTTR tracking and compression metrics

How to Run
1. Install dependencies
pip install -r requirements.txt
2. Install and run Ollama
ollama pull mistral
ollama run mistral
3. Set environment variables
SCALEDOWN_API_KEY=your_key
SCALEDOWN_BASE_URL=your_url
JIRA_API_KEY=your_key
4. Start application
python app.py
or

streamlit run ui/web_app.py
Benefits
Reduces log size by ~85%

Decreases troubleshooting time

Minimizes unnecessary escalations

Keeps sensitive logs local

Structured, enterprise-ready workflow

Limitations
Performance depends on knowledge base quality

Confidence thresholds require tuning

Not a full ITSM replacement

Dependent on ScaleDown API availability

Tech Stack
Python

Ollama (Local LLM)

ScaleDown API

Sentence Transformers

Streamlit

Jira REST API

If you want, I can now:

Add GitHub badges

Add a clean project tree section

Or make it recruiter-optimized in under 15 lines

