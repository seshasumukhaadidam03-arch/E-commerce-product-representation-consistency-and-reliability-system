# REVIEW I SOURCE PACK: COMPREHENSIVE PROJECT REFERENCE DOCUMENT
**Project Title:** AI-Based E-Commerce Product Representation Consistency and Reliability Assessment System  
**Document Purpose:** Master source document for generation of Major Project Review-I presentation via NotebookLM.  
**Academic Institution:** Matrusri Engineering College, Department of Computer Science and Engineering.  
**Status:** Authoritative, Fact-Checked, Repository-Verified.

---

## 1. Project Identity

* **Project Title:** AI-Based E-Commerce Product Representation Consistency and Reliability Assessment System
* **Domain:** Natural Language Processing (NLP), Natural Language Inference (NLI), Information Retrieval, Applied Artificial Intelligence in E-Commerce.
* **Academic Level:** Bachelor of Engineering (B.E.) — Final Year Major Project (Review I).
* **Department:** Department of Computer Science and Engineering (CSE).
* **Institution:** Matrusri Engineering College, Saidabad, Hyderabad (Affiliated to Osmania University).
* **Academic Year:** 2025 – 2026.
* **Team Members:** [Student Name(s) & Roll / Hall Ticket Number(s)]
* **Project Guide:** [Internal Guide Name, Designation, Department of CSE]

---

## 2. Official Review-I Requirements

Per the official departmental circular, **Review I** is strictly dedicated to establishing the academic foundation and project viability. It must encompass exactly the following five major sections:

1. **Introduction** (Real-world domain context and representation challenge)
2. **Background Knowledge** (Underlying technical concepts and definitions)
3. **Problem Statement** (Formal problem formulation, inputs, and constraints)
4. **Literature Survey** (Critical study of existing benchmarks, base papers, and related works)
5. **Scope & Objectives** (Boundaries of investigation and measurable implementation targets)

### Review Boundary Clarification (Review I vs. Review II)
* **In Scope for Review I:** Establishing the research motivation, literature gap, problem formalization, project boundaries, precise objectives, and demonstrating preliminary technical viability via a basic proof-of-concept prototype.
* **Reserved for Review II (Subsequent Milestone):** Full system architectural design, comprehensive proposed methodology, exhaustive technology stack defense, complete database schema, pipeline scalability profiling, and execution planning. Review I must **not** be overloaded with Review II deliverables.

---

## 3. Final Project Definition

### What is the Project?
The project is an automated, AI-assisted quality assurance framework designed to evaluate whether the multiple digital representations of an e-commerce product are mutually consistent and empirically supported by consumer feedback.

### Key Conceptual Definitions

* **Product Representation:** Any distinct modality or digital channel through which an e-commerce platform conveys information about an item to a consumer prior to purchase. The three primary representations studied are:
  1. *Seller Textual Representations:* Product titles, marketing bullet points, technical specifications, and manufacturer descriptions.
  2. *Seller Visual Representations:* Studio catalog images, promotional graphics, and idealized lifestyle photographs.
  3. *Customer Empirical Representations:* Verified textual customer reviews, ratings context, and customer-uploaded unboxing photographs.

* **Product Claim:** A discrete, verifiable, factual assertion made by a seller regarding a specific product attribute, physical property, or functional performance (e.g., *"Crafted from 100% waterproof polyester"*, *"Fits head circumferences up to 24 inches"*). Subjective slogans or marketing fluff (e.g., *"Make every shower a luxury"*, *"Best gift for mom"*) are non-verifiable statements and must be separated from true claims.

* **Customer Evidence:** Ground-truth post-purchase feedback submitted by real buyers describing their empirical experience with the product.

* **Consistency:** The degree of mutual logical agreement or alignment between two representations of the same product. If Representation A (Seller Claim) asserts Property $X$, and Representation B (Customer Review) confirms Property $X$, they exhibit high consistency. If Representation B demonstrates the opposite of Property $X$, they exhibit an inconsistency (contradiction).

* **Reliability (Crucial Clarification):** In this project, **"Reliability" strictly refers to Representation Reliability / Consistency.** It measures the statistical and empirical degree to which the seller's catalog claims are supported by available customer evidence.  
  * **What Reliability DOES NOT Mean:** It does **not** denote certified legal authenticity, physical lab verification, counterfeit detection, or absolute real-world objective truth. A seller whose listing states *"Basic plastic watch"* has high representation reliability if reviews confirm it is indeed basic plastic, even if the physical item is low quality.

---

## 4. Problem Context

