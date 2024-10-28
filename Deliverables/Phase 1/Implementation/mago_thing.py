from owlready2 import World, Ontology, NamedIndividual
from string import Template

import os
from itertools import chain
import textwrap
from json import loads

from aux import *

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="log.log",
)


class Thing:
    """Contains the methods that are common to all the classes that are a part of the translation process. These methods are used for setting the implementation template, rendering implementation based on the set template (no set prior template raises an error), getting the implementation, and writing the implementation to a file."""

    def __init__(
        self, entity_type: str, uri: str = None, name: str = None, onto_individual=None
    ) -> None:
        self.entity_type = clean_string(entity_type)
        self.uri = uri
        self.implementation_template = None
        self.implementation = None

        self.world = World()
        self.onto: Ontology = self.world.get_ontology("MAGO-Ag.owx").load(reload=True)
        self.onto_properties = {}

        self.onto_individual: NamedIndividual = onto_individual

        if name is None and onto_individual is not None:
            self.name = clean_string(self.onto_individual.has_name)
        else:
            self.name = clean_string(name)

        if uri is None and onto_individual is not None:
            self.uri = self.onto_individual.iri
        else:
            self.uri = uri

        if onto_individual:
            self.onto_properties.clear()
            for prop in onto_individual.get_properties():
                # print(prop.label)
                self.onto_properties.setdefault(
                    prop.label[0] if prop.label else prop.name,
                    getattr(onto_individual, prop.python_name),
                )

            # print(self.onto_properties)

            for name, value in self.onto_properties.items():
                setattr(self, name, value)

        logging.info(
            f"Individual {self.onto_individual if self.onto_individual else self.name} of type {self.entity_type} created."
        )

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
            file_name = os.path.join(
                os.getcwd(),
                "Template",
                f"{self.__class__.__name__}_{self.entity_type}.py",
            )
        with open(file_name, "w") as file:
            file.write(self.implementation)

        logging.info(
            f"Implementation of {self.onto_individual if self.onto_individual else self.name} saved to {file_name}."
        )

    def execute_sparql_query(self, query: dict, world: World) -> list:
        query_res = world.sparql(sparql=query.get("query"), params=query.get("params"))

        return list(query_res)
