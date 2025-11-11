#Source: https://cloud.google.com/blog/products/ai-machine-learning/build-multi-agentic-systems-using-google-adk?e=48754805

from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from google.adk.agents import SequentialAgent, ParallelAgent

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
#flight_tool = AgentTool(agent=flight_agent)
#hotel_tool = AgentTool(agent=hotel_agent)
#sightseeing_tool = AgentTool(agent=sightseeing_agent)

# 1. Create a parallel agent for concurrent tasks
plan_parallel = ParallelAgent(
    name="ParallelTripPlanner",
    sub_agents=[flight_agent, hotel_agent], # These run in parallel
)

# 2. Create a summary agent to gather results
trip_summary = LlmAgent(
    name="TripSummaryAgent",
    instruction="Summarize the trip details from the flight, hotel, and sightseeing agents...",
    output_key="trip_summary")

# 3. Create a sequential agent to orchestrate the full workflow
root_agent = SequentialAgent(
    name="PlanTripWorkflow",
    # Run tasks in a specific order, including the parallel step
    sub_agents=[sightseeing_agent, plan_parallel, trip_summary])