In online e-commerce environments, consumers experience an unavoidable **information asymmetry** (the "trust gap"):
1. The consumer cannot physically touch, wear, measure, or operate the product prior to committing funds.
2. The purchasing decision depends entirely on seller-curated digital representations.
3. Upon physical delivery, the actual product frequently deviates from the advertised representation:
   * *Material discrepancies:* Synthetic nylon advertised as "Pure Silk" or "Genuine Leather."
   * *Functional discrepancies:* An item advertised as "Completely Waterproof" failing upon light exposure to moisture.
   * *Dimensional discrepancies:* Apparel advertised as "Standard US Regular Fit" running two sizes smaller.
   * *Visual discrepancies:* Catalog photos featuring vibrant saturation or studio lighting while delivered items exhibit distinct colors or textures.
4. When representation discrepancies occur, consumers experience dissatisfaction, product return rates surge, logistical costs escalate, and trust in the digital marketplace degrades.

---

## 5. Background Knowledge

The technical concepts essential for understanding the project are:

* **Product Claims vs. Marketing Fluff:**  
  * *Claim:* *"Battery lasts 40 hours"* (Measurable, falsifiable).  
  * *Fluff:* *"Experience unbelievable acoustic bliss"* (Subjective, non-verifiable).

* **Natural Language Processing (NLP):** Computational techniques used to parse, clean, extract, and analyze human language text from unstructured e-commerce listings and review corpora.

* **Semantic Embeddings & Similarity:** Converting text into high-dimensional numerical vectors where distance correlates with semantic meaning.  
  * *Sentence-BERT (S-BERT):* A Siamese neural network architecture fine-tuned to generate dense sentence embeddings. Used in this project for **dense semantic retrieval**—finding relevant review sentences for a given claim based on conceptual meaning rather than exact keyword overlap.

* **Natural Language Inference (NLI):** A core NLP task that evaluates a pair of texts—a **Premise** and a **Hypothesis**—and determines the directional logical relationship between them:
  * **Entailment (Support):** If the Premise is true, the Hypothesis must be true (e.g., Premise: *"My hair remained bone dry under the shower"*; Hypothesis: *"The shower cap is waterproof"*).
  * **Contradiction:** If the Premise is true, the Hypothesis is false (e.g., Premise: *"Water soaked straight through the fabric"*; Hypothesis: *"The shower cap is waterproof"*).
  * **Neutral:** The Premise does not provide sufficient evidence to confirm or deny the Hypothesis (e.g., Premise: *"The floral pattern looks very retro and cute"*; Hypothesis: *"The shower cap is waterproof"*).

* **Cross-Encoder Architecture:** An attention mechanism where both texts are concatenated and passed through transformer layers simultaneously. More computationally expensive than bi-encoders, but delivers significantly higher precision for pairwise NLI classification.

* **Multimodal Analysis & Visual Consistency:** Assessing consistency across different data modalities (text vs. image, or image vs. image). In this context, comparing seller catalog images against customer-uploaded unboxing photographs using color distribution analysis (CIE LAB space) and structural edge comparison (Structural Similarity Index Measure - SSIM).

---

## 6. Existing Approaches & Their Limitations

E-commerce platforms currently provide several consumer decision-making mechanisms. However, each exhibits fundamental limitations regarding representation consistency:

| Mechanism | Description | Key Limitation in Context of Representation Consistency |
| :--- | :--- | :--- |
| **Star Ratings (1–5 Stars)** | Numerical average of all customer ratings for a product. | **Collapses multifaceted experiences into a single number.** A review giving 5 stars for cute packaging while noting *"fabric ripped on day one"* inflates the rating while burying a material failure. |
| **Traditional Sentiment Analysis** | Classifies text polarity as Positive, Negative, or Neutral. | **Measures emotional tone, not factual veracity.** A customer politely explaining that a garment runs two sizes smaller is classified as "Neutral/Constructive" rather than identifying a dimensional claim discrepancy. |
| **Generative Review Summaries (LLM Summaries)** | Paragraph summaries generated by LLMs over review text. | **Lacks claim-level attribution and verification.** Summaries generalize consensus sentiment but fail to map specific seller promises against empirical confirmation, frequently hallucinating or smoothing over critical contradictions. |
| **Fake Review / Bot Detection** | Classifies whether reviews originate from bots or incentivized rings. | **Does not assess the product listing itself.** Even if every review is 100% human and authentic, fake review detectors do not verify whether the seller's claims match what real customers received. |

---

## 7. Base Paper Analysis

### Complete Citation
* **Paper Title:** *PRAISE: Enhancing Product Descriptions with LLM-Driven Structured Insights*
* **Authors:** Adnan Qidwai$^*$, Srija Mukhopadhyay$^*$ (IIIT Hyderabad), Prerana Khatiwada (University of Delaware), Dan Roth (University of Pennsylvania), and Vivek Gupta (Arizona State University).
* **Publication Venue:** Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (ACL 2025), Volume 3: System Demonstrations, pages 644–652.
* **Venue Prestige:** Core A* (Ranked globally as the premier venue for Natural Language Processing).

