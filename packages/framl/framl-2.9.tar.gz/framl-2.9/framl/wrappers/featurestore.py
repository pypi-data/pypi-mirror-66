import json
import subprocess
import os

import requests
from framl.config_cli import ConfigFraml


class FeatureStore:
    HOST = os.getenv('FEATURE_STORE_HOST') or "https://feature-store-api-rzhg37iauq-ez.a.run.app"

    @staticmethod
    def _get_bearer() -> str:
        env = ConfigFraml.get_env()
        if env.lower() != "production":
            print("/!\\ using local identity token")
            result = subprocess.run(["gcloud", "auth", "print-identity-token"], stdout=subprocess.PIPE)
            jwt = result.stdout.decode('utf-8').replace("\n", "")
            return jwt

        metadata_server_token_url = 'http://metadata/computeMetadata/v1/instance/service-accounts/default/identity?audience='

        token_request_url = metadata_server_token_url + FeatureStore.HOST
        token_request_headers = {'Metadata-Flavor': 'Google'}

        # Fetch the token
        token_response = requests.get(token_request_url, headers=token_request_headers)
        jwt = token_response.content.decode("utf-8")

        return jwt

    @staticmethod
    def get(view: str, id: str) -> requests.Response:
        # Provide the token in the request to the receiving service
        receiving_service_headers = {
            'Authorization': f'bearer {FeatureStore._get_bearer()}',
            'Content-type':  'application/json; charset=utf-8'
        }

        # sending the request. Please make sure the payload is a valid json string
        r = requests.get(url=f"{FeatureStore.HOST}/kinds/{view}/{id}",
                                headers=receiving_service_headers)
        r.encoding = 'utf-8'
        return r

    @staticmethod
    def get_bulk(view: str, ids: list) -> requests.Response:
        # Provide the token in the request to the receiving service
        receiving_service_headers = {
            'Authorization': f'bearer {FeatureStore._get_bearer()}',
            'Content-type':  'application/json; charset=utf-8'
        }

        # sending the request. Please make sure the payload is a valid json string
        r = requests.post(url=f"{FeatureStore.HOST}/kinds/{view}",
                                data=json.dumps({"ids": ids}),
                                headers=receiving_service_headers)
        r.encoding = 'utf-8'
        return r
