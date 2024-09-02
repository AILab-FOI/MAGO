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

test_world = World()
onto: Ontology = test_world.get_ontology("MAGO-Ag.owx").load(reload=True)
# onto = get_ontology("https://raw.githubusercontent.com/AILab-FOI/MAGO/main/Deliverables/Phase%201/Implementation/MAGO-Ag.owx")
# onto.load()

# %% set rendering setting


def render_using_label(entity):
    return entity.label.first() or entity.name


def render_using_iri(entity):
    return entity.iri


set_render_func(render_using_label)

# %% list all the classes in ontology onto
query_prefixes = """
    PREFIX mago: <http://dragon.foi.hr/mago-a.owx#>
    """
sparql_queries = {
    "select roles of the agent": {
        "description": "Select all the roles this agent can play.",
        "query": """
            SELECT ?role
            {
                ?? mago:RCcC3SXJ5MvuHMJyzs8OpU6 ?role .  # can play role
            }
        """
    },
    "select behaviour individuals available to agent": {
        "description": "Select all the behaviour individuals available to the agent through various roles it can play.",
        "query": """
            SELECT ?behaviour
            {
                ?? mago:RCcC3SXJ5MvuHMJyzs8OpU6 ?role .  # can play role
                ?role mago:RY56GiCpqJHON677qnE5sT ?behaviour .  # provides behaviour
            }
        """
    },
    "select behaviour labels available to agent": {
        "description": "Select all the behaviour labels available to the agent through various roles it can play.",
        "query": """
            SELECT ?behaviour
            {
                ?? mago:RCcC3SXJ5MvuHMJyzs8OpU6 ?role .  # can play role
                ?role mago:RY56GiCpqJHON677qnE5sT ?individual_behav .  # provides behaviour
                ?individual_behav rdfs:label ?behaviour .
            }
        """
    }
}

# list(onto.classes())
entitet = test_world.search_one(label="Agent seven")
print(entitet)
query_res = test_world.sparql(
    sparql=query_prefixes + sparql_queries.get("select behaviour individuals available to agent").get("query"),
    params=[
        entitet
    ]
)

list(query_res)

# %% set base IRI for the ontology

# onto.base_iri = "http://dragon.foi.hr/mago-a.owx#"
onto.set_base_iri("http://dragon.foi.hr/mago-a.owx/", rename_entities=True)

# %%

onto.search(label="Agent")
onto.search(subclass_of=onto.search_one(label="Artefact"))

# %% add new individuals and make connection

Agent = onto.search_one(label="Agent")
aAgent = Agent()
aAgent.label = "Broj tri"
aAgent.has_name = "Barica"

AgentHost = onto.search(label="Agent Host Server")[0]
aHost = AgentHost()
aHost.label = "localhost"

aAgent.lives_on_host = [aHost]

aAgent.lives_on_host

# %% add new individual

AgentHost = onto.search(label="Agent Host Server")[0]
bHost = AgentHost()
bHost.label = "drugi_host.com"

# %% add a new individual Agent

Agent = onto.search_one(label="Agent")
bAgent = Agent()
bAgent.label.append(
    locstr("Agent eight", "en-gb")
)
# bProp = onto.search_one(label="has name")
# bProp.python_name = "has_name"
# bAgent.bProp = locstr("Jimmy", "en-gb")
bAgent.has_name = "Janice"

# %% list all the individuals in the ontology onto

list(onto.individuals())
# onto.search(label="Agent five")

# %% find agent individuals

agents = onto.search(type=onto.search(label="Agent"))
aProp = onto.search_one(label="has name")
aProp.python_name = "has_name"

aAgent = agents[0]

aAgent.has_name


# %% find agent and give him a role

cAgent = onto.search_one(label="Agent seven")
aRole = onto.search_one(label="Wizard")

cAgent.can_play_role.append(aRole)


# %% SPADE agent implementationDeliverables/Phase 1/Implementation/test.py

async def main():
    agent = Test_agent("agent@localhost", "tajna")
    await agent.start()


spade.run(main())

# %% general MAGO entity class with implementation handling


def clean_string(data: str) -> str:
    if not data or not isinstance(data, str):
        return data

    return data.replace(" ", "_")