### Problem Addressed by PRAISE
Sellers write incomplete, exaggerated, or unstructured product descriptions, while customer reviews contain a distributed wealth of factual ground truth. However, review insights are buried under subjective opinions, logistics feedback, and conversational noise, preventing direct comparison with seller claims.

### Methodology / Approach
PRAISE implements an LLM-driven pipeline (utilizing Gemini 2.0 Flash) structured in four steps:
1. *Attribute Extraction:* Prompting an LLM to extract objective, factual attribute-value pairs from individual customer reviews.
2. *Comparative Alignment:* Aligning extracted review attributes with seller descriptions to classify pairs into four alignment states: *Matching*, *Contradictory*, *Missing*, and *Partially Matching*.
3. *Attribute Grouping:* Clustering similar attributes into logical categories (Physical, Appearance, Performance).
4. *Insight Structuring:* Presenting insights via an interactive dashboard.

### Dataset Grounding
Evaluated across diverse categories of the standard Amazon Reviews benchmark (encompassing Apparel, Footwear, Electronics, and Home Appliances).

### Explicit Limitations Documented in PRAISE (Our Research Gaps)
1. **Exclusively Text-Based (Section 8 - Limitations):** PRAISE relies exclusively on written customer reviews and completely ignores product imagery. Visual mismatches (color shifts, structural differences) represent a major fraction of e-commerce returns.
2. **Computational Cost & Latency Bottleneck (Section 3 - Efficiency):** For a product with $R$ customer reviews, the PRAISE pipeline requires approximately $\approx (2R + 1)$ sequential LLM API calls. Processing 100 reviews requires over 200 API calls, introducing severe API cost, latency, and rate-limiting bottlenecks.
3. **Absence of a Unified Quantitative Metric:** PRAISE produces qualitative tables and categorical groupings, but does not formulate a unified numerical consistency or reliability index.

---

## 8. Literature Survey

The literature survey grounds the project across four distinct technical areas:

| # | Paper Citation | Core Focus / Problem | Approach / Architecture | Dataset | Relevant Finding | Key Limitation Relevant to Project |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | **Qidwai et al. (ACL 2025)**<br>*PRAISE: Enhancing Product Descriptions with LLM-Driven Structured Insights* | Extracting structured product insights from customer reviews vs. seller text. | Sequential LLM prompting (Gemini 2.0 Flash) across 4 stages. | Amazon Reviews Benchmark (multi-category). | Proves that customer reviews can be systematically extracted into factual attribute-value pairs. | Text-only; computational overhead of $\approx 2R+1$ LLM calls; no quantitative metric. |
| **2** | **Reimers & Gurevych (EMNLP 2019)**<br>*Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks* | Computational inefficiency of standard BERT cross-encoders for pairwise retrieval. | Siamese / Triplet network structure yielding fixed-size dense sentence embeddings; cosine similarity. | SNLI, MultiNLI, STS benchmark datasets. | Reduces semantic search from hours to milliseconds while retaining high semantic retrieval accuracy. | Bi-encoders capture semantic topicality, but lack directional logical inference (cannot distinguish contradiction from entailment). |
| **3** | **Williams, Nangia & Bowman (NAACL 2018)**<br>*A Broad-Coverage Challenge Corpus for Sentence Understanding through NLI (MultiNLI)* | Modeling natural language inference across diverse genres and conversational styles. | Collection of 433k sentence pairs; benchmark evaluations across deep neural architectures. | Multi-Genre Natural Language Inference (MultiNLI) corpus. | Establishes formal directional mapping (Entailment, Contradiction, Neutral) across complex real-world text. | Benchmark trained on general narrative/news text, requiring adaptation when applied to e-commerce review colloquialisms. |
| **4** | **Pontiki et al. (SemEval 2014 / 2016)**<br>*SemEval-2016 Task 5: Aspect-Based Sentiment Analysis* | Fine-grained aspect-level review parsing vs. coarse document-level sentiment. | Supervised classification of aspect categories, target terms, and aspect-specific polarities. | Customer review corpora (Restaurants, Laptops, Consumer Electronics). | Proves that customer opinions must be broken down by specific product aspects (e.g., battery vs. screen) rather than treated holistically. | Focused strictly on sentiment polarity (positive/negative), not on empirical consistency with seller claims. |
| **5** | **Ni, Li & McAuley (EMNLP 2019)**<br>*Justifying Recommendations using Distantly-Labeled Reviews and Visual Information* | Exploiting multimodal product data (reviews and images) in e-commerce decision systems. | Joint modeling of textual reviews and product image features for personalized recommendation. | Large-scale Amazon Product and Review Dataset (millions of products). | Demonstrates that visual representations provide complementary grounding to textual review descriptions. | Applied to recommendation ranking, not to auditing representation consistency or seller claim veracity. |
| **6** | **Wang et al. (KDD 2020)**<br>*Multi-modal Cross-domain Recommendation in E-Commerce* | Discrepancy and alignment between multimodal catalog items. | Cross-modal feature extraction and alignment across images and descriptions. | E-commerce production catalog datasets. | Highlights that visual and textual representations frequently exhibit cross-modal semantic gaps. | Focuses on cross-category mapping rather than seller-versus-customer post-purchase verification. |

