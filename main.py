import requests
import argparse
from urllib.parse import urlparse
from dotenv import load_dotenv
import os


def is_short_link(token, user_input):
    headers = {
        'Authorization': f'Bearer {token}'
    }

    url = user_input
    parsed = urlparse(url)
    response = requests.get(f'https://api-ssl.bitly.com/v4/bitlinks/{parsed.netloc + parsed.path}', headers=headers)

    return response.ok


def shorten_link(token, long_url):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }

    data = {"long_url": long_url}

    response = requests.post('https://api-ssl.bitly.com/v4/shorten', headers=headers, json=data)

    response.raise_for_status()

    return response.json()['link']


def get_clicks(token, user_input):
    headers = {
        'Authorization': f'Bearer {token}',
    }
    params = {
        'unit': 'week'
    }
    response = requests.get(f'https://api-ssl.bitly.com/v4/bitlinks/{user_input}/clicks', headers=headers, params=params)
    response.raise_for_status()
    return response.json()['link_clicks'][0]['clicks']


if __name__ == '__main__':
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument('link')
    args = parser.parse_args()
    user_input = args.link
    BITLY_TOKEN = os.getenv("BITLY_TOKEN")
    if is_short_link(BITLY_TOKEN, user_input):
        print(get_clicks(BITLY_TOKEN, user_input))
    else:
        print(shorten_link(BITLY_TOKEN, user_input))






