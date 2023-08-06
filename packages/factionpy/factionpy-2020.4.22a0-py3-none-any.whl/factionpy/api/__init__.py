import jwt
import requests
from gql import Client
from gql.transport.requests import RequestsHTTPTransport

from factionpy.config import get_config_value


def request_api_key(role, secret=get_config_value("FACTION_SERVICE_SECRET"), api_endpoint=get_config_value("API_ENDPOINT")):
    auth_url = api_endpoint + "/auth/service/"
    key = jwt.encode({"service_name": get_config_value("SERVICE_NAME"), "role": role}, secret, algorithm="HS256")
    r = requests.get(auth_url, headers={'X-Faction-Service-Auth': key})
    if r.status_code == 200:
        return r.json()['api_key']


def create_client(api_key, api_endpoint=get_config_value("API_ENDPOINT")):
    api_transport = RequestsHTTPTransport(
        url=api_endpoint,
        use_json=True,
        headers={
            "Content-type": "application/json",
            "X-API-Key": api_key
        },
        verify=False
    )

    client = Client(
        retries=3,
        transport=api_transport,
        fetch_schema_from_transport=True,
    )

    return client

