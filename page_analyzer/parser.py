import requests
from bs4 import BeautifulSoup


def parse(name):
    parse_dict = {}
    response = requests.get(name)
    response.raise_for_status()
    parse_dict['status_code'] = response.status_code
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    parse_dict['h1'] = soup.h1.text if soup.find('h1') else " "
    parse_dict['title'] = soup.title.text if soup.find('title') else " "
    description = soup.find("meta", attrs={"name": "description"})
    parse_dict['description'] = description.get("content") \
        if description else " "
    return parse_dict
