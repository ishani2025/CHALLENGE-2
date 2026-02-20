import re
from typing import Dict, List

EXCEPTION_REGEX = re.compile(r'([\w\.]+Exception|[\w\.]+Error)')
def extract_exception_hierarchy(log: str) -> Dict:
    parts = log.split("Caused by:")

    primary_block = parts[0]
    cause_blocks = parts[1:]

    primary_match = EXCEPTION_REGEX.search(primary_block)
    primary_exception = primary_match.group(0) if primary_match else "UnknownException"

    message_match = re.search(rf'{primary_exception}:\s*(.*)', primary_block)
    primary_message = message_match.group(1).strip() if message_match else ""

    cause_chain: List[str] = []
    for block in cause_blocks:
        cause_match = EXCEPTION_REGEX.search(block)
        if cause_match:
            cause_chain.append(cause_match.group(0))

    return {
        "primary_exception": primary_exception,
        "primary_message": primary_message,
        "cause_chain": cause_chain
    }
def build_retrieval_query(log: str) -> str:

    data = extract_exception_hierarchy(log)

    components = [
        data["primary_exception"],
        data["primary_message"],
        *data["cause_chain"],
        log
    ]

    return " | ".join(filter(None, components))