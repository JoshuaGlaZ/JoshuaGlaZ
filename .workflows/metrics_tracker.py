#!/usr/bin/env python3
"""Advanced GitHub metrics tracker with caching and rate-limit handling"""
from datetime import datetime, timezone, timedelta
from pathlib import Path
import json
import os
import urllib.request
import urllib.error

CACHE_FILE = Path(".workflows/.metrics_cache.json")
CACHE_DURATION = timedelta(hours=6)

def load_cache():
    if not CACHE_FILE.exists():
        return None
    
    try:
        data = json.loads(CACHE_FILE.read_text())
        cached_time = datetime.fromisoformat(data['timestamp'])
        if datetime.now(timezone.utc) - cached_time < CACHE_DURATION:
            return data['metrics']
    except Exception:
        pass
    return None

def save_cache(metrics):
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    cache_data = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'metrics': metrics
    }
    CACHE_FILE.write_text(json.dumps(cache_data, indent=2))

def gh_request(endpoint, token):
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'GitHub-Profile-Bot'
    }
    req = urllib.request.Request(f'https://api.github.com{endpoint}', headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 403:
            remaining = e.headers.get('X-RateLimit-Remaining', '0')
            if remaining == '0':
                raise Exception("Rate limit exceeded")
        raise

def fetch_contribution_stats(username, token):
    """Fetch detailed contribution statistics"""
    metrics = {'commits': 0, 'prs': 0, 'issues': 0, 'reviews': 0}
    
    since = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat()
    
    try:
        events = gh_request(f'/users/{username}/events?per_page=100', token)
        
        for event in events:
            if event['created_at'] < since:
                break
            
            event_type = event['type']
            if event_type == 'PushEvent':
                metrics['commits'] += len(event.get('payload', {}).get('commits', []))
            elif event_type == 'PullRequestEvent':
                metrics['prs'] += 1
            elif event_type == 'IssuesEvent':
                metrics['issues'] += 1
            elif event_type == 'PullRequestReviewEvent':
                metrics['reviews'] += 1
                
    except Exception as e:
        print(f"Warning: Could not fetch contribution stats: {e}")
    
    return metrics

def fetch_language_stats(username, token):
    """Aggregate language statistics from repositories"""
    try:
        repos = gh_request(f'/users/{username}/repos?per_page=100&sort=updated', token)
        
        languages = {}
        for repo in repos[:20]:
            try:
                repo_langs = gh_request(f'/repos/{username}/{repo["name"]}/languages', token)
                for lang, bytes_count in repo_langs.items():
                    languages[lang] = languages.get(lang, 0) + bytes_count
            except Exception:
                continue
        
        total = sum(languages.values())
        if total == 0:
            return {}
        
        return {lang: round(count / total * 100, 1) 
                for lang, count in sorted(languages.items(), key=lambda x: x[1], reverse=True)[:5]}
    
    except Exception as e:
        print(f"Warning: Could not fetch language stats: {e}")
        return {}

def generate_metrics_badge(label, value, color="blue"):
    """Generate simple text-based badge"""
    return f"[{label}: {value}]"

def main():
    token = os.getenv('GH_TOKEN') or os.getenv('GITHUB_TOKEN')
    if not token:
        print("No token available, skipping metrics")
        return
    
    username = os.getenv('GITHUB_REPOSITORY', '/').split('/')[0]
    
    cached = load_cache()
    if cached:
        print("Using cached metrics")
        metrics = cached
    else:
        print("Fetching fresh metrics...")
        try:
            user_data = gh_request(f'/users/{username}', token)
            contributions = fetch_contribution_stats(username, token)
            languages = fetch_language_stats(username, token)
            
            metrics = {
                'public_repos': user_data.get('public_repos', 0),
                'followers': user_data.get('followers', 0),
                'following': user_data.get('following', 0),
                'contributions_30d': contributions,
                'top_languages': languages,
                'last_updated': datetime.now(timezone.utc).isoformat()
            }
            
            save_cache(metrics)
        except Exception as e:
            print(f"Error fetching metrics: {e}")
            return
    
    output = {
        'badges': [
            generate_metrics_badge('Repos', metrics['public_repos']),
            generate_metrics_badge('Followers', metrics['followers']),
            generate_metrics_badge('Commits (30d)', metrics['contributions_30d']['commits'])
        ],
        'languages': metrics['top_languages'],
        'activity': metrics['contributions_30d']
    }
    
    print(json.dumps(output, indent=2))
    Path(".workflows/.metrics_output.json").write_text(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()
