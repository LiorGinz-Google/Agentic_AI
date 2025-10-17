
import sys
from google.cloud import geminidataanalytics

data_agent_client = geminidataanalytics.DataAgentServiceClient()
data_chat_client = geminidataanalytics.DataChatServiceClient()

# Billing project
billing_project = "jal-agentframework"
location = "global"

# Create a request that contains a single user message (your question)
if len(sys.argv) > 2:
  data_agent_id  = sys.argv[1]
  question = sys.argv[2]
else:
  print("Usage: ask_data_agent.py {dataagent_id} {question}")
  sys.exit(1)

messages = [geminidataanalytics.Message()]
messages[0].user_message.text = question

conversation_id = f"{data_agent_id}_conversation"

# Create a conversation_reference
conversation_reference = geminidataanalytics.ConversationReference()
conversation_reference.conversation = f"projects/{billing_project}/locations/global/conversations/{conversation_id}"
conversation_reference.data_agent_context.data_agent = f"projects/{billing_project}/locations/global/dataAgents/{data_agent_id}"
# conversation_reference.data_agent_context.credentials = credentials

# Form the request
request = geminidataanalytics.ChatRequest(
    parent = f"projects/{billing_project}/locations/global",
    messages = messages,
    conversation_reference = conversation_reference
)

# Make the request
stream = data_chat_client.chat(request=request)

# Handle the response
for response in stream:
    print(response)
