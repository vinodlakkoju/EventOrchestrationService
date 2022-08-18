from flask import Flask, request
from flask_cors import CORS
import requests
import Orchestrator.Constants as const
from typing import Dict

app = Flask(__name__)
CORS(app)


def triggerUrl(api_url: str, method: str, payload: Dict) -> None:
    print(f'Firing URL: {api_url}')
    if api_url:
        try:
            if method == 'GET':
                requests.get(url=api_url, params=payload, timeout=360)
            if method == 'POST':
                requests.post(url=api_url, params=payload, timeout=360)
        except Exception as ex:
            print(ex)
            pass


@app.route(const.FILTERING_SERVICE_API, methods=['POST'])
def filterService():
    ack = {"status": "success", "batch_ids": "[1,2,3,4,5]", "exception": "None"}
    api_url = f'{const.BASE_URL}{const.FILTERING_SERVICE_RESPONSE_API}'
    triggerUrl(api_url, 'POST', ack)
    return 'success'


@app.route(const.MATCHING_SERVICE_API, methods=['POST'])
def matchingService():
    batch_id = request.args.get('batch_id', '')
    ack = {"status": "success", "batch_id": batch_id, "exception": "None"}
    api_url = f'{const.BASE_URL}{const.MATCHING_SERVICE_RESPONSE_API}'
    triggerUrl(api_url, 'POST', ack)
    return 'success'


@app.route(const.POST_PROCESS_API, methods=['POST'])
def postProcessService():
    batch_id = request.args.get('batch_id', '')
    ack = {"status": "success", "batch_id": batch_id, "exception": "None"}
    api_url = f'{const.BASE_URL}{const.POST_PROCESS_RESPONSE_API}'
    triggerUrl(api_url, 'POST', ack)
    return 'success'


@app.route(const.POST_POST_SERVICE_API, methods=['POST'])
def postPostProcessService():
    ack = {"status": "success", "exception": "None"}
    api_url = f'{const.BASE_URL}{const.POST_POST_SERVICE_RESPONSE_API}'
    triggerUrl(api_url, 'POST', ack)
    return 'success'


def runService() -> None:
    """
    Entry-level for the service invocation
    :return: None
    """
    app.debug = True
    app.run(host=const.WEB_IP_ADR, port=4041, processes=True)


if __name__ == '__main__':
    runService()
