"""
evaluate_benchmark.py - Automated Benchmark Evaluation Suite
============================================================
Evaluates the rebuilt system across the 25 curated benchmark products.
Computes quantitative scientific performance metrics:
- Classification Accuracy
- Precision, Recall, Macro-F1 across the 4 classes
- Confusion Matrix
- Claim Extraction & Evidence Retrieval coverage metrics
Saves a complete scientific report to reports/evaluation_results.json
"""

import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from collections import defaultdict
from modules.pipeline import ReliabilityAssessmentPipeline
from modules.product_input.schema import UnifiedProductInput
from config.settings import BENCHMARK_DATA_DIR, REPORTS_DIR

CLASSES = ["CONSISTENT", "CONTRADICTORY", "MIXED EVIDENCE", "INSUFFICIENT EVIDENCE"]

def evaluate_system():
    benchmark_file = BENCHMARK_DATA_DIR / "benchmark_products.json"
    if not benchmark_file.exists():
        raise FileNotFoundError(f"Benchmark file not found at {benchmark_file}")

    with open(benchmark_file, "r", encoding="utf-8") as f:
        products = json.load(f)

    print(f"\n=======================================================")
    print(f"STARTING BENCHMARK EVALUATION ({len(products)} Products)")
    print(f"=======================================================\n")

    # Use Rule-based claim extraction for fast, deterministic evaluation
    pipeline = ReliabilityAssessmentPipeline(use_llm_claims=False)

    y_true = []
    y_pred = []
    detailed_results = []

    for idx, p in enumerate(products, 1):
        print(f"[{idx}/{len(products)}] Evaluating: {p['title'][:55]}...")
        
        prod_input = UnifiedProductInput(
            product_id=p["product_id"],
            title=p["title"],
            features=p.get("features", []),
            seller_images=p.get("seller_images", []),
            customer_reviews=p.get("customer_reviews", []),
            customer_images=p.get("customer_images", []),
            source_type="benchmark"
        )

        cust_img = p["customer_images"][0] if p.get("customer_images") else None
        report = pipeline.assess_product(prod_input, customer_image_url=cust_img)

        gt = p["ground_truth_classification"]
        pred = report.classification.value

        y_true.append(gt)
        y_pred.append(pred)

        detailed_results.append({
            "product_id": p["product_id"],
            "title": p["title"],
            "category": p.get("category", "General"),
            "ground_truth": gt,
            "predicted": pred,
            "match": (gt == pred),
            "overall_pri": report.overall_pri,
            "text_pri": report.text_pri,
            "visual_pri": report.visual_pri,
            "coverage": report.coverage,
            "claims_count": report.total_claims,
            "discrepancies": report.key_discrepancies
        })

    # =========================================================
    # CALCULATE METRICS
    # =========================================================
    total = len(y_true)
    correct = sum(1 for yt, yp in zip(y_true, y_pred) if yt == yp)
    accuracy = correct / total

    # Confusion Matrix
    confusion_matrix = {c_true: {c_pred: 0 for c_pred in CLASSES} for c_true in CLASSES}
    for yt, yp in zip(y_true, y_pred):
        confusion_matrix[yt][yp] += 1

    # Precision, Recall, F1 per class
    metrics_per_class = {}
    f1_scores = []

    for c in CLASSES:
        tp = confusion_matrix[c][c]
        fp = sum(confusion_matrix[other][c] for other in CLASSES if other != c)
        fn = sum(confusion_matrix[c][other] for other in CLASSES if other != c)

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

        metrics_per_class[c] = {
            "precision": round(precision, 3),
            "recall": round(recall, 3),
            "f1": round(f1, 3),
            "support": sum(confusion_matrix[c].values())
        }
        f1_scores.append(f1)

    macro_f1 = sum(f1_scores) / len(f1_scores)

    summary_report = {
        "total_products": total,
        "correct_predictions": correct,
        "accuracy": round(accuracy * 100, 1),
        "macro_f1": round(macro_f1, 3),
        "per_class_metrics": metrics_per_class,
        "confusion_matrix": confusion_matrix,
        "detailed_results": detailed_results
    }

    report_path = REPORTS_DIR / "evaluation_results.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(summary_report, f, indent=2)

    print("\n" + "=" * 60)
    print("BENCHMARK EVALUATION SUMMARY")
    print("=" * 60)
    print(f"Overall Accuracy:  {accuracy * 100:.1f}% ({correct}/{total} correct)")
    print(f"Macro F1-Score:    {macro_f1:.3f}")
    print("-" * 60)
    print(f"{'Class':24s} | {'Precision':9s} | {'Recall':7s} | {'F1-Score':8s}")
    print("-" * 60)
    for c in CLASSES:
        m = metrics_per_class[c]
        print(f"{c:24s} | {m['precision']:9.3f} | {m['recall']:7.3f} | {m['f1']:8.3f}")
    print("=" * 60)
    print(f"Full scientific report saved to: {report_path}\n")

    return summary_report

if __name__ == "__main__":
    evaluate_system()
