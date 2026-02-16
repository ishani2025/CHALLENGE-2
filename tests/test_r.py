import sys
import os
import json

sys.path.append(os.path.abspath("."))

from src.retrieval.search import Retriever   # replace correctly

# Load one sample log
with open("data/kb_issues/final_dataset_agent1.json", "r", encoding="utf-8") as f:
    data = json.load(f)

entry = data[0]
sample_query = "\n".join(entry["stack_trace"])

retriever = Retriever()

results = retriever.retrieve(sample_query, top_k=3)

print("\n=== RETRIEVER OUTPUT ===\n")

print("Type of results:", type(results))

if results:
    print("Type of first result:", type(results[0]))
    print("\nFirst result keys:")
    print(results[0].keys())
else:
    print("No results returned.")
