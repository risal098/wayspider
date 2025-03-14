from modules.fetch import *
from modules.features import *
import json
import os
import argparse
import ast
# dump https://web.archive.org/web/20250301002714/https://example.com/
"""
script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, 'config.json')
keyword_path = os.path.join(script_dir, 'keyword.json')
with open(config_path, 'r') as cfile:
	config = json.load(cfile)
with open(payload_path, 'r') as kfile:
	keyword = json.load(kfile)
"""
if __name__ == "__main__":

    # just to make it looks cool hehe
    header_text = """\033[91m                                     .__    .___            
__  _  _______  ___.__. ____________ |__| __| _/___________ 
\ \/ \/ /\__  \<   |  |/  ___/\____ \|  |/ __ |/ __ \_  __ \     / _ \   
 \     /  / __ \\___  |\___ \ |  |_> >  / /_/ \  ___/|  | \/    \_\(_)/_/  \033[94m
  \/\_/  (____  / ____/____  >|   __/|__\____ |\___  >__|       _//V\\\\_ 
              \/\/         \/ |__|           \/    \/            /   \\\033[0m"""
    print(header_text)
    print("ind subdomains,url with params, common lfi and data exposure vulnerability, bypass 403/404 file")
    print("NO SYSTEM IS SAFE!\n\n")
    parser = argparse.ArgumentParser(
        description="tools to find subdomains,url with params, common lfi and data exposure vulnerability, bypass 403/404 file")

    # Add arguments
    parser.add_argument('-d', '--domain', type=str,
                        help='domain for enumeration, e.g example.com', dest="domain")
    parser.add_argument('-e', '--expression-sensitive', type=str,
                        help='find spesific url that contain the expressions, argument must be python tuple like, e.g \'(".env",".pdf",".sql","eyJ")\'', dest="exp_sens")
    parser.add_argument('-i', '--expression-non-sensitive', type=str,
                        help='find spesific url that contain the non sensitive expressions, argument must be python tuple like, e.g \'("john-doe","social security","userid","token")\'', dest="exp_non_sens")
    parser.add_argument('-b', '--bypass', type=str,
                        help='bypass 403,404 and any restriction by fetching 200 status on wayback storage')
    parser.add_argument('-m', '--match-bypass', type=str,
                        help='check if url exist in bypass list also request in internet, and will generate bypass/wayback to check')
    parser.add_argument('-c', '--check-url', type=str,
                        help='check if url exist in status list and give code to wayback')           
    args = parser.parse_args()

    # target variable to save the program arguments
    domain = args.domain
    bypass=args.bypass
    check=args.check_url
    match_bypass=args.match_bypass
    user_exp_sens = list(ast.literal_eval(args.exp_sens)
                         ) if args.exp_sens else []
    user_exp_non_sens = list(ast.literal_eval(
        args.exp_non_sens)) if args.exp_non_sens else []

   # hardcode expresion for matching (common data/access exposure)
    common_exp_non_sens = ["token", "userid", "id=", "admin", "xls", "xml", "xlsx", "json", "pdf", "sql", "doc", "docx", "pptx", "txt", "git", "zip", "tar.gz", "tgz", "bak", "7z", "rar", "log", "cache", "secret", "db", "backup", "yml", "gz", "config", "csv", "yaml", "md", "md5", "exe", "dll", "bin",
                           "ini", "bat", "sh", "tar", "deb", "rpm", "iso", "img", "env", "apk", "msi", "dmg", "tmp", "crt", "pem", "key", "pub", "asc", "readme", "debug"]
    common_exp_sens = ["eyJ", "wp-content", "wp-json"]

    non_sens_keyword = common_exp_non_sens+user_exp_non_sens
    sens_keyword = common_exp_sens+user_exp_sens

    # naming for file and folders
    rawfilename = "results/raw.txt"
    urlfilename = "results/url.txt"
    statusurlfilename = "results/status.txt"
    bypassfilename = "results/bypass.txt"

    non_sens_name = "results/nonsens.txt"
    sens_name = "results/sens.txt"

    # keyword status
    keyword_status = {"sens": {}, "nonsens": {}}

    if domain:
        keyword_status = statusInsert(
            common_exp_non_sens, common_exp_sens, user_exp_non_sens, user_exp_sens,keyword_status)
        fetch_website_wayback(rawfilename, domain)
        urlFetcher(rawfilename, urlfilename)
        statusUrlFetcher(rawfilename, statusurlfilename)
        statusBypassFetcher(rawfilename, bypassfilename)
        keyword_status =commonKeywordFetcher(urlfilename, sens_name,
                             sens_keyword, keyword_status)
        keyword_status =userKeywordFetcher(urlfilename, sens_name,
                           sens_keyword, keyword_status)
        keyword_status =commonNonSensKeywordFetcher(
            urlfilename, non_sens_name, non_sens_keyword, keyword_status)
        keyword_status =userNonSensKeywordFetcher(
            urlfilename, non_sens_name, non_sens_keyword, keyword_status)
        writeStatusFound(keyword_status )
        showStatus()
    if bypass:
    	getUrlFromFile(bypassfilename,bypass)
    if match_bypass:
    	matchBypass(bypassfilename,match_bypass)
    if check:
    	getUrlFromFile(statusurlfilename ,check)
        
