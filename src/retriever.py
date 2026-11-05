import os
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'
os.environ['HF_HUB_DISABLE_PROGRESS_BARS'] = '1'

from sentence_transformers import SentenceTransformer, util
import torch

class ReviewRetriever:
    def __init__(self):
        print("Loading S-BERT model... (This takes a few seconds)", flush=True)
        # all-MiniLM-L6-v2 is a tiny, fast model perfect for 4GB RAM laptops
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        print("Model loaded successfully!", flush=True)

    def find_relevant_reviews(self, claim, review_list, top_k=3):
        """
        Takes a single claim and a list of review texts.
        Returns the top_k most relevant reviews based on semantic meaning.
        """
        if not review_list:
            return []

        # 1. Convert the claim into math (an embedding)
        claim_embedding = self.model.encode(claim, convert_to_tensor=True)

        # 2. Convert all reviews into math
        review_embeddings = self.model.encode(review_list, convert_to_tensor=True)

        # 3. Calculate how mathematically close the claim is to each review
        # Cosine similarity gives a score from -1.0 to 1.0 (1.0 means exactly identical meaning)
        cosine_scores = util.cos_sim(claim_embedding, review_embeddings)[0]

        # 4. Find the highest scores
        # We get the top_k scores (e.g., top 3)
        top_results = torch.topk(cosine_scores, k=min(top_k, len(review_list)))

        # 5. Format the output
        relevant_reviews = []
        for score, idx in zip(top_results[0], top_results[1]):
            # Convert tensors back to normal Python numbers
            relevance_score = score.item()
            
            # STRICT FILTER: Ignore irrelevant sentences!
            if relevance_score < 0.25:
                continue
                
            review_index = idx.item()
            
            relevant_reviews.append({
                "review_text": review_list[review_index],
                "relevance_score": round(relevance_score, 3)
            })

        return relevant_reviews

# ==========================================
# TESTING BLOCK
# ==========================================
if __name__ == "__main__":
    retriever = ReviewRetriever()
    
    test_claim = "100% waterproof, keeps hair completely dry"
    
    # Notice how Review 2 doesn't use the word "waterproof" or "dry" at all!
    test_reviews = [
        "The pattern on this cap is very beautiful.",
        "My hair got completely soaked the second I stepped under the showerhead.",
        "It fits my large head very comfortably.",
        "The elastic band broke after two days."
    ]
    
    print("\n" + "="*50)
    print(f"CLAIM: '{test_claim}'")
    print("="*50)
    print("Searching for relevant reviews based on meaning...\n")
    
    results = retriever.find_relevant_reviews(test_claim, test_reviews, top_k=2)
    
    for i, res in enumerate(results, 1):
        print(f"Match {i} (Score: {res['relevance_score']}): {res['review_text']}")
