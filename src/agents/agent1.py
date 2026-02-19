
from src.preprocessing.error_extractor import extract_exception_hierarchy
from src.retrieval.search import Retriever
import time
class Agent1:
    
    def __init__(self, retriever, compressor, llm):
        self.retriever = retriever
        self.compressor = compressor
        self.llm = llm

    def run(self, error_log: str):

        start_total = time.time()

        # ----------------------
        # Token Count
        # ----------------------
        original_tokens = len(error_log.split())

        # ----------------------
        # Compression
        # ----------------------
        start_compress = time.time()
        compressed_log, compression_ratio = self.compressor.compress(error_log)
        compression_time = round(time.time() - start_compress, 3)
        compressed_tokens = len(compressed_log.split())


        # ----------------------
        # Retrieval
        # ----------------------
        retrieval_output = self.retriever.retrieve(
            compressed_log, top_k=3
        )

        retrieved_cases = retrieval_output["results"]
        retrieval_time = retrieval_output["retrieval_time"]

        # ----------------------
        # Build Context
        # ----------------------
        knowledge_block = ""

        for case in retrieved_cases:
            knowledge_block += f"""
Error Type: {case.get("error_type")}
Root Cause: {case.get("root_cause")}
Solution Steps: {case.get("solution_steps")}
Prevention: {case.get("prevention_best_practices")}
---
"""


        prompt = f"""
You are a production IT troubleshooting engineer.
You must base your reasoning strictly on the reference cases.
Explain the meaning of the exception message if present.
If the reference cases do not sufficiently match,
respond exactly with:

INSUFFICIENT MATCHING REFERENCE CASE

Error Log:
{compressed_log}

Reference Cases:
{knowledge_block}

Provide:

Root Cause:
Step-by-Step Resolution:
Preventive Measures:
"""

        hierarchy = extract_exception_hierarchy(compressed_log)
        error_type = hierarchy["primary_exception"]

        start_llm = time.time()
        response = self.llm.generate(prompt, temperature=0.2)
        llm_time = round(time.time() - start_llm, 3)

        total_time = round(time.time() - start_total, 3)

        return {
            "error_type":error_type,
            "retrieved_cases": retrieved_cases,
            "draft_solution": response,
            "original_tokens": original_tokens,
            "compressed_tokens": compressed_tokens,
            "compression_ratio": compression_ratio,
            "retrieval_time": retrieval_time,
            "llm_time": llm_time,
            "total_time": total_time
        }
