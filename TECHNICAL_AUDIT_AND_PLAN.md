# TECHNICAL AUDIT REPORT & REBUILD ARCHITECTURAL PLAN
**Project Title:** AI-Based E-Commerce Product Representation Consistency and Reliability Assessment System  
**Audit Date:** November 5, 2026  
**Auditor:** Senior AI/ML Engineer & Systems Architect  
**Checkpoint:** Git commit `6481038` (Pre-rebuild baseline backup)

---

## 1. Executive Summary & Audit Overview

The existing codebase contains a functional proof-of-concept (POC) text pipeline that was hastily patched during Review-I preparation. While it successfully demonstrated that Sentence-BERT and Cross-Encoder NLI can detect discrepancies on a sample leather wallet, the architecture suffers from significant structural, algorithmic, and engineering deficiencies:

| Dimension | Existing State | Defects / Deficiencies | Rebuild Target |
| :--- | :--- | :--- | :--- |
| **Project Structure** | Flat `src/` directory with 5 loosely coupled scripts | No modular layers, no unit tests, no separation of concerns | Modular package hierarchy (`modules/`, `models/`, `evaluation/`) |
| **Input Ingestion** | Hardcoded sample JSON or manual text copy-paste | Zero URL parsing, zero image OCR/upload processing | 3 Input Channels: Live URL scraping, Advertised Image, Manual Input |
| **Visual Scorer** | Standalone script (`src/visual_scorer.py`), unintegrated | Simple average LAB color & whole-image SSIM, disconnected from pipeline | Multi-scale feature & color analysis integrated directly into PRI |
| **PRI Formula** | Ad-hoc voting heuristic in `src/pipeline.py` | Arbitrary hardcoded thresholds, no coverage factor, no visual weighting | Mathematically defensible, transparent, multi-component PRI engine |
| **Classification** | Implicit High/Moderate/Low label based purely on PRI $>60, >30$ | No formal classification logic handling mixed or insufficient evidence | 4 Formal States: `CONSISTENT`, `CONTRADICTORY`, `MIXED EVIDENCE`, `INSUFFICIENT EVIDENCE` |
| **Evaluation** | 0 test files in `tests/`, 0 quantitative metrics | No Precision/Recall/F1, no confusion matrices, no benchmark target | 25-product annotated benchmark with formal evaluation suite |
| **Dashboard** | Simple 2-page Streamlit layout | Unpolished styling, missing visual inspection tab, no model evaluation metrics | Professional AI research dashboard with 7 dedicated analytical views |

---

## 2. File-by-File Technical Audit

### A. Core Source Files (`src/`)
1. **`src/pipeline.py` (399 lines)**
   - *Status:* Working POC, but monolithic.
   - *Issues:* Combines claim cleaning, API calls, review splitting, keyword filtering, S-BERT retrieval, NLI scoring, and PRI calculation in a single file. Hardcodes dictionary paths, lacks typed schemas, and catches general exceptions.
   - *Action:* Decompose into `modules/preprocessing/`, `modules/pri_engine/`, and orchestrate via `pipeline.py`.

2. **`src/claim_extractor.py` (95 lines)**
   - *Status:* Working, but fragile.
   - *Issues:* Relies on raw Gemini API text generation with fragile markdown regex stripping (````json ... ````). Fallback is a primitive string split on periods (`.`) with arbitrary length $>15$. No structured schema validation.
   - *Action:* Replace with Pydantic-validated structured extraction using `gemini-3.8-flash` with deterministic JSON mode, and an intelligent regex/NLP rule-based fallback that extracts entity-attribute-value triplets.

3. **`src/retriever.py` (81 lines)**
   - *Status:* Working well.
   - *Model:* `sentence-transformers/all-MiniLM-L6-v2` (384-d, 80MB).
   - *Issues:* Encodes the entire review list on every single claim query without batch caching; hardcoded threshold `0.25` is too lenient for short sentences.
   - *Action:* Retain model (it is optimal for 4GB RAM CPU laptops), but encapsulate into `models/model_loader.py` with embedding caching and dynamic score filtering.

4. **`src/nli_scorer.py` (84 lines)**
   - *Status:* Working well.
   - *Model:* `cross-encoder/nli-MiniLM2-L6-H768` (220MB).
   - *Issues:* Correct Premise/Hypothesis orientation was applied, but the output dictionary only reports raw softmax percentages without calibration or token-length truncation guards.
   - *Action:* Move into `models/` with batch inference capability and threshold calibration.

5. **`src/visual_scorer.py` (114 lines)**
   - *Status:* Defective & Unintegrated.
   - *Issues:* Downscales images to 256x256, averages global LAB color (which compares background colors rather than the product!), and computes global SSIM (which fails completely if angles or crops differ slightly). Never invoked by `src/pipeline.py` or `app/dashboard.py`.
   - *Action:* Re-engineer in `modules/visual_verification/` using foreground-aware color distance, edge-density histograms, and multimodal CLIP/feature embeddings where resource permits.

