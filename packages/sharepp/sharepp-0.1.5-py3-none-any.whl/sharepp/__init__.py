from bs4 import BeautifulSoup
import requests
import sys

onvista_url = 'https://www.onvista.de/'


def parse_price(isin):
    response = requests.get(onvista_url+isin)
    parsed_html = BeautifulSoup(response.text, 'html.parser')
    try:
        # Single share.
        price_span = parsed_html.find("ul", class_="KURSDATEN").find("span")
        price_string = price_span.text.replace(",", ".")
    except AttributeError:
        # ETF.
        price_span = parsed_html.find("span", class_="price")
        price_string = price_span.text.split(" ")[0].replace(",", ".")

    return float(price_string)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("You must provide exactly one argument.")
    else:
        print(parse_price(sys.argv[1]))
