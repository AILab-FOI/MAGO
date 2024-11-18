import spade
from spade.behaviour import CyclicBehaviour
from spade.agent import Agent
from asyncio import sleep


class CoffeeMachineAgent(Agent):
    class MonitorCoffeeBehaviour(CyclicBehaviour):
        async def dispense_coffee(self):
            await sleep(1)
            self.coffee_level -= 1

        async def refill_coffee(self):
            self.coffee_level = 10
            print("Coffee refilled to 10 cups.")
            self.kill()
        
        async def on_start(self):
            print("Starting coffee monitoring . . .")
            self.coffee_level = 10

        async def run(self):
            print(f"Current coffee level: {self.coffee_level} cups")
            
            if self.coffee_level <= 2:
                print("Low coffee level detected! Refilling coffee . . .")
                await self.refill_coffee()
            else:
                print("Sufficient coffee level. Dispensing a cup . . .")
                await self.dispense_coffee()

    async def setup(self):
        print("Coffee Machine Agent starting . . .")
        behaviour = self.MonitorCoffeeBehaviour()
        self.add_behaviour(behaviour)


async def main():
    coffee_machine = CoffeeMachineAgent("coffeemachine@localhost", "password")
    await coffee_machine.start()


if __name__ == "__main__":
    spade.run(main())
