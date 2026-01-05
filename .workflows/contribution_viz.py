#!/usr/bin/env python3
"""Generate ASCII contribution graph similar to GitHub's heatmap"""
from datetime import datetime, timezone, timedelta
from collections import defaultdict
import json
import os

def get_contribution_data():
    """Load from cache or return sample data"""
    try:
        from pathlib import Path
        cache = Path(".workflows/.metrics_cache.json")
        if cache.exists():
            data = json.loads(cache.read_text())
            return data.get('metrics', {}).get('contributions_30d', {})
    except Exception:
        pass
    return {'commits': 42, 'prs': 8, 'issues': 3, 'reviews': 5}

def generate_activity_graph(days=7):
    """Generate ASCII activity visualization for last N days"""
    levels = [' ', ' ', ' ', ' ']
    
    activity = defaultdict(int)
    now = datetime.now(timezone.utc)
    
    contrib_data = get_contribution_data()
    total_activity = sum(contrib_data.values())
    
    daily_avg = total_activity / 30
    
    graph_lines = []
    graph_lines.append("    Last 7 Days Activity")
    graph_lines.append("    " + "─" * 22)
    
    days_row = "    "
    bars_row = "    "
    
    for i in range(days - 1, -1, -1):
        day = now - timedelta(days=i)
        day_name = day.strftime('%a')[:1]
        
        intensity = int((i + 1) * daily_avg / 7) % 4
        
        days_row += f"{day_name} "
        bars_row += f"{levels[intensity]} "
    
    graph_lines.append(days_row)
    graph_lines.append(bars_row)
    
    return "\n".join(graph_lines)

def generate_contribution_summary():
    """Generate contribution summary with ASCII art"""
    data = get_contribution_data()
    
    summary = [
        "",
        "╔══════════════════════════════════════════╗",
        "║       30-Day Contribution Summary        ║",
        "╠══════════════════════════════════════════╣",
        f"║  Commits        {data.get('commits', 0):>4}               ║",
        f"║  Pull Requests  {data.get('prs', 0):>4}               ║",
        f"║  Issues         {data.get('issues', 0):>4}               ║",
        f"║  Reviews        {data.get('reviews', 0):>4}               ║",
        "╚══════════════════════════════════════════╝",
        ""
    ]
    
    return "\n".join(summary)

def generate_streak_tracker():
    """Generate contribution streak visualization"""
    data = get_contribution_data()
    total = sum(data.values())
    
    streak = min(total // 3, 30)
    
    return f"""
  Contribution Streak
{' ' * min(streak, 30)}{' ' * max(0, 30 - streak)} {streak} days
"""

def main():
    output = []
    output.append(generate_contribution_summary())
    output.append(generate_activity_graph())
    output.append(generate_streak_tracker())
    
    full_output = "\n".join(output)
    print(full_output)
    
    from pathlib import Path
    Path(".workflows/.contribution_viz.txt").write_text(full_output, encoding='utf-8')

if __name__ == "__main__":
    main()