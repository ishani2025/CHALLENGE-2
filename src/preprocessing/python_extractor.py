import requests
import json
import re
import time
import os

STACKEXCHANGE_URL = "https://api.stackexchange.com/2.3/search/advanced"
def fetch_python_posts(pages=5):
    all_items = []

    for page in range(1, pages + 1):
        print(f"Fetching page {page}...")

        params = {
            "order": "desc",
            "sort": "relevance",
            "q": '"Traceback (most recent call last)"',
            "tagged": "python",
            "pagesize": 100,
            "page": page,
            "site": "stackoverflow",
            "filter": "withbody"
        }
        response = requests.get(STACKEXCHANGE_URL, params=params)
        data = response.json()

        items = data.get("items", [])
        all_items.extend(items)

        time.sleep(1)  # avoid rate limits

    print("Total posts fetched:", len(all_items))
    return all_items
def is_real_python_traceback(text):
    return (
        "Traceback (most recent call last)" in text and
        re.search(r'\n\s*File\s+"', text) and
        re.search(r'(Error|Exception)', text)
    )


def extract_error_type(trace):
    match = re.search(r'([A-Za-z_]+Error|[A-Za-z_]+Exception)', trace)
    return match.group(1) if match else "UnknownError"


def extract_code_blocks(body_html):
    blocks = re.findall(
        r'<pre.*?><code>(.*?)</code></pre>',
        body_html,
        re.DOTALL
    )

    cleaned = []

    for block in blocks:
        block = block.replace("&quot;", '"')
        block = block.replace("&lt;", "<")
        block = block.replace("&gt;", ">")
        block = block.replace("&amp;", "&")

        block = re.sub(r'<.*?>', '', block)
        cleaned.append(block.strip())

    return cleaned
def process_python_so():

    items = fetch_python_posts(pages=8)

    structured = []

    for item in items:
        body = item.get("body", "")
        code_blocks = extract_code_blocks(body)

        for block in code_blocks:
            if is_real_python_traceback(block):
                error_type = extract_error_type(block)

                structured.append({
                    "title": item.get("title"),
                    "error_type": error_type,
                    "stack_trace": block.split("\n"),
                    "tags": item.get("tags", []),
                    "source": "StackOverflow"
                })

    print("Total extracted Python stack traces:", len(structured))

    os.makedirs("data/kb_issues", exist_ok=True)

    with open("data/kb_issues/python_structured.json", "w", encoding="utf-8") as f:
        json.dump(structured, f, indent=2)

    print("Saved to data/kb_issues/python_structured.json")


# ------------------------------------------------------------
if __name__ == "__main__":
    process_python_so()