---

## 9. Research Gap

A rigorous examination of existing literature reveals a distinct gap between isolated research domains:

```
[ Domain A: Review Sentiment & Aspect Mining ] ──► Extracts customer sentiment on isolated attributes.
                                                   (Does NOT compare against seller promises).

[ Domain B: E-Commerce Base Paper (PRAISE) ]   ──► Compares text descriptions using pure LLM calls.
                                                   (Text-only, high latency ~2R+1, no unified score).

[ Domain C: General NLI & Semantic Search ]    ──► Formulates directional logical inference.
                                                   (Rarely integrated into e-commerce representation auditing).
                                       │
                                       ▼
                         ┌─────────────────────────────┐
                         │      THE RESEARCH GAP       │
                         ├─────────────────────────────┤
                         │ No integrated framework:    │
                         │ 1. Extracts atomic claims   │
                         │ 2. Efficiently retrieves    │
                         │    factual review evidence  │
                         │ 3. Performs directional NLI │
                         │ 4. Audits multimodal visual │
                         │    discrepancy              │
                         │ 5. Synthesizes an inter-    │
                         │    pretable reliability index│
                         └─────────────────────────────┘
```

### Gap Formulation
1. Existing review mining systems focus on **sentiment polarity** rather than **claim verification**.
2. State-of-the-art claim alignment systems (like PRAISE) suffer from **excessive computational overhead ($\approx 2R+1$ calls)** and **completely omit visual representations**.
3. No existing work provides an **interpretable, evidence-based composite reliability metric** that synthesizes textual support/contradiction and visual fidelity into an auditable score.

---

## 10. Problem Statement

> **Input:** An e-commerce product catalog profile containing multiple digital representations: seller-provided textual descriptions $T_{\text{seller}}$, advertised catalog images $I_{\text{catalog}}$, a corpus of customer written reviews $T_{\text{reviews}}$, and customer-uploaded unboxing photographs $I_{\text{customer}}$.
>
> **Problem:** Information provided across these disparate representations is frequently unaligned, exaggerated, contradictory, or unsupported by post-purchase customer experiences.
>
> **Limitation of Existing Approaches:** Current marketplace mechanisms (aggregate star ratings, sentiment classification, and generative summaries) collapse multidimensional attributes into coarse averages, failing to perform claim-level cross-representation consistency checking.
>
> **Proposed System Need:** An automated, evidence-based assessment framework that extracts atomic seller claims, retrieves relevant empirical customer evidence, evaluates directional consistency (Support, Contradiction, Neutrality), inspects visual alignment, and synthesizes an interpretable consistency and reliability index.

---

## 11. Project Scope

To maintain rigorous academic clarity, the boundaries of this Major Project are strictly demarcated:

### IN SCOPE
* Automated extraction of discrete, verifiable product claims from seller textual listings.
* Preprocessing, chunking, and noise filtration of raw customer review corpora.
* Semantic retrieval of relevant review evidence using dense vector embeddings (Sentence-BERT).
* Directional natural language inference (Support / Entailment, Contradiction, Neutrality) evaluating review evidence against specific seller claims.
* Qualitative and quantitative categorization of customer evidence at the claim level.
* Preliminary cross-representation visual consistency inspection (comparing catalog imagery against customer unboxing imagery for color and structural alignment).
* Mathematical synthesis of a composite **Product Representation Index (PRI)**.
* Development of an interactive, auditable user dashboard for transparent evidence presentation.
* Evaluation on benchmark e-commerce product datasets across distinct retail categories.

### OUT OF SCOPE
* Physical laboratory testing, chemical analysis, or hardware disassembly of products.
* Certifying legal authenticity, trademark compliance, or declaring a merchant fraudulent.
* Classifying subjective merchant intent (e.g., distinguishing an intentional scam from a manufacturing batch defect).
* Guaranteeing absolute objective real-world truth (the system only audits consistency relative to available evidence).
* Replacing human consumer judgment or providing financial purchase guarantees.

---

## 12. Project Objectives

The project executes six precisely defined, implementation-oriented objectives:

