'''
This code is used for subdomain enumeration and directory bruteforcing.
Usage: python subdomain.py abc.subdomain.com <subdomain_wordlist> <directory_wordlist>
example if the domain is owasp.org just add abc to the front and make it abc.owasp.org
2 files will be created one for subdomain with status 200 and another for directories with status 200
does not follow redirect
'''
import sys
import re
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# Output files
file_path = "subdomain.txt"
file_path2 = "directories.txt"

# Check for valid arguments
if len(sys.argv) != 4:
    print("Usage: python script.py <domain> <subdomain_wordlist> <directory_wordlist>")
    sys.exit(1)

# Parse arguments
target = sys.argv[1]
subdomain_wordlist_file = sys.argv[2]
directory_wordlist_file = sys.argv[3]

# Extract domain parts
spliting = re.split(r'[.]', target)
print(f"Target split: {spliting}")

# Read wordlists
with open(subdomain_wordlist_file, 'r') as file:
    subdomain_words = [line.strip() for line in file if line.strip()]

with open(directory_wordlist_file, 'r') as file:
    directories = [line.strip() for line in file if line.strip()]

# Clear previous output
open(file_path, 'w').close()
open(file_path2, 'w').close()

# === SUBDOMAIN ENUMERATION ===
def check_subdomain(word):
    modified = [word] + spliting[1:]
    domain = '.'.join(modified)
    subdomain_url = f"https://{domain}"
    print(f"Testing: {subdomain_url}")
    try:
        response = requests.get(subdomain_url, timeout=5)
        if response.status_code == 200:
            content = response.text.lower()
            if 'not found' in content or '<title>404' in content:
                return None
            with open(file_path, 'a') as f:
                f.write(f"{subdomain_url}\n")
            print(f"[+] {subdomain_url} - Status Code: {response.status_code}")
            return subdomain_url
    except requests.exceptions.RequestException:
        pass
    return None

print("\n--- Subdomain Enumeration ---")
with ThreadPoolExecutor(max_workers=30) as executor:
    results = list(executor.map(check_subdomain, subdomain_words))

# Load valid subdomains
with open(file_path, 'r') as file:
    valid_subdomains = [line.strip() for line in file if line.strip()]

# === DIRECTORY ENUMERATION ===
def check_directory(sub, directory):
    link = f"{sub.rstrip('/')}/{directory.lstrip('/')}"
    try:
        response = requests.get(link, timeout=2)
        content = response.text.lower()
        fake_404 = 'not found' in content or '<title>404' in content

        if response.status_code == 200 and not fake_404:
            print(f"[200 OK] {link}")
            with open(file_path2, 'a') as f:
                f.write(f"{link} \n")

        elif response.status_code == 301:
            print(f"[301 Moved Permanently] {link}")
            with open(file_path2, 'a') as f:
                f.write(f"{link} -> {response.headers.get('Location')}\n")

        elif response.status_code == 302 and not fake_404:
            print(f"[302 Found] {link}")
            with open(file_path2, 'a') as f:
                f.write(f"{link} -> {response.headers.get('Location')}\n")

        elif response.status_code == 403:
            print(f"[403 Forbidden] {link}")
            with open(file_path2, 'a') as f:
                f.write(f"{link} [403 Forbidden]\n")

        elif response.status_code == 404:
            print(f"[404 Not Found] {link}")

        elif response.status_code == 500:
            print(f"[500 Internal Server Error] {link}")
            with open(file_path2, 'a') as f:
                f.write(f"{link} [500 Error]\n")

        elif response.status_code in [401, 405, 503]:
            print(f"[{response.status_code}] {link}")
            with open(file_path2, 'a') as f:
                f.write(f"{link} [{response.status_code}]\n")

        else:
            print(f"[{response.status_code}] {link}")
            with open(file_path2, 'a') as f:
                f.write(f"{link} [{response.status_code}]\n")

    except requests.exceptions.RequestException as e:
        print(f"[Error] Failed to fetch {link}: {e}")

print("\n--- Directory Bruteforce ---")
with ThreadPoolExecutor(max_workers=50) as executor:
    futures = []
    for sub in valid_subdomains:
        for directory in directories:
            futures.append(executor.submit(check_directory, sub, directory))

    for _ in as_completed(futures):
        pass  # just to block until all are done
