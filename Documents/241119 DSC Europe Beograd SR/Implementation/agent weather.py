import spade
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template
import random


class WeatherStationAgent(Agent):
    class SendWeatherUpdateBehaviour(OneShotBehaviour):
        async def run(self):
            temperature = random.uniform(-10, 40)
            msg = Message(to="weather_app@localhost")
            msg.set_metadata("performative", "inform")
            msg.body = f"Current temperature: {temperature:.1f}°C"

            await self.send(msg)
            print(f"Weather update sent: {msg.body}")

            await self.agent.stop()

    async def setup(self):
        behaviour = self.SendWeatherUpdateBehaviour()
        self.add_behaviour(behaviour)


class WeatherAppAgent(Agent):
    class ReceiveWeatherUpdateBehaviour(OneShotBehaviour):
        async def run(self):
            print("Waiting for weather update...")
            msg = await self.receive(timeout=10)
            if msg:
                print(f"Weather update received: {msg.body}")
            else:
                print("No weather update received after 10 seconds.")

            await self.agent.stop()

    async def setup(self):
        behaviour = self.ReceiveWeatherUpdateBehaviour()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(behaviour, template)


async def main():
    weather_app = WeatherAppAgent("weather_app@localhost", "password")
    await weather_app.start()

    weather_station = WeatherStationAgent("weather_station@localhost", "password")
    await weather_station.start()

    await spade.wait_until_finished(weather_app)
    print("Agents finished")


if __name__ == "__main__":
    spade.run(main())
