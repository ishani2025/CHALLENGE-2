class Agent2:

    def __init__(self, retriever):
        self.retriever = retriever

    def evaluate(self, original_log, agent1_output):
        retrieved_cases = agent1_output["retrieved_cases"]
        solution = agent1_output["draft_solution"]
        error_type = agent1_output.get("error_type", "UnknownError")
        score = 0
        match_count = sum(
            1 for case in retrieved_cases
            if case.get("error_type") == error_type
    )
        if match_count >= 2:
            score += 2
        elif match_count == 1:
            score += 1
        for line in original_log.splitlines():
            if ".java:" in line or ".py" in line:
                if line.split("(")[0].split()[-1] in solution:
                    score += 1
                    break
        if any(word in solution.lower() for word in ["null", "memory", "dependency", "import", "cast"]):
            score += 1
        if score >= 3:
            return {"confidence": "CONFIDENT", "reason": "Strong structured and semantic alignment."}
        elif score == 2:
            return {"confidence": "MEDIUM", "reason": "Partial grounding detected."}
        else:
            return {"confidence": "WEAK", "reason": "Insufficient grounding or matching."}
