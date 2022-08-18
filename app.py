import flask
from flask import Flask, request
from flask_cors import CORS
from typing import Dict
import requests
import Constants as const
from BatchStates import BatchStates
from Database import Database

app = Flask(__name__)
CORS(app)
bStates = BatchStates()
db = Database()


def triggerUrl(api_url: str, method: str, payload: Dict = None) -> None:
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


@app.route('/healthcheck', methods=['GET'])
def healthCheck() -> str:
    return 'I am okay'


@app.route('/api/orchestrator/run-schedule', methods=['GET'])
def runPeriodicProcess() -> str:
    print('Schedule run triggered')
    event = (const.ServiceNames.aws_event_bridge.name, const.EventType.event_request.name,
             'None', const.EventStatus.event_success.name)
    db.recordEvent(event)
    try:
        if bStates.getPendingBatchCount() > 0:
            print("Schedule process is still running, can not start new run")
            raise ValueError(f'Request Failed: Schedule process is still running, can not start new run')
        bStates.resetStates()
        triggerUrl(const.FILTERING_SERVICE_URL, 'POST')
        event = (const.ServiceNames.filtering_service.name, const.EventType.event_request.name,
                 'None', const.EventStatus.event_success.name)
        db.recordEvent(event)
        return "Success"
    except Exception as ex:
        event = (const.ServiceNames.orchestrator_service.name, const.EventType.event_request.name,
                 ex, const.EventStatus.event_failure.name)
        db.recordEvent(event)
        flask.abort(404, description=ex)


@app.route('/api/orchestrator/filter-process-response', methods=['POST'])
def filterProcessResponce() -> str:
    print('Received response for Filtering service')
    status = request.args.get('status', 'failure')
    # batch_ids = request.args.get('batch_ids', '')
    exceptions = request.args.get('exception', 'None')
    # batch_ids = eval(batch_ids)
    batch_ids = db.getUniqueBatchIds()
    try:
        if len(batch_ids) < 1:
            exceptions = 'Error: No batch-ids received to process'
            raise ValueError(exceptions)
        if status == 'success':
            event = (const.ServiceNames.filtering_service.name, const.EventType.event_response.name,
                     'None', const.EventStatus.event_success.name)
            db.recordEvent(event)
            bStates.initStates(batch_ids)
            for id in batch_ids:
                api_url = const.MATCHING_SERVICE_URL
                triggerUrl(api_url, 'POST', {'batch_id': id})
                event = (const.ServiceNames.matching_service.name,
                         f'{const.EventType.event_request.name}-{id}',
                         'None',
                         const.EventStatus.event_success.name)
                db.recordEvent(event)
        else:
            raise ValueError(f'Request Failed')
        return "Success"
    except Exception as ex:
        event = (const.ServiceNames.filtering_service.name, const.EventType.event_response.name,
                 exceptions, const.EventStatus.event_failure.name)
        db.recordEvent(event)
        flask.abort(404, description=ex)


@app.route('/api/orchestrator/matching-process-response', methods=['POST'])
def matchingProcessResponse() -> str:
    print('Received response for matching service')
    status = request.args.get('status', 'failure')
    batch_id = request.args.get('batch_id', '')
    exceptions = request.args.get('exception', 'None')
    try:
        if status == 'success':
            event = (const.ServiceNames.matching_service.name, f'{const.EventType.event_response.name}-{batch_id}',
                     'None', const.EventStatus.event_success.name)
            db.recordEvent(event)
            if batch_id:
                api_url = const.POST_PROCESS_URL
                triggerUrl(api_url, 'POST', {'batch_id': batch_id})
                event = (const.ServiceNames.post_process_service.name, f'{const.EventType.event_request.name}-{batch_id}',
                         'None', const.EventStatus.event_success.name)
                db.recordEvent(event)
            else:
                raise ValueError(f'Request Failed: Invalid Batch-id received')
        else:
            raise ValueError(f'Request Failed: Matching Process Failed')
        return 'Success'
    except Exception as ex:
        event = (const.ServiceNames.matching_service.name, f'{const.EventType.event_response.name}-{batch_id}',
                 exceptions, const.EventStatus.event_failure.name)
        db.recordEvent(event)
        flask.abort(404, description=ex)


@app.route('/api/orchestrator/post-process-response', methods=['POST'])
def postProcessResponse() -> str:
    print('Received response for post process service')
    status = request.args.get('status', 'failure')
    batch_id = request.args.get('batch_id', '')
    exceptions = request.args.get('exception', 'None')
    print(status, batch_id, exceptions)
    try:
        if status == 'success':
            event = (const.ServiceNames.post_process_service.name, f'{const.EventType.event_response.name}-{batch_id}',
                     'None', const.EventStatus.event_success.name)
            db.recordEvent(event)

            if batch_id:
                bStates.setBatchState(batch_id, True)
                if bStates.getPendingBatchCount() <= 0:
                    event = (const.ServiceNames.post_post_process_service.name, const.EventType.event_request.name,
                             'None', const.EventStatus.event_success.name)
                    db.recordEvent(event)
                    triggerUrl(const.POST_POST_SERVICE_URL, 'POST')
            else:
                raise ValueError(f'Request Failed: Invalid Batch-id received')
        else:
            raise ValueError(f'Request Failed')
        return 'Success'
    except Exception as ex:
        event = (const.ServiceNames.post_process_service.name, f'{const.EventType.event_response.name}-{batch_id}',
                 exceptions, const.EventStatus.event_failure.name)
        db.recordEvent(event)
        flask.abort(404, description=ex)


@app.route('/api/orchestrator/post-post-process-response', methods=['POST'])
def postPostProcessResponse() -> str:
    print('Received response for post post process service')
    status = request.args.get('status', 'failure')
    exceptions = request.args.get('exception', 'None')
    try:
        if status == 'success':
            event = (const.ServiceNames.post_post_process_service.name, const.EventType.event_response.name,
                     'None', const.EventStatus.event_success.name)
            db.recordEvent(event)
            print('Post Post process completed successfully')
            bStates.resetStates()
        else:
            raise ValueError(f'Request Failed: {exceptions}')
        print('Schedule process completed successfully')
        return 'Success'
    except Exception as ex:
        event = (const.ServiceNames.post_post_process_service.name, const.EventType.event_response.name,
                 exceptions, const.EventStatus.event_failure.name)
        db.recordEvent(event)
        flask.abort(404, description=ex)


# This is only for testing
@app.route('/mock/<event>', methods=['GET', 'POST'])
@app.route('/mock/<event>/<id>', methods=['GET', 'POST'])
def mockApi(event: str, id=None) -> str:
    print(event)
    if event == 'filter-service':
        ack = {"status": "success", "batchids": "[1,2,3,4,5]", "exception": "None"}
    elif event == 'matching-service' or event == "post-processing-service":
        ack = {"status": "success", "batchid": {id}, "exception": "None"}
    else:
        ack = {"status": "success", "exception": "None"}
    params = {"ack": ack}
    api_url = f'{const.BASE_URL}/mock/{event}'
    print(api_url)
    print(params)
    requests.post(url=api_url, data=params, timeout=5)
    return "Success"


def runService() -> None:
    """
    Entry-level for the service invocation
    :return: None
    """
    app.debug = True
    app.run(host=const.WEB_IP_ADR, port=const.PORT, processes=True)


if __name__ == '__main__':
    runService()
