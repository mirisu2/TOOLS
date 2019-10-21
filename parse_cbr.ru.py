import requests
from bs4 import BeautifulSoup as bs


# pip install lxml
# pip install requests
# pip install bs4


def cbr_ru_parse(url, headers):
    """

    :param url: str
    :param headers: dict
    :return: list of dict
    """

    currency_arr = list()
    session = requests.session()
    req = session.get(url, data=headers)

    if req.status_code == 200:
        print('\nURL: {}'.format(url))
        print('NOTIFY: Data was received. STATUS_CODE: {}\n'.format(req.status_code))
        soup = bs(req.content, 'lxml')  # Default parser = 'lxml'. 'html.parser'
        currency_table = soup.find("table", attrs={"class": "data"})

        # print(currency_table.name) # table
        # print(currency_table['class']) # ['data']
        # print(currency_table.get('class'))  # ['data']
        # print(currency_table.attrs) # {'class': ['data']}
        # print(type(currency_table)) # <class 'bs4.element.Tag'>

        for row in currency_table.find_all('tr')[1:]:
            columns = row.find_all(
                'td')  # [<td>036</td>, <td>AUD</td>, <td>1</td>, <td>Австралийский доллар</td>, <td>43,5254</td>]
            currency_arr.append({
                'code': columns[0].text,
                'letter': columns[1].text,
                'unit': columns[2].text,
                'currency_name': columns[3].text,
                'exchange_rates': columns[4].text
            })
        return currency_arr
    else:
        print('ERROR: Data was not received')


headers = {
    'accept:': '*/*',
    'user-agent:': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}
url = "https://www.cbr.ru/currency_base/daily/"

if __name__ == '__main__':
    for i in cbr_ru_parse(url, headers):
        print(i)
