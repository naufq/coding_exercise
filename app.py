"""
Test 1b
"""
from flask import Flask
import os
import json
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

app = Flask(__name__)


ES_INDEX_NAME = "status-test"
ES_CONN = Elasticsearch(hosts=['127.0.0.1'], port="9200", timeout=5)

index_mapping = {
        "mappings": {
            "properties": {
                "@timestamp": {
                    "type": "date",
                    "format": "yyyy-MM-dd HH:mm:ss"
                }
            }
        }
    }


def bulk_gen(payloads: list):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    for index, payload in enumerate(payloads):
        yield {
            "_index": ES_INDEX_NAME,
            "_id": index,
            "@timestamp": timestamp,
            "data": payload
        }


@app.route('/add', methods=['POST'])
def add():
    current_status = []
    for file in os.listdir(os.path.join(os.getcwd(), 'json_payloads')):
        with open(os.path.join(os.getcwd(), 'json_payloads', file)) as f:
            current_status.append(json.load(f))
    ES_CONN.indices.create(index=ES_INDEX_NAME, body=index_mapping, ignore=400)
    bulk(ES_CONN, bulk_gen(payloads=current_status))
    return {
        "success": True,
        "msg": "Service status stored"
    }, 201


@app.route('/healthcheck', methods=['GET'])
def check():
    is_down = False
    res = ES_CONN.search(index=ES_INDEX_NAME,
                         body={
                             "query": {
                                 "match_all": {}
                             }
                         })
    # assume es always returns at least 1 res
    for result in res['hits']['hits']:
        if result['_source']['data']['service_status'].strip().lower() == "down":
            is_down = True
            break
    return {
        "success": True,
        "app_status": "DOWN" if is_down else "UP"
    }, 200


@app.route('/healthcheck/<string:service_name>', methods=['GET'])
def check_specific(service_name):
    service_list = ['rabbitmq-server', 'postgresql', 'apache2']
    if service_name in service_list:
        is_down = False
        # assume es always returns 1 res
        res = ES_CONN.search(index=ES_INDEX_NAME,
                             body={
                                 "query": {
                                     "bool": {
                                         "must": [
                                             {"match": {"data.service_name": service_name.strip().lower()}}
                                         ]
                                     }
                                 }
                             })
        return {
                   "success": True,
                   "service_status": res['hits']['hits'][0]['_source']['data']['service_status']
               }, 200
    else:
        return {
            "msg": f"service name needs to be one of {service_list}",
            "success": False
        }, 400


if __name__ == '__main__':
    app.run(ssl_context='adhoc')
