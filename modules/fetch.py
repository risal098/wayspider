import requests
import os
def fetch_website(rawfilename,config):
    url = "https://web.archive.org/cdx/search/cdx"
    os.makedirs(os.path.dirname(rawfilename), exist_ok=True)
    params = config
    try:
        with requests.get(url, params=params, stream=True) as response:
            response.raise_for_status()
            with open(rawfilename, "a", encoding="utf-8") as file:  # Append mode
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk.decode("utf-8"))
        print(f"Content appended to {rawfilename}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
