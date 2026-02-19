"""
Dataset normalization pipeline.

Purpose:
- Canonicalize error types
- Remove stack trace noise
- Standardize retrieval text
- Improve embedding quality

This deterministic preprocessing step is REQUIRED before vector indexing.
"""

import json
import re
from pathlib import Path


INPUT_FILE = Path("data/kb_issues/final_dataset_agent1.json")
OUTPUT_FILE = Path("data/kb_issues/final_dataset_agent1_cleaned.json")

ERROR_REGEX = r'([a-zA-Z0-9_.]+(?:Exception|Error))'
JAVA_FRAME_REGEX = r'\s*at\s+.+\(.+:\d+\)'
PYTHON_FRAME_REGEX = r'\s*File\s+".+",\s+line\s+\d+'


NOISE_PREFIXES = (
    "##",
    "Environment",
    "Steps to",
    "Expected",
    "Actual",
    "Description",
)


# -------------------------------------------------
# Error Type Normalization
# -------------------------------------------------
def normalize_error_type(raw_error):

    if not raw_error:
        return "UnknownError"

    matches = re.findall(ERROR_REGEX, raw_error)

    if matches:
        return matches[0]

    return raw_error.strip()


# -------------------------------------------------
# Stack Trace Cleaning
# -------------------------------------------------
def clean_stack_trace(stack_lines):

    if not stack_lines:
        return []

    cleaned = []

    for line in stack_lines:

        line = line.strip()

        if not line:
            continue

        if line.startswith(NOISE_PREFIXES):
            continue

        if (
            re.search(ERROR_REGEX, line)
            or re.search(JAVA_FRAME_REGEX, line)
            or re.search(PYTHON_FRAME_REGEX, line)
            or "Caused by" in line
        ):
            cleaned.append(line)

    return cleaned


# -------------------------------------------------
# Stack Summary Builder (Important for embeddings)
# -------------------------------------------------
def build_stack_summary(stack_lines):

    if not stack_lines:
        return ""

    exception_lines = []
    caused_by_lines = []

    for line in stack_lines:

        if "Exception" in line or "Error" in line:
            exception_lines.append(line)

        if "Caused by" in line:
            caused_by_lines.append(line)

    tail_frames = stack_lines[-4:]

    summary = (
        exception_lines[:2]
        + caused_by_lines[:2]
        + tail_frames
    )

    return "\n".join(summary)


# -------------------------------------------------
# Knowledge Text Rebuilder
# -------------------------------------------------
def rebuild_knowledge_text(entry):

    stack_summary = build_stack_summary(entry.get("stack_trace", []))

    return (
        f"Error Type: {entry.get('error_type')}\n"
        f"{stack_summary}\n"
        f"Root Cause: {entry.get('root_cause')}\n"
    )


# -------------------------------------------------
# Main Cleaning Routine
# -------------------------------------------------
def main():

    print("Loading dataset...")

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    cleaned_data = []

    for entry in data:

        entry["error_type"] = normalize_error_type(
            entry.get("error_type")
        )

        entry["stack_trace"] = clean_stack_trace(
            entry.get("stack_trace", [])
        )

        if not entry.get("root_cause"):
            entry["root_cause"] = "Root cause not explicitly documented."

        entry["knowledge_text"] = rebuild_knowledge_text(entry)

        cleaned_data.append(entry)

    print("Writing cleaned dataset...")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(cleaned_data, f, indent=2)

    print("✅ Dataset normalization complete.")
    print(f"Output file: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
