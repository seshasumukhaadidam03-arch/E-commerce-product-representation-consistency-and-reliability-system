from transformers import pipeline
import warnings

# Hide some annoying warnings that the transformers library sometimes prints
warnings.filterwarnings("ignore")

class NLIScorer:
    def __init__(self):
        print("Loading NLI model... (This takes a few seconds)", flush=True)
        # We use a pipeline for 'text-classification'
        # This specific model is trained to output 3 categories: Contradiction, Entailment (Support), Neutral
        self.classifier = pipeline(
            "text-classification", 
            model="cross-encoder/nli-MiniLM2-L6-H768", 
            top_k=None # This tells it to give us the percentages for all 3 categories
        )
        print("NLI Model loaded successfully!", flush=True)

    def check_consistency(self, claim, review_evidence):
        """
        Takes a claim and a piece of evidence.
        Returns whether the evidence supports, contradicts, or is neutral to the claim.
        """
        # NLI format: Premise (what we KNOW is true) = Review Evidence
        #             Hypothesis (what we're TESTING) = Seller's Claim
        result = self.classifier({"text": review_evidence, "text_pair": claim})
        
        # The model returns a list of dictionaries with labels (LABEL_0, LABEL_1, LABEL_2) and scores.
        # For this specific model:
        # LABEL_0 = Contradiction
        # LABEL_1 = Entailment (Support)
        # LABEL_2 = Neutral
        
        scores = {
            "Contradiction": 0.0,
            "Support": 0.0,
            "Neutral": 0.0
        }
        
        for item in result:
            # We lowercase the label to catch it no matter how the model spells it
            label = str(item['label']).lower()
            percentage = item['score'] * 100
            
            if "label_0" in label or "contradiction" in label:
                scores["Contradiction"] = round(percentage, 1)
            elif "label_1" in label or "entailment" in label:
                scores["Support"] = round(percentage, 1)
            elif "label_2" in label or "neutral" in label:
                scores["Neutral"] = round(percentage, 1)
                
        # Find the winner (the category with the highest percentage)
        winner = max(scores, key=scores.get)
        
        return {
            "winner": winner,
            "scores": scores
        }

# ==========================================
# TESTING BLOCK
# ==========================================
if __name__ == "__main__":
    scorer = NLIScorer()
    
    test_claim = "100% waterproof, keeps hair completely dry"
    test_evidence = "My hair got completely soaked the second I stepped under the showerhead."
    
    print("\n" + "="*50)
    print("THE COURTROOM TEST")
    print("="*50)
    print(f"SELLER PROMISE: '{test_claim}'")
    print(f"CUSTOMER EVIDENCE: '{test_evidence}'")
    print("-" * 50)
    print("Analyzing consistency...\n")
    
    analysis = scorer.check_consistency(test_claim, test_evidence)
    
    print(f"VERDICT: {analysis['winner'].upper()}")
    print("\nConfidence Scores:")
    print(f"- Contradiction: {analysis['scores']['Contradiction']}%")
    print(f"- Support:       {analysis['scores']['Support']}%")
    print(f"- Neutral:       {analysis['scores']['Neutral']}%")
