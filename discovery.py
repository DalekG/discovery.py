import os
import argparse


parser = argparse.ArgumentParser(
        prog='discovery.py',
        description="Helps automate the discovery scanning phase of a PenTest. Discovery.py will perform a ping sweep, create a live host file, conduct an nmap scan of live hosts, and convert output to a csv file by default. Optionally, the auditor can only conduct the ping sweep and produce a live host file, can add other nmap flags to the basic scan, and can skip the csv creation.",
        usage='python3 discovery.py ipaddr [-h] [-c csvFilename] [-d nmapFilename] [-l liveFilename] [-n nmapAdditionalOptions] [-p pingFilename]'
        )
parser.add_argument("ipaddr", help="the ip address or cidr notation of what you want to scan")
args = parser.parse_args()
parser.add_argument("-c", dest="csv", type=str, help="desired csv filename", default=(args.ipaddr.rsplit('.', 2)[0]+"_all.csv"), metavar="filename", required=False)
parser.add_argument("-d", dest="nmapfile", type=str, help="desired discovery filename", default=(args.ipaddr.rsplit('.', 2)[0]+"_all"), metavar="filename", required=False)
parser.add_argument("-l", dest="livehost", type=str, help="desired livehost filename", default=(args.ipaddr.rsplit('.', 2)[0]+"_live.txt"), metavar="filename", required=False)
parser.add_argument("-n", dest="nmapopt", type=str, help="specify scan type such as -sS/T/U/V/C; default runs sS; use this to add any other options as well", default="-sS", metavar="options", required=False)
parser.add_argument("-p", dest="pingsweep", type=str, help="desired pingsweep filename", default=(args.ipaddr.rsplit('.', 2)[0]+"_ping.txt"), metavar="filename", required=False)
args1 = parser.parse_args()

pingScan = "nmap -sn -g 80 -T4 -oG "
os.system(pingScan + args1.pingsweep + ' ' + args.ipaddr)

grepFile = "grep 'Up' "
cutFile = "| cut -f 2 -d ' ' >> "
os.system(grepFile + args1.pingsweep + ' ' + cutFile + args1.livehost)

nmapDiscovery1 = "nmap -Pn -p- -O -sV "
nmapDiscovery2 = " --version-light --reason --open -T4 -g 80 -oA "
nmapDiscovery3 = " -iL "
os.system(nmapDiscovery1 + args1.nmapopt + nmapDiscovery2 + args1.nmapfile + nmapDiscovery3 + args1.livehost)

nmapParse1 = "/path/to/your/nmap_xml_parser.py --csv "
nmapParse2 = " -f "
os.system(nmapParse1 + args1.csv + nmapParse2 + args1.nmapfile + '.xml')
