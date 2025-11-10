#based on: https://cloud.google.com/blog/products/ai-machine-learning/build-multi-agentic-systems-using-google-adk?e=48754805
#You can read more here: https://google.github.io/adk-docs/agents/

from google.adk.agents import LlmAgent

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

# Root agent acting as a Trip Planner coordinator
root_agent = LlmAgent(
    model='gemini-2.0-flash',
    name="TripPlanner",
    instruction=f"""
    Acts as a comprehensive trip planner.
    - Use the FlightAgent to find and book flights
    - Use the HotelAgent to find and book accommodation
    - Use the SightSeeingAgent to find information on places to visit
    ...
    """,
    sub_agents=[flight_agent, hotel_agent, sightseeing_agent] # The coordinator manages these sub-agents
)
