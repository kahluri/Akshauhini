#!/bin/bash

# Check if a domain is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <target.com>"
  exit 1
fi

TARGET="$1"
API_KEY="your_redhunt_api_key" # Replace with your API key for RedHunt Labs
OUTPUT_FILE="subdomain.txt"
TEMP_FILE="subdomain_temp.txt"

# Clear previous results
> "$TEMP_FILE"
> "$OUTPUT_FILE"

# Function to collect subdomains
collect_subdomains() {
  echo "[*] Collecting subdomains from $1..."
  echo "$2" >> "$TEMP_FILE"
}

# Juicy Subdomains
collect_subdomains "Juicy Subdomains" "$(subfinder -d "$TARGET" -silent | dnsx -silent | cut -d ' ' -f1 | grep 'api\|dev\|stg\|test\|admin\|demo\|stage\|pre\|vpn')"

# From BufferOver.run
collect_subdomains "BufferOver.run" "$(curl -s "https://dns.bufferover.run/dns?q=.$TARGET" | jq -r .FDNS_A[] | cut -d',' -f2 | sort -u)"

# From Riddler.io
collect_subdomains "Riddler.io" "$(curl -s "https://riddler.io/search/exportcsv?q=pld:$TARGET" | grep -Po "(([\w.-]*)\.([\w]*)\.([A-z]))\w+" | sort -u)"

# From RedHunt Labs Recon API
collect_subdomains "RedHunt Labs" "$(curl -s --request GET --url "https://reconapi.redhuntlabs.com/community/v1/domains/subdomains?domain=$TARGET&page_size=1000" \
  --header "X-BLOBR-KEY: $API_KEY" | jq -r '.subdomains[]')"

# From Nmap
collect_subdomains "Nmap" "$(nmap --script hostmap-crtsh.nse "$TARGET" | grep -Eo '([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}')"

# From CertSpotter
collect_subdomains "CertSpotter" "$(curl -s "https://api.certspotter.com/v1/issuances?domain=$TARGET&include_subdomains=true&expand=dns_names" \
  | jq .[].dns_names | grep -Po "(([\w.-]*)\.([\w]*)\.([A-z]))\w+" | sort -u)"

# From Archive
collect_subdomains "Archive" "$(curl -s "http://web.archive.org/cdx/search/cdx?url=*.$TARGET/*&output=text&fl=original&collapse=urlkey" \
  | sed -e 's_https*://__' -e "s/\/.*//" | sort -u)"

# From JLDC
collect_subdomains "JLDC" "$(curl -s "https://jldc.me/anubis/subdomains/$TARGET" | grep -Po "((http|https):\/\/)?(([\w.-]*)\.([\w]*)\.([A-z]))\w+" | sort -u)"

# From crt.sh
collect_subdomains "crt.sh" "$(curl -s "https://crt.sh/?q=%25.$TARGET&output=json" | jq -r '.[].name_value' | sed 's/\*\.//g' | sort -u)"

# From ThreatMiner
collect_subdomains "ThreatMiner" "$(curl -s "https://api.threatminer.org/v2/domain.php?q=$TARGET&rt=5" | jq -r '.results[]' | grep -o "\w.*$TARGET" | sort -u)"

# From ThreatCrowd
collect_subdomains "ThreatCrowd" "$(curl -s "https://www.threatcrowd.org/searchApi/v2/domain/report/?domain=$TARGET" \
  | jq -r '.subdomains' | grep -o "\w.*$TARGET")"

# From HackerTarget
collect_subdomains "HackerTarget" "$(curl -s "https://api.hackertarget.com/hostsearch/?q=$TARGET" | cut -d, -f1)"

# From AlienVault
collect_subdomains "AlienVault" "$(curl -s "https://otx.alienvault.com/api/v1/indicators/domain/$TARGET/url_list?limit=100&page=1" \
  | grep -o '"hostname": *"[^"]*' | sed 's/"hostname": "//' | sort -u)"

# From Censys
collect_subdomains "Censys" "$(censys subdomains "$TARGET" 2>/dev/null)"

# From Subdomain Center
collect_subdomains "Subdomain Center" "$(curl -s "https://api.subdomain.center/?domain=$TARGET" | jq -r '.[]' | sort -u)"

# Remove duplicates and save to the output file
sort -u "$TEMP_FILE" > "$OUTPUT_FILE"
rm "$TEMP_FILE"

echo "[*] Subdomains saved to $OUTPUT_FILE"

