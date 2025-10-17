from google.cloud import geminidataanalytics

data_agent_client = geminidataanalytics.DataAgentServiceClient()
data_chat_client = geminidataanalytics.DataChatServiceClient()

# Billing project
billing_project = "jal-agentframework"
location = "global"

request = geminidataanalytics.ListDataAgentsRequest(
    parent=f"projects/{billing_project}/locations/global",
)

# Make the request
page_result = data_agent_client.list_data_agents(request=request)

# Handle the response
for response in page_result:
    print(response)

