import requests
import os

PROMETHEUS_API_URL = os.environ.get(
    'PROMETHEUS_API_URL', 'http://localhost:9090/api/v1/query')


def get_prometheus_data(params):
    return requests.get(PROMETHEUS_API_URL,
                        params=params
                        )
