import sys,os
sys.path.append(os.path.abspath("."))
from src.retrieval.search import Retriever
from src.llm.client_llm import OllamaClient
from src.agents.agent1 import Agent1

retriever = Retriever()
llm = OllamaClient()
agent = Agent1(retriever, llm)

python_log = """
Traceback (most recent call last):
  File "app.py", line 3, in <module>
ModuleNotFoundError: No module named 'requests'
"""

result = agent.run(python_log)

print(result["draft_solution"])
