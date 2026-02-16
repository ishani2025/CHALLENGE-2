import requests
import json
import re
import time
import os
from dotenv import load_dotenv
import os

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {GITHUB_TOKEN}"
}

SEARCH_URL = "https://api.github.com/search/issues"
def fetch_java_issues(pages=5):
    all_items = []

    for page in range(1, pages + 1):
        print(f"Fetching page {page}...")

        params = {
            "q": 'is:issue is:closed "Exception in thread" language:Java',
            "per_page": 100,
            "page": page
        }

        response = requests.get(SEARCH_URL, headers=HEADERS, params=params)

        if response.status_code != 200:
            print("Error:", response.status_code, response.text)
            break

        data = response.json()
        items = data.get("items", [])
        all_items.extend(items)

        time.sleep(1)

    print("Total GitHub issues fetched:", len(all_items))
    return all_items
def is_real_stack_trace(text):
    return (
        re.search(r'Exception|Error', text) and
        re.search(r'\n\s*at\s+[a-zA-Z0-9_.]+', text)
    )


def extract_error_type(text):
    match = re.search(r'([a-zA-Z0-9_.]+(?:Exception|Error))', text)
    return match.group(1) if match else "UnknownError"
def process_github_java():
    issues = fetch_java_issues(pages=8)

    structured = []

    for issue in issues:
        body = issue.get("body", "")
        if not body:
            continue

        if is_real_stack_trace(body):
            error_type = extract_error_type(body)

            structured.append({
                "title": issue.get("title"),
                "error_type": error_type,
                "stack_trace": body.split("\n"),
                "source": "GitHub"
            })

    print("Extracted Java stack traces:", len(structured))

    BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)
    output_dir = os.path.join(BASE_DIR, "data", "kb_issues")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "github_java_structured.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(structured, f, indent=2)
    print("Saved to:", output_file)


    print("Saved to data/kb_issues/github_java_structured.json")
if __name__ == "__main__":
    process_github_java()
