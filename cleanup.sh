#!/bin/bash
sam delete --no-prompts --stack-name project-flight-event-generator
sam delete --no-prompts --stack-name project-desk-agent
sam delete --no-prompts --stack-name project-bag-api
sam delete --no-prompts --stack-name project-bag-handler-api
sam delete --no-prompts --stack-name project-ddb
