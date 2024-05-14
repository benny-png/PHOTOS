import os.path
import requests

def check_file_exists(url):
    try:
        response = requests.head(url)
        return response.status_code == 200
    except requests.ConnectionError:
        return False

def save_ids_to_text_file(existing_ids, filename):
    with open(filename, "w") as file:
        for file_id in existing_ids:
            file.write(file_id + "\n")

def main():
    base_url = "https://aris3.udsm.ac.tz/uploaded_files/student/photos/"
    start_index = 1
    end_index = 99999

    existing_ids = []  # List to store existing file IDs

    for i in range(start_index, end_index + 1):
        file_url = f"{base_url}2023-04-{i:05d}.jpg"
        print("NONE")
        if check_file_exists(file_url):
            existing_ids.append(f"2023-04-{i:05d}")

    # Save existing IDs to a text file
    filename = "existing_ids.txt"
    save_ids_to_text_file(existing_ids, filename)
    print(f"Saved existing IDs to {filename}")

if __name__ == "__main__":
    main()
