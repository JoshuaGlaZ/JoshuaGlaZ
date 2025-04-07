from datetime import datetime, timezone

def generate_output(progress_percentage):
  passed_progress_bar_index = int(progress_percentage * 63)
  progress_bar = "▓" * passed_progress_bar_index + "░" * (63 - passed_progress_bar_index)

  now = datetime.now(timezone.utc)
  user_info = """### Hey, I'm JoshuaGlaZ

- ☁ API, Automation & NLP Enthusiast
- 📖 Currently learning ~~Hapi.js~~, Django
- ☕ Preferred Coffee over Tea
"""
  update_message = f"Updated on {now.strftime('%a, %d %b %Y %H:%M:%S')} UTC"

  ascii_art =  f"""
```text
'
'     ___       __      ___    ______    
'   /'___`\\   /'__`\\  /'___`\\ /\\  ___\\   
'  /\\_\\ /\\ \\ /\\ \\/\\ \\/\\_\\ /\\ \\\\ \\ \\__/      ▛▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
'  \\/_/// /__\\ \\ \\ \\ \\/_/// /__\\ \\___``\\      {progress_bar} {(progress_percentage * 100):.2f}%
'     // /_\\ \\\\ \\ \\_\\ \\ // /_\\ \\\\/\\ \\L\\ \\   ▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▞
'    /\\______/ \\ \\____//\\______/ \\ \\____/
'    \\/_____/   \\/___/ \\/_____/   \\/___/ 
'                                                                         📢 {update_message} 
'
```"""
  return f"{user_info}{ascii_art}" 

if __name__ == "__main__" :
  now = datetime.now()
  start_of_year = datetime(now.year, 1, 1)
  end_of_year = datetime(now.year, 12, 31, 23, 59, 59)
  progress_of_this_year = (now - start_of_year) / (end_of_year - start_of_year)
  print(generate_output(progress_of_this_year))