# Offensive-Security-Tools

Here, you'll find tools, configurations, and clever tricks that deliver powerful results, all accomplished with just one line of code. Whether you're streamlining your workflow or automating tasks, these snippets will save you time and effort in your penetration testing and security operations.

---

# Table of Contents

- [MythicC2-Configuration.sh](#1-mythicc2-configurationsh)
- [reverseshell.py](#2-reverseshellpy)
- [subdomain.py](#3-subdomainpy)
- [pathtraversal.py](#4-pathtraversalpy)
- [Windows_enum.ps1](#5-Windows_enumps1)
  
---

## 1. MythicC2-Configuration.sh

Make the script executable and run it:

```bash
sudo chmod +x MythicC2-Configuration.sh
sudo ./MythicC2-Configuration.sh
```

## 2. reverseshell.py

Run the script with the desired language:

```bash
python3 reverseshell.py <language>
```
Supported payloads:
bash, socat, java, python, php, nc.exe, ruby, perl, go, lua, rust, haskell, d, swift, zsh, docker, vim, android, c, bash_timeout, openssl, tcl, c#, and powershell.

This script quickly generates reverse shell one-liners in various programming languages.

## 3. subdomain.py

Bruteforce subdomains and directories with HTTP status code 200:

```bash
python3 subdomain.py <domain> <subdomain_wordlist> <directory_wordlist>
```
This script helps find hidden subdomains and accessible directories during reconnaissance.

If executed in linux then create an environment and install required packages to run the script.

## 4. pathtraversal.py

Finds the one with an url we can change to check for pathtraversal:

```bash
python3 pathtraversal.py <type> <domain> <wordlist>
```
Here there are only 2 types 0 and 1. 0 is when the code find an url that can be used to check if it have pathtraversal vulnerability. 1 is when you give the exploitable link and it just bruteforces that part

This Python script scans a web page for potential file paths or vulnerable URLs using regex and tests them with a list of payloads to detect path traversal vulnerabilities. It checks for URLs containing =, splits them, and attempts to exploit potential vulnerabilities by appending payloads to the URL..

If executed in linux then create an environment and install required packages to run the script.

## 5. Windows_enum.ps1

Run it in the windows machine (This is a post exploitation tool):

```bash
./Windows_enum.ps1
```
