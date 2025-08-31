#Agent => Class for instant inisiasi Agent
#Runner => reAct Feadback event loop 

from agents import Agent, Runner, function_tool
from dotenv import load_dotenv

@function_tool
def get_weather(city: str) -> str:
    return f"weather of {city} is sunny"

load_dotenv()

emojis_agent = Agent(
    name="Emojis Agent",
    instructions="You are fun assistant, with a sense of humor, and always having extra extra emojis in your answer",
    model="gpt-4.1",
)

haiku_agent = Agent(
    name="Haiku Agent",
    instructions="You are haiku assistant, you always reply in haiku's form!",
    model="gpt-4.1",
    tools=[get_weather]
)

triage_agent = Agent(
    name="Triage Agent",
    instructions="""
        You are Triage Agent, that decide to handsoff the conversation based on user query.

        # RULES :
        - If user asking to talk to emojis agent, then hands off the conversation to Emojis Agent.
        - if user asking about fun activity, then hands off the conversation to Emojis Agent.

        - If user asking to talk to haiku agent, then hands off the conversation to Haiku Agent.
        - if user asking about haiku, then hands off the conversation to Haiku Agent.
        - if user asking about weather, then hands off the conversation to Haiku Agent.
        """,
    model="gpt-4.1",
    handoffs=[haiku_agent, emojis_agent]
)

async def main():
    messages = []

    while True:
        user_input = input("User: ")
        messages.append({"role": "user", "content": user_input})
        runner = await Runner.run(starting_agent=triage_agent, input=messages)
        messages = runner.to_input_list()

        print(runner.last_agent.name)
        print(runner.final_output)
        print("===" * 20)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())