# discovery.py

discovery.py is designed to automate the discovery phase of pentesting.

Requirements:
- ipaddr, cidr, or pre-generated live host file of what you want to scan
- naming scheme of your output files (ie. 192.168_texthere)
- run as root level user

How to use:\
`python3 discovery.py ip_or_host [-h] [-f filename] [-n '-sU --max-retries=0']`

- Nmap output will be supplied to the terminal window you executed the script, the script will not complete until all phases have finished executing.
- You can check the status of the scans by hitting a key during the execution
