"""
Core client functionality, common across all API requests.
"""

versie = "1.0"

import requests
from urllib.parse import urlencode
import json

from bol import __version__ as __version
_USER_AGENT = "BolApiClientPython/%s" % __version
_DEFAULT_BASE_URL = "https://api.bol.com/retailer"
_DEMO_BASE_URL = "https://api.bol.com/retailer-demo"


class Client(object):
    """Performs requests to the Bol.com API."""

    def __init__(self, client_id, client_secret, demo=False):
        """Base Bol.com api client."""

        if demo:
            self.BASE_URL = _DEMO_BASE_URL
            print("Using demo environment")
        else:
            self.BASE_URL = _DEFAULT_BASE_URL
        
        self.client_id = client_id
        self.client_secret = client_secret
        self.session = requests.Session()
        self._login()

    def _login(self):
        """Log in to the api by retrieving a Bearer token"""

        # drop all cookies and headers to prevent 2nd login failure due to timed out tokens
        self.session.cookies.clear()
        self.session.headers.clear()

        self.session.headers.update({
            'User-Agent': _USER_AGENT,
            'Accept': 'application/json'
        })

        payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials'
        }

        self.token = self.session.post(
            url='https://login.bol.com/token',
            data=payload
        ).json()['access_token']

        self.session.headers.update({
            'User-Agent': _USER_AGENT,
            'Accept': 'application/vnd.retailer.v10+json',
            'Content-Type': 'application/vnd.retailer.v10+json',
            'Authorization': 'Bearer ' + self.token
        })

    def _post(self, url, payload=None):
        """Performs HTTP POST with credentials, returning the body as JSON."""

        response = self.session.post(url, data=payload)
        if response.status_code == 401:
            self._login()
            response = self.session.post(url, data=payload)
        return response.json()

    def _put(self, url, payload=None):
        """Performs HTTP PUT with credentials, returning the body as JSON."""

        response = self.session.put(url, data=payload)
        if response.status_code == 401:
            self._login()
            response = self.session.put(url, data=payload)
        return response.json()

    def _get(self, url, payload=None):
        """Performs HTTP GET with credentials, returning the body as JSON."""

        response = self.session.get(url)
        if response.status_code == 401:
            self._login()
            response = self.session.get(url)
        return response.json()

    def _orders(self):
        """Fetch the open orders."""

        return self._get(self.BASE_URL + "/orders?status=OPEN")['orders']

    def _order(self, orderId):
        """Fetch order by id."""

        uri = self.BASE_URL + "/orders/" + str(orderId)
        return self._get(uri)
        

    def _order_item_shipment(self, orderItemId, trackAndTrace, transporterCode="TNT"):
        """Push shipping info for orderItemId to bol."""

        payload = {
            "transport": {
                "transporterCode": transporterCode,
                "trackAndTrace": trackAndTrace
            }
        }
        return self._put(self.BASE_URL + "/orders/" + str(orderItemId) + "/shipment", payload=json.dumps(payload))

    def _product(self, ean):
        """Fetch product details by ean"""

        uri = self.BASE_URL + "/content/catalog-products/" + str(ean)
        return self._get(uri)
