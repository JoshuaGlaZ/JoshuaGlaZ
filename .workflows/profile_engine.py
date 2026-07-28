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
'     ___       __      ___      ____    
'   /'___`\\   /'__`\\  /'___`\\   /'___\\   
'  /\\_\\ /\\ \\ /\\ \\/\\ \\/\\_\\ /\\ \\ /\\ \\__/         ▛{'▔' * 21}
'  \\/_/// /__\\ \\ \\ \\ \\/_/// /__\\ \\  _``\\         {bar} {pct}
'     // /_\\ \\\\ \\ \\_\\ \\ // /_\\ \\\\ \\ \\L\\ \\      {'▁' * 22}▞
'    /\\______/ \\ \\____//\\______/ \\ \\____/
'    \\/_____/   \\/___/ \\/_____/   \\/___/ 
'                                              Updated on {ts} UTC 
'"""

def load_metrics():
    cache_path = Path(".workflows/.metrics_cache.json")
    if cache_path.exists():
        try:
            data = json.loads(cache_path.read_text(encoding='utf-8'))
            return data.get('metrics', {})
        except Exception:
            pass
    return {}

def generate_readme(progress, timestamp, metrics):
    ascii_block = f"```text\n{generate_ascii_art(progress, timestamp)}\n```"
    
    return f"""### Hey, I'm JoshuaGlaZ

- ☁ API, Automation & NLP Enthusiast
- 📖 Currently learning Django, React/Next.js
- ☕ Preferred Coffee over Tea

---

### Tech Stack & Tools

<table>
  <tr>
    <td valign="top" width="50%">
      <strong>Backend &amp; Web Development</strong><br/>
      <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&amp;logo=python&amp;logoColor=white" alt="Python"/>
      <img src="https://img.shields.io/badge/Django-092E20?style=flat-square&amp;logo=django&amp;logoColor=white" alt="Django"/>
      <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&amp;logo=javascript&amp;logoColor=black" alt="JavaScript"/>
      <img src="https://img.shields.io/badge/Next.js-000000?style=flat-square&amp;logo=nextdotjs&amp;logoColor=white" alt="Next.js"/>
    </td>
    <td valign="top" width="50%">
      <strong>APIs, Automation &amp; Devops</strong><br/>
      <img src="https://img.shields.io/badge/GitHub%20Actions-2088FF?style=flat-square&amp;logo=githubactions&amp;logoColor=white" alt="GitHub Actions"/>
      <img src="https://img.shields.io/badge/APIs-REST-009688?style=flat-square&amp;logo=postman&amp;logoColor=white" alt="REST APIs"/>
      <img src="https://img.shields.io/badge/Git-F05032?style=flat-square&amp;logo=git&amp;logoColor=white" alt="Git"/>
      <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&amp;logo=postgresql&amp;logoColor=white" alt="PostgreSQL"/>
    </td>
  </tr>
</table>

---

### Year Progress

{ascii_block}

"""

def main():
    progress, timestamp = calculate_year_progress()
    
    # Load metrics from cache
    metrics = load_metrics()
    
    # Generate README and ASCII art
    readme_content = generate_readme(progress, timestamp, metrics)
    ascii_content = generate_ascii_art(progress, timestamp)
    
    Path("README.md").write_text(readme_content, encoding='utf-8')
    Path(".workflows/progress.txt").write_text(ascii_content, encoding='utf-8')
    
    metadata = {
        'progress': f"{progress * 100:.2f}",
        'timestamp': timestamp.isoformat()
    }
    Path(".workflows/.metadata.json").write_text(json.dumps(metadata, indent=2), encoding='utf-8')
    
    print(f"{progress * 100:.2f}")

if __name__ == "__main__":
    main()