1. **Objective 1 (Claim Extraction):** To design and implement a structured extraction pipeline that identifies and isolates atomic, verifiable product claims from unstructured seller listings while filtering out promotional marketing fluff.
2. **Objective 2 (Evidence Retrieval & Preprocessing):** To develop a dense semantic retrieval mechanism using sentence embeddings to clean customer reviews, filter non-factual commentary, and retrieve topically relevant evidence sentences corresponding to each extracted claim.
3. **Objective 3 (Directional Consistency Assessment):** To formulate an NLI-based inference engine that evaluates the directional logical relationship between retrieved customer evidence sentences and seller claims, classifying pairs into Support, Contradiction, or Neutral states with associated confidence metrics.
4. **Objective 4 (Visual Representation Consistency):** To investigate and implement computer vision methods for evaluating visual consistency between advertised catalog images and customer-uploaded unboxing photographs based on color fidelity and structural similarity.
5. **Objective 5 (Reliability Index Formulation):** To formulate an interpretable mathematical metric—the Product Representation Index (PRI)—that synthesizes claim-level textual support/contradiction ratios and visual discrepancy into an aggregated reliability score.
6. **Objective 6 (Interactive Verification Dashboard):** To develop an interactive, user-facing prototype that transparently visualizes the assessed representations, exposes the underlying review evidence, and benchmarks system performance across sample e-commerce categories.

---

## 13. Current Implementation Status

This section provides an honest, fact-checked inventory of the actual codebase present in the repository (`d:\Major_Project`):

| Component / File | Current State | Repository Verification | Functional Description |
| :--- | :--- | :--- | :--- |
| **Claim Extractor**<br>`src/claim_extractor.py` | **PROTOTYPE / EXPERIMENTAL** | Verified in repo | Uses Google GenAI SDK (`gemini-3.8-flash`) to parse titles and features into atomic JSON bullet points. Contains a rule-based fallback mechanism to handle API timeouts and 503 errors. |
| **Semantic Retriever**<br>`src/retriever.py` | **IMPLEMENTED** | Verified in repo | Implements `SentenceTransformer('all-MiniLM-L6-v2')`. Converts claims and review sentences into dense embeddings, computes cosine similarity, and applies a strict relevance threshold ($> 0.25$) to isolate top-K evidence sentences. |
| **NLI Consistency Scorer**<br>`src/nli_scorer.py` | **IMPLEMENTED** | Verified in repo | Implements a Hugging Face cross-encoder pipeline (`cross-encoder/nli-MiniLM2-L6-H768`). Takes customer evidence as Premise and seller claim as Hypothesis; outputs probability distribution over Contradiction, Support, and Neutral. |
| **Master Text Pipeline**<br>`src/pipeline.py` | **IMPLEMENTED (POC STAGE)** | Verified in repo | Connects Claim Extraction, Review Preprocessing (chunking and `_is_factual` rule filter), S-BERT retrieval, and NLI scoring. Computes an experimental composite PRI: $\text{PRI} = \max(0, \min(100, \text{Avg Support} - 1.5 \times \text{Avg Contradict}))$. |
| **Pre-Extracted Claim Cache**<br>`data/sample/cached_claims.json` | **IMPLEMENTED** | Verified in repo | Contains curated, verifiable atomic claims for 5 benchmark products, eliminating live external API dependencies and preventing rate-limit crashes during demonstrations. |
| **Sample Dataset**<br>`data/sample/sample_products.json` | **IMPLEMENTED** | Verified in repo | Contains 5 products spanning Apparel, Seasoning, Beauty Shears, Makeup Cases, and Nail Care, downloaded from the Amazon Reviews dataset with titles, features, catalog images, and review arrays. |
| **Interactive UI Dashboard**<br>`app/dashboard.py` | **IMPLEMENTED** | Verified in repo | Built with Streamlit. Features two operational modes: (1) Sample Products Mode, and (2) Manual Input Mode. Displays seller claims, color-coded PRI metric, categorized evidence columns (✅ Support, ❌ Contradict, ➖ Neutral), and claim-by-claim drill-downs. Uses `@st.cache_resource` for model persistence. |
| **Visual Scorer (Standalone)**<br>`src/visual_scorer.py` | **EXPERIMENTAL POC (STANDALONE)** | Verified in repo | Standalone script using OpenCV (`cv2`) and `scikit-image`. Computes Euclidean color distance in CIE LAB space and structural edge similarity via SSIM. **Note:** Operates as an isolated test script; *not yet integrated into the master pipeline or dashboard.* |
| **Multimodal Vision Integration (CLIP)** | **PLANNED** | Not in repo | Deep multimodal feature matching using vision-language models (e.g., CLIP) remains planned for Review II development. |
| **Real-Time Live Web Scraper** | **PLANNED** | Not in repo | Selenium/Playwright scraper for live URL extraction is scheduled for subsequent phases. Current implementation relies on sample datasets and manual text input. |

