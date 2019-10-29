#!/home/arty/documents/REPOSITORIES/tools/venv/bin/python3.7
import re
from builtins import IndexError
import requests
import sys

headers = {
    'accept:': '*/*',
    'user-agent:': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 '
                   'Safari/537.36 '
}


def main():
    try:
        mac = sys.argv[1]
        if re.search('..-..-..-..-..-..', mac):
            mac_addr = mac[:8].replace('-', '')
        elif re.search('....\.....\.....', mac):
            mac_addr = mac[:8].replace('.', '')
        req = requests.get('https://macvendors.com/query/{}'.format(mac_addr), data=headers)
        print(req.text)
    except IndexError:
        print('\nUSAGE:\n\n\t$ mac [00-60-37-99-AF-C2 or c8be.19c2.8ee0]')
        
        
if __name__ == '__main__':
    main()