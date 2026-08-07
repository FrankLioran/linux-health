# generator.py
from datetime import datetime
from config import REPORTS_DIR
from base import CheckCategory, Status

def generate_html_report(categories: list[CheckCategory], score: int) -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = REPORTS_DIR / f"{timestamp}_HealthReport.html"

    # HTML voor categorieën en items
    rows_html = ""
    for cat in categories:
        rows_html += f"<div class='category'><h3>{cat.name}</h3><ul>"
        for item in cat.items:
            color = "#22c55e" if item.status == Status.OK else "#f59e0b" if item.status == Status.WARN else "#ef4444"
            rows_html += f"""
            <li>
                <span class='badge' style='background-color:{color}22; color:{color}; border: 1px solid {color}44;'>
                    {item.status.value}
                </span>
                <strong>{item.label}:</strong> {item.message}
            </li>"""
        rows_html += "</ul></div>"

    # Kleur van de health score
    score_color = '#22c55e' if score >= 80 else '#f59e0b' if score >= 50 else '#ef4444'

    html_content = f"""<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Linux Health Report</title>
    <style>
        body {{ 
            font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
            margin: 40px auto; 
            background: #0f172a; 
            color: #e2e8f0; 
            max-width: 800px; 
            line-height: 1.5; 
        }}
        .card {{ 
            background: #1e293b; 
            padding: 32px; 
            border-radius: 16px; 
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3); 
            border: 1px solid #334155; 
        }}
        h1 {{ color: #38bdf8; margin-top: 0; font-size: 1.8rem; }}
        .meta {{ color: #94a3b8; font-size: 0.9rem; margin-bottom: 24px; }}

        /* Score Card & Progress bar */
        .score-section {{ 
            margin: 24px 0; 
            background: #0f172a; 
            padding: 20px; 
            border-radius: 12px; 
            border: 1px solid #334155; 
        }}
        .score-header {{ 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            margin-bottom: 12px; 
        }}
        .score-title {{ font-weight: bold; color: #f8fafc; font-size: 1.1rem; }}
        .score-value {{ font-size: 1.6rem; font-weight: bold; color: {score_color}; }}
        .progress-bar {{ 
            background: #334155; 
            height: 12px; 
            border-radius: 6px; 
            overflow: hidden; 
        }}
        .progress-fill {{ 
            height: 100%; 
            width: {score}%; 
            background: {score_color}; 
            border-radius: 6px;
        }}

        /* Categories & Items */
        .category {{ margin-top: 28px; }}
        h3 {{ color: #7dd3fc; border-bottom: 1px solid #334155; padding-bottom: 8px; margin-bottom: 12px; font-size: 1.2rem; }}
        ul {{ list-style: none; padding: 0; margin: 0; }}
        li {{ 
            padding: 10px 0; 
            border-bottom: 1px solid #334155; 
            display: flex; 
            align-items: center; 
            gap: 12px; 
        }}
        .badge {{ 
            font-family: monospace; 
            font-weight: bold; 
            padding: 4px 10px; 
            border-radius: 6px; 
            font-size: 0.9rem; 
        }}
    </style>
</head>
<body>
    <div class="card">
        <h1>Linux Health Report</h1>
        <div class="meta">Gegenereerd op: {datetime.now().strftime('%d-%m-%Y om %H:%M')}</div>

        <div class="score-section">
            <div class="score-header">
                <span class="score-title">Health Score</span>
                <span class="score-value">{score} / 100</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill"></div>
            </div>
        </div>

        {rows_html}
    </div>
</body>
</html>
"""
    file_path.write_text(html_content, encoding="utf-8")
    return str(file_path)