"""
MedTrust — Production Case Similarity & Intelligence System
(src/similarity/__init__.py)
"""

from src.similarity.report_schema import (
    CANONICAL_DISEASES,
    SCHEMA_VERSION,
    create_reference_report,
    validate_reference_report,
)
from src.similarity.embedding_index import PersistentEmbeddingIndex
from src.similarity.evidence_engine import (
    EvidenceComparisonEngine,
    STANDARD_DISCLAIMER,
    METHODOLOGICAL_EXPLANATION,
)
from src.similarity.feature_extractor import DenseNetSimilarityExtractor
from src.similarity.retrieval_engine import (
    SimilarityRetrievalEngine,
    SimilarityRetrievalEngineV2,
)
from src.similarity.similarity_analyzer import SimilarityAnalyzer
from src.similarity.builder import ReferenceLibraryBuilder
from src.similarity.service import (
    get_embedding_index,
    get_embedding_index_v2,
    get_similarity_engine,
    get_similarity_engine_v2,
    get_reference_case_report,
    get_index_health,
    get_v2_index_health,
)

__all__ = [
    "CANONICAL_DISEASES",
    "SCHEMA_VERSION",
    "create_reference_report",
    "validate_reference_report",
    "PersistentEmbeddingIndex",
    "EvidenceComparisonEngine",
    "STANDARD_DISCLAIMER",
    "METHODOLOGICAL_EXPLANATION",
    "DenseNetSimilarityExtractor",
    "SimilarityRetrievalEngine",
    "SimilarityRetrievalEngineV2",
    "SimilarityAnalyzer",
    "ReferenceLibraryBuilder",
    "get_embedding_index",
    "get_embedding_index_v2",
    "get_similarity_engine",
    "get_similarity_engine_v2",
    "get_reference_case_report",
    "get_index_health",
    "get_v2_index_health",
]
