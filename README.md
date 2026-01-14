# Anubis - Recon
## AnubisDB Subdomain Enumerator with Random User-Agent Rotation

---

##  Overview

**anubis-recon** is a lightweight, CLI-based subdomain reconnaissance tool that leverages [AnubisDB](https://anubisdb.com) to fetch subdomains for a given domain or list of domains.  
It is designed for **bug bounty hunters**, **security researchers**, and anyone doing **attack surface mapping**.  

---

##  Features

- Fetch subdomains from **AnubisDB**
- Supports **single domain** (`-d`) or **file of domains** (`-f`)
- Output in **TXT** (flat list) or **JSON** (domain → subdomain mapping)
- Random **User-Agent rotation** (5000+ unique UAs)
- Rate-limit safe (`0.5s` delay between requests)
- Handles API errors gracefully
- Clean, professional CLI with banner and examples

---

##  Installation

```bash
# Clone repository
git clone https://github.com/0xAshura/anubis-recon.git
cd anubis-recon

# Make executable (optional)
chmod +x anubis_enum1.py

# Install dependencies
pip3 install requests
