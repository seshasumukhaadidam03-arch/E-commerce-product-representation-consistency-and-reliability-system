# MAJOR PROJECT REVIEW-I PRESENTATION (EXACTLY 6 SLIDES)

**Project Title:** AI-Based E-Commerce Product Representation Consistency and Reliability Assessment System  
**Academic Year:** 2025 – 2026  
**Department:** Department of Computer Science and Engineering  
**Institution:** Matrusri Engineering College (Affiliated to Osmania University)

---

## SLIDE 1 — TITLE SLIDE

### Slide Content:
# AI-Based E-Commerce Product Representation Consistency and Reliability Assessment System
**Major Project — Review I (Proof-of-Concept Stage)**

* **Department:** Department of Computer Science and Engineering  
* **Institution:** Matrusri Engineering College, Saidabad, Hyderabad  
* **Academic Year:** 2025 – 2026  

**Project Team:**
* [Student Name 1] — [Roll / Hall Ticket Number]
* [Student Name 2] — [Roll / Hall Ticket Number]
* [Student Name 3] — [Roll / Hall Ticket Number]
* [Student Name 4] — [Roll / Hall Ticket Number]

**Project Guide:**
* [Internal Guide Name], [Designation], Department of CSE

**Project Coordinators:**
* **Dr. L. K. Indumathi**, Associate Professor, Dept. of CSE
* **Mrs. K. Bhagya Laxmi**, Assistant Professor, Dept. of CSE

---

### Speaker Notes (Slide 1):
> *"Good morning respected coordinators Dr. Indumathi ma'am, Mrs. Bhagya Laxmi ma'am, our project guide, and faculty members. Today we are presenting Review-I of our Major Project titled 'AI-Based E-Commerce Product Representation Consistency and Reliability Assessment System'. In this review, we will establish the real-world problem, underlying research background, literature survey, research gaps, project scope, finalized objectives, and demonstrate our initial proof-of-concept progress."*

---

## SLIDE 2 — INTRODUCTION & BACKGROUND KNOWLEDGE

### Slide Content:
### The Multi-Representation Reality in E-Commerce
* **The Information Asymmetry:** Online buyers cannot touch or test goods physically; they rely entirely on digital representations before spending money.
* **Product Representations:**
  1. *Seller Text:* Titles, bullet features, and technical specifications.
  2. *Seller Images:* Idealized catalog and promotional studio photographs.
  3. *Customer Evidence:* Post-purchase customer reviews and unboxing images.
* **Core Phenomenon:** These representations frequently diverge, leading to high product returns and lost consumer trust.

### Essential Technical Concepts
* **Atomic Claim:** A discrete, testable assertion regarding a product's physical or functional attribute (e.g., *"Crafted from 100% waterproof polyester"* vs. non-testable fluff like *"Best gift ever"*).
* **Semantic Embeddings (S-BERT):** Converting text into numerical vectors to find relevant review evidence based on conceptual meaning rather than exact keyword overlap.
* **Natural Language Inference (NLI):** Directional logic evaluating whether customer evidence (Premise) **Supports (Entails)**, **Contradicts**, or is **Neutral** toward a seller claim (Hypothesis).

---

### Speaker Notes (Slide 2):
> *"When we shop online, we face an information gap. We cannot physically inspect the item, so we evaluate multiple digital representations: what the seller writes, what the catalog photos show, and what buyers report in reviews. Often, these representations do not match. To evaluate consistency computationally, we break listings down into 'Atomic Claims'—verifiable facts rather than marketing slogans. We use Sentence-BERT embeddings to retrieve topically relevant customer review sentences, and Natural Language Inference (NLI) to mathematically determine if the customer's real experience supports or contradicts the seller's claim."*

---

## SLIDE 3 — PROBLEM STATEMENT

### Slide Content:
### The Problem: Cross-Representation Inconsistency
* **The Reality:** A seller's catalog claims frequently fail to align with the physical product experienced by customers.
* **Concrete Example:**
  * **Seller Claim:** *"100% waterproof shower cap with leakproof silicone forehead seal."*
  * **Customer Evidence:** *"Water seeped through the seams immediately; my hair got completely wet."*
  * **Logical Verdict:** **Contradiction** (Direct claim-level inconsistency).

