from mago_thing import *


class Agent(Thing):
    """A class containing all the data describing a MAGO agent."""

    def __init__(
        self,
        agent_type: str,
        host_server: str = None,
        password: str = None,
        # knowledge_artefact_uris: dict[str, str] = None,
        *args,
        **kwargs,
    ):
        super().__init__(entity_type=agent_type, *args, **kwargs)
        self.agent_type = clean_string(agent_type)
        self.host_server = host_server
        self.password = password
        self.behaviours = []
        self.query_roles = """"""
        self.knowledge_artefact_uris = get_related_knowledge_artefact_uris(
            self.onto_individual
        )
        self.system_features = loads(self.onto_individual.has_system_features) if self.onto_individual.has_system_features else None

    def render_agent_implementation(self):
        self.set_implementation_template(
            """
from itertools import chain

from owlready2 import World
from spade.agent import Agent
from Behaviours import *


class $agent_type(Agent):

    def execute_sparql(self, world: World=None, query: str=None, parameters: list=None) -> list:
        \"\"\"Execute a SPARQL query in the provided owlready2 World instance.

        Args:
            world (World): An owlready2 World instance containing the relevant data.
            query (str): The SPARQL query to be executed. Parameters are designated as `??`.
            parameters (list, optional): Parameters to be sequentially provided to the query. Defaults to None.

        Returns:
            list: The result of the query.
        \"\"\"
        if world is None:
            world = self.world

        if query is None:
            ValueError("Query string must be provided.")

        prepared_query = world.prepare_sparql(sparql=query)
        column_names = [name.replace("?", "") for name in prepared_query.column_names]

        query_res = prepared_query.execute(params=parameters)
        query_res = [dict(zip(column_names, result)) for result in query_res]

        return query_res

    async def setup(self):
        print(f"{self.name}: New agent running.")

        self.knowledge_artefacts = {}

        for ka_name, ka_uri in self.knowledge_artefact_uris.items():
            world = World()
            self.knowledge_artefacts.setdefault(ka_name, {}).update({
                "world": world,
                "ontology": world.get_ontology(ka_uri).load(reload=True)
            })

        if self.available_roles_and_behaviours is not None:
            self.available_roles = list([entry.get("name") for entry in self.available_roles_and_behaviours.values()])
            self.available_behaviours = list(set(chain(*[entry.get("behaviours", {}).values()
              for entry in self.available_roles_and_behaviours.values()])))
        else:
            self.available_roles = None
            self.available_behaviours = None

        print(self.name, self.available_roles, self.available_behaviours, self.knowledge_artefacts)

        self.world = self.knowledge_artefacts.get("Main ontology").get("world")
        self.onto_individual = self.world.search_one(iri=self.uri)
"""
        )
        self.render_implementation()
        return self.get_implementation()

    def get_related_roles_and_behaviours(self):
        result = {}

        result.update(
            {
                role.iri: {"name": role.has_name, "behaviours": {}}
                for role in self.onto_individual.can_play_role
            }
        )

        for role in self.onto_individual.can_play_role:
            result.get(role.iri).get("behaviours").update(
                {
                    behaviour.iri: behaviour.has_name
                    for behaviour in role.provides_behaviour
                }
            )

        return result if result else None

    def render_agent_instantiation(self):
        self.related_roles_and_behaviours = self.get_related_roles_and_behaviours()

        agent_instantiation_template = """
agent = $agent_type("$name@$host_server", "$password")
agent.uri = "$uri"
agent.knowledge_artefact_uris = $knowledge_artefact_uris
agent.available_roles_and_behaviours = $related_roles_and_behaviours
agent.system_features = $system_features
agent_individuals.setdefault("$host_server", {}).update({"$name": agent})
"""
        self.set_implementation_template(agent_instantiation_template)

        self.render_implementation()
        return self.get_implementation()

    def render_agent_import(self):
        self.set_implementation_template(
            """
from Agent_$agent_type import *
"""
        )
        self.render_implementation()
        return self.get_implementation()
