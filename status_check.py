"""
Test 1a
"""
import os
import socket
import json
import requests
import urllib3
from datetime import datetime


ITERATION_TIME = datetime.utcnow().strftime('%Y-%m-%dT%H-%M-%S')
SAVE_DIR = f'{os.getcwd()}/json_payloads'


def clean_old():
    try:
        for file in os.scandir(os.path.join(os.getcwd(), 'json_payloads')):
            os.remove(file.path)
    except FileNotFoundError:
        pass


def service_check(services: list):
    clean_old()
    for service in services:
        write_json = {
            "service_name": service.strip().lower(),
            "service_status": "UP" if os.system(f'systemctl is-active --quiet {service}') == 0 else "DOWN",
            "host_name": socket.getfqdn()
        }
        if not os.path.exists(SAVE_DIR):
            os.makedirs(SAVE_DIR)
        with open(os.path.join(SAVE_DIR, f'{service}-status-{ITERATION_TIME}.json'), 'w+') as j_file:
            json.dump(write_json, j_file)


if __name__ == "__main__":
    service_check(services=["apache2", "rabbitmq-server", "postgresql"])
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    print(requests.post(url='https://localhost:5000/add', verify=False).text)