---

## 14. Current Development Findings & Technical Lessons

The initial proof-of-concept phase was deliberately conducted to uncover real-world failure modes. These constitute **valuable engineering findings** for Review I:

1. **DOM Scrape Contamination:**  
   Copying raw text from e-commerce product pages injects immense structural noise: sponsored product advertisements, related items carousel text, pricing tables, delivery estimates, reviewer names, dates, and navigation buttons. If fed directly to an NLP pipeline, these non-claim elements get treated as claims, corrupting the analysis.
2. **Review Asymmetry & The "Context Overload" Problem:**  
   Passing entire 200-word conversational reviews directly into a compact NLI model overwhelms the model's sequence capacity. The model cannot identify the specific clause related to the claim and defaults to a 90%+ "Neutral" verdict. **Engineering Solution:** Reviews must be chopped into atomic sentences prior to retrieval.
3. **The False Contradiction Trap (Pure Opinions):**  
   Short, purely emotional sentences (e.g., *"I love this product"*, *"Waste of money"*) lack verifiable attributes. When evaluated against a factual claim like *"Waterproof polyester"*, an NLI model flags *"I love this"* as a contradiction because loving an item does not logically entail water resistance. **Engineering Solution:** Implemented an `_is_factual()` filter to strip pure opinions prior to inference.
4. **Directional Sensitivity in NLI:**  
   In NLI, input order is strictly directional. Setting `Premise = Seller Claim` and `Hypothesis = Review Evidence` asks: *"If the product is waterproof, does that prove the customer had a good shower?"* This produces false neutrals. The correct formulation must always be: `Premise = Customer Evidence` (the ground truth fact), and `Hypothesis = Seller Claim` (the statement being tested).
5. **Retrieval Thresholding is Mandatory:**  
   A standard top-K dense retriever returns the top $K$ sentences regardless of how irrelevant they are. If a review has zero sentences discussing waterproofing, S-BERT will still force-feed the "least irrelevant" sentence to the NLI model. A strict cosine similarity threshold ($> 0.25$) is essential to discard irrelevant text.

---

## 15. What MUST NOT Be Claimed in Review I

To ensure strict academic honesty and avoid faculty rejection, the following claims **must never be made**:

* **DO NOT claim 100% accuracy or state that the system is fully validated.** The system is an early proof of concept operating on sample data.
* **DO NOT claim that PRI is a certified, standardized industry score.** It is currently an experimental heuristic formula under active development.
* **DO NOT claim that the system detects "fake products" or "fraudulent sellers."** It is strictly an empirical representation consistency audit.
* **DO NOT claim that OpenAI CLIP is implemented.** Only basic OpenCV color distance and SSIM have been explored in a standalone script.
* **DO NOT cite hypothetical metrics as real experimental data.** Statements like *"reduces latency by 80%"* or *"exhibits 86% contradiction across 42 reviews"* were illustrative architectural examples, not empirical measurements from our prototype.
* **DO NOT claim real-time live Amazon scraping is functional.** Live anti-bot protections require specialized scrapers planned for later phases.

---

## 16. Review-I Demonstration Evidence

The following repository components represent the safest, most academically compelling artifacts to showcase during the presentation:

1. **The Clean Streamlit User Interface:**  
   Demonstrating the side-by-side representation view: Seller Advertised Claims on top, and Categorized Customer Evidence (Supportive vs. Contradicting) below.
2. **The Factual Extraction & Categorization Trace (Shower Cap Test Case):**  
   * *Claim:* *"The shower cap is 100% waterproof and keeps hair completely dry."*  
   * *Retrieved Supporting Evidence:* *"This works outstandingly! It stays on and keeps my hair dry."* $\rightarrow$ Classified as **✅ SUPPORT**.  
   * *Retrieved Contradicting Evidence:* *"No shower cap is going to be completely, perfectly water tight."* $\rightarrow$ Classified as **❌ CONTRADICTION**.  
   * This proves that the semantic retrieval + NLI pipeline functions as intended when data is clean.
3. **The Standalone Visual Consistency Test:**  
   Showcasing the output of `src/visual_scorer.py` demonstrating how CIE LAB color math flags a color discrepancy (27.1% match on color divergence) while SSIM maintains structural edge awareness.
4. **Developmental Finding Evidence:**  
   Showing how uncleaned Amazon DOM text (e.g., sponsored ads) corrupted initial runs, justifying why structured preprocessing is a major contribution of the project.

---

## 17. Likely Faculty Questions & Concise Answers (26 Questions)

