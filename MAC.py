import requests


headers = {
    'accept:': '*/*',
    'user-agent:': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 '
                   'Safari/537.36 '
}
# url = "https://macvendors.com/query/00055f" # Cisco Systems, Inc
# url = "https://macvendors.com/query/80acac" # Juniper Networks
MAC = '80ac.acdb.834e'
url = "https://macvendors.com/query/{}".format(MAC[:4] + MAC[5:7])


if __name__ == '__main__':
    print(url)
    req = requests.get(url, data=headers)
    print(req.text)