### B. User Interface & Data (`app/`, `data/`)
1. **`app/dashboard.py` (240 lines)**
   - *Issues:* Standard Streamlit cards; lacks tabs for live web URL extraction, visual image comparison, detailed model evaluation metrics, and downloadable PDF/JSON assessment audits.
   - *Action:* Completely redesign into a multi-page professional research workbench with clean visual hierarchy.
2. **`data/sample/sample_products.json` & `cached_claims.json`**
   - *Issues:* 6 products with inconsistent schema; product #2 has mismatched reviews from early dataset downloads.
   - *Action:* Curate and structure into a standardized 25-product benchmark dataset with ground-truth labels across 4 categories.

---

## 3. Target Rebuilt Software Architecture

```
d:/Major_Project/
├── app.py                            # Streamlit entry point / Dashboard orchestrator
├── config/
│   ├── __init__.py
│   └── settings.py                   # Centralized paths, thresholds, model names, weights
├── modules/
│   ├── __init__.py
│   ├── product_input/
│   │   ├── __init__.py
│   │   ├── url_parser.py             # E-commerce URL scraper (Amazon, Flipkart, generic HTML)
│   │   ├── image_input.py            # Advertised image validation & OCR feature extraction
│   │   └── schema.py                 # Pydantic data models for Product, Claim, Evidence
│   ├── preprocessing/
│   │   ├── __init__.py
│   │   ├── text_cleaner.py           # DOM noise removal, review sentence segmenter, fact filter
│   │   └── image_preprocessor.py     # Image normalization, aspect ratio padding, foreground mask
│   ├── claim_extraction/
│   │   ├── __init__.py
│   │   ├── llm_extractor.py          # Structured Gemini extractor with Pydantic JSON schema
│   │   └── rule_extractor.py         # Advanced rule/regex entity-attribute fallback
│   ├── evidence_retrieval/
│   │   ├── __init__.py
│   │   └── semantic_retriever.py     # Sentence-BERT retrieval with claim-level ranking
│   ├── nli_verification/
│   │   ├── __init__.py
│   │   └── cross_encoder_nli.py      # RoBERTa/MiniLM cross-encoder inference with calibration
│   ├── visual_verification/
│   │   ├── __init__.py
│   │   └── visual_comparator.py      # Foreground color delta (LAB), structural contour, edge match
│   ├── evidence_aggregation/
│   │   ├── __init__.py
│   │   └── aggregator.py             # Claim-level evidence synthesis, provenance, confidence
│   ├── pri_engine/
│   │   ├── __init__.py
│   │   └── pri_calculator.py         # Defensible mathematical PRI formulation with breakdown
│   └── classification/
│       ├── __init__.py
│       └── decision_rules.py         # 4-state rule engine (Consistent, Contradictory, Mixed, Insufficient)
├── models/
│   ├── __init__.py
│   └── model_loader.py               # Singleton / cached model loader (CPU & RAM optimized)
├── data/
│   ├── sample/
│   └── benchmark/
│       └── benchmark_products.json   # 25 curated products with verified ground-truth labels
├── evaluation/
│   ├── __init__.py
│   ├── evaluate_benchmark.py         # Automated evaluation script computing Precision/Recall/F1
│   └── metrics_tracker.py
└── tests/
    ├── __init__.py
    ├── test_url_parser.py
    ├── test_claim_extractor.py
    ├── test_retrieval.py
    ├── test_nli.py
    ├── test_visual.py
    └── test_pri_engine.py
```

---

## 4. Phase-by-Phase Implementation Execution Plan

- **Phase 0:** Codebase audit, environment verification, and baseline Git checkpoint (COMPLETED).
- **Phase 1:** Core configuration & Pydantic data schema definition (`config/settings.py`, `modules/product_input/schema.py`).
- **Phase 2:** Multi-modal product input layer (`url_parser.py`, `image_input.py`).
- **Phase 3:** Preprocessing pipeline (`text_cleaner.py`, `image_preprocessor.py`).
- **Phase 4:** Structured atomic claim extraction (`llm_extractor.py`, `rule_extractor.py`).
- **Phase 5:** Evidence retrieval & NLI verification (`semantic_retriever.py`, `cross_encoder_nli.py`).
- **Phase 6:** Evidence aggregation & Mathematical PRI engine (`aggregator.py`, `pri_calculator.py`).
- **Phase 7:** Functional visual verification module (`visual_comparator.py`).
- **Phase 8:** 4-State Final Decision Engine (`decision_rules.py`).
- **Phase 9:** High-performance dashboard redesign (`app.py`, components, charts).
- **Phase 10:** 25-Product Benchmark dataset curation, automated evaluation suite, unit testing, and full documentation.
