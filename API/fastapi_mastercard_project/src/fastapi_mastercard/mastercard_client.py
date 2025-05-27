import asyncio
import requests
from requests_oauthlib import OAuth1

class MastercardClient:
    def __init__(self, consumer_key: str, private_key_path: str):
        self.consumer_key = consumer_key
        self.private_key_path = private_key_path
        self.base_url = "https://sandbox.api.mastercard.com"
        self.private_key_pem = self._load_private_key()

    def _load_private_key(self) -> str:
        with open(self.private_key_path, 'r') as key_file:
            return key_file.read()

    async def clear_online_pin_try_counter(self, card_id: str):
        url = f"{self.base_url}/processing/v1/pin-management/clear-online-pin-try-counter"
        payload = {"cardId": card_id}

        oauth = OAuth1(
            client_key=self.consumer_key,
            rsa_key=self.private_key_pem,
            signature_method='RSA-SHA1',
            signature_type='auth_header'
        )

        def send_sync_request():
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, json=payload, headers=headers, auth=oauth)
            response.raise_for_status()
            return response.json()

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, send_sync_request)
