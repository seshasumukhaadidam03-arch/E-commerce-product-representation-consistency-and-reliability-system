import os
import subprocess
import markdown

EDGE_PATHS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
]

edge_exe = None
for path in EDGE_PATHS:
    if os.path.exists(path):
        edge_exe = path
        break

if not edge_exe:
    print("Error: Microsoft Edge executable not found.")
    exit(1)

CSS_STYLE = """
<style>
    @page {
        size: A4;
        margin: 20mm 15mm 20mm 15mm;
        @bottom-right {
            content: counter(page);
        }
    }
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        font-size: 10.5pt;
        line-height: 1.55;
        color: #1a202c;
        background-color: #ffffff;
        margin: 0;
        padding: 0;
    }
    h1 {
        font-size: 20pt;
        font-weight: 700;
        color: #1a365d;
        border-bottom: 2px solid #2b6cb0;
        padding-bottom: 8px;
        margin-top: 24pt;
        margin-bottom: 12pt;
        page-break-after: avoid;
    }
    h2 {
        font-size: 15pt;
        font-weight: 600;
        color: #2c5282;
        border-bottom: 1px solid #e2e8f0;
        padding-bottom: 6px;
        margin-top: 18pt;
        margin-bottom: 8pt;
        page-break-after: avoid;
    }
    h3 {
        font-size: 12pt;
        font-weight: 600;
        color: #2b6cb0;
        margin-top: 14pt;
        margin-bottom: 6pt;
        page-break-after: avoid;
    }
    h4 {
        font-size: 11pt;
        font-weight: 600;
        color: #4a5568;
        margin-top: 10pt;
        margin-bottom: 4pt;
        page-break-after: avoid;
    }
    p, li {
        color: #2d3748;
        margin-bottom: 6pt;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 12pt 0;
        font-size: 9.5pt;
        page-break-inside: avoid;
    }
    th, td {
        border: 1px solid #cbd5e0;
        padding: 6pt 8pt;
        text-align: left;
        vertical-align: top;
    }
    th {
        background-color: #ebf8ff;
        color: #2b6cb0;
        font-weight: 600;
    }
    tr:nth-child(even) td {
        background-color: #f7fafc;
    }
    blockquote {
        border-left: 4px solid #3182ce;
        background-color: #ebf8ff;
        margin: 10pt 0;
        padding: 8pt 12pt;
        color: #2c5282;
        border-radius: 0 4px 4px 0;
    }
    code {
        font-family: Consolas, "Courier New", Courier, monospace;
        font-size: 9pt;
        background-color: #edf2f7;
        padding: 2px 5px;
        border-radius: 3px;
        color: #805ad5;
    }
    pre {
        background-color: #1a202c;
        color: #edf2f7;
        padding: 10pt;
        border-radius: 6px;
        overflow-x: auto;
        font-size: 8.5pt;
        line-height: 1.4;
        margin: 10pt 0;
        page-break-inside: avoid;
    }
    pre code {
        background-color: transparent;
        color: inherit;
        padding: 0;
        border-radius: 0;
    }
    hr {
        border: 0;
        height: 1px;
        background: #e2e8f0;
        margin: 20pt 0;
    }
    ul, ol {
        padding-left: 20px;
        margin-top: 4pt;
        margin-bottom: 8pt;
    }
    li {
        margin-bottom: 3pt;
    }
</style>
"""

DOCS = [
    ("REVIEW_I_6_SLIDES_PRESENTATION.md", "REVIEW_I_6_SLIDES_PRESENTATION.pdf"),
    ("TEAM_KNOWLEDGE_BASE.md", "TEAM_KNOWLEDGE_BASE.pdf"),
    ("MENTORSHIP_JOURNEY_AND_LEARNING_LOG.md", "MENTORSHIP_JOURNEY_AND_LEARNING_LOG.pdf"),
    ("REVIEW_I_SOURCE_PACK.md", "REVIEW_I_SOURCE_PACK.pdf"),
]

base_dir = r"d:\Major_Project"

for md_file, pdf_file in DOCS:
    md_path = os.path.join(base_dir, md_file)
    pdf_path = os.path.join(base_dir, pdf_file)
    html_path = os.path.join(base_dir, f"temp_{os.path.splitext(md_file)[0]}.html")
    
    if not os.path.exists(md_path):
        print(f"Skipping {md_file}, file not found.")
        continue

    print(f"Converting {md_file} -> {pdf_file}...")
    
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    html_content = markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "toc", "nl2br", "sane_lists"]
    )
    
    full_html = f"<!DOCTYPE html><html><head><meta charset='utf-8'>{CSS_STYLE}</head><body>{html_content}</body></html>"
    
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(full_html)
        
    cmd = [
        edge_exe,
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={pdf_path}",
        html_path
    ]
    
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0:
        print(f"  [SUCCESS] Created {pdf_file} ({round(os.path.getsize(pdf_path)/1024, 1)} KB)")
    else:
        print(f"  [ERROR] Failed to create {pdf_file}. Code: {res.returncode}")
        
    # Clean up temp html
    if os.path.exists(html_path):
        os.remove(html_path)

print("\nAll PDF conversions complete!")
