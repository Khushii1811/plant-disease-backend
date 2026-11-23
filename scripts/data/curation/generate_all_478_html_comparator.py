import os
import sys
import json
from pathlib import Path

# Force UTF-8 on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path(__file__).resolve().parents[3]
MANIFEST_PATH = PROJECT_ROOT / "data" / "raw" / "comprehensive_crop_audit_manifest.json"

ROOT_HTML_OUTPUT = PROJECT_ROOT / "reports" / "history" / "v0_interactive_all_478_cropped_comparison.html"
RAW_HTML_OUTPUT = PROJECT_ROOT / "data" / "raw" / "interactive_all_478_cropped_comparison.html"

def main():
    print("=" * 80)
    print("🌐 GENERATING INTERACTIVE SIDE-BY-SIDE HTML COMPARATOR (478 IMAGES)")
    print("=" * 80)

    if not MANIFEST_PATH.exists():
        print(f"❌ Error: {MANIFEST_PATH} not found.")
        sys.exit(1)

    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    records = manifest["records"]
    print(f"📋 Loaded {len(records)} records.")

    # Prepare formatted items for web client
    items = []
    classes_count = {}
    for r in records:
        c = r["class"]
        classes_count[c] = classes_count.get(c, 0) + 1
        
        # relative paths with forward slashes for root HTML
        proc_rel = r["processed_path"].replace("\\", "/")
        raw_rel = r["raw_path"].replace("\\", "/")
        
        items.append({
            "class": r["class"],
            "split": r["split"],
            "filename": r["filename"],
            "proc_path": proc_rel,
            "raw_path": raw_rel,
            "proc_size": f"{r['processed_size'][0]} × {r['processed_size'][1]}",
            "raw_size": f"{r['raw_size'][0]} × {r['raw_size'][1]}",
            "diff_w": r["diff_w"],
            "diff_h": r["diff_h"],
            "diff_label": f"Loss: {abs(r['diff_w'])}w × {abs(r['diff_h'])}h" if (r['diff_w'] != 0 or r['diff_h'] != 0) else "Altered"
        })

    # Sort: Apple, Bean, Broccoli, Cabbage, Corn, Ginger
    items.sort(key=lambda x: (x["class"], x["split"], x["filename"]))

    # Build Class Options for Dropdown
    class_options_html = '<option value="ALL">All Classes (478 images)</option>'
    for c, count in sorted(classes_count.items(), key=lambda x: x[1], reverse=True):
        class_options_html += f'<option value="{c}">{c} ({count} images)</option>'

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Global Cropped Images Audit: Side-by-Side Comparator (478 Images)</title>
<style>
  :root {{
    --bg-main: #090d16;
    --bg-card: #131b2e;
    --bg-header: #0f172a;
    --border-color: #1e293b;
    --text-primary: #f8fafc;
    --text-muted: #94a3b8;
    --accent-blue: #38bdf8;
    --master-green: #22c55e;
    --cropped-red: #ef4444;
  }}

  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background-color: var(--bg-main);
    color: var(--text-primary);
    padding: 24px 32px;
    line-height: 1.5;
  }}

  /* Header Bar */
  .header {{
    background: var(--bg-header);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 24px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
  }}
  .header h1 {{
    font-size: 26px;
    color: var(--accent-blue);
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 10px;
  }}
  .header p {{
    color: var(--text-muted);
    font-size: 14px;
    margin-bottom: 18px;
  }}

  /* Filter Controls */
  .controls {{
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
    align-items: center;
    background: #090d16;
    padding: 14px 18px;
    border-radius: 8px;
    border: 1px solid var(--border-color);
  }}
  select, input {{
    background: #1e293b;
    color: #fff;
    border: 1px solid #334155;
    padding: 10px 14px;
    border-radius: 6px;
    font-size: 14px;
    outline: none;
    transition: border-color 0.2s;
  }}
  select:focus, input:focus {{
    border-color: var(--accent-blue);
  }}
  .counter {{
    margin-left: auto;
    font-weight: 600;
    font-size: 14px;
    color: var(--accent-blue);
  }}

  /* Grid of Side-by-Side Cards */
  .grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(580px, 1fr));
    gap: 22px;
    margin-top: 24px;
  }}
  .card {{
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    overflow: hidden;
    padding: 16px;
    transition: transform 0.15s, border-color 0.15s;
  }}
  .card:hover {{
    border-color: #3b82f6;
    box-shadow: 0 6px 24px rgba(0,0,0,0.5);
  }}

  /* Card Meta */
  .card-top {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    padding-bottom: 10px;
  }}
  .card-title {{
    font-size: 14px;
    font-weight: 700;
    color: #f1f5f9;
  }}
  .card-split {{
    font-size: 11px;
    text-transform: uppercase;
    background: #334155;
    padding: 2px 8px;
    border-radius: 4px;
    margin-left: 8px;
  }}
  .badge-diff {{
    background: rgba(239, 68, 68, 0.15);
    color: #f87171;
    border: 1px solid rgba(239, 68, 68, 0.3);
    padding: 3px 10px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 600;
  }}

  /* Side-by-Side Image Pair */
  .pair-container {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
    background: #090d16;
    padding: 10px;
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.04);
  }}
  .panel {{
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
  }}
  .panel-header {{
    font-size: 12px;
    font-weight: 600;
    margin-bottom: 6px;
    padding: 3px 8px;
    border-radius: 4px;
    width: 100%;
  }}
  .header-master {{
    background: rgba(34, 197, 94, 0.15);
    color: var(--master-green);
    border: 1px solid rgba(34, 197, 94, 0.3);
  }}
  .header-proc {{
    background: rgba(239, 68, 68, 0.15);
    color: var(--cropped-red);
    border: 1px solid rgba(239, 68, 68, 0.3);
  }}

  .img-wrapper {{
    width: 100%;
    height: 250px;
    background: #020617;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    cursor: pointer;
  }}
  .img-wrapper img {{
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
    transition: transform 0.2s;
  }}
  .img-wrapper:hover img {{
    transform: scale(1.04);
  }}

  .file-path {{
    margin-top: 8px;
    font-size: 10px;
    color: #64748b;
    word-break: break-all;
    text-align: left;
  }}

  /* Modal Zoom View */
  .modal {{
    display: none;
    position: fixed;
    top: 0; left: 0; width: 100%; height: 100%;
    background: rgba(0,0,0,0.88);
    z-index: 9999;
    align-items: center;
    justify-content: center;
    padding: 20px;
  }}
  .modal-content {{
    max-width: 90%;
    max-height: 90%;
    border-radius: 8px;
    box-shadow: 0 0 30px rgba(0,0,0,0.8);
  }}
  .modal-close {{
    position: absolute;
    top: 25px;
    right: 35px;
    font-size: 36px;
    color: #fff;
    cursor: pointer;
  }}

  /* Load More */
  .pagination {{
    display: flex;
    justify-content: center;
    margin: 35px 0;
  }}
  .btn-load {{
    background: #2563eb;
    color: #fff;
    border: none;
    padding: 12px 28px;
    border-radius: 8px;
    font-size: 15px;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s;
  }}
  .btn-load:hover {{
    background: #1d4ed8;
  }}
