from modules.fetch import fetch_website
import json
import os

if __name__ == "__main__":
    rawfilename = "results/raw.txt"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, 'config.json')
    keyword_path = os.path.join(script_dir, 'keyword.json')
    with open(config_path, 'r') as cfile:
    	config = json.load(cfile)
    with open(payload_path, 'r') as kfile:
    	keyword = json.load(kfile)
    
    
    fetch_website(rawfilename,config)

