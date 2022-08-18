# EventOrchestrationService
Description: 
Event Orchestration is a service which works like Linux crontab but for specific purpose.

Requirement:
- I was working on system with no.of microservices. Every service communicate other service over the REST api. To make the whole solution working there is one url needs to trigglre every day. We were using a Linux crontab to trigger the URL.
- But this became a single point failure and when I move the system to AWS cloud, I had a problem of using crontab as I need to have a separate EC2.

Solution:
- To over come the problem, I designed and implemented this Python module.
- Instread of trigger one url to run the whole solution in microservices, I de-coupled the services and made Orchestrator as a main point of contact for any service.
- This Orchestrator maintains the states of all the services and call the respective over the REST API.
