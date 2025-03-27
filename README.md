<h1>
<p align="center">
  <img src="https://github.com/risal098/wayspider/blob/main/logo%20way.png" alt="Logo" width="128">
  <br>wayspider
</h1>
 <p align="center">
    Fast, Strong, Accurate secret url,subdomain,parameter finder 
    <br />
    <a href="#about">About</a>
    ·
    <a href="#installation">Installation</a>
    ·
    <a href="#Documentation">Documentation</a>
    ·
    
  </p>
</p>

## About
wayspider is a penetration testing tool that help you to enumerate urls that might contain secret data, url with parameter ,even subdomains, all in one tool



## Installation
1. git clone https://github.com/risal098/wayspider.git
2. pip install requests


## Documentation
```
usage: wayspider.py [-h] [-d DOMAIN] [-e EXP_SENS] [-i EXP_NON_SENS]
                    [-b BYPASS] [-m MATCH_BYPASS] [-c CHECK_URL] [-s] [--sdp]
                    [--sd] [-l LIST] [--vwp]

tools to find subdomains,url with params, common lfi and data exposure
vulnerability, bypass 403/404 file

options:
  -h, --help            show this help message and exit
  -d DOMAIN, --domain DOMAIN
                        domain for enumeration, e.g example.com
  -e EXP_SENS, --expression-sensitive EXP_SENS
                        find spesific url that contain the expressions,
                        argument must be python tuple like, e.g
                        '(".env",".pdf",".sql","eyJ")'
  -i EXP_NON_SENS, --expression-non-sensitive EXP_NON_SENS
                        find spesific url that contain the non sensitive
                        expressions, argument must be python tuple like, e.g
                        '("john-doe","social security","userid","token")'
  -b BYPASS, --bypass BYPASS
                        bypass 403,404 and any restriction by fetching 200
                        status on wayback storage
  -m MATCH_BYPASS, --match-bypass MATCH_BYPASS
                        check if url exist in bypass list also request in
                        internet, and will generate bypass/wayback to check
  -c CHECK_URL, --check-url CHECK_URL
                        check if url exist in status list and give code to
                        wayback
  -s, --status-url      show status url
  --sdp                 show subdomains with protocol
  --sd                  show subdomains
  -l LIST, --list LIST  get list of domain in txt file
  --vwp                 validate wp content and wp include

```


## big thanks
shoutout to https://github.com/coffinxp as my inspiration also this tool is the modified version of his creation
