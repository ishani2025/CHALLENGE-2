import json
import numpy as np
import faiss
import re
import time
from sentence_transformers import SentenceTransformer
from src.preprocessing.error_extractor import build_retrieval_query

JAVA_ERROR_REGEX = r'([a-zA-Z0-9_.]+(?:Exception|Error))'
PYTHON_ERROR_REGEX = r'([a-zA-Z0-9_.]+(?:Error|Exception))'


class Retriever:

    def __init__(
        self,
        dataset_path="data/kb_issues/final_dataset_agent1_cleaned.json",
        model_name="all-MiniLM-L6-v2"
    ):

        self.model = SentenceTransformer(model_name)

        with open(dataset_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

        self.documents = [self._build_document(entry) for entry in self.data]

        self.embeddings = self.model.encode(
            self.documents,
            convert_to_numpy=True,
            show_progress_bar=True
        )

        self.embeddings = self._normalize(self.embeddings)

        dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(self.embeddings)

    def _normalize(self, vectors):
        return vectors / np.linalg.norm(vectors, axis=1, keepdims=True)
    def _extract_error_type(self, text):

        matches = re.findall(JAVA_ERROR_REGEX, text)
        if matches:
            return matches[0]

        matches = re.findall(PYTHON_ERROR_REGEX, text)
        if matches:
            return matches[-1]

        return None
    def _build_stack_summary(self, stack_lines):

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
    def _build_document(self, entry):

        stack_preview = self._build_stack_summary(
            entry.get("stack_trace", [])
        )

        return (
            f"Error Type: {entry.get('error_type')}\n"
            f"{stack_preview}\n"
            f"Root Cause: {entry.get('root_cause')}\n"
        )
    def retrieve(self, query, top_k=3):

        start_time = time.time()
        query_text = build_retrieval_query(query)
        query_embedding = self.model.encode(
            [query_text],convert_to_numpy=True)
        query_embedding = self._normalize(query_embedding)
        detected_error = self._extract_error_type(query)
        if detected_error:

            strict_matches = [
                i for i, entry in enumerate(self.data)
                if entry.get("error_type", "").lower() == detected_error.lower()
            ]

            if len(strict_matches) >= top_k:
                return self._semantic_subset_search(
                    strict_matches,
                    query_embedding,
                    start_time,
                    mode="strict_structured+semantic"
                )
            partial_matches = [
                i for i, entry in enumerate(self.data)
                if detected_error.lower() in entry.get("error_type", "").lower()
            ]

            if len(partial_matches) >= top_k:
                return self._semantic_subset_search(
                    partial_matches,
                    query_embedding,
                    start_time,
                    mode="partial_structured+semantic"
                )
            distances, indices = self.index.search(query_embedding, top_k)
            MIN_SIMILARITY = 0.35
            scored_results = [
                {
                    **self.data[idx],
                    "similarity": float(score)
                }
                for score, idx in zip(distances[0], indices[0])
                if score > MIN_SIMILARITY
                ]
            retrieval_time = round(time.time() - start_time, 3)
            return {
                "results": scored_results,
                "retrieval_time": retrieval_time,
                "filtered_count": len(scored_results),
                "mode": "semantic_only"
                }
    def _semantic_subset_search(self, subset_indices, query_embedding, start_time, mode):

        subset_embeddings = self.embeddings[subset_indices]

        scores = np.dot(subset_embeddings, query_embedding.T).flatten()

        top_local_indices = np.argsort(-scores)[:len(subset_indices)]

        MIN_SIMILARITY = 0.35

        results = [
            {
                **self.data[subset_indices[i]],
                "similarity": float(scores[i])
            }
            for i in top_local_indices
            if scores[i] > MIN_SIMILARITY
            ]

        retrieval_time = round(time.time() - start_time, 3)

        return {
            "results": results,
            "retrieval_time": retrieval_time,
            "filtered_count": len(results),
            "mode": mode
        }