### Why Existing Marketplace Mechanisms Fail
* **Star Ratings (1–5 Stars):** Compress diverse experiences into a single number. A 5-star review praising pretty packaging obscures a severe material or functional failure.
* **Sentiment Analysis:** Detects emotional polarity (Positive/Negative), not factual validity. A customer politely reporting that a jacket runs two sizes small is classified as positive/neutral, ignoring the sizing discrepancy.

### Formal Problem Statement
> *"To design an automated, evidence-based assessment framework that extracts atomic product claims from seller representations, retrieves relevant post-purchase customer evidence, evaluates directional consistency (Support, Contradiction, Neutrality), and provides an interpretable reliability audit without relying on coarse star ratings."*
* *Boundary Note: The system assesses representation consistency against available evidence; it does not perform physical laboratory tests or legal fraud verification.*

---

### Speaker Notes (Slide 3):
> *"The core problem is that e-commerce platforms offer no mechanism to check if a specific seller claim is actually true according to customer experiences. If a seller promises a 'Waterproof Shower Cap' and a customer writes 'water seeped right through', that is a direct contradiction. Star ratings cannot expose this because ratings average everything together. Sentiment analysis only detects whether a customer is happy or angry, not whether a specific specification was fulfilled. Our problem statement addresses this: we evaluate the directional consistency of seller claims against empirical review evidence. We do not claim to detect counterfeit items or verify legal authenticity; we audit the empirical consistency of digital representations."*

---

## SLIDE 4 — LITERATURE SURVEY & RESEARCH GAP

### Slide Content:
### Key Literature Surveyed

| Paper & Citation | Approach / Architecture | Key Contribution | Identified Limitation |
| :--- | :--- | :--- | :--- |
| **PRAISE (ACL 2025)**<br>*Qidwai et al. (IIIT-H, UPenn, ASU)* | Sequential LLM prompting (Gemini 2.0 Flash) on reviews. | Proved feasibility of structured attribute extraction from reviews. | **Text-only** (omits images); excessive latency/cost ($\approx 2R+1$ LLM API calls); lacks unified score. |
| **Sentence-BERT (EMNLP 2019)**<br>*Reimers & Gurevych* | Siamese neural networks yielding dense vector embeddings. | Reduced semantic search from hours to milliseconds. | Captures **semantic similarity**, but cannot determine directional logical truth (Entailment vs. Contradiction). |
| **MultiNLI (NAACL 2018)**<br>*Williams, Nangia & Bowman* | Deep cross-encoder transformer inference benchmark. | Standardized directional NLI (Entailment, Contradiction, Neutral). | Trained on formal text; sensitive to noisy colloquial e-commerce text and DOM artifacts. |

### The Research Gap
```
Existing Research:
Isolated Sentiment Analysis & Costly Text-Only LLM Prompting
                     │
                     ▼
Limitation:
No multimodal assessment, computational bottlenecks (~2R+1 calls), no claim-level auditable score
                     │
                     ▼
Our Proposed Direction:
A computationally efficient framework combining dense S-BERT retrieval,
local NLI consistency scoring, and visual representation inspection into an interpretable metric
```

---

### Speaker Notes (Slide 4):
> *"Our primary base paper is PRAISE, published at ACL 2025 by IIIT Hyderabad, UPenn, and ASU. PRAISE demonstrated that LLMs can extract structured attributes from reviews. However, PRAISE has three documented limitations: it is text-only (ignoring product images), it makes roughly 2R+1 LLM calls per product which creates high cost and latency, and it lacks an aggregated score. To solve this, our literature survey incorporates Sentence-BERT for fast semantic retrieval and Cross-Encoder NLI for directional verification. The research gap is clear: existing systems either measure isolated sentiment or rely on costly brute-force LLMs. We propose an integrated, efficient approach combining dense retrieval, directional NLI, and visual inspection into a unified, interpretable reliability assessment."*

---

## SLIDE 5 — SCOPE & OBJECTIVES

### Slide Content:
### Project Scope: Defined Boundaries
* **IN-SCOPE:**
  * Extracting discrete, verifiable claims from seller textual listings.
  * Dense semantic retrieval of factual customer review sentences using S-BERT.
  * Directional NLI classification (Support, Contradiction, Neutral) for claim-evidence pairs.
  * Preliminary visual consistency inspection between catalog images and unboxing photos.
  * Formulating a composite Product Representation Index (PRI) and an interactive dashboard.
* **OUT-OF-SCOPE:**
  * Physical laboratory product testing or chemical material verification.
  * Declaring a seller fraudulent or legally prosecuting counterfeit listings.
  * Guaranteeing absolute real-world truth (we audit consistency relative to available evidence).

