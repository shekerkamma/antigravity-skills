import os
from typing import Dict, Any, Optional, List

class SemanticCache:
    """
    SemanticCache implements token cost optimization (Trend 6) by storing
    past tickets and their generated solutions. If a new query is semantically
    similar to a cached one, it returns the cached result, saving API costs.
    It uses a hybrid model: Cosine similarity on embeddings if API is available,
    falling back to Jaccard word-overlap similarity offline.
    """
    def __init__(self, threshold: float = 0.85):
        self.threshold = threshold
        # Schema: {"text": str, "embedding": List[float], "value": Dict[str, Any]}
        self.cache: List[Dict[str, Any]] = []

    def _jaccard_similarity(self, s1: str, s2: str) -> float:
        """Fallback word-overlap similarity calculation (no API costs)."""
        words1 = set(s1.lower().split())
        words2 = set(s2.lower().split())
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        if not union:
            return 0.0
        return len(intersection) / len(union)

    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Pure-Python Cosine similarity (no numpy dependency needed)."""
        dot_product = sum(x * y for x, y in zip(a, b))
        norm_a = sum(x * x for x in a) ** 0.5
        norm_b = sum(x * x for x in b) ** 0.5
        if not norm_a or not norm_b:
            return 0.0
        return dot_product / (norm_a * norm_b)

    def lookup(self, query: str, query_embedding: Optional[List[float]] = None) -> Optional[Dict[str, Any]]:
        """
        Looks up query in the semantic cache.
        Returns the cached value if similarity exceeds threshold.
        """
        best_score = 0.0
        best_match = None

        for item in self.cache:
            if query_embedding and item["embedding"]:
                score = self._cosine_similarity(query_embedding, item["embedding"])
            else:
                score = self._jaccard_similarity(query, item["text"])
            
            if score > best_score:
                best_score = score
                best_match = item

        if best_score >= self.threshold and best_match:
            print(f"[SemanticCache] Cache HIT (similarity score: {best_score:.4f})")
            return best_match["value"]
        
        print(f"[SemanticCache] Cache MISS (best similarity score: {best_score:.4f})")
        return None

    def store(self, query: str, value: Dict[str, Any], embedding: Optional[List[float]] = None) -> None:
        """Stores a query and its enriched result in the cache."""
        self.cache.append({
            "text": query,
            "embedding": embedding,
            "value": value
        })
        print(f"[SemanticCache] Cached new query (cache size: {len(self.cache)})")
