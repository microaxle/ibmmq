import os
import argparse
import time

def remove_old_files(directory, extension, days):
    try:
        days = int(days)
        current_time = time.time()

        for filename in os.listdir(directory):
            if filename.endswith(extension):
                file_path = os.path.join(directory, filename)
                # Get the file's last modification time
                file_mtime = os.path.getmtime(file_path)
                # Calculate the age of the file in days
                age_in_days = (current_time - file_mtime) / (24 * 3600)

                if age_in_days > days:
                    # Print filename and its exact timestamp before removing
                    print(f"Removing old file: {filename}, || Timestamp: {time.ctime(file_mtime)}")
                    os.remove(file_path)

        print("Removal process completed.")
    except ValueError:
        print("Please enter a valid number of days.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove old files with a specific extension from a directory.")
    parser.add_argument("-d", "--directory", help="Directory path", required=True)
    parser.add_argument("-e", "--extension", help="File extension (e.g., txt)", required=True)
    parser.add_argument("-days", help="Number of days", required=True)

    args = parser.parse_args()

    remove_old_files(args.directory, args.extension, args.days)
