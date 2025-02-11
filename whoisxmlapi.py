import requests
import json

def fetch_subdomains(domain):
    api_key = "at_qTGlA4z8d8YSE7Dii1jj0UPm3EZ82"
    url = f"https://subdomains.whoisxmlapi.com/api/v1?apiKey={api_key}&domainName={domain}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        domains = [record.get("domain", "") for record in data.get("result", {}).get("records", [])]
        
        filename = f"{domain}.txt"
        with open(filename, "w") as file:
            file.write("\n".join(domains))
        
        print(f"Subdomains saved to {filename}")
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
    except json.JSONDecodeError:
        print("Error decoding JSON response")

if __name__ == "__main__":
    user_domain = input("Enter the domain name: ")
    fetch_subdomains(user_domain)

