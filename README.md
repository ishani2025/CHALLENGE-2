# 🤖   LogSentiel

<div align="center"> <b>LogSentinel</b> <p><strong>Dual-Agent AI System for Enterprise IT Troubleshooting</strong></p> <p> <img src="https://img.shields.io/badge/Python-3.8+-blue" alt="Python Version"/> <img src="https://img.shields.io/badge/LLM-Ollama%20(Mistral)-green" alt="LLM"/> <img src="https://img.shields.io/badge/API-ScaleDown-orange" alt="ScaleDown API"/> <img src="https://img.shields.io/badge/License-MIT-yellow" alt="License"/> <img src="https://img.shields.io/badge/Status-Active-success" alt="Status"/> </p> </div>

## 🌟 Overview
LogSentinel is an enterprise-grade troubleshooting assistant that analyzes large error logs (10,000+ lines), retrieves similar historical issues, generates structured step-by-step solutions, and intelligently escalates low-confidence cases.

It combines:
   - ScaleDown API for log compression
   - Local LLM (Ollama + Mistral) for reasoning
   - Embedding-based similarity search
   - Confidence-driven escalation workflow
   - Optional Jira integration

### 🎯 Key Features

- 🧠 Dual-Agent Architecture (Log Analyst + Solution Engineer)
- 💭Log Compression (~85% reduction via ScaleDown)
- 🔎 Semantic Similarity Search (StackOverflow, GitHub, Runbooks)
- 📊 Confidence-Based Decision Engine
- 🔄 Automated Escalation to Jira
- 🏠 Local LLM Processing (Sensitive logs stay local)
- 📈 MTTR Tracking & Observability

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Ollama installed
- Mistral model pulled
- ScaleDown API Key
- Optional: Jira API credentials

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ishani2025/CHALLENGE-2.git
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install & Start Ollama**
   ```bash 
   ollama pull mistral
   ollama run  mistral
   ```

4. **Configure Environment Variables**
   ```bash
   Create a .env file and in that have:
   SCALEDOWN_API_KEY=your_key
   SCALEDOWN_BASE_URL=your_url
   JIRA_API_KEY=your_jira_key
   ```



## 🏗️ Architecture

```
LogSentiel
├── src/
│   ├── agents/
│   │   ├── agent1.py
│   │   ├── agent2.py
│   │------llm/
│   ├── embeddings/
│   │   ├── __init__t.py     
│   │   ├── embedder.py       
│   │   └── vector_store.py    
│   ├── utils/
│   │   ├── file_utils.py        
│   │   └── logger.py       
│   └── decision/
│       └── decision_controller.py    
├── data/
│   ├──compressed_logs/              
│   └── raw_logs/            
├── tests/
├──assessts/
└── config/
├── requirements.txt
└── app.py
```

## 🤖 Dual-Agent Logic

### Agent 1 – Log Analyst
- Calls ScaleDown API
- Reduces noise
- Extracts primary error signals
- Categorizes failure type
### Agent 2 – Solution Engineer
- Retrieves similar historical cases
- Generates grounded resolution steps
- Computes confidence score

## 💬 Confidence Thresholds
```bash 
   Score     | Action         
   | ------- | -------------- |
   | ≥ 0.85  | Auto Resolve   |
   | 0.65–0.85 | Suggest Review |
   | < 0.65  | Escalate       |
```
## 📊 Metrics & Observability

The system tracks:
- Compression Ratio
- Resolution Success Rate
- Escalation Frequency
- Estimated MTTR Reduction
## 🔧 Running the Application
CLI Mode:
```bash
python app.py
```
Web Interface:
```bash
streamlit run ui/web_app.py
```
## 📈 Benefits
- Reduces log size by up to 85%
- Accelerates troubleshooting workflows
- Minimizes unnecessary escalations
- Keeps sensitive data local
- Structured enterprise-aligned pipeline

## ⚠️ Limitations

- Depends on knowledge base quality
- Confidence scoring requires tuning
- Novel errors may not match historical cases
- Not a full ITSM replacement
- Relies on ScaleDown API availability

🧪
---
