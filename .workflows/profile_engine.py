#!/usr/bin/env python3
from datetime import datetime, timezone
from pathlib import Path
import json

def calculate_year_progress():
    now = datetime.now(timezone.utc)
    start = datetime(now.year, 1, 1, tzinfo=timezone.utc)
    end = datetime(now.year, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
    return (now - start) / (end - start), now

def render_progress_bar(progress, width=22):
    filled = int(progress * width)
    return "▓" * filled + "░" * (width - filled)

def generate_ascii_art(progress, timestamp):
    bar = render_progress_bar(progress)
    pct = f"{progress * 100:.2f}%"
    ts = timestamp.strftime('%a, %d %b %Y %H:%M:%S')
    
    return f"""'
'     ___       __      ___    ______    
'   /'__`\\   /'__`\\  /'___`\\ /\\  ___\\   
'  /\\_\\ /\\ \\ /\\ \\/\\ \\/\\_\\ /\\ \\\\ \\ \\__/      ▛{'▔' * 21}
'  \\/_/// /__\\ \\ \\ \\ \\/_/// /__\\ \\___``\\         {bar} {pct}
'     // /_\\ \\\\ \\ \\_\\ \\ // /_\\ \\\\/\\ \\L\\ \\   {'▁' * 22}▞
'    /\\______/ \\ \\____//\\______/ \\ \\____/
'    \\/_____/   \\/___/ \\/_____/   \\/___/ 
'                                                          Updated on {ts} UTC 
'"""

def generate_readme(progress, timestamp):
    ascii_block = f"```text\n{generate_ascii_art(progress, timestamp)}\n```"
    
    return f"""### Hey, I'm JoshuaGlaZ
- ☁ API, Automation & NLP Enthusiast
- 📖 Currently learning ~~Hapi.js~~, Django
- ☕ Preferred Coffee over Tea

{ascii_block}
"""

def main():
    progress, timestamp = calculate_year_progress()
    
    readme_content = generate_readme(progress, timestamp)
    ascii_content = generate_ascii_art(progress, timestamp)
    
    metadata_dir = Path(".workflows")
    metadata_dir.mkdir(exist_ok=True)
    
    Path("README.md").write_text(readme_content, encoding='utf-8')
    (metadata_dir / "progress.txt").write_text(ascii_content, encoding='utf-8')
    
    metadata = {
        'progress': f"{progress * 100:.2f}",
        'timestamp': timestamp.isoformat()
    }
    (metadata_dir / ".metadata.json").write_text(json.dumps(metadata, indent=2), encoding='utf-8')
    
    print(f"{progress * 100:.2f}")

if __name__ == "__main__":
    main()