"""
generate_review_1_ppt.py
========================
Generates the official 6-Slide PowerPoint Presentation (.pptx)
for Major Project Review-I:
"AI-Based E-Commerce Product Representation Consistency and Reliability Assessment System"
Matrusri Engineering College - Department of CSE
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    # Color Palette
    PRIMARY = RGBColor(15, 34, 64)       # Deep Navy
    SECONDARY = RGBColor(26, 86, 160)    # Royal Blue
    ACCENT = RGBColor(14, 116, 144)      # Teal / Cyan Accent
    BG_LIGHT = RGBColor(248, 250, 252)   # Slate 50
    CARD_BG = RGBColor(255, 255, 255)    # Pure White
    CARD_BORDER = RGBColor(226, 232, 240)# Slate 200
    TEXT_DARK = RGBColor(15, 23, 42)     # Slate 900
    TEXT_MUTED = RGBColor(71, 85, 105)   # Slate 600
    SUCCESS = RGBColor(16, 149, 113)     # Emerald
    WARNING = RGBColor(225, 29, 72)      # Rose/Red

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_LIGHT
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_tag):
        # Header banner card
        banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.5), Inches(11.733), Inches(1.0))
        banner.fill.solid()
        banner.fill.fore_color.rgb = CARD_BG
        banner.line.color.rgb = CARD_BORDER
        banner.line.width = Pt(1)

        tf = banner.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.3)
        tf.margin_top = Inches(0.12)
        tf.margin_right = Inches(0.3)
        tf.margin_bottom = Inches(0.1)

        p_tag = tf.paragraphs[0]
        p_tag.text = category_tag.upper()
        p_tag.font.size = Pt(10)
        p_tag.font.bold = True
        p_tag.font.color.rgb = SECONDARY

        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.size = Pt(20)
        p_title.font.bold = True
        p_title.font.color.rgb = PRIMARY

    def add_card(slide, left, top, width, height, border_color=CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = border_color
        card.line.width = Pt(1.2)
        return card

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1)

    # Accent decorative top strip
    strip = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.2))
    strip.fill.solid()
    strip.fill.fore_color.rgb = SECONDARY
    strip.line.fill.background()

    # Main Center Card
    center_card = add_card(slide1, Inches(1.0), Inches(0.7), Inches(11.333), Inches(6.1))
    tf1 = center_card.text_frame
    tf1.word_wrap = True
    tf1.margin_left = Inches(0.6)
    tf1.margin_right = Inches(0.6)
    tf1.margin_top = Inches(0.4)

    p = tf1.paragraphs[0]
    p.text = "MAJOR PROJECT REVIEW — I"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = SECONDARY
    p.alignment = PP_ALIGN.CENTER

    p = tf1.add_paragraph()
    p.text = "AI-Based E-Commerce Product Representation\nConsistency and Reliability Assessment System"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = PRIMARY
    p.alignment = PP_ALIGN.CENTER
    p.space_before = Pt(8)
    p.space_after = Pt(6)

    p = tf1.add_paragraph()
    p.text = "Department of Computer Science and Engineering\nMatrusri Engineering College, Saidabad, Hyderabad | Academic Year 2025–2026"
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_MUTED
    p.alignment = PP_ALIGN.CENTER
    p.space_after = Pt(20)

    # Three-column layout for Team, Guide, Coordinators inside Slide 1
    # 1. Project Team Card
    c_team = add_card(slide1, Inches(1.4), Inches(3.6), Inches(3.2), Inches(2.8))
    tf_t = c_team.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = Inches(0.25)
    tf_t.margin_top = Inches(0.2)
    p = tf_t.paragraphs[0]
    p.text = "PROJECT TEAM"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = SECONDARY

    team_members = [
        "Student 1 — Roll Number",
        "Student 2 — Roll Number",
        "Student 3 — Roll Number",
        "Student 4 — Roll Number"
    ]
    for tm in team_members:
        p = tf_t.add_paragraph()
        p.text = f"•  {tm}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(4)

    # 2. Project Guide Card
    c_guide = add_card(slide1, Inches(5.066), Inches(3.6), Inches(3.2), Inches(2.8))
    tf_g = c_guide.text_frame
    tf_g.word_wrap = True
    tf_g.margin_left = Inches(0.25)
    tf_g.margin_top = Inches(0.2)
    p = tf_g.paragraphs[0]
    p.text = "PROJECT GUIDE"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = SECONDARY

    p = tf_g.add_paragraph()
    p.text = "[Internal Guide Name]"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = TEXT_DARK
    p.space_before = Pt(8)

    p = tf_g.add_paragraph()
    p.text = "Assistant / Associate Professor\nDepartment of CSE\nMatrusri Engineering College"
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_MUTED
    p.space_before = Pt(4)

    # 3. Project Coordinators Card
    c_coord = add_card(slide1, Inches(8.733), Inches(3.6), Inches(3.2), Inches(2.8))
    tf_c = c_coord.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = Inches(0.25)
    tf_c.margin_top = Inches(0.2)
    p = tf_c.paragraphs[0]
    p.text = "PROJECT COORDINATORS"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = SECONDARY

    p = tf_c.add_paragraph()
    p.text = "Dr. L. K. Indumathi"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEXT_DARK
    p.space_before = Pt(8)
    p = tf_c.add_paragraph()
    p.text = "Associate Professor, Dept. of CSE"
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_MUTED

    p = tf_c.add_paragraph()
    p.text = "Mrs. K. Bhagya Laxmi"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEXT_DARK
    p.space_before = Pt(8)
    p = tf_c.add_paragraph()
    p.text = "Assistant Professor, Dept. of CSE"
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_MUTED

    slide1.notes_slide.notes_text_frame.text = (
        "Good morning respected coordinators Dr. Indumathi ma'am, Mrs. Bhagya Laxmi ma'am, "
        "our project guide, and faculty members. Today we are presenting Review-I of our Major Project titled "
        "'AI-Based E-Commerce Product Representation Consistency and Reliability Assessment System'. "
        "In this review, we will establish the real-world problem, underlying research background, literature survey, "
        "research gaps, project scope, finalized objectives, and demonstrate our initial proof-of-concept progress."
    )

    # =========================================================================
    # SLIDE 2: INTRODUCTION & BACKGROUND KNOWLEDGE
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2)
    add_header(slide2, "Introduction & Core Background Concepts", "Official Area 1 & 2 — Context & Foundations")

    # Left Card: E-Commerce Reality
    c_left2 = add_card(slide2, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.3))
    tf2_l = c_left2.text_frame
    tf2_l.word_wrap = True
    tf2_l.margin_left = Inches(0.35)
    tf2_l.margin_top = Inches(0.3)
    tf2_l.margin_right = Inches(0.35)

    p = tf2_l.paragraphs[0]
    p.text = "E-Commerce Information Asymmetry"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = PRIMARY

    points_l = [
        ("The Buyer's Dilemma:", " Online shoppers cannot touch, test, or inspect products physically prior to purchase; they rely completely on digital representations."),
        ("Seller Representations:", " Catalog titles, bullet claims, technical specs, and professionally styled marketing photographs."),
        ("Customer Evidence:", " Post-purchase customer reviews, verified feedback, and real unboxing photographs."),
        ("The Discrepancy Phenomenon:", " Seller claims frequently diverge from physical product reality, leading to consumer distrust and massive return rates ($800B+ globally).")
    ]
    for title, desc in points_l:
        p = tf2_l.add_paragraph()
        p.text = f"•  {title}"
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = SECONDARY
        p.space_before = Pt(8)
        
        # Add normal text
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = TEXT_DARK

    # Right Card: Technical Concepts
    c_right2 = add_card(slide2, Inches(6.8), Inches(1.7), Inches(5.733), Inches(5.3))
    tf2_r = c_right2.text_frame
    tf2_r.word_wrap = True
    tf2_r.margin_left = Inches(0.35)
    tf2_r.margin_top = Inches(0.3)
    tf2_r.margin_right = Inches(0.35)

    p = tf2_r.paragraphs[0]
    p.text = "Essential Technical Foundations"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = PRIMARY

    points_r = [
        ("Atomic Claim:", " A discrete, single-attribute testable assertion (e.g., '100% genuine leather' or '7 credit card slots') isolated from subjective fluff ('the best wallet ever')."),
        ("Dense Semantic Retrieval (S-BERT):", " Sentence-BERT transforms claims and review sentences into dense 384-dimensional vector embeddings to retrieve topically relevant reviews via cosine similarity in milliseconds."),
        ("Natural Language Inference (NLI):", " Directional cross-encoder logic where Premise = Customer Review Observation and Hypothesis = Seller Claim. Outputs Entailment (Support), Contradiction, or Neutral.")
    ]
    for title, desc in points_r:
        p = tf2_r.add_paragraph()
        p.text = f"•  {title}"
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = ACCENT
        p.space_before = Pt(8)
        
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = TEXT_DARK

    slide2.notes_slide.notes_text_frame.text = (
        "When shopping online, buyers face severe information asymmetry. We cannot physically inspect items, "
        "so we rely on seller representations: text claims and catalog photos. However, post-purchase customer reviews "
        "and unboxing photos frequently contradict seller promises. To evaluate this computationally, our system decomposes "
        "marketing text into 'Atomic Claims'—testable factual statements. We then utilize Sentence-BERT to retrieve "
        "topically relevant customer reviews and apply Natural Language Inference (NLI) to mathematically verify whether "
        "customer observations support or contradict each seller claim."
    )

    # =========================================================================
    # SLIDE 3: PROBLEM STATEMENT
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3)
    add_header(slide3, "Problem Statement & Analytical Gaps", "Official Area 3 — The Core Challenge")

    # Card 1: Concrete Example of Inconsistency
    c3_top = add_card(slide3, Inches(0.8), Inches(1.7), Inches(11.733), Inches(1.8))
    tf3_top = c3_top.text_frame
    tf3_top.word_wrap = True
    tf3_top.margin_left = Inches(0.35)
    tf3_top.margin_top = Inches(0.18)
    tf3_top.margin_right = Inches(0.35)

    p = tf3_top.paragraphs[0]
    p.text = "The Cross-Representation Inconsistency Problem"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = PRIMARY

    p = tf3_top.add_paragraph()
    p.text = "• Seller Claim (Hypothesis): "
    p.font.bold = True
    p.font.size = Pt(10.5)
    p.font.color.rgb = SECONDARY
    run = p.add_run()
    run.text = "\"100% waterproof shower cap with leakproof silicone seal\""
    run.font.bold = False
    run.font.color.rgb = TEXT_DARK

    p = tf3_top.add_paragraph()
    p.text = "• Customer Evidence (Premise): "
    p.font.bold = True
    p.font.size = Pt(10.5)
    p.font.color.rgb = WARNING
    run = p.add_run()
    run.text = "\"Water seeped through the seams immediately; my hair got completely soaked in the shower.\""
    run.font.bold = False
    run.font.color.rgb = TEXT_DARK

    p = tf3_top.add_paragraph()
    p.text = "• Logical Outcome: Direct Contradiction — yet the product maintains an inflated 4.2-star rating due to gift packaging reviews."
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_MUTED
    p.space_before = Pt(3)

    # Card 2: Why Existing Tools Fail (Left)
    c3_bot_l = add_card(slide3, Inches(0.8), Inches(3.7), Inches(5.6), Inches(3.3))
    tf3_bl = c3_bot_l.text_frame
    tf3_bl.word_wrap = True
    tf3_bl.margin_left = Inches(0.35)
    tf3_bl.margin_top = Inches(0.2)
    tf3_bl.margin_right = Inches(0.35)

    p = tf3_bl.paragraphs[0]
    p.text = "Why Existing Marketplace Tools Fail"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = PRIMARY

    fails = [
        ("Star Ratings (1–5 Stars):", " Aggregates overall satisfaction into a single coarse number. Fails to indicate whether specific technical attributes (e.g., waterproof, leather) held true."),
        ("Sentiment Analysis:", " Measures emotional polarity (positive/negative), not factual veracity. A polite review stating 'Size runs 2 sizes small' is classified as neutral/positive, masking defect.")
    ]
    for title, desc in fails:
        p = tf3_bl.add_paragraph()
        p.text = f"•  {title}"
        p.font.bold = True
        p.font.size = Pt(10.5)
        p.font.color.rgb = WARNING
        p.space_before = Pt(6)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = TEXT_DARK

    # Card 3: Formal Problem Statement (Right)
    c3_bot_r = add_card(slide3, Inches(6.8), Inches(3.7), Inches(5.733), Inches(3.3), border_color=SECONDARY)
    tf3_br = c3_bot_r.text_frame
    tf3_br.word_wrap = True
    tf3_br.margin_left = Inches(0.35)
    tf3_br.margin_top = Inches(0.2)
    tf3_br.margin_right = Inches(0.35)

    p = tf3_br.paragraphs[0]
    p.text = "Formal Problem Statement"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = SECONDARY

    p = tf3_br.add_paragraph()
    p.text = (
        "\"To design an automated, evidence-based assessment framework that extracts atomic product claims "
        "from seller representations, retrieves relevant post-purchase customer evidence, evaluates directional consistency "
        "(Support, Contradiction, Neutrality), and provides an interpretable reliability audit without relying on coarse star ratings.\""
    )
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_DARK
    p.space_before = Pt(6)

    p = tf3_br.add_paragraph()
    p.text = "Critical Boundary Definition:"
    p.font.bold = True
    p.font.size = Pt(10.5)
    p.font.color.rgb = PRIMARY
    p.space_before = Pt(8)

    p = tf3_br.add_paragraph()
    p.text = "• The system audits empirical consistency between seller claims and customer evidence; it does NOT perform physical lab testing, chemical analysis, or certify legal authenticity."
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_MUTED

    slide3.notes_slide.notes_text_frame.text = (
        "The fundamental problem is that e-commerce platforms offer no mechanism to check if a specific seller claim "
        "is actually true according to customer experiences. If a seller promises a 'Waterproof Shower Cap' and a customer "
        "writes 'water seeped right through', that is a direct contradiction. Star ratings cannot expose this because ratings "
        "average everything together. Sentiment analysis only detects whether a customer is happy or angry, not whether a specific "
        "specification was fulfilled. Our problem statement addresses this: we evaluate the directional consistency of seller claims "
        "against empirical review evidence. We do not claim to detect counterfeit items or verify legal authenticity; we audit the empirical consistency of digital representations."
    )

    # =========================================================================
    # SLIDE 4: LITERATURE SURVEY & RESEARCH GAP
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4)
    add_header(slide4, "Literature Survey & Research Gap Analysis", "Official Area 4 — Related Works & Innovation")

    # Table for Literature Survey
    table_shape = slide4.shapes.add_table(4, 4, Inches(0.8), Inches(1.7), Inches(11.733), Inches(2.6))
    table = table_shape.table

    # Column widths
    table.columns[0].width = Inches(2.4)
    table.columns[1].width = Inches(2.9)
    table.columns[2].width = Inches(3.2)
    table.columns[3].width = Inches(3.233)

    headers = ["Paper & Citation", "Architecture / Method", "Key Contribution", "Identified Limitation"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = PRIMARY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(10.5)
        p.font.color.rgb = RGBColor(255, 255, 255)

    rows_data = [
        ("PRAISE (ACL 2025)\nQidwai et al. (IIIT-H, UPenn, ASU)",
         "Sequential LLM prompting (Gemini 2.0 Flash) on customer reviews.",
         "Demonstrated LLM feasibility for structured attribute extraction from reviews.",
         "Text-only (ignores photos); high latency & cost (~2R+1 API calls); no aggregated reliability score."),
        ("Sentence-BERT (EMNLP 2019)\nReimers & Gurevych",
         "Siamese & triplet network architectures yielding dense vector embeddings.",
         "Reduced semantic search over large text corpora from hours to milliseconds.",
         "Captures topical similarity, but cannot determine directional truth (Entailment vs Contradiction)."),
        ("MultiNLI (NAACL 2018)\nWilliams, Nangia & Bowman",
         "Cross-Encoder Transformer benchmark for Natural Language Inference.",
         "Standardized 3-way directional logic: Entailment, Contradiction, and Neutral.",
         "Trained on formal text; sensitive to noisy colloquial e-commerce text and DOM artifacts.")
    ]

    for row_idx, data in enumerate(rows_data, start=1):
        for col_idx, text in enumerate(data):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = CARD_BG if row_idx % 2 == 1 else RGBColor(241, 245, 249)
            p = cell.text_frame.paragraphs[0]
            p.text = text
            p.font.size = Pt(9.5)
            p.font.color.rgb = TEXT_DARK
            if col_idx == 0:
                p.font.bold = True
                p.font.color.rgb = SECONDARY

    # Research Gap Card (Bottom)
    c4_gap = add_card(slide4, Inches(0.8), Inches(4.5), Inches(11.733), Inches(2.5), border_color=ACCENT)
    tf4_gap = c4_gap.text_frame
    tf4_gap.word_wrap = True
    tf4_gap.margin_left = Inches(0.35)
    tf4_gap.margin_top = Inches(0.18)
    tf4_gap.margin_right = Inches(0.35)

    p = tf4_gap.paragraphs[0]
    p.text = "Identified Research Gap & Our Proposed Direction"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ACCENT

    gaps = [
        ("Current Gap in Literature:", " Existing systems rely either on isolated sentiment analysis or costly, brute-force LLM prompting. None offer a lightweight, multimodal framework that connects discrete seller claims with review evidence into an auditable reliability index."),
        ("Our Architectural Synthesis:", " We address these limitations by decoupling claim extraction (performed once via Gemini/Cache) from evidence verification (handled locally via fast S-BERT retrieval and Cross-Encoder NLI), combined with preliminary computer vision inspection to create a cost-effective, auditable system.")
    ]
    for title, desc in gaps:
        p = tf4_gap.add_paragraph()
        p.text = f"•  {title}"
        p.font.bold = True
        p.font.size = Pt(10.5)
        p.font.color.rgb = PRIMARY
        p.space_before = Pt(5)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = TEXT_DARK

    slide4.notes_slide.notes_text_frame.text = (
        "Our primary base paper is PRAISE, published at ACL 2025 by IIIT Hyderabad, UPenn, and ASU. PRAISE demonstrated "
        "that LLMs can extract structured attributes from reviews. However, PRAISE has three documented limitations: "
        "it is text-only (ignoring product images), it makes roughly 2R+1 LLM calls per product which creates high cost and latency, "
        "and it lacks an aggregated score. To solve this, our literature survey incorporates Sentence-BERT for fast semantic retrieval "
        "and Cross-Encoder NLI for directional verification. The research gap is clear: existing systems either measure isolated sentiment "
        "or rely on costly brute-force LLMs. We propose an integrated, efficient approach combining dense retrieval, directional NLI, "
        "and visual inspection into a unified, interpretable reliability assessment."
    )

    # =========================================================================
    # SLIDE 5: SCOPE & OBJECTIVES
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5)
    add_header(slide5, "Project Scope & Finalized Objectives", "Official Area 5 — Boundaries & Milestones")

    # Left Card: Boundaries
    c5_scope = add_card(slide5, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.3))
    tf5_s = c5_scope.text_frame
    tf5_s.word_wrap = True
    tf5_s.margin_left = Inches(0.35)
    tf5_s.margin_top = Inches(0.25)
    tf5_s.margin_right = Inches(0.35)

    p = tf5_s.paragraphs[0]
    p.text = "Defined Project Scope"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = PRIMARY

    p = tf5_s.add_paragraph()
    p.text = "IN-SCOPE (System Capabilities):"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = SUCCESS
    p.space_before = Pt(6)

    in_scope = [
        "Extracting discrete, verifiable claims from seller textual listings.",
        "Dense semantic retrieval of factual customer review sentences using S-BERT.",
        "Directional NLI classification (Support, Contradiction, Neutral) for claim-evidence pairs.",
        "Preliminary visual consistency inspection between catalog images and unboxing photos.",
        "Formulating a composite Product Representation Index (PRI) and dashboard."
    ]
    for item in in_scope:
        p = tf5_s.add_paragraph()
        p.text = f"✓  {item}"
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(2)

    p = tf5_s.add_paragraph()
    p.text = "OUT-OF-SCOPE (Explicit Boundaries):"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = WARNING
    p.space_before = Pt(10)

    out_scope = [
        "Physical laboratory product testing or chemical material verification.",
        "Declaring a seller fraudulent or legally prosecuting counterfeit listings.",
        "Guaranteeing absolute real-world truth (we audit consistency relative to available evidence)."
    ]
    for item in out_scope:
        p = tf5_s.add_paragraph()
        p.text = f"✗  {item}"
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(2)

    # Right Card: Objectives
    c5_obj = add_card(slide5, Inches(6.8), Inches(1.7), Inches(5.733), Inches(5.3))
    tf5_o = c5_obj.text_frame
    tf5_o.word_wrap = True
    tf5_o.margin_left = Inches(0.35)
    tf5_o.margin_top = Inches(0.25)
    tf5_o.margin_right = Inches(0.35)

    p = tf5_o.paragraphs[0]
    p.text = "Finalized Project Objectives"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = PRIMARY

    objectives = [
        ("Objective 1 — Claim Extraction:", " Extract atomic, verifiable product claims from seller descriptions while eliminating marketing fluff."),
        ("Objective 2 — Semantic Retrieval:", " Implement a dense semantic retrieval pipeline using S-BERT to identify relevant customer review evidence sentences."),
        ("Objective 3 — Directional NLI:", " Develop an NLI inference engine to classify directional consistency (Support, Contradiction, Neutral) between claims and evidence."),
        ("Objective 4 — Multimodal Inspection:", " Investigate visual consistency between catalog photos and customer-uploaded imagery using color distance and structural similarity."),
        ("Objective 5 — Composite Index & UI:", " Formulate a mathematical Product Representation Index (PRI) and develop an interactive dashboard for transparent, evidence-backed evaluation.")
    ]
    for title, desc in objectives:
        p = tf5_o.add_paragraph()
        p.text = f"•  {title}"
        p.font.bold = True
        p.font.size = Pt(10.5)
        p.font.color.rgb = SECONDARY
        p.space_before = Pt(6)
        run = p.add_run()
        run.text = f" {desc}"
        run.font.bold = False
        run.font.color.rgb = TEXT_DARK

    slide5.notes_slide.notes_text_frame.text = (
        "To ensure academic and technical rigor, we have strictly defined our scope. In-scope is the automated extraction "
        "of verifiable claims, semantic retrieval of review sentences, directional NLI consistency scoring, preliminary visual comparison, "
        "and dashboard visualization. Out-of-scope is physical destructive testing or legal fraud determination; our system performs "
        "a digital representation consistency audit. Our objectives are organized sequentially across five implementation steps: "
        "extracting atomic claims, retrieving relevant review evidence via S-BERT, evaluating consistency using NLI, auditing visual representations, "
        "and formulating an interpretable Product Representation Index (PRI) inside an interactive interface."
    )

    # =========================================================================
    # SLIDE 6: CURRENT PROGRESS & ROADMAP
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6)
    add_header(slide6, "Current Progress, Findings & Review II Roadmap", "Proof-of-Concept & Future Work")

    # Card 1: Working POC Components
    c6_poc = add_card(slide6, Inches(0.8), Inches(1.7), Inches(3.7), Inches(5.3))
    tf6_p = c6_poc.text_frame
    tf6_p.word_wrap = True
    tf6_p.margin_left = Inches(0.3)
    tf6_p.margin_top = Inches(0.25)
    tf6_p.margin_right = Inches(0.3)

    p = tf6_p.paragraphs[0]
    p.text = "Working POC Components"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = PRIMARY

    poc_items = [
        ("Claim Extraction Engine:", " Hybrid mechanism supporting cached claims, rule-based fallback, and Gemini API."),
        ("Dense Retrieval:", " Sentence-BERT (all-MiniLM-L6-v2) cosine matching on review sentences."),
        ("NLI Inference Engine:", " Local Cross-Encoder (nli-MiniLM2-L6-H768) 3-way classification."),
        ("Interactive Prototype:", " Streamlit dashboard supporting pre-loaded products and manual claim/review input."),
        ("Visual Scorer (Standalone):", " OpenCV script testing CIE LAB color distance and SSIM structural similarity.")
    ]
    for title, desc in poc_items:
        p = tf6_p.add_paragraph()
        p.text = f"✓  {title}"
        p.font.bold = True
        p.font.size = Pt(9.5)
        p.font.color.rgb = SUCCESS
        p.space_before = Pt(5)
        run = p.add_run()
        run.text = f" {desc}"
        run.font.bold = False
        run.font.color.rgb = TEXT_DARK

    # Card 2: Developmental Findings & Lessons Learned
    c6_find = add_card(slide6, Inches(4.7), Inches(1.7), Inches(3.8), Inches(5.3))
    tf6_f = c6_find.text_frame
    tf6_f.word_wrap = True
    tf6_f.margin_left = Inches(0.3)
    tf6_f.margin_top = Inches(0.25)
    tf6_f.margin_right = Inches(0.3)

    p = tf6_f.paragraphs[0]
    p.text = "Developmental Findings"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = PRIMARY

    findings = [
        ("DOM & Metadata Noise:", " Direct copy-pasting of product pages captures advertising artifacts and breadcrumbs that confuse claim extractors."),
        ("Subjectivity Filtering Needed:", " Unfiltered subjective opinions ('I love this product') cause false contradictions; rule-based factual sentence filtering is vital."),
        ("NLI Asymmetry Discovery:", " Pretrained NLI models excel at contradiction detection (90%+ confidence) but exhibit conservatism toward conversational entailment."),
        ("Honest POC Status:", " Current results demonstrate technical feasibility; formal benchmarking is planned for Review II.")
    ]
    for title, desc in findings:
        p = tf6_f.add_paragraph()
        p.text = f"•  {title}"
        p.font.bold = True
        p.font.size = Pt(9.5)
        p.font.color.rgb = SECONDARY
        p.space_before = Pt(5)
        run = p.add_run()
        run.text = f" {desc}"
        run.font.bold = False
        run.font.color.rgb = TEXT_DARK

    # Card 3: Review II Roadmap & Conclusion
    c6_road = add_card(slide6, Inches(8.7), Inches(1.7), Inches(3.833), Inches(5.3), border_color=PRIMARY)
    tf6_r = c6_road.text_frame
    tf6_r.word_wrap = True
    tf6_r.margin_left = Inches(0.3)
    tf6_r.margin_top = Inches(0.25)
    tf6_r.margin_right = Inches(0.3)

    p = tf6_r.paragraphs[0]
    p.text = "Roadmap to Review II"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = PRIMARY

    roadmap = [
        ("Direct Web Scraping:", " Automate clean URL-based ingestion with DOM parsing."),
        ("Multimodal Integration:", " Incorporate image-level consistency directly into the PRI calculation pipeline."),
        ("Formula Calibration:", " Refine contradiction penalty weighting against human benchmark annotations."),
        ("Formal Evaluation:", " Evaluate Precision, Recall, and F1-score across 50+ benchmark product categories.")
    ]
    for title, desc in roadmap:
        p = tf6_r.add_paragraph()
        p.text = f"→  {title}"
        p.font.bold = True
        p.font.size = Pt(9.5)
        p.font.color.rgb = ACCENT
        p.space_before = Pt(5)
        run = p.add_run()
        run.text = f" {desc}"
        run.font.bold = False
        run.font.color.rgb = TEXT_DARK

    p = tf6_r.add_paragraph()
    p.text = "Summary Conclusion:"
    p.font.bold = True
    p.font.size = Pt(10.5)
    p.font.color.rgb = PRIMARY
    p.space_before = Pt(8)

    p = tf6_r.add_paragraph()
    p.text = "Review-I successfully establishes the problem, validates literature foundations, and demonstrates early feasibility toward building a trustworthy e-commerce assessment system."
    p.font.size = Pt(9)
    p.font.color.rgb = TEXT_MUTED

    slide6.notes_slide.notes_text_frame.text = (
        "To demonstrate feasibility, we have already initiated an initial proof-of-concept. We built a baseline pipeline "
        "using Sentence-BERT for retrieval and a Cross-Encoder for NLI, paired with an interactive Streamlit prototype "
        "and a standalone OpenCV visual analysis script. Importantly, early testing exposed key engineering challenges: "
        "raw e-commerce pages contain sponsored ads and metadata that corrupt the pipeline, and long reviews overload NLI models "
        "unless chunked into factual sentences. We present this honestly as a development finding, not a final validated system. "
        "Moving into Review II, we will refine structured extraction, calibrate the PRI formula, integrate multimodal analysis, "
        "and evaluate on benchmark datasets. This concludes our Review-I presentation. Thank you, and we are ready for questions."
    )

    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "MAJOR_PROJECT_REVIEW_I_PRESENTATION.pptx")
    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path}")

if __name__ == "__main__":
    create_presentation()
