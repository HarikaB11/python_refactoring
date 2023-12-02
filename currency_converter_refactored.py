import json
import requests
from argparse import ArgumentParser

class CurrencyConverter:
    API_URL = 'https://api.exchangerate-api.com/v4/latest/'

    def __init__(self, from_currency, to_currency, amount):
        self.from_currency = from_currency.upper()
        self.to_currency = to_currency.upper()
        self.amount = amount

    def convert_currency(self):
        try:
            exchange_rate = self.get_exchange_rate()
            converted_amount = float(self.amount) * exchange_rate
            print(f"{self.amount} {self.from_currency} = {converted_amount:.2f} "
                  f"{self.to_currency} (exchange rate: {exchange_rate})")
        except Exception as err:
            print(err)

    def get_exchange_rate(self):
        api_url = f"{self.API_URL}{self.from_currency}"
        response = requests.get(api_url)
        json_response = response.json()

        if response.status_code == 200:
            if self.to_currency not in json_response['rates']:
                raise Exception('To Currency not supported')

            return json_response['rates'][self.to_currency]

        if response.status_code == 404 and json_response.get('error_type') == 'unsupported_code':
            raise Exception('From Currency not supported')

        raise Exception('Could not get exchange rate')

def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument("-from", dest="from_currency", default="usd",
                        help="From currency (e.g., usd)", metavar="CURRENCY")
    parser.add_argument("-to", dest="to_currency", default="cad",
                        help="To currency (e.g., usd)", metavar="CURRENCY")
    parser.add_argument("-amount", dest="amount", default=100,
                        help="Amount", metavar="AMOUNT")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    currency_converter = CurrencyConverter(args.from_currency, args.to_currency, args.amount)
    currency_converter.convert_currency()
