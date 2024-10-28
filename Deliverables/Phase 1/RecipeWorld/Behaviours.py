from spade.behaviour import *

class Register(CyclicBehaviour):

    async def on_start(self) -> None:
        print("Starting behaviour.")

    async def on_end(self) -> None:
        print("Ending behaviour.")

    async def run(self) -> None:
        print("Running the behaviour.")


class Request_service(State):

    async def on_start(self) -> None:
        print("Starting behaviour.")

    async def on_end(self) -> None:
        print("Ending behaviour.")

    async def run(self) -> None:
        print("Running the behaviour.")


class Receive_messages(CyclicBehaviour):

    async def on_start(self) -> None:
        print("Starting behaviour.")

    async def on_end(self) -> None:
        print("Ending behaviour.")

    async def run(self) -> None:
        print("Running the behaviour.")


class Send_message(CyclicBehaviour):

    async def on_start(self) -> None:
        print("Starting behaviour.")

    async def on_end(self) -> None:
        print("Ending behaviour.")

    async def run(self) -> None:
        print("Running the behaviour.")


class Consume_service(State):

    async def on_start(self) -> None:
        print("Starting behaviour.")

    async def on_end(self) -> None:
        print("Ending behaviour.")

    async def run(self) -> None:
        print("Running the behaviour.")


class Find_service(State):

    async def on_start(self) -> None:
        print("Starting behaviour.")

    async def on_end(self) -> None:
        print("Ending behaviour.")

    async def run(self) -> None:
        print("Running the behaviour.")


class Produce_part(FSMBehaviour):

    async def on_start(self) -> None:
        print("Starting behaviour.")

    async def on_end(self) -> None:
        print("Ending behaviour.")

    async def state_setup(self):
        self.add_state(name='Find_service', state=Find_service(), initial=True)
        self.add_state(name='Request_service', state=Request_service())
        self.add_state(name='Consume_service', state=Consume_service())
        self.add_transition(source='Find_service', dest='Request_service')
        self.add_transition(source='Request_service', dest='Consume_service')
        self.add_transition(source='Consume_service', dest='Find_service')