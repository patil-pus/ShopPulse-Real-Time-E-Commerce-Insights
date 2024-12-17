import csv

def save_to_csv(data, file_name):
    name = file_name
    filename = f"{name}.csv"
    keys = ["Name", "Price", "Original Price", "Rating", "Number of Ratings"] 
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
    print(f"Data saved to {filename}")






