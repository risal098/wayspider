import requests
import os
import sys

def fetch_website_wayback(rawfilename, domain):
    print("\n\ngetting all the history..")
    url = "https://web.archive.org/cdx/search/cdx"
    os.makedirs(os.path.dirname(rawfilename), exist_ok=True)
    params = {
    "url": "*."+domain+"/*",
    "collapse": "urlkey",
    "output": "text",
    }
    try:
        with requests.get(url, params=params, stream=True) as response:
            response.raise_for_status()
            with open(rawfilename, "w", encoding="utf-8") as file:  
            		data = 0.0
            		for chunk in response.iter_content(chunk_size=8192):
                		if chunk:
                			file.write(chunk.decode("utf-8"))
                			data+=0.008
        print(f"Content appended to {rawfilename}, total of {data} MB")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
