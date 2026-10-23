"""
MedTrust — Similarity Subsystem Service
(src/similarity/service.py)

Provides singleton service instances and health monitoring for Similarity Analyzer.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

from src.similarity.embedding_index import PersistentEmbeddingIndex
from src.similarity.evidence_engine import EvidenceComparisonEngine
from src.similarity.retrieval_engine import SimilarityRetrievalEngine

_INDEX_INSTANCE: Optional[PersistentEmbeddingIndex] = None
_ENGINE_INSTANCE: Optional[SimilarityRetrievalEngine] = None


def get_embedding_index() -> PersistentEmbeddingIndex:
    """Get or initialize singleton PersistentEmbeddingIndex."""
    global _INDEX_INSTANCE
    if _INDEX_INSTANCE is None:
        _INDEX_INSTANCE = PersistentEmbeddingIndex()
    return _INDEX_INSTANCE


# Alias for backward compatibility
get_embedding_index_v2 = get_embedding_index


def get_similarity_engine() -> SimilarityRetrievalEngine:
    """Get or initialize singleton SimilarityRetrievalEngine."""
    global _ENGINE_INSTANCE
    if _ENGINE_INSTANCE is None:
        idx = get_embedding_index()
        ev_eng = EvidenceComparisonEngine()
        _ENGINE_INSTANCE = SimilarityRetrievalEngine(index=idx, evidence_engine=ev_eng)
    return _ENGINE_INSTANCE


# Alias for backward compatibility
get_similarity_engine_v2 = get_similarity_engine


def get_reference_case_report(reference_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve structured reference report for a given case ID."""
    engine = get_similarity_engine()
    return engine.get_reference_report(reference_id)


def get_index_health() -> Dict[str, Any]:
    """Return health and readiness report for the reference intelligence library."""
    idx = get_embedding_index()
    integrity = idx.verify_integrity(verify_hashes=True)

    reports_dir = Path(idx.index_path).parent / "reference_reports"
    report_count = len(list(reports_dir.glob("*.json"))) if reports_dir.exists() else 0

    return {
        "status": "HEALTHY" if integrity.get("valid") else "UNHEALTHY",
        "version": "2.0.0",
        "indexed_cases": integrity.get("count", 0),
        "embedding_dimension": integrity.get("dimension", 1024),
        "is_unit_normalized": integrity.get("is_normalized", False),
        "reports_available": report_count,
        "hashes_verified": integrity.get("hashes_verified", False),
        "requires_original_images": False,
        "errors": integrity.get("errors", []),
    }


# Alias for backward compatibility
get_v2_index_health = get_index_health
