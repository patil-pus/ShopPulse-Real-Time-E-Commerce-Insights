import json

def save_to_json(data, file_name):
    with open(f"{file_name}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