### Finalized Project Objectives
1. **Objective 1:** Extract atomic, verifiable product claims from seller textual descriptions while filtering promotional marketing fluff.
2. **Objective 2:** Implement a dense semantic retrieval pipeline using S-BERT to identify relevant customer review evidence sentences.
3. **Objective 3:** Develop an NLI inference engine to classify directional consistency (Support, Contradiction, Neutral) between claims and evidence.
4. **Objective 4:** Investigate visual consistency between catalog photos and customer-uploaded imagery using color and structural similarity metrics.
5. **Objective 5:** Formulate a mathematical Product Representation Index (PRI) and develop an interactive dashboard for transparent, evidence-backed evaluation.

---

### Speaker Notes (Slide 5):
> *"To ensure academic and technical rigor, we have strictly defined our scope. In-scope is the automated extraction of verifiable claims, semantic retrieval of review sentences, directional NLI consistency scoring, preliminary visual comparison, and dashboard visualization. Out-of-scope is physical destructive testing or legal fraud determination; our system performs a digital representation consistency audit. Our objectives are organized sequentially across five implementation steps: extracting atomic claims, retrieving relevant review evidence via S-BERT, evaluating consistency using NLI, auditing visual representations, and formulating an interpretable Product Representation Index (PRI) inside an interactive interface."*

---

## SLIDE 6 — CURRENT PROGRESS & CONCLUSION

### Slide Content:
### Current Progress: Proof-of-Concept (POC) Initiated
* **Status:** Initial proof-of-concept pipeline developed; tested across 5 sample benchmark products.
* **Working Components:**
  * *Text Pipeline:* Implemented claim parsing, S-BERT semantic retrieval (`all-MiniLM-L6-v2`), and cross-encoder NLI scoring (`nli-MiniLM2-L6-H768`).
  * *Interactive Interface:* Developed a functional Streamlit prototype supporting catalog selection, manual input, and side-by-side evidence categorization.
  * *Visual Module Prototype:* Standalone OpenCV script testing color distance (CIE LAB) and structural edge alignment (SSIM).

### Real-World Developmental Findings (Lessons Learned)
* **DOM & Metadata Contamination:** Raw e-commerce page text contains severe noise (sponsored ads, related products) that must be filtered out to prevent false claims.
* **Review Asymmetry & Opinions:** Full 200-word reviews cause NLI context overload; subjective opinions (*"I love this"*) trigger false contradictions unless filtered into factual sentences.
* *Note: Current results represent an exploratory proof-of-concept, not a fully validated system.*

### Roadmap to Review II & Conclusion
* **Next Steps:** Implement structured web extraction, calibrate the mathematical PRI formula, integrate the visual module into the live pipeline, and conduct benchmark evaluations.
* **Conclusion:** Review-I validates the problem significance, establishes a grounded literature foundation, and demonstrates early feasibility toward building a trustworthy e-commerce assessment system.

---

### Speaker Notes (Slide 6):
> *"To demonstrate feasibility, we have already initiated an initial proof-of-concept. We built a baseline pipeline using Sentence-BERT for retrieval and a Cross-Encoder for NLI, paired with an interactive Streamlit prototype and a standalone OpenCV visual analysis script. Importantly, early testing exposed key engineering challenges: raw e-commerce pages contain sponsored ads and metadata that corrupt the pipeline, and long reviews overload NLI models unless chunked into factual sentences. We present this honestly as a development finding, not a final validated system. Moving into Review II, we will refine structured extraction, calibrate the PRI formula, integrate multimodal analysis, and evaluate on benchmark datasets. This concludes our Review-I presentation. Thank you, and we are ready for questions."*

---

# LIKELY FACULTY QUESTIONS AND SHORT ANSWERS (20 Q&As)

### Category 1: Problem Definition, Representation & Scope
1. **What exactly do you mean by "product representation"?**  
   *Answer:* Any digital medium used by an e-commerce platform to convey an item's characteristics to buyers before purchase (seller descriptions, specifications, catalog photos, and customer review evidence).
2. **How is this different from traditional sentiment analysis?**  
   *Answer:* Sentiment analysis measures emotional polarity (positive/negative); our system verifies factual claim validity (true/false/unproven) at the specific attribute level.
3. **Does a high reliability score mean the product is guaranteed to be genuine?**  
   *Answer:* No. Reliability strictly denotes representation consistency between seller promises and customer feedback. We do not certify legal authenticity or detect physical counterfeits.
