"""
MedTrust — Case-Based Similarity Analyzer
(src/similarity/similarity_analyzer.py)

Unified analyzer for case-based radiograph similarity retrieval.
Delegates to SimilarityRetrievalEngine against the 2,500-case authentic reference repository.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Union
import numpy as np
import torch
import torch.nn as nn
from PIL import Image

from src.similarity.feature_extractor import DenseNetSimilarityExtractor
from src.similarity.retrieval_engine import SimilarityRetrievalEngine
from src.similarity.service import get_similarity_engine


class SimilarityAnalyzer:
    """
    Case-based radiograph similarity analyzer for MedTrust.
    """

    def __init__(
        self,
        extractor: Optional[DenseNetSimilarityExtractor] = None,
        model: Optional[nn.Module] = None,
        device: Optional[torch.device] = None,
        engine: Optional[SimilarityRetrievalEngine] = None,
    ) -> None:
        self.device = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")
        if extractor is not None:
            self.extractor = extractor
        else:
            self.extractor = DenseNetSimilarityExtractor(model=model, device=self.device)

        if engine is not None:
            self.engine = engine
            self.engine._extractor = self.extractor
        else:
            self.engine = get_similarity_engine()
            self.engine._extractor = self.extractor

    def find_similar_cases(
        self,
        image_input: Union[str, Path, bytes, Image.Image, torch.Tensor],
        top_k: int = 5,
        predicted_findings: Optional[Sequence[str]] = None,
        primary_finding: Optional[str] = None,
        query_findings: Optional[Sequence[str]] = None,
        exclude_filenames: Optional[Union[str, Sequence[str]]] = None,
        authentic_only: bool = True,
        exclude_identical_embeddings: bool = True,
    ) -> Dict[str, Any]:
        """Extract features from input image and retrieve Top-K most similar reference cases."""
        query_vector = self.extractor.extract_features(image_input, normalize=True)
        return self.engine.find_similar_by_vector(
            query_vector=query_vector,
            top_k=top_k,
            predicted_findings=predicted_findings,
            primary_finding=primary_finding,
            query_findings=query_findings,
            exclude_ids=exclude_filenames,
            exclude_identical=exclude_identical_embeddings,
        )

    def find_similar_by_vector(self, *args, **kwargs) -> Dict[str, Any]:
        return self.engine.find_similar_by_vector(*args, **kwargs)

    def analyze(self, *args, **kwargs) -> Dict[str, Any]:
        """Alias for find_similar_cases to satisfy MedTrust analyzer protocol."""
        return self.find_similar_cases(*args, **kwargs)

