#!/usr/bin/env python3

import argparse
import requests
import json
import time
import random
import sys
import colorama
from colorama import Fore, Style

# ================= BANNER ================= #

BANNER = r"""
 _______ __   _ _     _ ______  _____ _______       ______ _______ _______  _____  __   _
 |_____| | \  | |     | |_____]   |   |______      |_____/ |______ |       |     | | \  |
 |     | |  \_| |_____| |_____] __|__ ______|      |    \_ |______ |_____  |_____| |  \_|
                                                                                         
                         anubis‑recon :: subdomain intelligence
                                       by 0xMmehir
"""

# ================= CONFIG ================= #

API_URL = "https://anubisdb.com/anubis/subdomains/"
REQUEST_DELAY = 0.5
TIMEOUT = 15

# ================= COLOR ================= #

colorama.init(autoreset=True)

# ================= CUSTOM PARSER ================= #

class BannerParser(argparse.ArgumentParser):
    def print_help(self, *args, **kwargs):
        print(Fore.CYAN + BANNER + Style.RESET_ALL)
        super().print_help(*args, **kwargs)

# ================= USER AGENT GENERATOR ================= #

def generate_user_agents(count=5000):
    browsers = {
        "Chrome": list(range(90, 123)),
        "Firefox": list(range(85, 122)),
        "Safari": list(range(13, 18)),
        "Edge": list(range(90, 122))
    }

    os_list = [
        "Windows NT 10.0; Win64; x64",
        "Windows NT 11.0; Win64; x64",
        "Macintosh; Intel Mac OS X 10_15_7",
        "Macintosh; Intel Mac OS X 11_6",
        "X11; Linux x86_64",
        "X11; Ubuntu; Linux x86_64"
    ]

    uas = set()

    while len(uas) < count:
        os_choice = random.choice(os_list)
        browser = random.choice(list(browsers.keys()))
        version = random.choice(browsers[browser])

        if browser == "Chrome":
            ua = (
                f"Mozilla/5.0 ({os_choice}) AppleWebKit/537.36 "
                f"(KHTML, like Gecko) Chrome/{version}.0."
                f"{random.randint(1000,5000)}.{random.randint(10,150)} Safari/537.36"
            )
        elif browser == "Firefox":
            ua = (
                f"Mozilla/5.0 ({os_choice}; rv:{version}.0) "
                f"Gecko/20100101 Firefox/{version}.0"
            )
        elif browser == "Safari":
            ua = (
                f"Mozilla/5.0 ({os_choice}) AppleWebKit/605.1.15 "
                f"(KHTML, like Gecko) Version/{version}.0 Safari/605.1.15"
            )
        else:  # Edge
            ua = (
                f"Mozilla/5.0 ({os_choice}) AppleWebKit/537.36 "
                f"(KHTML, like Gecko) Chrome/{version}.0."
                f"{random.randint(1000,5000)}.{random.randint(10,150)} "
                f"Safari/537.36 Edg/{version}.0"
            )

        uas.add(ua)

    return list(uas)

USER_AGENTS = generate_user_agents(5000)

# ================= CORE LOGIC ================= #

def fetch_subdomains(domain):
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "application/json"
    }

    try:
        r = requests.get(API_URL + domain, headers=headers, timeout=TIMEOUT)

        if r.status_code == 200:
            return r.json()

        elif r.status_code == 300:
            print(Fore.RED + f"[!] {domain}: Not found in AnubisDB" + Style.RESET_ALL)

        elif r.status_code == 403:
            print(Fore.RED + f"[!] {domain}: Invalid domain" + Style.RESET_ALL)

        else:
            print(Fore.RED + f"[!] {domain}: Server error ({r.status_code})" + Style.RESET_ALL)

    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"[!] {domain}: Request failed -> {e}" + Style.RESET_ALL)

    return []

# ================= OUTPUT ================= #

def save_txt(results, filename):
    with open(filename, "w") as f:
        for subs in results.values():
            for sub in subs:
                f.write(sub + "\n")

def save_json(results, filename):
    data = []
    for domain, subs in results.items():
        data.append({
            "domain": domain,
            "subdomains": subs
        })
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

# ================= MAIN ================= #

def main():
    parser = BannerParser(
        description="AnubisDB Subdomain Enumerator with Random UA Rotation",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""Examples:
  python3 anubis_enum1.py -d example.com
  python3 anubis_enum1.py -f domains.txt -o results --format json
"""
    )

    parser.add_argument("-d", "--domain", help="Single domain")
    parser.add_argument("-f", "--file", help="File with domains")
    parser.add_argument("-o", "--output", default="output", help="Output filename (no extension)")
    parser.add_argument("--format", choices=["txt", "json"], default="txt")

    args = parser.parse_args()

    # Banner at start
    print(Fore.CYAN + BANNER + Style.RESET_ALL)

    domains = []

    if args.domain:
        domains.append(args.domain.strip())

    if args.file:
        try:
            with open(args.file, "r") as f:
                domains.extend(line.strip() for line in f if line.strip())
        except FileNotFoundError:
            print(Fore.RED + "[!] Domain file not found" + Style.RESET_ALL)
            sys.exit(1)

    if not domains:
        parser.print_help()
        sys.exit(1)

    results = {}

    for domain in domains:
        print(Fore.YELLOW + f"[*] Fetching subdomains for: {domain}" + Style.RESET_ALL)
        subs = fetch_subdomains(domain)
        if subs:
            results[domain] = sorted(set(subs))
        time.sleep(REQUEST_DELAY)

    if args.format == "txt":
        save_txt(results, args.output + ".txt")
    else:
        save_json(results, args.output + ".json")

    print(Fore.GREEN + f"[+] Done. Output saved to {args.output}.{args.format}" + Style.RESET_ALL)

if __name__ == "__main__":
    main()
