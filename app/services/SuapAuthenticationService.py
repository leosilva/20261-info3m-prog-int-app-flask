import json
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from app import app


class SuapAuthenticationService:
    @staticmethod
    def authorization_url(state, redirect_uri):
        params = urlencode({
            'response_type': 'code',
            'client_id': app.config['SUAP_CLIENT_ID'],
            'redirect_uri': redirect_uri,
            'state': state,
        })
        return f"{app.config['SUAP_URL']}/o/authorize/?{params}"

    @staticmethod
    def exchange_code(code, redirect_uri):
        data = urlencode({
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri,
            'client_id': app.config['SUAP_CLIENT_ID'],
            'client_secret': app.config['SUAP_CLIENT_SECRET'],
        }).encode()
        try:
            with urlopen(Request(
                f"{app.config['SUAP_URL']}/o/token/",
                data=data,
                headers={'Content-Type': 'application/x-www-form-urlencoded'},
            )) as response:
                return json.load(response)
        except URLError:
            return None

    @staticmethod
    def meus_dados(access_token):
        request = Request(
            f"{app.config['SUAP_URL']}/api/rh/meus-dados/",
            headers={
                'Authorization': f'Bearer {access_token}',
                'Accept': 'application/json',
            },
        )
        try:
            with urlopen(request) as response:
                return json.load(response)
        except URLError:
            return None
