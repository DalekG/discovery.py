# discovery.py

discovery.py is designed to automate the discovery phase of pentesting.

Requirements:
- install nmap_xml_parser.py from https://github.com/laconicwolf/Nmap-Scan-to-CSV
- change nmapParse1 so that it uses the path to your nmap_xml_parser.py
- run as root level user

How to use:\
`python3 discovery.py ipaddr [-h] [-c csvFilename] [-d nmapFilename] [-l liveFilename] [-n nmapAdditionalOptions] [-p pingsweepFilename]`

- Nmap output will be supplied to the terminal window you executed the script, the script will not complete until all phases have finished executing.
- You can check the status of the scans by hitting a key during the execution
