import os
import argparse
import re
import csv
import xml.etree.ElementTree as ET


def ping_sweep(args):
    os.system(f"nmap {args.ip_or_file} -sn -g 80 -T4 -oG {args.outfile}_ping")

def create_host_file(args):
    os.system(f"grep 'Up' {args.outfile}_ping | cut -f 2 -d ' ' >> {args.outfile}_live.txt")
    return f'{args.outfile}_live.txt'

def scan(args, filename):
    os.system(f"nmap -Pn -p- -O -sV {args.nmapopt} --version-light --reason --open -T4 -g 80 -oX {args.outfile}.xml -iL {filename}")

def create_csv(args):    
    tree = ET.parse(f'{args.outfile}.xml')
    root = tree.getroot()

    ip_dict = {}
    sort_number = 1

    with open(f'{args.outfile}.csv', mode='w', newline='') as cf:
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
                                 

if __name__ == '__main__':                                 
	parser = argparse.ArgumentParser(
	        prog='discovery.py',
	        description="Helps automate the discovery scanning phase of a PenTest. Discovery.py will perform a ping sweep, create a live host file, conduct an nmap scan of live hosts, and convert output to a csv file by default.",
	        usage="python3 discovery.py ip_or_file [-h] [-f filename] [-n '-/--nmapOption']"
	        )
	parser.add_argument("ip_or_file", help="the ip address, cidr notation, or pre-generated livehost file of what you want to scan",)
	parser.add_argument("-f", dest="outfile", type=str, help="desired filename scheme (i.e. 192.168_etc_etc)", metavar="filename", required=True)
	parser.add_argument("-n", dest="nmapopt", type=str, help="specify scan type such as -sS/T/U/V/C; default runs sS; use this to add any other options as well", default="-sS", metavar="'-sE --example'", required=False)
	args = parser.parse_args()                                 

	live_host=""
	if os.path.isfile(args.ip_or_file):
		live_host = args.ip_or_file
	else:
		#ping sweep, create live_host
		ping_sweep(args)
		live_host = create_host_file(args)
		
	scan(args, live_host)
	create_csv(args)
