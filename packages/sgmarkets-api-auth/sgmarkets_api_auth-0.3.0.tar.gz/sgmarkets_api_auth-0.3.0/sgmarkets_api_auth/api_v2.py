

import os
import json
import urllib
import shutil

import requests as rq
import random as rd
import datetime as dt

from dotenv import load_dotenv
from IPython.display import display, Image

from requests.packages.urllib3.exceptions import InsecureRequestWarning
rq.packages.urllib3.disable_warnings(InsecureRequestWarning)


class Api_v2:
    """
    """


    def __init__(self,
                 token=None,
                 file_secret='my-secret.env',
                 verbose=False
                 ):
        """
        """
        self._show_logo()
        self.verbose = verbose
        self.url_get_token = 'https://digital.sgmarkets.com/analytics-token/'

        path_secret = os.path.join(os.path.expanduser('~'),
                                   file_secret)

        if not os.path.exists(path_secret):
            print(f'File {path_secret} was not found.')
            print(f'It was created with sample values and is printed below.')
            print(f'Edit it with your credentials.')
            print(f'To get an SG Market token visit {self.url_get_token}')

            here = os.path.dirname(__file__)
            path_tpl = os.path.join(here, 'sample', 'my_secret.tpl.txt')
            shutil.copy2(path_tpl, path_secret)
            with open(path_tpl, 'r') as f:
                content = f.read()
            print('---')
            print(content)
            return

        load_dotenv(path_secret)
        self.access_token = os.getenv('SG_TOKEN')
        self.PROXY_LOGIN = os.getenv('PROXY_LOGIN')
        self.PROXY_PASSWORD = os.getenv('PROXY_PASSWORD')
        self.PROXY_HOST = os.getenv('PROXY_HOST')
        self.PROXY_PORT = os.getenv('PROXY_PORT')

        if not self.access_token or len(self.access_token)<20:
            print('ERROR: The token is invalid.')
            print(f'Visit {self.url_get_token}\nto get an SG Market token.')
            print(f'Then put it in {path_secret}')
            return

        else:
            if self.verbose:
                print(f'Loaded SG Markets token from {path_secret}')


        self.path_secret = path_secret
        self.proxies = self._get_proxies()

    def clear_secret(self):
        """
        """
        if os.path.isfile(self.path_secret):
            os.remove(self.path_secret)
        print('Deleted file {}'.format(self.path_secret))

    def _get_proxies(self):
        """
        """
        try:
            rq.get('https://google.com')
            proxies = None
            if self.verbose:
                print('No proxy is necessary')
        except:

            dic = {'login': self.PROXY_LOGIN,
                   'pwd': urllib.parse.quote(self.PROXY_PASSWORD),
                   'proxy_host': self.PROXY_HOST,
                   'proxy_port': self.PROXY_PORT}
            proxies = {
                'http': 'http://{login}:{pwd}@{proxy_host}:{proxy_port}'.format(**dic),
                'https': 'https://{login}:{pwd}@{proxy_host}:{proxy_port}'.format(**dic)
            }
            print(f'You need go through a proxy defined in {self.path_secret}')

        return proxies

    def get(self, url, payload=None):
        """
        """
        if payload is None:
            payload = {}
        headers = {'authorization': 'Bearer ' + self.access_token}
        r = rq.get(url,
                   headers=headers,
                   params=payload,
                   proxies=self.proxies)
        if r.status_code != 200:
            raise Exception('Error in API request: {}'.format(r.text))

        return r.json()

    def post(self, url, payload=None):
        """
        """

        headers = {'authorization': 'Bearer ' + self.access_token,
                   'Content-type': 'application/json'
                   }
        r = rq.post(url,
                    headers=headers,
                    json=payload,
                    proxies=self.proxies)
        if r.status_code != 200:
            raise Exception('Error in API request: {}'.format(r.text))

        return r.json()

    def _show_logo(self):
        """
        """
        url_image = 'https://gitlab.com/sgmarkets/sgmarkets-api-auth/raw/master/sgmarkets_api_auth/img/sg-sgmarkets-logo.png'
        display(Image(url=url_image, width=200))


