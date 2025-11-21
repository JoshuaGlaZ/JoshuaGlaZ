import os
import re
from datetime import datetime, timezone

def main():
    now = datetime.now(timezone.utc)
    start_of_year = datetime(now.year, 1, 1, tzinfo=timezone.utc)
    end_of_year = datetime(now.year + 1, 1, 1, tzinfo=timezone.utc)
    progress = (now - start_of_year) / (end_of_year - start_of_year)
    
    length = 22
    filled_len = int(progress * length)
    bar = "▓" * filled_len + "░" * (length - filled_len)
    upper = "▛" + "▔" * (length - 1)
    bottom = " " * length + "▞"
    percent_str = f"{progress * 100:.2f}%"
    date_str = now.strftime('%a, %d %b %Y %H:%M:%S')
    
    ascii_art = f"""```text
'
'     ___       __      ___    ______    
'   /'___`\\   /'__`\\  /'___`\\ /\\  ___\\   
'  /\\_\\ /\\ \\ /\\ \\/\\ \\/\\_\\ /\\ \\\\ \\ \\__/      {upper}
'  \\/_/// /__\\ \\ \\ \\ \\/_/// /__\\ \\___``\\         {bar} {percent_str}
'     // /_\\ \\\\ \\ \\_\\ \\ // /_\\ \\\\/\\ \\L\\ \\   {bottom}
'    /\\______/ \\ \\____//\\______/ \\ \\____/
'    \\/_____/   \\/___/ \\/_____/   \\/___/ 
'                                                                         📢 Updated on {date_str} UTC 
'
```"""
    readme_path = "README.md"
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()

        pattern = r"()(.*?)()"
        
        if re.search(pattern, content, re.DOTALL):
            new_content = re.sub(
                pattern, 
                lambda m: f"{m.group(1)}\n{ascii_art}\n{m.group(3)}", 
                content, 
                flags=re.DOTALL
            )
            
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print("✅ README updated successfully.")
        else:
            print("⚠️ Markers not found in README.")
    
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
            f.write(f"commit_message=Update progress to {percent_str}\n")

if __name__ == "__main__":
    main()