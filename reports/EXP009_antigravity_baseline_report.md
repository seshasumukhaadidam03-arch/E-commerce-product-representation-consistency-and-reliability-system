# EXP-009: Running the existing Antigravity pipeline on real products

- **Date:** 2026-11-11
- **Run by:** Claude, in the cloud workspace
- **Code:** `D:\Major_Project` (Antigravity version, `modules/pipeline.py`), unchanged
- **Status:** COMPLETED. This is a diagnostic run, not an evaluation (no human labels exist yet)

## Setup
- **Products:** P4 Ucharge 50L backpack (41 reviews) and P1 DASH Co. wallet (21 reviews). Both come from the EXP-008 sample and are pilot products.
- **Claim extractor:** the rule-based extractor (`use_llm_claims=False`). The Gemini key in `.env` was not read or used.
- **Retrieval model:** `all-MiniLM-L6-v2`, threshold 0.28, top-5 sentences per claim.
- **NLI model:** `cross-encoder/nli-MiniLM2-L6-H768` (premise = review sentence, hypothesis = claim).
- **Libraries:** torch 2.15.0 (CPU), sentence-transformers 6.2.0, transformers 5.22.2.
- **Full output:** `EXP009_antigravity_baseline_P1_P4.json`.

## Results

| Product | Claims extracted | Support | Contradict | Neutral | Product label | PRI |
|---|---|---|---|---|---|---|
| P4 backpack | 1 ("Nylon lining") | 0 | 2 | 3 | CONTRADICTORY | 52.6 |
| P1 wallet | 3 (whole bullets) | 0 | 5 | 10 | CONTRADICTORY | 60.0 |

Run time was about 1 second per product once the models were loaded.

## What works
- The pipeline runs end to end on real data, on a CPU, quickly.
- Retrieval finds on-topic sentences. Example for the wallet compartments claim: "Holds all the cards I carry around comfortably…" (similarity 0.65).
- Some contradictions are real. "This revealed the materials underneath - paper" was scored 98% contradiction against "durable construction / premium canvas".

## Defects found (each one is a concrete fix for Phase 3)
1. **Claims written only in the title are lost.** The rule extractor ignores the title whenever bullets exist. On the backpack this dropped 50 L, waterproof and rain cover, which are the three most important claims.
2. **Claims are not atomic.** Whole bullets become one claim, including the "★ DURABLE CONSTRUCTION -" marker text. The output is also capped at 8 claims.
3. **NLI almost never says "Support".** It gave 0 supports out of 20 judged sentences. "Like the ID window" scored 87% Neutral against the ID-window claim. Likely causes: the hypothesis is a long marketing sentence, and the small NLI model is strict.
4. **Neutral is counted as consistent.** In `aggregator.py`, `consistent_count = support + neutral`. A claim with zero supporting sentences can therefore still score 60–80% "consistency". This is exactly the "insufficient evidence treated as consistent" error.
5. **Off-attribute contradictions.** "Pockets and exterior developed holes" was counted against "Nylon lining". A review mentioning another wallet brand ("Havok") was counted against the ID-pocket claim.
6. **The product verdict comes from the PRI threshold.** A product with a single extracted claim was still labelled CONTRADICTORY.

## Decision
These defects confirm the Option B redesign:
- atomic claim extraction that includes the title,
- an attribute filter on retrieval,
- an NLI hypothesis rewritten as a short plain claim, plus a stronger NLI model compared as an ablation,
- neutral sentences no longer counted as support,
- Beta-rule verdicts per claim.

This unchanged pipeline will also serve as "Baseline 0 (Antigravity v1)" in the final evaluation.
