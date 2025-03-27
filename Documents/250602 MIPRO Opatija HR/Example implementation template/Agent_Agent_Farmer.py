from itertools import chain

from owlready2 import World
from spade.agent import Agent
from Behaviours import *


class Agent_Farmer(Agent):

    def execute_sparql(self, world: World=None, query: str=None, parameters: list=None) -> list:
        """Execute a SPARQL query in the provided owlready2 World instance.

        Args:
            world (World): An owlready2 World instance containing the relevant data.
            query (str): The SPARQL query to be executed. Parameters are designated as `??`.
            parameters (list, optional): Parameters to be sequentially provided to the query. Defaults to None.

        Returns:
            list: The result of the query.
        """
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