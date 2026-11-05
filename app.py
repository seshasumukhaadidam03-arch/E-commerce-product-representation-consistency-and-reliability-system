"""
app.py - Professional AI Research Platform Dashboard
====================================================
End-to-end interface supporting:
1. Product Assessment (URL Input, Image Upload, Manual Input, Benchmark selection)
2. Executive Overview (PRI score gauge, 4-state classification, evidence coverage)
3. Claim-by-Claim Intelligence Breakdown
4. Review Evidence Auditing (S-BERT relevance + NLI Support/Contradiction/Neutral)
5. Multimodal Visual Verification (CIE-Lab Color Delta & SSIM Structural Alignment)
6. Comprehensive Explainability & Downloadable JSON Assessment Report
7. Quantitative Benchmark Evaluation & Scientific Metrics Suite
"""

import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import json
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

from modules.pipeline import ReliabilityAssessmentPipeline
from modules.product_input.schema import UnifiedProductInput, FinalClassification
from modules.product_input.url_parser import ProductURLExtractor
from config.settings import BENCHMARK_DATA_DIR, REPORTS_DIR

# ==========================================
# PAGE CONFIGURATION & STYLING
# ==========================================
st.set_page_config(
    page_title="AI E-Commerce Reliability Assessment",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Clean Professional CSS
st.markdown("""
<style>
    .metric-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .status-badge-consistent {
        background-color: #ecfdf5;
        color: #065f46;
        padding: 4px 12px;
        border-radius: 12px;
        font-weight: 600;
        border: 1px solid #a7f3d0;
    }
    .status-badge-contradictory {
        background-color: #fff1f2;
        color: #9f1239;
        padding: 4px 12px;
        border-radius: 12px;
        font-weight: 600;
        border: 1px solid #fecdd3;
    }
    .status-badge-mixed {
        background-color: #fffbeb;
        color: #92400e;
        padding: 4px 12px;
        border-radius: 12px;
        font-weight: 600;
        border: 1px solid #fde68a;
    }
    .status-badge-insufficient {
        background-color: #f1f5f9;
        color: #475569;
        padding: 4px 12px;
        border-radius: 12px;
        font-weight: 600;
        border: 1px solid #cbd5e1;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# PIPELINE CACHING
# ==========================================
@st.cache_resource
def get_assessment_pipeline():
    return ReliabilityAssessmentPipeline(use_llm_claims=True)

@st.cache_data
def load_benchmark_products():
    path = BENCHMARK_DATA_DIR / "benchmark_products.json"
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

@st.cache_data
def load_evaluation_metrics():
    path = REPORTS_DIR / "evaluation_results.json"
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

pipeline = get_assessment_pipeline()
benchmark_catalog = load_benchmark_products()
eval_data = load_evaluation_metrics()

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================
st.sidebar.title("🛍️ Assessment System")
st.sidebar.caption("AI-Based Product Representation Consistency & Reliability Engine")

nav_selection = st.sidebar.radio(
    "Navigation Mode",
    ["Run Product Assessment", "Benchmark Evaluation Suite", "Architecture & Research Docs"]
)

# ==========================================
# SECTION 1: PRODUCT ASSESSMENT
# ==========================================
if nav_selection == "Run Product Assessment":
    st.title("Product Representation Assessment")
    st.markdown("Audits consistency between **seller representations** (text + photos) and **customer evidence** (reviews + photos).")

    input_mode = st.radio(
        "Choose Ingestion Channel:",
        ["Curated Benchmark Catalog", "Live Product URL", "Manual Data Input"],
        horizontal=True
    )

    product_to_assess = None
    customer_image_upload = None

    if input_mode == "Curated Benchmark Catalog":
        if benchmark_catalog:
            product_titles = [f"[{p['category']}] {p['title'][:65]}..." for p in benchmark_catalog]
            selected_idx = st.selectbox("Select Benchmark Product:", range(len(benchmark_catalog)), format_func=lambda i: product_titles[i])
            raw_p = benchmark_catalog[selected_idx]

            product_to_assess = UnifiedProductInput(
                product_id=raw_p["product_id"],
                title=raw_p["title"],
                features=raw_p.get("features", []),
                seller_images=raw_p.get("seller_images", []),
                customer_reviews=raw_p.get("customer_reviews", []),
                customer_images=raw_p.get("customer_images", []),
                source_type="benchmark_catalog"
            )

            col1, col2 = st.columns([3, 1])
            with col1:
                st.info(f"**Selected:** {raw_p['title']}")
                with st.expander("📝 View Advertised Specifications & Claims", expanded=False):
                    for f in raw_p.get("features", []):
                        st.markdown(f"- {f}")
            with col2:
                st.metric("Reviews Available", len(raw_p.get("customer_reviews", [])))
                st.caption(f"Ground Truth Class: **{raw_p.get('ground_truth_classification', 'N/A')}**")
        else:
            st.warning("No benchmark products found. Run benchmark_generator.py first.")

    elif input_mode == "Live Product URL":
        url_input = st.text_input("Enter E-Commerce Product URL (Amazon, Flipkart, etc.):", placeholder="https://www.amazon.in/dp/B08Z387RXH")
        if url_input:
            url_extractor = ProductURLExtractor()
            if url_extractor.validate_url(url_input):
                with st.spinner("Extracting accessible page representations..."):
                    try:
                        product_to_assess = url_extractor.extract_from_url(url_input)
                        st.success(f"Successfully parsed listing: {product_to_assess.title[:70]}...")
                    except Exception as e:
                        st.error(f"URL Extraction Error: {e}")
            else:
                st.error("Please enter a valid HTTP/HTTPS URL.")

    elif input_mode == "Manual Data Input":
        st.subheader("Manual Representation Ingestion")
        m_title = st.text_input("Product Title:", value="Minimalist RFID Slim Front Pocket Bifold Wallet")
        m_features = st.text_area("Seller Claims / Features (one per line):", value="Crafted with durable top-grain genuine leather.\nEquipped with advanced RFID blocking lining.\nFeatures 6 credit card slots and 1 cash pocket.\nUltra-slim 0.4 inch thickness design.")
        m_reviews = st.text_area("Customer Reviews (one per line):", value="The genuine leather smells authentic and has held up nicely.\nThe card slots are tight at first but easily hold 6 cards.\nExtremely slim wallet, fits into my front pocket effortlessly.")
        
        col_img1, col_img2 = st.columns(2)
        with col_img1:
            seller_img_url = st.text_input("Seller Catalog Image URL (Optional):", value="")
        with col_img2:
            cust_img_url = st.text_input("Customer Uploaded Image URL (Optional):", value="")

        if m_title and m_features:
            feat_list = [f.strip() for f in m_features.strip().split("\n") if f.strip()]
            rev_list = [{"text": r.strip(), "id": f"rev_{i+1}"} for i, r in enumerate(m_reviews.strip().split("\n")) if r.strip()]

            product_to_assess = UnifiedProductInput(
                product_id="manual_test",
                title=m_title,
                features=feat_list,
                seller_images=[seller_img_url] if seller_img_url else [],
                customer_reviews=rev_list,
                customer_images=[cust_img_url] if cust_img_url else [],
                source_type="manual"
            )

    st.divider()

    if product_to_assess:
        if st.button("🚀 Execute AI Reliability Assessment", type="primary", use_container_width=True):
            with st.spinner("Running End-to-End Pipeline (S-BERT Retrieval -> NLI Verification -> Visual Inspection -> PRI Engine)..."):
                report = pipeline.assess_product(product_to_assess)

            st.session_state["latest_report"] = report

    # ==========================================
    # DISPLAY ASSESSMENT REPORT
    # ==========================================
    if "latest_report" in st.session_state:
        report = st.session_state["latest_report"]

        st.subheader("📊 Assessment Summary")

        # KPI Metrics Row
        col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)

        # Classification Badge Styling
        cls_val = report.classification.value
        if cls_val == "CONSISTENT":
            cls_badge = '<span class="status-badge-consistent">🟢 CONSISTENT</span>'
        elif cls_val == "CONTRADICTORY":
            cls_badge = '<span class="status-badge-contradictory">🔴 CONTRADICTORY</span>'
        elif cls_val == "MIXED EVIDENCE":
            cls_badge = '<span class="status-badge-mixed">🟡 MIXED EVIDENCE</span>'
        else:
            cls_badge = '<span class="status-badge-insufficient">⚪ INSUFFICIENT EVIDENCE</span>'

        with col_kpi1:
            st.metric("Product Reliability Index (PRI)", f"{report.overall_pri} / 100")
        with col_kpi2:
            st.markdown(f"**Final Verdict**<br>{cls_badge}", unsafe_allow_html=True)
        with col_kpi3:
            st.metric("Evidence Coverage", f"{int(report.coverage * 100)}%", f"{report.evaluated_claims}/{report.total_claims} claims covered")
        with col_kpi4:
            st.metric("Text PRI / Visual Contribution", f"{report.text_pri}%", f"Visual: {report.visual_pri if report.visual_pri is not None else 'N/A'}")

        st.divider()

        # Detailed Analytical Tabs
        tab_overview, tab_claims, tab_reviews, tab_visual, tab_report = st.tabs([
            "Executive Overview",
            "Claim Intelligence",
            "Review Evidence Audit",
            "Multimodal Visual Inspection",
            "Downloadable Audit Report"
        ])

        with tab_overview:
            st.markdown("### Decision Findings & Provenance")
            col_ov1, col_ov2 = st.columns(2)

            with col_ov1:
                st.markdown("#### ❌ Key Discrepancies Detected")
                if report.key_discrepancies:
                    for d in report.key_discrepancies:
                        st.error(d)
                else:
                    st.success("No critical contradictions or discrepancies identified.")

            with col_ov2:
                st.markdown("#### ✅ Corroborated Attributes")
                if report.supporting_reasons:
                    for s in report.supporting_reasons:
                        st.info(s)
                else:
                    st.warning("No explicit corroborating review evidence found.")

        with tab_claims:
            st.markdown("### Claim-by-Claim Verification Breakdown")
            for c in report.claims:
                with st.expander(f"[{c.claim.attribute.upper()}] {c.claim.text} — Status: {c.status} ({c.consistency_percentage}%)"):
                    st.write(f"**Evidence Votes:** {c.support_count} Supporting | {c.neutral_count} Consistent/Neutral | {c.contradict_count} Contradicting")
                    st.progress(c.consistency_percentage / 100.0)
                    for ev in c.evidence:
                        if ev.verdict.value == "Contradiction":
                            st.error(f"[{ev.verdict.value.upper()}] \"{ev.sentence}\" (Relevance: {ev.relevance_score})")
                        elif ev.verdict.value == "Support":
                            st.success(f"[{ev.verdict.value.upper()}] \"{ev.sentence}\" (Relevance: {ev.relevance_score})")
                        else:
                            st.info(f"[{ev.verdict.value.upper()}] \"{ev.sentence}\" (Relevance: {ev.relevance_score})")

        with tab_reviews:
            st.markdown("### Customer Evidence Provenance")
            st.write(f"Total reviews processed: **{report.provenance_metadata.get('cleaned_reviews_count', 0)} factual sentences**")
            all_evidence = []
            for c in report.claims:
                for ev in c.evidence:
                    all_evidence.append({
                        "Claim": c.claim.text[:40] + "...",
                        "Evidence Sentence": ev.sentence,
                        "Verdict": ev.verdict.value,
                        "Relevance": ev.relevance_score,
                        "Confidence": max(ev.confidence_scores.values()) if ev.confidence_scores else 0.0
                    })
            if all_evidence:
                st.dataframe(all_evidence, use_container_width=True)
            else:
                st.info("No matching evidence sentences met the retrieval threshold.")

        with tab_visual:
            st.markdown("### Multimodal Visual Verification")
            v_obs = report.visual_assessment
            if v_obs.available:
                col_v1, col_v2 = st.columns(2)
                with col_v1:
                    st.metric("CIE-Lab Color Similarity", f"{v_obs.color_similarity}%")
                with col_v2:
                    st.metric("SSIM Structural Match", f"{v_obs.structural_similarity}%")
                for obs in v_obs.observations:
                    st.write(f"• {obs}")
            else:
                st.info("Visual verification inactive: No valid pair of seller catalog and customer unboxing images provided.")

        with tab_report:
            st.markdown("### Full Audit JSON Report")
            json_str = report.model_dump_json(indent=2)
            st.download_button(
                label="📥 Download Assessment Report (JSON)",
                data=json_str,
                file_name=f"reliability_report_{report.product_id}.json",
                mime="application/json"
            )
            st.code(json_str, language="json")

# ==========================================
# SECTION 2: BENCHMARK EVALUATION SUITE
# ==========================================
elif nav_selection == "Benchmark Evaluation Suite":
    st.title("Automated Benchmark Evaluation Suite")
    st.markdown("Quantitative evaluation of the assessment engine across the **25-product curated benchmark dataset**.")

    if eval_data:
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric("Overall Accuracy", f"{eval_data['accuracy']}%", f"{eval_data['correct_predictions']}/{eval_data['total_products']} correct")
        with col_m2:
            st.metric("Macro F1-Score", f"{eval_data['macro_f1']}")
        with col_m3:
            st.metric("Total Test Products", f"{eval_data['total_products']}")

        st.subheader("Classification Performance by Class")
        per_class_df = []
        for c, m in eval_data["per_class_metrics"].items():
            per_class_df.append({
                "Classification": c,
                "Precision": m["precision"],
                "Recall": m["recall"],
                "F1-Score": m["f1"],
                "Support Count": m["support"]
            })
        st.dataframe(per_class_df, use_container_width=True)

        st.subheader("Confusion Matrix")
        matrix_data = eval_data["confusion_matrix"]
        classes = list(matrix_data.keys())
        z_matrix = [[matrix_data[true_c][pred_c] for pred_c in classes] for true_c in classes]

        fig = px.imshow(
            z_matrix,
            x=classes,
            y=classes,
            labels=dict(x="Predicted Class", y="Ground Truth Class", color="Count"),
            text_auto=True,
            color_continuous_scale="Blues"
        )
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("No evaluation metrics found. Please run evaluation/evaluate_benchmark.py to generate results.")

# ==========================================
# SECTION 3: ARCHITECTURE & RESEARCH DOCS
# ==========================================
elif nav_selection == "Architecture & Research Docs":
    st.title("System Architecture & Research Specification")
    st.markdown("""
    ### Project Overview
    **Title:** AI-Based E-Commerce Product Representation Consistency and Reliability Assessment System  
    **Institution:** Matrusri Engineering College (Affiliated to Osmania University)  
    **Department:** Department of Computer Science and Engineering  
    **Academic Year:** 2025 – 2026

    ---

    ### Pipeline Workflow
    ```
    1. Multi-Modal Ingestion (URL Scraping / Image Upload / Manual Input)
           │
           ▼
    2. Data Preprocessing (DOM Cleaning, Review Sentence Segmentation, Subjectivity Filtering)
           │
           ▼
    3. Atomic Claim Extraction (Gemini 3.8 Flash / Rule-Based Entity-Attribute Extractor)
           │
           ▼
    4. Dense Semantic Evidence Retrieval (Sentence-BERT all-MiniLM-L6-v2)
           │
           ▼
    5. Directional NLI Verification (Cross-Encoder nli-MiniLM2-L6-H768)
           │
           ▼
    6. Multimodal Visual Verification (CIE-Lab Color Delta E + SSIM Structural Match)
           │
           ▼
    7. Evidence Aggregation & Product Reliability Index (PRI Engine)
           │
           ▼
    8. 4-State Final Decision Engine (CONSISTENT, CONTRADICTORY, MIXED, INSUFFICIENT)
    ```

    ---

    ### The 4 Formal Assessment Classes
    1. **CONSISTENT:** Verified claims predominantly confirmed by customer evidence with zero contradictions and high coverage.
    2. **CONTRADICTORY:** One or more material discrepancies between advertised claims and customer reality.
    3. **MIXED EVIDENCE:** Substantial supporting evidence and contradicting evidence co-exist across claims.
    4. **INSUFFICIENT EVIDENCE:** Sparse or off-topic customer reviews inadequate for statistical verification.
    """)
