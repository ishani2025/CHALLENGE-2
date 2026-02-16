import streamlit as st
import time
import sys
import os

sys.path.append(os.path.abspath("."))

from src.retrieval.search import Retriever
from src.llm.client_llm import OllamaClient
from src.agents.agent1 import Agent1
from src.agents.agent2 import Agent2
from src.compression.log_compressor import ScaleDownClient
st.markdown("""
<style>

/* Global App Background */
.stApp {
    background-color: #0B0F1A;   /* deep dark */
    color: #E5E7EB;
}

/* Title Styling */
h1, h2, h3 {
    color: #F9FAFB;
}

/* Buttons — CodeChef Red */
div.stButton > button {
    background-color: #B91C1C;   /* deep red */
    color: white;
    font-weight: 600;
    border-radius: 10px;
    padding: 0.6em 1.4em;
    border: none;
    transition: all 0.2s ease-in-out;
}

/* Button Hover Effect */
div.stButton > button:hover {
    background-color: #DC2626;   /* brighter red */
    transform: scale(1.03);
}

/* Text Area */
textarea {
    background-color: #111827;
    color: #F3F4F6;
    border-radius: 10px;
    border: 1px solid #1F2933;
}

/* Metric Cards */
[data-testid="stMetric"] {
    background-color: #111827;
    padding: 12px;
    border-radius: 12px;
    border: 1px solid #1F2933;
}

/* Success / Warning / Error Boxes */
[data-testid="stAlert"] {
    border-radius: 10px;
}

/* Divider */
hr {
    border-color: #1F2933;
}

</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
         .stApp{
            background-color: #0E1117;
    color: white;
            }
div.stButton > button {
    background-color: #007BFF;
    color: white;
    font-weight: 600;
    border-radius: 8px;
    padding: 0.5em 1.2em;
}
div.stButton > button:hover {
    background-color: #0056b3;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# Initialize components
retriever = Retriever()
compressor = ScaleDownClient()
llm = OllamaClient()

agent1 = Agent1(retriever, compressor, llm)

agent2 = Agent2(retriever)


st.set_page_config(page_title="LogSentiel-AI IT Troubleshooter", layout="wide")

st.title("🚀LogSentiel:AI-Powered IT Troubleshooting System")
st.markdown("RAG + Compression + Validation + Escalation")

st.divider()

error_log = st.text_area("📥 Paste Error Log Here", height=250)

if st.button("Analyze Error"):

    if not error_log.strip():
        st.warning("Please paste an error log.")
    else:

        start_time = time.time()

        # Agent 1
        result1 = agent1.run(error_log)

        # Agent 2
        result2 = agent2.evaluate(error_log, result1)

        total_time = round(time.time() - start_time, 2)

        st.subheader("🔎 Retrieved Cases")
        for i, case in enumerate(result1["retrieved_cases"]):
            st.write(f"Case {i+1}: {case.get('error_type')}")

        st.divider()

        st.subheader("🤖 Proposed Solution")
        st.write(result1["draft_solution"])

        st.divider()

        st.subheader("🧠 Confidence Assessment")

        if result2["confidence"] == "CONFIDENT":
            st.success("CONFIDENT – Proceed")
        elif result2["confidence"] == "MEDIUM":
            st.warning("MEDIUM – Human Review Recommended")
        else:
            st.error("WEAK – Human Intervention Required")

        st.write("Reason:", result2["reason"])
        st.subheader("📊 System Metrics")
        col1, col2, col3 = st.columns(3)
        col1.metric("Original Tokens", result1["original_tokens"])
        col2.metric("Compressed Tokens", result1["compressed_tokens"])
        col3.metric("Compression Ratio", result1["compression_ratio"])
        st.divider()
        col4, col5, col6 = st.columns(3)
        col4.metric("Retrieval Time (s)", result1["retrieval_time"])
        col5.metric("LLM Time (s)", result1["llm_time"])
        col6.metric("Total Time (s)", result1["total_time"])
