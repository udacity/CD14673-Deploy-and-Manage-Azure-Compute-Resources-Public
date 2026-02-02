#/bin/bash

#Ensure a clean dist directory
rm -rf ./dist
mkdir -p ./dist
mkdir -p ./state

# Build and deploy the DDB table
echo "Deploying the DDB Table Stack"
sam deploy -t ./infrastructure_templates/DDB.yaml --stack-name project-ddb --resolve-s3
sam list stack-outputs --stack-name project-ddb --output json > ./state/project-ddb.json
ddb_table=$(./read_stack_outputs ./state/project-ddb.json DDBTableName)

# Build and deploy the Bag API
echo "Deploying the Bag API Stack"
sam build -t ./infrastructure_templates/Bag_API.yaml  -s python_apps/bag_api -b ./dist/bag_api
sam deploy -t ./dist/bag_api/template.yaml --stack-name project-bag-api \
  --resolve-s3 --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND \
  --parameter-overrides ProjectBagCheckTable=${ddb_table}
sam list stack-outputs --stack-name project-bag-api --output json > ./state/project-bag-api.json
api_endpoint=$(./read_stack_outputs ./state/project-bag-api.json APIEndpoint)

# Build and deploy the Bag Handler API
echo "Deploying the Bag Handler API"
sam build -t ./infrastructure_templates/Bag_Handler_API.yaml  -s python_apps/bag_handler_api -b ./dist/bag_handler_api
sam deploy -t ./dist/bag_handler_api/template.yaml --stack-name project-bag-handler-api \
  --resolve-s3 --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND
sam list stack-outputs --stack-name project-bag-handler-api --output json > ./state/project-bag-handler-api.json
bag_handler_api_endpoint=$(./read_stack_outputs ./state/project-bag-handler-api.json APIEndpoint)

# Build and deploy the Desk Agent
# Contains the scheduled function, API Gateway, and integration to push bag data to a SQS Queue
echo "Deploying the Desk Agent Stack"
sam build -t infrastructure_templates/Desk_Agent.yaml  -s python_apps/desk_agent -b ./dist/desk_agent
sam deploy -t ./dist/desk_agent/template.yaml --stack-name project-desk-agent \
    --resolve-s3 --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND
sam list stack-outputs --stack-name project-desk-agent --output json > ./state/project-desk-agent.json
desk_agent_queue_arn=$(./read_stack_outputs ./state/project-desk-agent.json SQSQueueArn)


# Build and deploy the Flight Event Generator
echo "Deploying the Flight Event Generator Stack"
sam build -t infrastructure_templates/Flight_Event_Generator.yaml  -s python_apps/flight_event_generator -b ./dist/flight_event_generator
sam deploy -t ./dist/flight_event_generator/template.yaml --stack-name project-flight-event-generator \
    --resolve-s3 --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND 
sam list stack-outputs --stack-name project-flight-event-generator --output json > ./state/project-flight-event-generator.json

# Get the output of the generated SNS Topic
flight_event_topic_arn=$(./read_stack_outputs ./state/project-flight-event-generator.json SNSTopicArn)

echo " "
echo "****************"
echo " Deployment complete. Take note of these outputs:"
echo " DynamoDB Table: ${ddb_table}"
echo " Desk Agent Queue: ${desk_agent_queue_arn}"
echo " Bag API Endpoint: ${api_endpoint}"
echo " Bag Handler API Endpoint: ${bag_handler_api_endpoint}"
echo " Flight Events SNS Topic: ${flight_event_topic_arn}"
echo " "