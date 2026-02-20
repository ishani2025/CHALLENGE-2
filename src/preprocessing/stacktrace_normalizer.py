import re
from typing import List
def normalize_stack_trace(stack_trace_lines: List[str]) -> List[str]:
    cleaned_lines = []
    for line in stack_trace_lines:
        line = re.sub(r':\d+', '', line)
        line = re.sub(r'\$\$Lambda\$\d+\/\d+', '$$Lambda', line)
        line = re.sub(r'\(.*?\)', '', line)
        cleaned_lines.append(line.strip())
    return cleaned_lines