class MAGO_Entity:
    """Contains the methods that are common to all the classes that are a part of the translation process. These methods are used for setting the implementation template, rendering implementation based on the set template (no set prior template raises an error), getting the implementation, and writing the implementation to a file.
    """    
    def __init__(self, entity_type: str, uri: str=None, name: str=None, onto_individual=None) -> None:
        self.entity_type = clean_string(entity_type)
        self.uri = uri
        self.name = clean_string(name)
        self.implementation_template = None
        self.implementation = None

        self.world = World()
        self.onto: Ontology = self.world.get_ontology("MAGO-Ag.owx").load(reload=True)
        self.onto_properties = {}

        if onto_individual:
            self.onto_properties.clear()
            for prop in onto_individual.get_properties():
                print(prop.label)
                self.onto_properties.setdefault(
                    prop.label[0] if prop.label else prop.name,
                    getattr(onto_individual, prop.python_name)
                )

            print(self.onto_properties)

            for name, value in self.onto_properties.items():
                setattr(self, name, value)

            print(self.__dict__)

    def set_implementation_template(self, implementation_template: str):
        """Set the implementation template, following the string.Template syntax. This template is used to generate implementation of the object.

        Args:
            implementation_template (str): The implementation template to be filled in with appropriate values of objects of this class. Has to follow string.Template syntax.
        """        
        self.implementation_template = Template(implementation_template)
        self.implementation = None

    def render_implementation(self, substitutes: dict = None):
        """Fill in the provided implementation template with data. If no `substitutes` value is provided, attributes of the object are used (those must have the same names as the variables in the template string).

        Args:
            substitutes (dict, optional): A dictionary of the values to be used in the provided template. Defaults to None.

        Raises:
            ValueError: Error is raised if no template was set.
        """        
        if not self.implementation_template:
            raise ValueError("No implementation template set.")

        substitutes = self.__dict__ if not substitutes else substitutes
        self.implementation = self.implementation_template.substitute(
            substitutes
        ).strip()

    def get_implementation(self):
        """Return the rendered implementation.

        Returns:
            Returns the rendered implementation template or None if unavailable.
        """        
        return self.implementation if self.implementation else None

    def write_implementation_to_file(self, file_name: str = None):
        """Save the rendered implementation to a file. 

        Args:
            file_name (str, optional): Name of the file to be written. If not provided, will be rendered based on the name of the class (`self.__class__.__name__`) and type of entity (`self.entity_type`). Defaults to None.
        """        
        if not self.implementation:
            self.render_implementation()
        if not file_name:
            file_name = f"{self.__class__.__name__}_{self.entity_type}.py"
        with open(file_name, "w") as file:
            file.write(self.implementation)

    def execute_sparql_query(self, query: str) -> list:
        return list(
            self.world.
        )


class Role():
    pass

class MAGO_Behaviour(MAGO_Entity):
    """A class containing all the data describing a MAGO agent behaviour. Contains all the methods and attributes common to all the behaviour types."""
    def __init__(self, behaviour_type: str, *args, **kwargs):
        super(MAGO_Behaviour, self).__init__(*args, **kwargs)
        self.behaviour_type: str = behaviour_type


class MAGO_Behaviour_Cyclic(MAGO_Behaviour):
    """Specific type of behaviour that is constantly looped."""
    def __init__(self, period: int=None, *args, **kwargs):
        super(MAGO_Behaviour_Cyclic, self).__init__(*args, **kwargs)
        self.period: int = period

    def render_behaviour_implementation(self):
        self.set_implementation_template(
            """
class $name(CyclicBehaviour):
    async def on_start(self) -> None:
        print("Starting behaviour.")

    async def on_end(self) -> None:
        print("Ending behaviour.")

    async def run(self) -> None:
        print("Running the behaviour.")
"""
        )
        self.render_implementation()
        return self.get_implementation()


class MAGO_Agent(MAGO_Entity):
    """A class containing all the data describing a MAGO agent."""

    def __init__(
        self,
        agent_type: str,
        host_server: str = None,
        password: str = None,
        *args,
        **kwargs,
    ):
        super().__init__(entity_type=agent_type, *args, **kwargs)
        self.agent_type = clean_string(agent_type)
        self.host_server = host_server
        self.password = password
        self.behaviours = []
        self.query_roles = """"""

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
agent_${host_server}_$name = $agent_type("$name@$host_server", "$password")
await agent_${host_server}_$name.start()
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

    def render_agent_import(self):
        self.set_implementation_template(
            """
from MAGO_Agent_$agent_type import *
"""
        )
        self.render_implementation()
        return self.get_implementation()


