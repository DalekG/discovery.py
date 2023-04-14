import os
import argparse
import re
import csv
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser(
        prog='discovery.py',
        description="Helps automate the discovery scanning phase of a PenTest. Discovery.py will perform a ping sweep, create a live host file, conduct an nmap scan of live hosts, and convert output to a csv file by default.",
        usage="python3 discovery.py ipaddr [-h] [-f filename] [-n '-/--nmapOption']"
        )
parser.add_argument("ipaddr", help="the ip address or cidr notation of what you want to scan")
parser.add_argument("-f", dest="filename", type=str, help="desired filename scheme (i.e. 192.168_etc_etc)", metavar="filename", required=True)
parser.add_argument("-n", dest="nmapopt", type=str, help="specify scan type such as -sS/T/U/V/C; default runs sS; use this to add any other options as well", default="-sS", metavar="-sE/--example", required=False)
args = parser.parse_args()

os.system(f"nmap {args.ipaddr} -sn -g 80 -T4 -oG {args.filename}_ping")

os.system(f"grep 'Up' {args.filename}_ping | cut -f 2 -d ' ' >> {args.filename}_live.txt")

os.system(f"nmap -Pn -p- -O -sV {args.nmapopt} --version-light --reason --open -T4 -g 80 -oX {args.filename}.xml -iL {args.filename}_live.txt")
    
tree = ET.parse(f'{args.filename}.xml')
root = tree.getroot()

ip_dict = {}
sort_number = 1

with open(f'{args.filename}.csv', mode='w', newline='') as cf:
    cols = ['Sort', 'IP', 'Technology', 'Finding', 'Notes', 'Port', 'Service', 'Host', 'OS', 'Proto', 'Product']
    writer = csv.DictWriter(cf, fieldnames=cols)
    writer.writeheader()

    for host in root.findall('.//host'):
        ip = host.find('.//address').get('addr')
        hostname = host.find('.//hostnames/hostname').get('name') if host.find('.//hostnames/hostname') is not None else ''
        os = host.find('.//os/osmatch').get('name') if host.find('.//os/osmatch') is not None else ''

        if ip not in ip_dict:
            ip_dict[ip] = sort_number
            sort_number += 1

        for port in host.findall('.//ports/port'):
            portid = port.get('portid')
            proto = port.get('protocol')
            service = port.find('.//service').get('name') if port.find('.//service') is not None else 'unkown'
            product = port.find('.//service').get('product') if port.find('.//service') is not None else ''

            writer.writerow({'Sort': ip_dict[ip], 
                             'IP': ip, 
                             'Technology': '', 
                             'Finding': '', 
                             'Notes': '', 
                             'Port': portid, 
                             'Service': service, 
                             'Host': hostname, 
                             'OS': os, 
                             'Proto': proto, 
                             'Product': product})
