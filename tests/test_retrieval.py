import sys
import os

sys.path.append(os.path.abspath("."))

from src.retrieval.search import Retriever

retriever = Retriever()

query = """
Exception in thread "main" java.lang.NullPointerException
    at com.example.service.UserService.getUser(UserService.java:48)
"""

results = retriever.retrieve(query, top_k=3)

print("\n=== RETRIEVAL RESULTS ===\n")

for i, r in enumerate(results):
    print(f"\nResult {i+1}:")
    print("Error Type:", r.get("error_type"))
