
import sys

from google.cloud import geminidataanalytics

data_agent_client = geminidataanalytics.DataAgentServiceClient()
data_chat_client = geminidataanalytics.DataChatServiceClient()

# Billing project
billing_project = "jal-agentframework"
location = "global"

if len(sys.argv) > 1:
    data_agent_id = sys.argv[1]
else:
    print("Usage:python delete_data_agent.py {dataagentid}")
    sys.exit(1)

request = geminidataanalytics.DeleteDataAgentRequest(
    name=f"projects/{billing_project}/locations/global/dataAgents/{data_agent_id}",
)

try:
    # Make the request
    data_agent_client.delete_data_agent(request=request)
    print("Data Agent Deleted")
except Exception as e:
    print(f"Error deleting Data Agent: {e}")
