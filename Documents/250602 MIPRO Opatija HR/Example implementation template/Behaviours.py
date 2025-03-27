from spade.behaviour import *


class Survey(State):

    async def on_start(self):
        print("Starting behaviour.")

    async def on_end(self):
        print("Ending behaviour.")

    async def run(self):
        print("Running the behaviour.")


class AssessTasks(State):

    async def on_start(self):
        print("Starting behaviour.")

    async def on_end(self):
        print("Ending behaviour.")

    async def run(self):
        print("Running the behaviour.")


class Idle(State):

    async def on_start(self):
        print("Starting behaviour.")

    async def on_end(self):
        print("Ending behaviour.")

    async def run(self):
        print("Running the behaviour.")


class DecideOnTask(State):

    async def on_start(self):
        print("Starting behaviour.")

    async def on_end(self):
        print("Ending behaviour.")

    async def run(self):
        print("Running the behaviour.")


class Task_planning_behaviour(FSMBehaviour):

    async def on_start(self):
        print("Starting behaviour.")

    async def on_end(self):
        print("Ending behaviour.")

    async def state_setup(self):
        self.add_state(name="ImplementTask", state=ImplementTask())
        self.add_state(name="AssessTasks", state=AssessTasks(), initial=True)
        self.add_state(name="DecideOnTask", state=DecideOnTask())
        self.add_transition(source="AssessTasks", dest="DecideOnTask")
        self.add_transition(source="DecideOnTask", dest="ImplementTask")


class Return(State):

    async def on_start(self):
        print("Starting behaviour.")

    async def on_end(self):
        print("Ending behaviour.")

    async def run(self):
        print("Running the behaviour.")


class ImplementTask(State):

    async def on_start(self):
        print("Starting behaviour.")

    async def on_end(self):
        print("Ending behaviour.")

    async def run(self):
        print("Running the behaviour.")


class Navigation_behaviour(FSMBehaviour):

    async def on_start(self):
        print("Starting behaviour.")

    async def on_end(self):
        print("Ending behaviour.")

    async def state_setup(self):
        self.add_state(name="Survey", state=Survey())
        self.add_state(name="Idle", state=Idle(), initial=True)
        self.add_state(name="Return", state=Return())
        self.add_transition(source="Idle", dest="Survey")
        self.add_transition(source="Survey", dest="Return")


class Aerial_survey_behaviour(OneShotBehaviour):

    async def on_start(self):
        print("Starting behaviour.")

        self.system_features = {"threshold": 50}

    async def on_end(self):
        print("Ending behaviour.")

    async def run(self):
        print("Running the behaviour.")
