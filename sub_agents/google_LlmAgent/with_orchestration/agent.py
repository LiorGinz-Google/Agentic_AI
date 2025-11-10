#Turned the specialized agents to agent tools
from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

# Flight Agent: Specializes in flight booking and information
flight_agent = LlmAgent(
    model='gemini-2.0-flash',
    name="FlightAgent",
    description="Flight booking agent",
    instruction=f"""You are a flight booking agent... You always return a valid JSON...""")

# Hotel Agent: Specializes in hotel booking and information
hotel_agent = LlmAgent(
    model='gemini-2.0-flash',
    name="HotelAgent",
    description="Hotel booking agent",
    instruction=f"""You are a hotel booking agent... You always return a valid JSON...""")

# Sightseeing Agent: Specializes in providing sightseeing recommendations
sightseeing_agent = LlmAgent(
    model='gemini-2.0-flash',
    name="SightseeingAgent",
    description="Sightseeing information agent",
    instruction=f"""You are a sightseeing information agent... You always return a valid JSON...""")

# Convert specialized agents into AgentTools
flight_tool = AgentTool(agent=flight_agent)
hotel_tool = AgentTool(agent=hotel_agent)
sightseeing_tool = AgentTool(agent=sightseeing_agent)

# Root agent now uses these agents as tools
root_agent = LlmAgent(
    model='gemini-2.0-flash',
    name="TripPlanner",
    instruction=f"""Acts as a comprehensive trip planner...
    Based on the user request, sequentially invoke the tools to gather all necessary trip details...""",
    tools=[flight_tool, hotel_tool, sightseeing_tool] # The root agent can use these tools
)