#### Category A: Problem Definition & Relevance
1. **Q: What exactly is a "product representation"?**  
   *A:* A product representation is any digital channel or asset through which an e-commerce platform conveys an item's characteristics to a buyer prior to purchase, such as textual descriptions, technical specifications, catalog photographs, and customer review corpora.

2. **Q: Why is this different from traditional sentiment analysis?**  
   *A:* Sentiment analysis measures emotional polarity (positive, negative, or neutral). It cannot verify whether specific factual claims (e.g., *"100% cotton"* or *"40-hour battery"*) are supported or refuted by customer experiences. Our system performs claim-level factual verification rather than mood detection.

3. **Q: How does this differ from fake review detection systems?**  
   *A:* Fake review detection asks: *"Was this review written by a bot or paid user?"* Our system asks: *"Regardless of author, does the body of customer evidence corroborate or contradict what the seller promised in the catalog listing?"*

4. **Q: What does "reliability" mean in this project? Are you certifying product authenticity?**  
   *A:* No. Reliability here strictly denotes **Representation Consistency**—the degree to which the seller's catalog promises align with empirical customer feedback. We do not certify legal authenticity, perform lab testing, or detect physical counterfeit goods.

5. **Q: What is a "product claim"? Give an example.**  
   *A:* A product claim is a discrete, measurable, verifiable assertion about a product's physical or functional attributes (e.g., *"Waterproof up to 50 meters"*). It excludes subjective promotional slogans like *"Loved by millions worldwide."*

#### Category B: Natural Language Processing & NLI
6. **Q: What is Natural Language Inference (NLI)?**  
   *A:* NLI is an NLP task that takes two sentences—a Premise (ground truth) and a Hypothesis (claim)—and determines whether the relationship is Entailment (Support), Contradiction, or Neutral.

7. **Q: Why can't you just use keyword matching or cosine similarity instead of NLI?**  
   *A:* Semantic similarity only measures whether two sentences discuss the *same topic*; it cannot determine logical agreement. For example, *"The jacket is waterproof"* and *"The jacket leaks water immediately"* have high semantic similarity because they share the same topic, but logically they are direct contradictions. NLI is required to determine the directional truth relationship.

8. **Q: What do Support, Contradiction, and Neutral mean in your pipeline?**  
   *A:* **Support** means the review confirms the claim. **Contradiction** means the review refutes the claim. **Neutral** means the review discusses the product but does not provide sufficient factual evidence to confirm or deny that specific claim.

9. **Q: What is the difference between a Bi-Encoder and a Cross-Encoder? Why do you use both?**  
   *A:* A Bi-Encoder (Sentence-BERT) encodes sentences into separate vectors, making it extremely fast for retrieving relevant sentences from thousands of reviews. A Cross-Encoder processes sentence pairs together with full cross-attention, making it much more accurate for NLI classification. We use S-BERT for fast retrieval and a Cross-Encoder for precise scoring.

10. **Q: In your NLI model, which text is the Premise and which is the Hypothesis?**  
    *A:* The customer review evidence is the **Premise** (accepted as ground truth observation), and the seller's claim is the **Hypothesis** (the statement being tested against reality).

#### Category C: Architecture & Methodology
11. **Q: What is the role of Gemini in your system, and why not use it for the whole pipeline?**  
    *A:* In our prototype, Gemini is used strictly for extracting clean atomic claims from unstructured seller text. We avoid using it for review scoring because calling an LLM API for hundreds of reviews introduces severe latency, high API costs, and rate-limiting failures, whereas local S-BERT and NLI models run fast, free, and deterministically.

12. **Q: What was the primary base paper for this project?**  
    *A:* The base paper is *PRAISE: Enhancing Product Descriptions with LLM-Driven Structured Insights*, published at ACL 2025 (System Demonstrations) by researchers from IIIT Hyderabad, University of Pennsylvania, and Arizona State University.

13. **Q: What are the key limitations of the PRAISE base paper?**  
    *A:* PRAISE is strictly text-based (no image analysis), incurs massive computational latency by executing $\approx 2R+1$ LLM API calls per product, and lacks a unified quantitative reliability metric.

14. **Q: What is the Product Representation Index (PRI)?**  
    *A:* PRI is an experimental composite index (scaled 0–100) that synthesizes claim-level support ratios, penalizes contradictions, and incorporates visual consistency to provide a single, auditable representation quality score.

15. **Q: Why do you penalize contradictions more heavily than rewarding support in the PRI formula?**  
    *A:* In e-commerce quality assurance, a single unverified contradiction (e.g., non-functioning safety feature or wrong material) destroys consumer trust and triggers returns far more severely than several matching features build confidence.

