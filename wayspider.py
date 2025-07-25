from modules.fetch import *
from modules.features import *
import json
import os
import argparse
import ast
# dump https://web.archive.org/web/20250301002714/https://example.com/

if __name__ == "__main__":

    # just to make it looks cool hehe
    header_text = """\033[91m                                     .__    .___
__  _  _______  ___.__. ____________ |__| __| _/___________
\ \/ \/ /\__  \<   |  |/  ___/\____ \|  |/ __ |/ __ \_  __ \     / _ \\\n \     /  / __ \\___  |\___ \ |  |_> >  / /_/ \  ___/|  | \/    \_\(_)/_/  \033[94m
  \/\_/  (____  / ____/____  >|   __/|__\____ |\___  >__|       _//V\\\\_
              \/\/         \/ |__|           \/    \/            /   \\\033[0m"""
    print(header_text)
    print("ind subdomains,url with params, common lfi and data exposure vulnerability, bypass 403/404 file")
    print("NO SYSTEM IS SAFE!\n\n")
    nasecs_text="""\033[94m@@@@@@@@@@@@@@@@@@@@@@@@@%%@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@%%%%%%@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@%%%%%%%%%@@@@@@@@%%@@@@@@@@@@@@@@@@@
@@@@@@@@@@%%%%%%%%%%%%%%%@@@@@@@@@%%%%%%%%%@@@@@@@@@@
@@@@@%%%%%%%%%%%%%%%%%%%%@@@@@@@@%%%%%%%%%%%%%%%@@@@@
@@@@@%%%%%%%%%%%%%%%%%%%@@@%@@@@%%@@%%%%%%%%%%%@@@@@@
@@@@@%%%%%%%%%%%%%%%%%%%%##@@@@@@@@%%%%%%%%%%%%@@@@@@
@@@@@%%%%%%%%%%%%%%%%%%%#+*@@@@@@@%*+**%%%%%%%%@@@@@@
@@@@@%%%%%%%%*+*%%%%%%%#*+%@@@@@@%*++++*%%%%%%%@@@@@@
@@@@@%%%%%%%#+++*%%%%%%*+#@@@@@@@#+++++*#%%%%%%@@@@@@
@@@@@%%%%%%%+++++*%%%%#++%%%%@@@%*+**++*#%%%%%%@@@@@@
@@@@@@%%%%%*++*++*#%%%+++*#%%@@%*++**++*#%%%%%%@@@@@@
@@@@@@%%%%#++*#*++*%%*++*#%%@@@#++*##++*#%%%%%@@@@@@@
@@@@@@%%%%++*#%#++*##+++*#%%@@%*+++**++*#%%%%%@@@@@@@
@@@@@@@%%*++*#%%*++++++*#%%%@%*++++++++*#%%%%%@@@@@@@
@@@@@@@%#++*#%%%%#+++++*#%%@@%*+++**#++*#%%%%@@@@@@@@
@@@@@@@@#**#%%%%%%#**###%%%@%#*++*#%%%++*%%%%@@@@@@@@
@@@@@@@@%%%%%%%%%%%%%%%%%%%%%#++*#%%%%*+*#%%@@@@@@@@@
@@@@@@@@@%%%%%%%%%%%%%%%%%%%%#++*#%%%%%**#%@@@@@@@@@@
@@@@@@@@@@%%%%%%%%%%%%%%%%%%%%#*#%%%%%%%#%%@@@@@@@@@@
@@@@@@@@@@@%%%%%%%%##%%%%%%%%%%%##%%%%%%%%@@@@@@@@@@@
@@@@@@@@@@@@%%%%%#+*#+*=**#+**#+###%%%%%@@@@@@@@@@@@@
@@@@@@@@@@@@@%%%%#++*#*=*#**#*##==+#%%%@@@@@@@@@@@@@@
@@@@@@@@@@@@@@%%*##+##**###=%%%%*#**%%@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@%##*#%#=####=###%#+*#%@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@%%%%%###%%%##%%%%%@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@%%%%%%%%%%%%%%@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@%%%%%%%%%@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@\033[91mNA\033[94m%%%@@@@@@@@@@@@@@@@@@@@@@@@@\033[0m"""

    #print(nasecs_text)
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
    # parser.add_argument('--rc', type=str,
    #                   help='check with regex if url exist in status list and give code to wayback')
    parser.add_argument('-s', '--status-url',  action="store_true",
                        help='show status url')
    parser.add_argument('--sdp',   action="store_true",
                        help='show subdomains with protocol')
    parser.add_argument('--sd',   action="store_true",
                        help='show subdomains ')
    parser.add_argument('-l', '--list', type=str,
                        help='get list of domain in txt file')
    parser.add_argument('--vwp', action="store_true",
                        help='validate wp content and wp include')                                                
    parser.add_argument('--about', action="store_true",
                        help='about this tool')
    args = parser.parse_args()

    # target variable to save the program arguments
    domain = args.domain
    regex_check = None  # args.rc
    bypass = args.bypass
    check = args.check_url
    listfile = args.list
    # subdomains=args.subdomains
    match_bypass = args.match_bypass
    user_exp_sens = list(ast.literal_eval(args.exp_sens)
                         ) if args.exp_sens else []
    user_exp_non_sens = list(ast.literal_eval(
        args.exp_non_sens)) if args.exp_non_sens else []

   # hardcode expresion for matching (common data/access exposure)
    common_exp_non_sens = ["token", "userid", "id=", "admin", ".xls", ".xml", ".xlsx", ".json", ".pdf", ".sql", "doc", ".docx", ".pptx", ".txt", ".git", ".zip", ".tar.gz", ".tgz", ".bak", ".7z", ".rar", "log", "cache", ".secret", ".db", "backup", ".yml", ".gz", "config", ".csv", ".yaml", ".md", ".md5", ".exe", ".dll", ".bin",
                           ".ini", ".bat", ".sh", ".tar", ".deb", ".rpm", ".iso", ".img", ".env", ".apk", ".msi", ".dmg", ".tmp", ".crt", ".pem", "key", "pub", "asc", "readme", "debug"]
    common_exp_sens = ["eyJ", "wp-content", "wp-json"]

    non_sens_keyword = common_exp_non_sens+user_exp_non_sens
    sens_keyword = common_exp_sens+user_exp_sens

    # naming for file and folders
    rawfilename = "raw.txt"
    urlfilename = "url.txt"
    statusurlfilename = "status.txt"
    bypassfilename = "bypass.txt"
    subdomainfilename = "subdomain.txt"
    subdomainonlyfilename = "subdomainonly.txt"
    non_sens_name = "nonsens.txt"
    sens_name = "sens.txt"
    statusfoundfile = "statusFound.json"
    wpcfile="wpcontent.txt"
    winfile="wpinclude.txt"
    wpjsonfile="wpjson.txt"
    # keyword status
    keyword_status = {"sens": {}, "nonsens": {}}

    if domain:
        rawfilename = domain+"/"+rawfilename
        urlfilename = domain+"/"+urlfilename
        statusurlfilename = domain+"/"+statusurlfilename
        bypassfilename = domain+"/"+bypassfilename
        subdomainfilename = domain+"/"+subdomainfilename
        subdomainonlyfilename = domain+"/"+subdomainonlyfilename
        non_sens_name = domain+"/"+non_sens_name
        sens_name = domain+"/"+sens_name
        statusfoundfile = domain+"/"+statusfoundfile
        wpcfile = domain+"/"+wpcfile
        winfile = domain+"/"+winfile
        wpjsonfile = domain+"/"+wpjsonfile
        keyword_status = statusInsert(
            common_exp_non_sens, common_exp_sens, user_exp_non_sens, user_exp_sens, keyword_status)
        fetch_website_wayback(rawfilename, domain)
        urlFetcher(rawfilename, urlfilename)
        statusUrlFetcher(rawfilename, statusurlfilename)
        statusBypassFetcher(rawfilename, bypassfilename)
        keyword_status = commonKeywordFetcher(urlfilename, sens_name,
                                              sens_keyword, keyword_status)
        keyword_status = userKeywordFetcher(urlfilename, sens_name,
                                            sens_keyword, keyword_status)
        keyword_status = commonNonSensKeywordFetcher(
            urlfilename, non_sens_name, non_sens_keyword, keyword_status)
        keyword_status = userNonSensKeywordFetcher(
            urlfilename, non_sens_name, non_sens_keyword, keyword_status)
        writeStatusFound(statusfoundfile, keyword_status)
        subdomainFetch(urlfilename, subdomainfilename)
        subdomainOnlyFetch(urlfilename, subdomainonlyfilename)
        wpcontentFetch(urlfilename,wpcfile)
        wpincludeFetch(urlfilename,winfile)
        wpjsonuser(urlfilename,wpjsonfile)
        showStatus(statusfoundfile)
    if bypass:
        getUrlFromFile(bypassfilename, bypass)
    if match_bypass:
        matchBypass(bypassfilename, match_bypass)
    if check:
        getUrlFromFile(statusurlfilename, check)
    if regex_check:
        getUrlRegexFromFile(statusurlfilename, check)
    if args.status_url:
        showStatus(statusfoundfile)
    if args.sdp:
        getSubdomains(subdomainfilename)
    if args.sd:
        getSubdomains(subdomainonlyfilename)
    if args.about:
    		print(nasecs_text)
    if args.vwp:
    		validatewp(wpcfile)
    		validatewp(winfile)
    if listfile:
        with open(listfile, "r", encoding="utf-8") as file:
            while (line := file.readline()):
                domain = line.strip()
                rawfilename = domain+"/"+rawfilename
                urlfilename = domain+"/"+urlfilename
                statusurlfilename = domain+"/"+statusurlfilename
                bypassfilename = domain+"/"+bypassfilename
                subdomainfilename = domain+"/"+subdomainfilename
                subdomainonlyfilename = domain+"/"+subdomainonlyfilename
                non_sens_name = domain+"/"+non_sens_name
                sens_name = domain+"/"+sens_name
                statusfoundfile = domain+"/"+statusfoundfile
                wpcfile = domain+"/"+wpcfile
                winfile = domain+"/"+winfile
                wpjsonfile = domain+"/"+wpjsonfile
                keyword_status = statusInsert(
                    common_exp_non_sens, common_exp_sens, user_exp_non_sens, user_exp_sens, keyword_status)
                fetch_website_wayback(rawfilename, domain)
                urlFetcher(rawfilename, urlfilename)
                statusUrlFetcher(rawfilename, statusurlfilename)
                statusBypassFetcher(rawfilename, bypassfilename)
                keyword_status = commonKeywordFetcher(urlfilename, sens_name,
                                                      sens_keyword, keyword_status)
                keyword_status = userKeywordFetcher(urlfilename, sens_name,
                                                    sens_keyword, keyword_status)
                keyword_status = commonNonSensKeywordFetcher(
                    urlfilename, non_sens_name, non_sens_keyword, keyword_status)
                keyword_status = userNonSensKeywordFetcher(
                    urlfilename, non_sens_name, non_sens_keyword, keyword_status)
                writeStatusFound(statusfoundfile, keyword_status)
                subdomainFetch(urlfilename, subdomainfilename)
                subdomainOnlyFetch(urlfilename, subdomainonlyfilename)
                wpcontentFetch(urlfilename,wpcfile)
                wpincludeFetch(urlfilename,winfile)
                wpjsonuser(urlfilename,wpjsonfile)
