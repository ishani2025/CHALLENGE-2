import streamlit as st
import time
import sys
import os
st.set_page_config(
    page_title="LogSentiel-AI IT Troubleshooter",
    layout="wide"
)

sys.path.append(os.path.abspath("."))

from src.retrieval.search import Retriever
from src.llm.client_llm import OllamaClient
from src.agents.agent1 import Agent1
from src.agents.agent2 import Agent2
from src.compression.log_compressor import ScaleDownClient

# -----------------------------
# Cached Resource Loaders
# -----------------------------

@st.cache_resource
def load_retriever():
    return Retriever()

@st.cache_resource
def load_compressor():
    return ScaleDownClient()

@st.cache_resource
def load_llm():
    return OllamaClient()

@st.cache_resource
def load_agent1():
    return Agent1(load_retriever(), load_compressor(), load_llm())

@st.cache_resource
def load_agent2():
    return Agent2(load_retriever())

retriever = load_retriever()
compressor = load_compressor()
llm = load_llm()

agent1 = load_agent1()
agent2 = load_agent2()
st.markdown("""
<style>
.stApp {
    background-color: #0B0F1A;
    color: #E5E7EB;
}
h1, h2, h3 {
    color: #F9FAFB;
}
div.stButton > button {
    background-color: #B91C1C;
    color: white;
    font-weight: 600;
    border-radius: 10px;
    padding: 0.6em 1.4em;
    border: none;
}
div.stButton > button:hover {
    background-color: #DC2626;
}
textarea {
    background-color: #fff !important;
    color: #222 !important;
}
label[for^="📥 Paste Error Log Here"] {
    color: white !important;
    font-weight: 600;
    font-size: 1.1em;
}
[data-testid="stMetric"] {
    background-color: white !important;
    padding: 12px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

st.title("🚀 LogSentiel: AI-Powered IT Troubleshooting System")
st.markdown("RAG + Compression + Validation + Escalation")
st.divider()

error_log = st.text_area("📥 Paste Error Log Here", height=250)

if st.button("Analyze Error"):

    if not error_log.strip():
        st.warning("Please paste an error log.")
        st.stop()
    
    start_time = time.time()
    result1 = agent1.run(error_log)

    if not result1["retrieved_cases"]:
        st.error("No sufficiently similar historical cases found.")
        st.stop()
    result2 = agent2.evaluate(error_log, result1)

    total_time = round(time.time() - start_time, 2)
    st.subheader("🔎 Retrieved Cases")
    for i, case in enumerate(result1["retrieved_cases"]):
        similarity = case.get("similarity", 0.0)
        st.markdown(f"""
        **Case {i+1}**
        * Exception Type: `{case.get('error_type', 'Unknown')}`  
        * Similarity Score: **{similarity:.3f}**
        """)
        if case.get("root_cause"):
            st.markdown(f"• Root Cause: {case['root_cause']}")
        st.divider()
    

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
