from datetime import datetime, timezone

def generate_output(progress_percentage):
  passed_progress_bar_index = int(progress_percentage * 63)
  progress_bar = "▓" * passed_progress_bar_index + "░" * (63 - passed_progress_bar_index)

  now = datetime.now(timezone.utc)
  user_info = """### Hey, I'm JoshuaGlaZ

- ☁ API & Automation enthusiast
- 📖 Currently learning ~~Hapi.js~~, Django
- ☕ Preferred Coffee over Tea
"""
  update_message = f"Updated on {now.strftime('%a, %d %b %Y %H:%M:%S')} UTC"

  ascii_art =  f"""
```text
'
'     ___       __       ___    __ __
'   /'___`\\   /'__`\\   /'___`\\ /\\ \\\\ \\      
'  /\\_\\ /\\ \\ /\\ \\/\\ \\ /\\_\\ /\\ \\\\ \\ \\\\ \\     ▛▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
'  \\/_/// /__\\ \\ \\ \\ \\\\/_/// /__\\ \\ \\\\ \\_     {progress_bar} {(progress_percentage * 100):.2f}%
'     // /_\\ \\\\ \\ \\_\\ \\  // /_\\ \\\\ \\__ ,__\\ ▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▞
'    /\\______/ \\ \\____/ /\\______/ \\/_/\\_\\_/
'    \\/_____/   \\/___/  \\/_____/     \\/_/
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