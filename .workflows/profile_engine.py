#!/usr/bin/env python3
from datetime import datetime, timezone
from pathlib import Path
import json
import os

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
'                                                                         Updated on {ts} UTC 
'"""

def fetch_github_stats():
    """Fetch GitHub stats via API if token available"""
    token = os.getenv('GH_TOKEN')
    username = os.getenv('GITHUB_REPOSITORY', '/').split('/')[0]
    
    if not token:
        return {}
    
    try:
        import urllib.request
        headers = {'Authorization': f'token {token}', 'Accept': 'application/vnd.github.v3+json'}
        
        req = urllib.request.Request(f'https://api.github.com/users/{username}', headers=headers)
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            return {
                'repos': data.get('public_repos', 0),
                'gists': data.get('public_gists', 0),
                'followers': data.get('followers', 0),
                'stars': sum(repo.get('stargazers_count', 0) for repo in fetch_user_repos(username, token)[:10])
            }
    except Exception:
        return {}

def fetch_user_repos(username, token):
    """Fetch user repositories"""
    try:
        import urllib.request
        headers = {'Authorization': f'token {token}', 'Accept': 'application/vnd.github.v3+json'}
        req = urllib.request.Request(f'https://api.github.com/users/{username}/repos?per_page=100', headers=headers)
        with urllib.request.urlopen(req, timeout=5) as response:
            return json.loads(response.read().decode())
    except Exception:
        return []

def generate_stats_section(stats):
    """Generate statistics section if available"""
    if not stats:
        return ""
    
    return f"""
**Quick Stats**
```
{stats.get('repos', 0):>3} Public Repos    {stats.get('stars', 0):>3} Stars Earned
{stats.get('gists', 0):>3} Gists           {stats.get('followers', 0):>3} Followers
```
"""

def generate_readme(progress, timestamp, stats):
    ascii_block = f"```text\n{generate_ascii_art(progress, timestamp)}\n```"
    stats_section = generate_stats_section(stats)
    
    return f"""### Hey, I'm JoshuaGlaZ
- ☁ API, Automation & NLP Enthusiast
- 📖 Currently learning ~~Hapi.js~~, Django
- ☕ Preferred Coffee over Tea
{stats_section}
{ascii_block}
"""

def main():
    progress, timestamp = calculate_year_progress()
    stats = fetch_github_stats()
    
    readme_content = generate_readme(progress, timestamp, stats)
    ascii_content = generate_ascii_art(progress, timestamp)
    
    metadata_dir = Path(".workflows")
    metadata_dir.mkdir(exist_ok=True)
    
    Path("README.md").write_text(readme_content, encoding='utf-8')
    (metadata_dir / "progress.txt").write_text(ascii_content, encoding='utf-8')
    
    metadata = {
        'progress': f"{progress * 100:.2f}",
        'timestamp': timestamp.isoformat(),
        'stats': stats
    }
    (metadata_dir / ".metadata.json").write_text(json.dumps(metadata, indent=2), encoding='utf-8')
    
    print(f"{progress * 100:.2f}")

if __name__ == "__main__":
    main()
