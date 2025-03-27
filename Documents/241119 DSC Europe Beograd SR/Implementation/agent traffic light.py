import spade
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
import asyncio

STATE_GREEN = "GREEN"
STATE_YELLOW = "YELLOW"
STATE_RED = "RED"


class TrafficLightFSMBehaviour(FSMBehaviour):
    async def on_start(self):
        print(f"Traffic Light FSM starting at initial state {self.current_state}")

    async def on_end(self):
        print(f"Traffic Light FSM finished at state {self.current_state}")
        await self.agent.stop()


class GreenLightState(State):
    async def run(self):
        print("Green Light: Cars may go!")
        await asyncio.sleep(5)
        self.set_next_state(STATE_YELLOW)


class YellowLightState(State):
    async def run(self):
        print("Yellow Light: Prepare to stop!")
        await asyncio.sleep(2)
        self.set_next_state(STATE_RED)


class RedLightState(State):
    async def run(self):
        print("Red Light: Cars must stop!")
        await asyncio.sleep(5)
        self.set_next_state(STATE_GREEN)


class TrafficLightAgent(Agent):
    async def setup(self):
        fsm = TrafficLightFSMBehaviour()
        fsm.add_state(name=STATE_GREEN, state=GreenLightState(), initial=True)
        fsm.add_state(name=STATE_YELLOW, state=YellowLightState())
        fsm.add_state(name=STATE_RED, state=RedLightState())
        fsm.add_transition(source=STATE_GREEN, dest=STATE_YELLOW)
        fsm.add_transition(source=STATE_YELLOW, dest=STATE_RED)
        fsm.add_transition(source=STATE_RED, dest=STATE_GREEN)
        self.add_behaviour(fsm)


async def main():
    traffic_light = TrafficLightAgent("trafficlight@localhost", "password")
    await traffic_light.start()

    await spade.wait_until_finished(traffic_light)
    await traffic_light.stop()
    print("Traffic Light Agent finished")


if __name__ == "__main__":
    spade.run(main())
