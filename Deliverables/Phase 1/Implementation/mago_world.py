# from owlready2 import Ontology
from mago_thing import *
from mago_agent import Agent
from mago_behaviour import Behaviour
from mago_plan import Plan


class World(Thing):
    """The world containing general system data and agent instantiation."""

    def __init__(self, ontology: Ontology = None, *args, **kwargs):
        super().__init__(entity_type="world", *args, **kwargs)
        self.agents: dict[str, list[Agent]] = {}
        self.agent_import_sources = None
        self.agent_instantiation = None
        self.behaviours_rendered = None
        self.onto = ontology

    def add_agent_to_list(self, agent: Agent):
        self.agents.setdefault(agent.is_a[0].label[0], []).extend(agent)

    def get_list_of_agents(self):
        return self.agents

    def read_agents_from_ontology(self, onto: Ontology = None):
        if onto is None:
            onto = self.onto

        agent_classes = onto.search(subclass_of=onto.search(label="Agent"))
        for agent_class in agent_classes:
            agents = onto.search(type=agent_class)
            self.agents.setdefault(agent_class.label[0], []).extend(
                [
                    Agent(
                        agent_type=agent.is_a[0].label[0],
                        host_server=agent.lives_on_host[0].label[0],
                        name=agent.has_name,
                        password="tajna",
                        onto_individual=agent,
                    )
                    for agent in agents
                ]
            )

    def render_behaviours_from_ontology(self, onto: Ontology = None):
        if onto is None:
            onto = self.onto

        has_name = onto.search_one(label="has name")

        behaviours = onto.search(type=onto.search_one(label="Behaviour"))

        behaviours_mago = [
            Behaviour(
                cycling=behaviour.is_repeating,
                period=behaviour.has_period if behaviour.has_period else None,
                onto_individual=behaviour,
            )
            for behaviour in behaviours
        ]

        self.behaviours_rendered = "\n\n\n".join(
            [
                behaviour.render_behaviour_implementation()
                for behaviour in behaviours_mago
            ]
        )

        return self.behaviours_rendered

    def read_plan_from_ontology(self, onto: Ontology = None):
        if onto is None:
            onto = self.onto

        result = {}

        plan = onto.search_one(
            iri="http://dragon.foi.hr/mago-a.owx#RDm65h4GNQjimv0axMIRnMX"
        ).instances()

        for plan in plan:
            result.update(
                Plan(
                    onto_individual=plan
                ).get_plan_action_behaviour_objective()
            )

        return result

    def write_behaviour_implementations_to_file(self):
        if not self.behaviours_rendered:
            self.render_behaviours_from_ontology()

        file_name = os.path.join(os.getcwd(), "Template", "Behaviours.py")
        with open(file_name, "w") as file:
            file.write("from spade.behaviour import *\n\n")
            file.write(self.behaviours_rendered)

    def render_agent_import_sources(self):
        if not self.agents:
            self.read_agents_from_ontology()

        self.agent_import_sources = "\n".join(
            [agents[0].render_agent_import() for agents in self.agents.values()]
        )

    def render_agent_instantiation(self):
        if not self.agents:
            self.read_agents_from_ontology()

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

    def write_agent_implementations_to_files(self):
        for agents in self.agents.values():
            agents[0].render_agent_implementation()
            agents[0].write_implementation_to_file()

    def render_world_implementation(self):
        self.set_implementation_template(
            """
import spade
$agent_import_sources


async def main():
    agent_individuals = {}
$agent_instantiation
    for agent in [agent for host_dict in agent_individuals.values() for agent in host_dict.values()]:
        agent.plan_action_behaviour_objective = $plan_action_behaviour_objective
        await agent.start()

spade.run(main())
"""
        )

        self.plan_action_behaviour_objective = self.read_plan_from_ontology()

        self.render_agent_import_sources()
        self.render_agent_instantiation()

        self.render_implementation()
        return self.get_implementation()

    def write_implementation_to_disk(self):
        if not self.implementation:
            self.render_world_implementation()

        self.write_behaviour_implementations_to_file()

        self.write_agent_implementations_to_files()

        self.write_implementation_to_file()

        logging.info(f"{self.name} system successfully written to disk.")
