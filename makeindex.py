# -*- coding: utf-8 -*-
"""
Aktualisiert am 17. Januar 2026
Erstellt eine magische index.html mit automatischer Versionsnummer (x.y)
"""

import os
import re
from datetime import datetime
from bs4 import BeautifulSoup

def get_next_version(item_count):
    output_file = "index.html"
    default_version = f"{item_count}.1"

    if not os.path.exists(output_file):
        return default_version

    try:
        with open(output_file, "r", encoding="utf-8") as f:
            content = f.read()
            match = re.search(r"Version:\s*\d+\.(\d+)", content)
            if match:
                last_y = int(match.group(1))
                return f"{item_count}.{last_y + 1}"
    except Exception:
        pass

    return default_version

def extract_page_info(full_path, rel_path):
    """Extrahiert Titel und Beschreibung aus einer HTML-Datei."""
    title = rel_path
    description = ""

    try:
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
            # Falls der Inhalt in Markdown-Code-Blöcken ist, extrahiere HTML
            if "```html" in content:
                match = re.search(r"```html\s*(.*?)```", content, re.DOTALL)
                if match:
                    content = match.group(1)

            soup = BeautifulSoup(content, "html.parser")

            # Titel aus h1 oder title-Tag
            h1 = soup.find("h1")
            if h1:
                title = h1.get_text(strip=True)
            elif soup.title:
                title = soup.title.get_text(strip=True)

            # Beschreibung aus .description, p.description oder erstem p-Tag
            desc_elem = soup.find(class_="description")
            if not desc_elem:
                desc_elem = soup.find("p")
            if desc_elem:
                description = desc_elem.get_text(strip=True)[:100]
                if len(desc_elem.get_text(strip=True)) > 100:
                    description += "..."
    except Exception:
        pass

    return title, description

def generate_index():
    base_dir = "."
    output_file = "index.html"

    html_files = []

    # Suche in Unterverzeichnissen
    for root, dirs, files in os.walk(base_dir):
        if root == base_dir:
            continue

        for file in files:
            if file.endswith(".html"):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, base_dir)
                folder = os.path.dirname(rel_path)

                title, description = extract_page_info(full_path, rel_path)

                # Änderungsdatum der Datei
                try:
                    mtime = os.path.getmtime(full_path)
                    mod_date = datetime.fromtimestamp(mtime).strftime("%d.%m.%Y")
                except Exception:
                    mod_date = ""

                html_files.append({
                    "path": rel_path,
                    "folder": folder,
                    "title": title,
                    "description": description,
                    "mod_date": mod_date
                })

    # Sortieren nach Ordner, dann nach Titel
    html_files.sort(key=lambda x: (x["folder"], x["title"]))
    item_count = len(html_files)
    version_str = get_next_version(item_count)

    # HTML für Listeneinträge generieren
    adventure_emojis = ["🚀", "🐉", "🐎", "✨", "🏰", "🦄", "☄️", "🔥"]
    list_items = []

    for i, item in enumerate(html_files):
        emoji = adventure_emojis[i % len(adventure_emojis)]
        web_path = item["path"].replace("\\", "/")

        desc_html = ""
        if item["description"]:
            desc_html = f'<span class="description">{item["description"]}</span>'

        date_html = ""
        if item["mod_date"]:
            date_html = f'<span class="date">{item["mod_date"]}</span>'

        list_items.append(f'''            <li>
                <span class="emoji">{emoji}</span>
                <a href="{web_path}">
                    <span class="title">{item["title"]}</span>
                    {desc_html}
                </a>
                {date_html}
            </li>''')

    list_items_html = "\n".join(list_items)

    html_content = f"""<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Abenteuer-Code-Zentrale</title>
    <style>
        :root {{
            --bg-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            --card-bg: rgba(255, 255, 255, 0.97);
            --text-color: #2c3e50;
            --accent: #667eea;
        }}
        * {{ box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: var(--bg-gradient);
            background-attachment: fixed;
            min-height: 100vh;
            margin: 0;
            padding: 40px 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        .container {{
            width: 100%;
            max-width: 700px;
            background: var(--card-bg);
            padding: 40px;
            border-radius: 24px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.2);
            position: relative;
        }}
        .version-badge {{
            position: absolute;
            top: 20px;
            right: 25px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.75em;
            font-weight: 600;
            letter-spacing: 0.5px;
        }}
        .header-icons {{
            font-size: 3.5em;
            margin-bottom: 15px;
            text-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }}
        h1 {{
            color: #333;
            text-align: center;
            font-size: 2em;
            margin: 0 0 30px 0;
            font-weight: 700;
        }}
        .item-count {{
            text-align: center;
            color: #888;
            font-size: 0.9em;
            margin-bottom: 25px;
        }}
        ol {{
            padding: 0;
            margin: 0;
            list-style: none;
        }}
        li {{
            background: linear-gradient(135deg, #fff 0%, #f8f9ff 100%);
            margin-bottom: 12px;
            padding: 18px 20px;
            border-radius: 16px;
            display: flex;
            align-items: center;
            border: 2px solid transparent;
            transition: all 0.25s ease;
            cursor: pointer;
        }}
        li:hover {{
            transform: translateX(8px);
            border-color: var(--accent);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
        }}
        li:active {{
            transform: translateX(8px) scale(0.98);
        }}
        .emoji {{
            font-size: 2em;
            margin-right: 18px;
            flex-shrink: 0;
        }}
        a {{
            text-decoration: none;
            color: var(--text-color);
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            gap: 4px;
        }}
        .title {{
            font-weight: 600;
            font-size: 1.15em;
            color: #333;
        }}
        .description {{
            font-size: 0.85em;
            color: #666;
            font-weight: 400;
        }}
        .date {{
            font-size: 0.75em;
            color: #999;
            flex-shrink: 0;
            margin-left: 15px;
        }}
        .footer {{
            text-align: center;
            margin-top: 25px;
            font-weight: 600;
            color: rgba(255,255,255,0.9);
            text-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }}
        @media (max-width: 500px) {{
            .container {{ padding: 25px 20px; }}
            li {{ padding: 15px; }}
            .emoji {{ font-size: 1.6em; margin-right: 12px; }}
            .title {{ font-size: 1em; }}
            .date {{ display: none; }}
        }}
    </style>
</head>
<body>
    <div class="header-icons">🐎 🐉 🚀</div>
    <div class="container">
        <div class="version-badge">v{version_str}</div>
        <h1>📜 Abenteuer-Zentrale<br>für N 👩‍🦰 & I 👱‍♂️</h1>
        <div class="item-count">{item_count} Abenteuer warten auf dich!</div>
        <ol>
{list_items_html}
        </ol>
    </div>
    <div class="footer">Bereit für die nächste Mission? ✨</div>
</body>
</html>"""

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Erfolg: {output_file} (v{version_str}) mit {item_count} Einträgen erstellt.")

if __name__ == "__main__":
    generate_index()