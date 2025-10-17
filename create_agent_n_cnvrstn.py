import sys
from google.cloud import geminidataanalytics

data_agent_client = geminidataanalytics.DataAgentServiceClient()
data_chat_client = geminidataanalytics.DataChatServiceClient()

# Billing project
billing_project = "jal-agentframework"

if len(sys.argv) > 1:
    data_agent_id = sys.argv[1]
else:
    print("Usage:python create_agent_n_cnvrstn.py {dataagentid}")
    sys.exit(1)

# System instructions
system_instruction = "Help the user analyze their ecomm data."

bigquery_table_reference = geminidataanalytics.BigQueryTableReference()
bigquery_table_reference.project_id = "jal-agentframework"
bigquery_table_reference.dataset_id = "thelook_ecommerce"
bigquery_table_reference.table_id = "orders"

bigquery_table_reference2 = geminidataanalytics.BigQueryTableReference()
bigquery_table_reference2.project_id = "jal-agentframework"
bigquery_table_reference2.dataset_id = "thelook_ecommerce"
bigquery_table_reference2.table_id = "order_items"

bigquery_table_reference3 = geminidataanalytics.BigQueryTableReference()
bigquery_table_reference3.project_id = "jal-agentframework"
bigquery_table_reference3.dataset_id = "thelook_ecommerce"
bigquery_table_reference3.table_id = "products"

bigquery_table_reference4 = geminidataanalytics.BigQueryTableReference()
bigquery_table_reference4.project_id = "jal-agentframework"
bigquery_table_reference4.dataset_id = "thelook_ecommerce"
bigquery_table_reference4.table_id = "users"


# Connect to your data source
datasource_references = geminidataanalytics.DatasourceReferences()
datasource_references.bq.table_references = [bigquery_table_reference, bigquery_table_reference2, bigquery_table_reference3, bigquery_table_reference4]

# Set up context for stateful chat
published_context = geminidataanalytics.Context()
published_context.system_instruction = system_instruction
published_context.datasource_references = datasource_references
# Optional: To enable advanced analysis with Python, include the following line:
published_context.options.analysis.python.enabled = True

## Create a data agent ##
##

data_agent = geminidataanalytics.DataAgent()
data_agent.data_analytics_agent.published_context = published_context
data_agent.name = f"projects/{billing_project}/locations/global/dataAgents/{data_agent_id}" # Optional

request = geminidataanalytics.CreateDataAgentRequest(
    parent=f"projects/{billing_project}/locations/global",
    data_agent_id=data_agent_id, # Optional
    data_agent=data_agent,
)

try:
    data_agent_client.create_data_agent(request=request)
    print("Data Agent created")
except Exception as e:
    print(f"Error creating Data Agent: {e}")

## Create a conversation ##
# Initialize request arguments
conversation_id = f"{data_agent_id}_conversation"

conversation = geminidataanalytics.Conversation()
conversation.agents = [f'projects/{billing_project}/locations/global/dataAgents/{data_agent_id}']
conversation.name = f"projects/{billing_project}/locations/global/conversations/{conversation_id}"

request = geminidataanalytics.CreateConversationRequest(
    parent=f"projects/{billing_project}/locations/global",
    conversation_id=conversation_id,
    conversation=conversation,
)

# Make the request
response = data_chat_client.create_conversation(request=request)

# Handle the response
print(response)

