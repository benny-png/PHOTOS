import threading
import requests
import os

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

def process_range(start_index, end_index, base_url, output_filename, thread_name):
    existing_ids = []  # List to store existing file IDs for this range

    print(f"[{thread_name}] started with process ID: {os.getpid()}")
    
    for i in range(start_index, end_index + 1):
        file_url = f"{base_url}2023-04-{i:05d}.jpg"
        if check_file_exists(file_url):
            reg_no = f"2023-04-{i:05d}"
            existing_ids.append(reg_no)
            print(f"[{thread_name}] FOUND: {reg_no}.jpg")

    # Save existing IDs for this range to a text file
    save_ids_to_text_file(existing_ids, output_filename)
    print(f"[{thread_name}] Saved existing IDs to {output_filename}")

def main():
    base_url = "https://aris3.udsm.ac.tz/uploaded_files/student/photos/"
    total_start_index = 1
    total_end_index = 9999
    num_threads = 4  # Number of threads to use
    range_size = (total_end_index - total_start_index + 1) // num_threads

    print("ID of process running main program: {}".format(os.getpid()))
    print("Main thread name: {}".format(threading.current_thread().name))

    threads = []
    for i in range(num_threads):
        start_index = total_start_index + i * range_size
        end_index = start_index + range_size - 1
        if i == num_threads - 1:  # Ensure the last range goes to the end
            end_index = total_end_index
        output_filename = f"existing_ids_part_{i}.txt"
        thread_name = f'thread_{i}'
        thread = threading.Thread(target=process_range, args=(start_index, end_index, base_url, output_filename, thread_name), name=thread_name)
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Merge all partial files into one
    with open("existing_ids.txt", "w") as outfile:
        for i in range(num_threads):
            output_filename = f"existing_ids_part_{i}.txt"
            if os.path.exists(output_filename):
                with open(output_filename, "r") as infile:
                    outfile.write(infile.read())
                os.remove(output_filename)  # Remove the partial file after merging

    print("Saved all existing IDs to existing_ids.txt")

if __name__ == "__main__":
    main()
