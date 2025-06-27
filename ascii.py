from datetime import datetime, timezone


def generate_ascii(progress_percentage, length = 22):
    passed_progress_bar_index = int(progress_percentage * length)
    progress_bar = "▓" * passed_progress_bar_index + \
        "░" * (length - passed_progress_bar_index)
    upper_bar = "▛" + (length - 1) * "▔"
    bottom_bar = "▁" * length + "▞"
    now = datetime.now(timezone.utc)
    update_message = f"Updated on {now.strftime('%a, %d %b %Y %H:%M:%S')} UTC"
    return f"""
```text

'
'     ___       __      ___    ______    
'   /'___`\\   /'__`\\  /'___`\\ /\\  ___\\   
'  /\\_\\ /\\ \\ /\\ \\/\\ \\/\\_\\ /\\ \\\\ \\ \\__/      {upper_bar}
'  \\/_/// /__\\ \\ \\ \\ \\/_/// /__\\ \\___``\\         {progress_bar} {(progress_percentage * 100):.2f}%
'     // /_\\ \\\\ \\ \\_\\ \\ // /_\\ \\\\/\\ \\L\\ \\   {bottom_bar}
'    /\\______/ \\ \\____//\\______/ \\ \\____/
'    \\/_____/   \\/___/ \\/_____/   \\/___/ 
'                                                                         📢 {update_message} 
'
```
"""


def generate_readme(progress_percentage, length = 22):
    snippet = generate_ascii(progress_percentage, length)
    return f"""### Hey, I'm JoshuaGlaZ

- ☁ API, Automation & NLP Enthusiast
- 📖 Currently learning ~~Hapi.js~~, Django
- ☕ Preferred Coffee over Tea

    {snippet}
"""


if __name__ == "__main__":
    now = datetime.now()
    start_of_year = datetime(now.year, 1, 1)
    end_of_year = datetime(now.year, 12, 31, 23, 59, 59)
    progress_of_this_year = (now - start_of_year) / \
        (end_of_year - start_of_year)
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(generate_readme(progress_of_this_year))
    with open("progress.txt", "w", encoding="utf-8") as f:
        snippet  = generate_ascii(progress_of_this_year)
        lines   = snippet.splitlines()
        start   = lines.index("```text") + 1
        end     = lines.index("```", start)
        ascii_block = "\n".join(lines[start:end])
        f.write(ascii_block)