class MAGO_World(MAGO_Entity):
    """The world containing general system data and agent instantiation."""

    def __init__(self, *args, **kwargs):
        super().__init__(entity_type="world", *args, **kwargs)
        self.agents: dict[str, list[MAGO_Agent]] = {}
        self.agent_import_sources = None
        self.agent_instantiation = None

    def add_agent_to_list(self, agent: MAGO_Agent):
        self.agents.setdefault(agent.is_a[0].label[0], []).extend(agent)

    def get_list_of_agents(self):
        return self.agents

    def read_agents_from_ontology(self, onto: Ontology):
        prop = onto.search_one(label="lives on host")
        prop.python_name = "property_lives_on_host"
        
        prop = onto.search_one(label="has name")
        prop.python_name = "property_has_name"

        agent_classes = onto.search(subclass_of=onto.search(label="Agent"))
        for agent_class in agent_classes:
            agents = onto.search(type=agent_class)
            self.agents.setdefault(agent_class.label[0], []).extend(
                [
                    MAGO_Agent(
                        agent_type=agent.is_a[0].label[0],
                        host_server=agent.property_lives_on_host[0].label[0],
                        name=agent.property_has_name,
                        password="tajna",
                        uri=agent.name,
                        onto_individual=agent
                    )
                    for agent in agents
                ]
            )

    def render_world_implementation(self):
        self.set_implementation_template(
            """
import spade
$agent_import_sources


async def main():
$agent_instantiation


spade.run(main())
"""
        )

        self.agent_import_sources = "\n".join(
            [agents[0].render_agent_import() for agents in self.agents.values()]
        )

        self.agent_instantiation = textwrap.indent(
            "\n".join(
                [
                    agent.render_agent_instantiation()
                    for agent in [
                        agent
                        for agent_class in self.agents.values()
                        for agent in agent_class
                    ]
                ]
            ),
            "    ",
        )

        self.render_implementation()
        return self.get_implementation()

    def write_implementation_to_disk(self):
        if not self.implementation:
            self.render_world_implementation()

        for agent in [
            agent
            for agent_class in self.agents.values()
            for agent in agent_class
        ]:
            agent.render_agent_implementation()
            agent.write_implementation_to_file()

        self.write_implementation_to_file()

        


# %% testing MAGO Agent class

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

aMAGOWorld.read_agents_from_ontology(onto)
aMAGOWorld.render_world_implementation()
aMAGOWorld.write_implementation_to_disk()
aMAGOWorld.get_list_of_agents()
# aMAGOWorld.add_agent_to_import(aMAGOAgent.agent_type)
# aMAGOWorld.add_agent_to_instantiate(aMAGOAgent.render_agent_instantiation(3))

# aMAGOWorld.render_world_implementation()
# aMAGOWorld.write_implementation_to_file()


# %% load agents from ontology and render them

agents = onto.search(type=onto.search(label="Agent"))

has_name = onto.search_one(label="has name")
has_name.python_name = "property_has_name"

has_name = onto.search_one(label="lives on host")
has_name.python_name = "property_lives_on_host"

agent_types = onto.search(subclass_of=onto.search(label="Agent"))
print(agent_types)


def render_agent_instantiation(agent):
    entity = MAGO_Agent(
        agent_type=agent.is_a[0].label[0],
        host_server=agent.property_lives_on_host[0].label[0],
        name=agent.property_has_name,
        password="tajna",
    )
    return entity.render_agent_instantiation()


for agent_type in agent_types:
    agent_implementation = MAGO_Agent(agent_type=agent_type.label[0])
    print(agent_implementation.render_agent_implementation())
    agent_implementation.write_implementation_to_file()

    agents = onto.search(type=agent_type)
    agent_instantiation = map(render_agent_instantiation, agents)

    print("\n".join(agent_instantiation))


# %% save the ontology

onto.save()

# %% plans for near future

"""
1. translate onto into implementation
2. have two agents, A creates individual, sends it to B, B checks it in the onto and creates implementation
3. store current system data into onto
"""