#### Category D: Implementation, Data & Scope
16. **Q: What dataset are you using?**  
    *A:* We are using product categories sourced from the standard Amazon Reviews benchmark dataset (McAuley et al.), which contains paired product metadata, seller bullet points, high-resolution catalog images, and verified customer review corpora.

17. **Q: What has been implemented so far for Review I?**  
    *A:* We have established a working proof-of-concept pipeline: atomic claim extraction (with fallback caching), review cleaning and sentence chunking, dense semantic retrieval via S-BERT, cross-encoder NLI scoring, a standalone OpenCV visual analysis prototype, and an interactive Streamlit dashboard.

18. **Q: What is still under development for Review II?**  
    *A:* Developing robust web scrapers for live e-commerce URLs, integrating multimodal vision models (CLIP) directly into the master pipeline, fine-tuning extraction heuristics, establishing formal evaluation metrics (Precision/Recall/F1 against annotated benchmarks), and conducting scalability testing.

19. **Q: How do you handle subjective customer opinions like "I love this product"?**  
    *A:* We implemented a rule-based subjectivity filter (`_is_factual()`) that detects pure sentiment phrases lacking attribute descriptors and removes them, preventing opinion statements from polluting the factual NLI analysis.

20. **Q: What happens if a seller listing has marketing fluff like "Best gift ever"?**  
    *A:* The claim extraction stage filters out non-verifiable marketing phrases, retaining only factual, testable assertions (e.g., material, dimensions, compatibility, performance).

21. **Q: What major technical challenges did you uncover during initial prototype development?**  
    *A:* We discovered that raw e-commerce pages contain severe DOM noise (sponsored ads, related products) that must be filtered, that long reviews cause NLI context overload unless chunked into sentences, and that NLI models generate false contradictions on pure opinions unless filtered.

22. **Q: How will you evaluate the accuracy of your system?**  
    *A:* In Review II, we will evaluate the system by constructing an annotated ground-truth test set of claim-evidence pairs labeled by human annotators as Support, Contradiction, or Neutral, and measuring Precision, Recall, and F1-score against standard NLI and retrieval baselines.

23. **Q: What are the hardware constraints of this project?**  
    *A:* The system is designed to execute locally on standard consumer hardware (e.g., 4GB–8GB RAM, multi-core CPU) without requiring high-end dedicated enterprise GPUs, which is why we utilize lightweight, optimized models like `all-MiniLM-L6-v2` and quantized cross-encoders.

24. **Q: How does the visual consistency module work?**  
    *A:* Our experimental visual module uses OpenCV to compare catalog images with customer unboxing photos. It converts images to the CIE LAB color space to compute Euclidean color distance ($\Delta E$), and applies Structural Similarity (SSIM) to grayscale edge maps to detect structural shape discrepancies.

25. **Q: What is the main research gap your project addresses?**  
    *A:* While existing works study review sentiment or perform costly text-only LLM prompting, no unified, computationally efficient framework combines dense semantic retrieval, directional NLI consistency checking, and visual representation analysis into an auditable reliability metric.

26. **Q: What is the ultimate deliverable of this Major Project?**  
    *A:* A fully functional, deployable web application that allows users or auditing analysts to inspect e-commerce listings, transparently examine how each seller claim holds up against real customer evidence, and review an evidence-backed representation reliability assessment.

---

## 18. Key Terminology Glossary

* **Atomic Claim:** A single, self-contained factual assertion describing one specific product property (e.g., *"Weight is 1.05 kg"*).
* **Bi-Encoder:** A model architecture that embeds two sentences independently into vector representations; optimized for fast vector search and retrieval.
* **CIE LAB:** A color space designed to approximate human vision, separating lightness ($L$) from color opponent dimensions ($A$ and $B$).
* **Cross-Encoder:** A model architecture that processes two texts simultaneously through transformer layers with full cross-attention; optimized for classification accuracy.
* **Dense Retrieval:** Information retrieval using continuous vector embeddings and cosine similarity rather than discrete keyword frequency (sparse retrieval).
* **Entailment:** A logical condition in NLI where the truth of the premise guarantees the truth of the hypothesis.
* **Information Asymmetry:** An economic condition where one party (the seller) possesses vastly more accurate product information than the other (the buyer).
* **Marketing Fluff:** Non-verifiable, hyperbolic promotional language designed to evoke emotion rather than convey factual specifications.
* **Multimodal:** Involving multiple distinct data types simultaneously (specifically text and imagery).
* **Natural Language Inference (NLI):** The formal NLP task of determining whether a hypothesis is true, false, or undetermined given a premise.
* **Product Representation Index (PRI):** The composite score formulated in this project to quantify overall multi-representation consistency.
* **SSIM (Structural Similarity Index Measure):** A perceptual metric that quantifies image degradation and structural shape alignment between two images.
