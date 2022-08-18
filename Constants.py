from enum import Enum, auto
# Define all constants here

WEB_IP_ADR = '0.0.0.0'
PORT = 4040
DEBUG = True
# Service APIs
FILTERING_SERVICE_API = f'/api/match_employee_to_employer/batch_run_filter_service'
MATCHING_SERVICE_API = f'/api/match_employee_to_employer/batch_run_matching_service'
POST_PROCESS_API = f'/api/match_employee_to_employer/batch_run_post_processing_service'
POST_POST_SERVICE_API = f'/api/post-post-processing-service'

# Response APIs
EB_SERVICE_RESPONSE_API = '/api/orchestrator/run-schedule'
FILTERING_SERVICE_RESPONSE_API = '/api/orchestrator/filter-process-response'
MATCHING_SERVICE_RESPONSE_API = f'/api/orchestrator/matching-process-response'
POST_PROCESS_RESPONSE_API = f'/api/orchestrator/post-process-response'
POST_POST_SERVICE_RESPONSE_API = f'/api/orchestrator/post-post-process-response'

if DEBUG:
    BASE_URL = 'http://localhost:4040'
    MOCK_BASE_URL = 'http://localhost:4041'
    FILTERING_SERVICE_URL = f'{MOCK_BASE_URL}{FILTERING_SERVICE_API}'
    MATCHING_SERVICE_URL = f'{MOCK_BASE_URL}{MATCHING_SERVICE_API}'
    POST_PROCESS_URL = f'{MOCK_BASE_URL}{POST_PROCESS_API}'
    POST_POST_SERVICE_URL = f'{MOCK_BASE_URL}{POST_POST_SERVICE_API}'
else:
    BASE_URL = 'https://services.compaira.com'
    FILTERING_SERVICE_URL = f'{BASE_URL}:5050{FILTERING_SERVICE_API}'
    MATCHING_SERVICE_URL = f'{BASE_URL}:5000{MATCHING_SERVICE_API}'
    POST_PROCESS_URL = f'{BASE_URL}:7070{POST_PROCESS_API}'
    POST_POST_SERVICE_URL = 'https://jobseeker.compaira.com/Createcache/startprocess'


class ServiceNames(Enum):
    aws_event_bridge = auto(),
    orchestrator_service = auto(),
    filtering_service = auto(),
    matching_service = auto(),
    post_process_service = auto(),
    post_post_process_service = auto(),


class EventType(Enum):
    event_request = auto(),
    event_response = auto(),


class EventStatus(Enum):
    event_success = auto(),
    event_failure = auto(),

