## Create a Function App

https://portal.azure.com/?quickstart=true#blade/HubsExtension/BrowseResource/resourceType/Microsoft.Web%2Fsites/kind/functionapp

## Create a new function

```bash
# .NET Core SDK is required
npm install -g azure-functions-core-tools
func function new -l python -t "HTTP trigger" -n hello_bolt
```

## Local Development

```bash
# Python 3.6 or 3.7 required

# Single Workspace App
export SLACK_SIGNING_SECRET=xxx
export SLACK_BOT_TOKEN=xoxb-xxx
func start --port 3000
# use ngrok or similar to have a public enndpoint

# OAuth App
export SLACK_SIGNING_SECRET=xxx
export SLACK_CLIENT_ID=111.222
export SLACK_CLIENT_SECRET=xxx
export SLACK_SCOPES=app_mentions:read,chat:write.public,chat:write
func start --port 3000
# use ngrok or similar to have a public enndpoint
```

## Deployment

```bash
brew install azure-cli

# Set env variables
az functionapp config appsettings set --name <FUNCTION_APP_NAME> \
  --resource-group <RESOURCE_GROUP_NAME> \
  --settings SLACK_BOT_TOKEN=xxx
az functionapp config appsettings set --name <FUNCTION_APP_NAME> \
  --resource-group <RESOURCE_GROUP_NAME> \
  --settings SLACK_SIGNING_SECRET=xxx

# Deploy a function
func azure functionapp publish <YOUR_APP_NAME>
```
