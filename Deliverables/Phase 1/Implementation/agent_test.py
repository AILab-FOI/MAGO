import spade
from spade.agent import Agent


class Test_agent(Agent):
    async def setup(self):
        print("New agent running.")


async def main():
    agent = Test_agent("agent@localhost", "tajna")
    await agent.start()


spade.run(main())
