# %% libraries

import os
from owlready2 import *

from string import Template
import textwrap

import spade
from spade.agent import Agent

# %% set ontology path

onto_path.append(os.getcwd())
print(onto_path)

# %% load ontology

onto = get_ontology("MAGO-Ag.owx")
onto.load()

# %% set base IRI for the ontology

onto.base_iri = "http://dragon.foi.hr/mago-a.owx#"
onto.set_base_iri("http://dragon.foi.hr/mago-a.owx#", rename_entities=True)

# %% set rendering setting


def render_using_label(entity):
    return entity.label.first() or entity.name


def render_using_iri(entity):
    return entity.iri


set_render_func(render_using_label)

# %%

for concept in onto.classes():
    print(concept)


# %%

onto.search(label="Agent")
onto.search(subclass_of=onto.search(label="Artefact"))

# %% add new individuals and make connection

Agent = onto.search(label="Agent")[0]
aAgent = Agent()
aAgent.label = "Broj dva"
aAgent.has_name = ["Barica"]

AgentHost = onto.search(label="Agent Host Server")[0]
aHost = AgentHost()
aHost.label = "localhost"

aAgent.lives_on_host = [aHost]

aAgent.lives_on_host

# %% add new individual

AgentHost = onto.search(label="Agent Host Server")[0]
bHost = AgentHost()
bHost.label = "drugi_host.com"

# %%

list(onto.individuals())

# %% find agent individuals

agents = onto.search(type=onto.search(label="Agent"))
aProp = onto.search_one(label="has name")
aProp.python_name = "has_name"

aAgent = agents[0]

aAgent.has_name

# %% SPADE agent implementation


class Test_agent(Agent):
    async def setup(self):
        print("New agent running.")


async def main():
    agent = Test_agent("agent@localhost", "tajna")
    await agent.start()


spade.run(main())

# %% general MAGO entity class with implementation handling


class MAGO_Entity:
    def __init__(self, entity_type: str) -> None:
        self.entity_type = entity_type
        self.implementation_template = None
        self.implementation = None

    def set_implementation_template(self, implementation_template: str):
        self.implementation_template = Template(implementation_template)
        self.implementation = None

    def render_implementation(self, substitutes: dict = None):
        if not self.implementation_template:
            raise ValueError("No implementation template set.")

        substitutes = self.__dict__ if not substitutes else substitutes
        self.implementation = self.implementation_template.substitute(
            substitutes
        ).strip()

    def get_implementation(self):
        return self.implementation if self.implementation else None

    def write_implementation_to_file(self, file_name: str = None):
        if not self.implementation:
            self.render_implementation()
        if not file_name:
            file_name = f"{self.__class__.__name__}_{self.entity_type}.py"
        with open(file_name, "w") as file:
            file.write(self.implementation)


# %% MAGO world class 


class MAGO_World(MAGO_Entity):
    """The world containing general system data and agent instantiation."""
    def __init__(self, *args, **kwargs):
        super().__init__(entity_type='world', *args, **kwargs)
        self.agents_to_import = []
        self.agent_import_sources = None

        self.agents_to_instantiate = []
        self.agent_instantiations = None

    def add_agent_to_import(self, agent_names: str | list):
        if isinstance(agent_names, str):
            self.agents_to_import.append(agent_names)
        elif isinstance(agent_names, list):
            self.agents_to_import.extend(agent_names)

    def add_agent_to_instantiate(self, instantiation_implementation: str | list):
        if isinstance(instantiation_implementation, str):
            self.agents_to_instantiate.append(instantiation_implementation)
        if isinstance(instantiation_implementation, list):
            self.agents_to_instantiate.extend(instantiation_implementation)

    def render_world_implementation(self):
        self.set_implementation_template(
            """
import spade
$agent_import_sources


async def main():
$agent_instantiations


spade.run(main())
"""
        )

        self.agent_import_sources = "\n".join([f'from MAGO_Agent_{agent_name} import *' for agent_name in self.agents_to_import])
        self.agent_instantiations = "\n".join(self.agents_to_instantiate)
        self.agent_instantiations = textwrap.indent(self.agent_instantiations, '    ')

        self.render_implementation()
        return self.get_implementation()
        


# %% MAGO agent class


class MAGO_Agent(MAGO_Entity):
    """A class containing all the data describing a MAGO agent."""

    def __init__(
        self, agent_type: str, name: str, host_server: str, password: str, *args, **kwargs
    ):
        super().__init__(entity_type=agent_type, *args, **kwargs)
        self.agent_type = agent_type
        self.name = name
        self.host_server = host_server
        self.password = password

    def render_agent_implementation(self):
        self.set_implementation_template(
            """
from spade.agent import Agent
# from behaviours import *


class $agent_type(Agent):
    async def setup(self):
        print("New agent running.")
"""
        )
        self.render_implementation()
        return self.get_implementation()

    def render_agent_instantiation(self, number_of_agents: int = 1):
        agent_implementation_base = """
agent = $agent_type("$name@$host_server", "$password")
await agent.start()
""".strip()
        if number_of_agents == 1:
            self.set_implementation_template(agent_implementation_base)
        elif number_of_agents > 1:
            self.set_implementation_template(
                f"""
for _ in range({number_of_agents}):
{textwrap.indent(agent_implementation_base, '    ')}
""".strip()
            )
        else:
            return None

        self.render_implementation()
        return self.get_implementation()


aMAGOAgent = MAGO_Agent(
    agent_type="Test_agent",
    name="agent",
    host_server="localhost",
    password="tajna",
)

aMAGOAgent.render_agent_implementation()
print(aMAGOAgent.get_implementation())
aMAGOAgent.write_implementation_to_file()

aMAGOAgent.render_agent_instantiation(3)
print(aMAGOAgent.get_implementation())

# %% using the MAGO World class

aMAGOWorld = MAGO_World()
aMAGOWorld.add_agent_to_import(aMAGOAgent.agent_type)
aMAGOWorld.add_agent_to_instantiate(aMAGOAgent.render_agent_instantiation(3))

aMAGOWorld.render_world_implementation()
aMAGOWorld.write_implementation_to_file()


# %% save the ontology

onto.save()
