import re

def get_percentage_from_file(filename: str) -> float:
  with open(filename, "r", encoding="utf-8") as f:
    content = f.read()
  match = re.search(r"(\d+\.\d+)\s*%", content)

  if match:
    try:
      return float(match.group(1))
    except ValueError:
      raise ValueError("Invalid percentage format in file")
  else:
    raise FileNotFoundError(f"Percentage not found in {filename}")

if __name__ == "__main__":
  try:
    print(get_percentage_from_file("README.md"))
  except (FileNotFoundError, ValueError) as e:
    print(f"Error: {e}")
    exit(1)