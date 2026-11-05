"""
semantic_retriever.py - Sentence-BERT Evidence Retrieval Engine
===============================================================
Encodes candidate review sentences and finds top-k topically relevant
evidence for each atomic claim using dense cosine similarity.
Employs batch caching to ensure minimal latency and RAM overhead on 4GB laptops.
"""

from typing import List, Dict, Any
import torch
from sentence_transformers import util
from config.settings import SBERT_SIMILARITY_THRESHOLD, TOP_K_EVIDENCE_PER_CLAIM
from models.model_loader import ModelLoader
from modules.product_input.schema import AtomicClaim

class SemanticRetriever:
    def __init__(self, threshold: float = SBERT_SIMILARITY_THRESHOLD):
        self.model = ModelLoader().get_sbert_model()
        self.threshold = threshold

    def retrieve_evidence_for_claims(
        self,
        claims: List[AtomicClaim],
        segmented_reviews: List[Dict[str, str]],
        top_k: int = TOP_K_EVIDENCE_PER_CLAIM
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Retrieves top-k relevant sentences for each claim.
        Returns a map: claim_id -> list of candidate evidence items with scores and review_ids.
        """
        if not claims or not segmented_reviews:
            return {}

        review_sentences = [r["sentence"] for r in segmented_reviews]

        # Batch encode all review sentences once
        review_embeddings = self.model.encode(
            review_sentences,
            convert_to_tensor=True,
            show_progress_bar=False,
            normalize_embeddings=True
        )

        claim_texts = [c.text for c in claims]
        claim_embeddings = self.model.encode(
            claim_texts,
            convert_to_tensor=True,
            show_progress_bar=False,
            normalize_embeddings=True
        )

        # Compute cosine similarity matrix (N_claims x M_reviews)
        similarity_matrix = util.cos_sim(claim_embeddings, review_embeddings)

        retrieval_results: Dict[str, List[Dict[str, Any]]] = {}

        for i, claim in enumerate(claims):
            scores = similarity_matrix[i]
            k_val = min(top_k, len(review_sentences))
            top_k_res = torch.topk(scores, k=k_val)

            candidate_evidence: List[Dict[str, Any]] = []
            for score_tensor, idx_tensor in zip(top_k_res[0], top_k_res[1]):
                sim_score = score_tensor.item()
                if sim_score >= self.threshold:
                    idx = idx_tensor.item()
                    candidate_evidence.append({
                        "sentence": segmented_reviews[idx]["sentence"],
                        "review_id": segmented_reviews[idx].get("review_id", ""),
                        "relevance_score": round(sim_score, 3)
                    })

            retrieval_results[claim.claim_id] = candidate_evidence

        return retrieval_results