</style>
</head>
<body>

<div class="header">
  <h1>🔍 Complete Side-by-Side Audit: Cropped vs Original Master Images</h1>
  <p>Comparing all 478 images across 8 classes where dimensions in <code>data/processed</code> differ from original raw images in <code>data/raw</code>.</p>
  
  <div class="controls">
    <select id="classFilter" onchange="applyFilters()">
      {class_options_html}
    </select>
    <input type="text" id="searchFilter" placeholder="Search filename or path..." onkeyup="applyFilters()" style="min-width: 280px;">
    <div class="counter" id="activeCount">Showing 478 / 478 items</div>
  </div>
</div>

<div class="grid" id="gridContainer"></div>

<div class="pagination" id="paginationBar">
  <button class="btn-load" onclick="loadMore()">Load More Images</button>
</div>

<!-- Modal Zoom -->
<div class="modal" id="imageModal" onclick="closeModal()">
  <span class="modal-close">&times;</span>
  <img class="modal-content" id="modalImg" src="">
</div>

<script>
const allItems = {json.dumps(items)};
let currentFiltered = allItems;
let displayedCount = 0;
const BATCH_SIZE = 60;

function renderBatch() {{
  const container = document.getElementById("gridContainer");
  const nextSlice = currentFiltered.slice(displayedCount, displayedCount + BATCH_SIZE);
  
  nextSlice.forEach(it => {{
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `
      <div class="card-top">
        <div class="card-title">
          ${{it.class}}
          <span class="card-split">${{it.split}}</span>
        </div>
        <div class="badge-diff">${{it.diff_label}}</div>
      </div>
      <div class="pair-container">
        <!-- Master Panel -->
        <div class="panel">
          <div class="panel-header header-master">RAW MASTER: ${{it.raw_size}}</div>
          <div class="img-wrapper" onclick="openModal('${{it.raw_path}}')">
            <img src="${{it.raw_path}}" alt="Raw Master" loading="lazy">
          </div>
        </div>
        <!-- Cropped Panel -->
        <div class="panel">
          <div class="panel-header header-proc">CROPPED: ${{it.proc_size}}</div>
          <div class="img-wrapper" onclick="openModal('${{it.proc_path}}')">
            <img src="${{it.proc_path}}" alt="Processed Cropped" loading="lazy">
          </div>
        </div>
      </div>
      <div class="file-path">${{it.filename}}</div>
    `;
    container.appendChild(card);
  }});

  displayedCount += nextSlice.length;
  document.getElementById("activeCount").innerText = `Showing ${{displayedCount}} / ${{currentFiltered.length}} items`;
  
  const pBar = document.getElementById("paginationBar");
  if (displayedCount >= currentFiltered.length) {{
    pBar.style.display = "none";
  }} else {{
    pBar.style.display = "flex";
  }}
}}

