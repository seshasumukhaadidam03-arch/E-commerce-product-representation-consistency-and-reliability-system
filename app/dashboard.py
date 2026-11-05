"""
dashboard.py - Streamlit Web Interface
=======================================
Two modes:
  1. Sample Products: Pre-loaded dataset for demo
  2. Manual Input: Paste any product's claims and reviews to test live
"""

import streamlit as st
import sys
import os
import json

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from pipeline import ReliabilityPipeline

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="Product Reliability Assessment",
    page_icon="🛍️",
    layout="wide"
)

st.title("🛍️ Product Reliability Assessment System")
st.caption("AI-Based E-Commerce Product Representation Consistency & Reliability Assessment | Review 1 - Proof of Concept")

# ==========================================
# CACHE: Load models ONCE and keep in memory
# ==========================================
@st.cache_resource
def load_pipeline():
    return ReliabilityPipeline()

@st.cache_data
def load_sample_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "data", "sample", "sample_products.json")
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)

# ==========================================
# SIDEBAR
# ==========================================
st.sidebar.header("Control Panel")
mode = st.sidebar.radio("Input Mode:", ["Sample Products", "Manual Input"])

# ==========================================
# BUILD PRODUCT DATA BASED ON MODE
# ==========================================
selected_product = None

if mode == "Sample Products":
    try:
        products = load_sample_data()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()

    product_names = [p["title"][:60] + "..." for p in products]
    selected_idx = st.sidebar.selectbox(
        "Select Product:", range(len(products)),
        format_func=lambda i: product_names[i]
    )
    selected_product = products[selected_idx]

    # Show seller info
    col_info1, col_info2 = st.columns([2, 1])
    with col_info1:
        st.markdown(f"### 📦 {selected_product['title']}")
    with col_info2:
        st.metric("Reviews Available", len(selected_product.get("reviews", [])))

    with st.expander("📝 View Seller's Advertised Features", expanded=True):
        for feature in selected_product["features"]:
            st.markdown(f"- {feature}")

elif mode == "Manual Input":
    st.markdown("### 📝 Paste Product Details")
    st.info("Enter the seller's claims and customer reviews below. One item per line.")

    manual_title = st.text_input(
        "Product Name:",
        placeholder="e.g. Noise-Cancelling Bluetooth Headphones"
    )

    manual_features = st.text_area(
        "Seller's Claims (one per line):",
        placeholder="40-hour battery life\nActive Noise Cancellation\nPremium deep bass sound quality",
        height=100
    )

    manual_reviews = st.text_area(
        "Customer Reviews (one per line):",
        placeholder="Battery barely lasts 10 hours on a full charge.\nSound quality is amazing with very clear and deep bass.\nNoise cancellation works perfectly on flights.\nThe headphones broke after 2 weeks of use.",
        height=130
    )

    if manual_title and manual_features and manual_reviews:
        features_list = [f.strip() for f in manual_features.strip().split('\n') if f.strip()]
        reviews_list = [{"text": r.strip()} for r in manual_reviews.strip().split('\n') if r.strip()]

        selected_product = {
            "product_id": "manual",
            "title": manual_title,
            "features": features_list,
            "description": [],
            "reviews": reviews_list,
            "images": []
        }

        with st.expander("📝 Your Input (Seller Claims)", expanded=True):
            for f in features_list:
                st.markdown(f"- {f}")

st.divider()

# ==========================================
# RUN ASSESSMENT
# ==========================================
if selected_product:
    if st.button("🚀 Run AI Reliability Assessment", type="primary", use_container_width=True):

        with st.spinner("Running AI Analysis..."):
            pipeline = load_pipeline()
            results = pipeline.analyze_product(selected_product)

        # ==================================
        # RESULTS DISPLAY
        # ==================================
        st.header("📊 Assessment Results")

        # --- PRI Score with color ---
        pri = results["overall_pri"]
        if pri >= 60:
            score_color = "🟢"
            score_label = "HIGH RELIABILITY"
        elif pri >= 30:
            score_color = "🟡"
            score_label = "MODERATE RELIABILITY"
        else:
            score_color = "🔴"
            score_label = "LOW RELIABILITY"

        col_score, col_label = st.columns([1, 2])
        with col_score:
            st.metric("Product Reliability Index (PRI)", f"{pri} / 100")
        with col_label:
            st.markdown(f"### {score_color} {score_label}")

        st.divider()

        # --- Customer Review Breakdown ---
        st.markdown("### 🗣️ Customer Review Evidence")

        supportive = []
        contradicting = []
        neutral = []

        for claim_data in results["claim_details"]:
            claim_text = claim_data["claim"]
            for ev in claim_data.get("evidence", []):
                text = ev["text"]
                verdict = ev["verdict"]
                conf = ev.get("confidence", {})

                entry = {
                    "text": text,
                    "claim": claim_text,
                    "confidence": conf
                }

                if verdict == "Contradiction" and conf.get("Contradiction", 0) > 40:
                    contradicting.append(entry)
                elif verdict == "Support" and conf.get("Support", 0) > 40:
                    supportive.append(entry)
                else:
                    neutral.append(entry)

        # Remove duplicates by text
        seen = set()
        def dedup(lst):
            result = []
            for item in lst:
                if item["text"] not in seen:
                    seen.add(item["text"])
                    result.append(item)
            return result

        supportive = dedup(supportive)
        contradicting = dedup(contradicting)
        neutral = dedup(neutral)

        # Display side by side
        col1, col2 = st.columns(2)

        with col1:
            st.subheader(f"✅ Supportive ({len(supportive)})")
            if not supportive:
                st.info("No strongly supportive evidence found.")
            for item in supportive:
                st.success(f'"{item["text"]}"')
                st.caption(f"Supports claim: _{item['claim'][:80]}_")

        with col2:
            st.subheader(f"❌ Contradicting ({len(contradicting)})")
            if not contradicting:
                st.info("No contradicting evidence found.")
            for item in contradicting:
                st.error(f'"{item["text"]}"')
                st.caption(f"Contradicts claim: _{item['claim'][:80]}_")

        with st.expander(f"➖ Neutral / Unrelated Reviews ({len(neutral)})"):
            if not neutral:
                st.write("None.")
            for item in neutral:
                st.write(f'"{item["text"]}"')

        # --- Claim-level Detail ---
        st.divider()
        st.markdown("### Claim-by-Claim Breakdown")
        for i, cd in enumerate(results["claim_details"], 1):
            cons = cd.get("consistent_count", 0)
            cont = cd.get("contradict_count", 0)
            total = cd.get("total_evidence", cons + cont)
            label = f"Claim {i}: {cd['claim']}  |  Consistent: {cons}  Contradict: {cont}  (of {total})"
            with st.expander(label):
                st.write(f"**Evidence:** {cons} consistent, {cont} contradict out of {total} relevant reviews")
                st.write(f"**Claim Consistency:** {cd['support']}%")
                for ev in cd["evidence"]:
                    v = ev["verdict"]
                    if v == "Support":
                        st.success(f"[SUPPORT] \"{ev['text']}\"")
                    elif v == "Consistent":
                        st.info(f"[CONSISTENT] \"{ev['text']}\"")
                    elif v == "Contradiction":
                        st.error(f"[CONTRADICTION] \"{ev['text']}\"")
                    else:
                        st.info(f"[{v}] \"{ev['text']}\"")

else:
    if mode == "Manual Input":
        st.warning("Please fill in all fields above to run the assessment.")
