import os
import time
import requests
import sys

def retrieve_html():
    base_url = "http://en.tutiempo.net/climate"

    for year in range(2013, 2019):
        for month in range(1, 13):
            month_str = f"0{month}" if month < 10 else str(month)
            url = f"{base_url}/{month_str}-{year}/ws-421820.html"

            try:
                response = requests.get(url, timeout=10)  # Added timeout
                response.raise_for_status()  # Raise error for bad responses
                text_utf = response.content  # Directly use `.content` for binary writing

                save_path = f"Data/Html_Data/{year}"
                os.makedirs(save_path, exist_ok=True)  # Ensures directory exists

                file_path = os.path.join(save_path, f"{month}.html")
                with open(file_path, "wb") as output:
                    output.write(text_utf)

                print(f"Saved: {file_path}")

            except requests.exceptions.RequestException as e:
                print(f"Error fetching {url}: {e}")

        sys.stdout.flush()

if __name__ == "__main__":
    start_time = time.time()
    retrieve_html()
    stop_time = time.time()
    print(f"Time taken: {stop_time - start_time:.2f} seconds")
