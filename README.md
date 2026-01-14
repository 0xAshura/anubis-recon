# Anubis - Recon
## AnubisDB Subdomain Enumerator with Random User-Agent Rotation

##  Overview

**anubis-recon** is a lightweight, CLI-based subdomain reconnaissance tool that leverages [AnubisDB](https://anubisdb.com) to fetch subdomains for a given domain or list of domains. It is designed for **bug bounty hunters**, **security researchers**, and anyone doing **attack surface mapping**.  

##  Features

- Fetch subdomains from **AnubisDB**
- Supports **single domain** (`-d`) or **file of domains** (`-f`)
- Output in **TXT** (flat list) or **JSON** (domain → subdomain mapping)
- Random **User-Agent rotation** (5000+ unique UAs)
- Rate-limit safe (`0.5s` delay between requests)
- Handles API errors gracefully
- Clean, professional CLI with banner and examples

##  Installation

```bash
# Clone repository
git clone https://github.com/0xAshura/anubis-recon.git
cd anubis-recon

# Make executable (optional)
chmod +x anubis-recon.py

# Install dependencies
pip3 install requests
```

## Usage
Single Domain
```bash
python3 anubis-recon.py -d example.com
```
Multiple Domains from a File
```bash
python3 anubis-recon.py -f domains.txt -o results --format json
```
## Notes / Limitations

API Rate Limit: 2000 requests per 15 minutes

Maximum subdomains per domain: 10,000 (AnubisDB limit)

Duplicate domains in a file are automatically filtered

Continues execution even if a domain is missing or invalid

## Author

Mihir Limbad aka 0xMmehir | Security Researcher | Bug Bounty | Recon Automation

## Disclaimer

This tool is intended for authorized security testing and research only.
The author is not responsible for misuse. Use responsibly.


---