function loadMore() {{
  renderBatch();
}}

function applyFilters() {{
  const selectedClass = document.getElementById("classFilter").value;
  const searchQ = document.getElementById("searchFilter").value.toLowerCase();
  
  currentFiltered = allItems.filter(it => {{
    const matchClass = (selectedClass === "ALL" || it.class === selectedClass);
    const matchText = it.filename.toLowerCase().includes(searchQ) || it.class.toLowerCase().includes(searchQ);
    return matchClass && matchText;
  }});
  
  // Reset grid
  document.getElementById("gridContainer").innerHTML = "";
  displayedCount = 0;
  renderBatch();
}}

function openModal(src) {{
  document.getElementById("modalImg").src = src;
  document.getElementById("imageModal").style.display = "flex";
}}

function closeModal() {{
  document.getElementById("imageModal").style.display = "none";
}}

// Initial load
applyFilters();
</script>
</body>
</html>
"""

    # Write root HTML
    with open(ROOT_HTML_OUTPUT, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✅ Generated root HTML comparator: {ROOT_HTML_OUTPUT}")

    # For raw HTML, adjust paths relative to data/raw/
    raw_html_content = html_content.replace('src="data/', 'src="../../data/')
    with open(RAW_HTML_OUTPUT, "w", encoding="utf-8") as f:
        f.write(raw_html_content)
    print(f"✅ Generated raw HTML comparator: {RAW_HTML_OUTPUT}")

    print("\n🎉 HTML Comparators successfully built!")
    print("=" * 80)

if __name__ == "__main__":
    main()