4. **What is the difference between a product claim and marketing fluff?**  
   *Answer:* An atomic claim is a discrete, measurable, verifiable assertion (e.g., *"100% waterproof"*). Fluff is non-testable promotional puffery (e.g., *"The best luxury experience"*).
5. **Why are star ratings insufficient for assessing product reliability?**  
   *Answer:* Star ratings collapse multidimensional attributes into a coarse average, hiding specific critical defects behind high ratings for secondary features like packaging.

### Category 2: NLP, Semantic Search & Natural Language Inference (NLI)
6. **What is Natural Language Inference (NLI) and why is it needed?**  
   *Answer:* NLI evaluates a Premise and a Hypothesis to determine whether the logical relationship is Entailment (Support), Contradiction, or Neutral. We need it to determine if customer observations corroborate or refute seller claims.
7. **Why can't you just use keyword matching or semantic cosine similarity instead of NLI?**  
   *Answer:* Semantic similarity measures if two texts discuss the same topic, not if they agree. *"Waterproof jacket"* and *"Jacket leaks immediately"* have high semantic similarity but are direct logical contradictions.
8. **In your NLI setup, which text is the Premise and which is the Hypothesis?**  
   *Answer:* The customer review evidence is the Premise (ground truth observation), and the seller claim is the Hypothesis (the statement being tested).
9. **What is the difference between Sentence-BERT and a Cross-Encoder?**  
   *Answer:* Sentence-BERT (Bi-Encoder) embeds texts separately for fast vector retrieval. A Cross-Encoder processes sentence pairs simultaneously with full cross-attention, making it much more accurate for NLI classification.
10. **How do you handle purely subjective customer opinions like "I love this cap"?**  
    *Answer:* Pure opinions lack factual descriptors and trigger false contradictions. We use a rule-based subjectivity filter (`_is_factual()`) to strip pure sentiment before NLI inference.

### Category 3: Base Paper & Architecture
11. **What is your base paper, and what conference was it published in?**  
    *Answer:* *PRAISE: Enhancing Product Descriptions with LLM-Driven Structured Insights*, published at ACL 2025 (System Demonstrations), Core A\*.
12. **What did the PRAISE paper do, and what are its main limitations?**  
    *Answer:* It extracted structured attributes from reviews using LLMs. Its limitations are that it is strictly text-only, requires $\approx 2R+1$ expensive API calls per product, and lacks a unified numerical score.
13. **What is the role of Gemini in your project, and why not use it for everything?**  
    *Answer:* Gemini is used strictly for extracting atomic claims from seller text. Using an LLM for review scoring causes high latency, API costs, and rate limits; local S-BERT and NLI models score in milliseconds for free.
14. **What is the Product Representation Index (PRI)?**  
    *Answer:* An experimental composite metric (0–100) synthesizing claim-level support ratios, penalizing contradictions, and incorporating visual consistency.
15. **Why do you penalize contradictions more heavily than rewarding support in PRI?**  
    *Answer:* A single critical contradiction (e.g., false waterproofing or sizing defect) destroys buyer trust and triggers returns far more severely than multiple matching claims build confidence.

### Category 4: Implementation Status, Findings & Evaluation
16. **What is the current implementation status of the project for Review-I?**  
    *Answer:* Initial proof-of-concept pipeline developed: claim extraction with caching, S-BERT retrieval, cross-encoder NLI scoring, standalone OpenCV visual script, and an interactive Streamlit prototype tested on 5 products.
17. **Is your visual module integrated into the live dashboard yet?**  
    *Answer:* No. It exists as an experimental standalone script (`src/visual_scorer.py`) evaluating CIE LAB color distance and SSIM edges. Live integration is scheduled for Review II.
18. **What major engineering challenges did you discover during prototype testing?**  
    *Answer:* Raw e-commerce text contains severe DOM noise (sponsored ads, related products) that must be filtered, and long reviews overload NLI models unless chunked into sentences.
19. **What dataset are you using for this project?**  
    *Answer:* A 5-product sample dataset streamed from the public Amazon Reviews 2023 benchmark by McAuley et al. across diverse retail categories.
20. **How do you plan to formally evaluate the system in Review II?**  
    *Answer:* By constructing an annotated benchmark test set of claim-evidence pairs labeled as Support, Contradiction, or Neutral, and measuring Precision, Recall, and F1-score against baseline models.
