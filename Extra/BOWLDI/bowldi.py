import owlready2
from owlready2 import World, Ontology, sync_reasoner, set_render_func, locstr
from pathlib import Path
import argparse
import os
import json
import hashlib
from pprint import pprint

import re

LANGUAGE = "en-gb"


def render_using_label(entity):
    return entity.label.first() or entity.name


class BOWLDIConverter:
    def __init__(
        self,
        input_data_path: str = None,
        output_data_path: str = None,
        input_data: str = None,
    ):
        if input_data_path is None and input_data is None:
            self.prepare_response(
                status="error",
                message="Please provide a valid input.",
            )

        else:

            self.input_data_path = input_data_path
            self.data = {}

            if output_data_path is None:
                if input_data is not None:
                    output_data_path = "output.owl"
                else:
                    output_data_path = (
                        "output.owl"
                        if Path(self.input_data_path).suffix == ".asl"
                        else "output.asl"
                    )

            self.output_data_path = Path(output_data_path)

            if input_data is not None:
                self.ontology, self.world = self.load_ontology(
                    self.output_data_path.resolve().as_uri()
                )

                self.input_data = input_data
                self.parse_agentspeak_expressions(self.input_data)
                self.save_ontology(self.output_data_path)

                self.prepare_response(
                    status="success",
                    message="Conversion complete.",
                    file=self.output_data_path.resolve().as_posix(),
                )

            else:

                if Path(self.input_data_path).exists():
                    self.input_data_path = Path(self.input_data_path).resolve()

                    if self.input_data_path.suffix in [".owx", ".owl", ".rdf", ".ttl"]:
                        self.ontology, self.world = self.load_ontology(
                            self.input_data_path.as_uri()
                        )
                        self.generate_agentspeak()

                    if self.input_data_path.suffix == ".asl":
                        self.ontology, self.world = self.load_ontology(
                            self.output_data_path.resolve().as_uri()
                        )

                        expressions = self.input_data_path.read_text()
                        self.parse_agentspeak_expressions(expressions)

                        self.save_ontology(self.output_data_path)
                    self.prepare_response(
                        status="success",
                        message="Conversion complete.",
                        file=self.output_data_path.resolve().as_posix(),
                    )

                else:
                    self.prepare_response(
                        status="error",
                        message="Input file does not exist.",
                    )

    def clean_data(self, input):
        """Summary: Clean the input data by removing extra spaces and converting to snake case.

        Args:
            input (_type_):

        Returns:
            _type_:
        """
        if isinstance(input, str):
            return self.clean_string(input)
        elif isinstance(input, list):
            return [self.clean_string(i) for i in input]
        else:
            return input

    def clean_string(self, input: str):
        def replace_spaces(match):
            line = match.group(0)
            # Split the line into parts that are inside and outside quotes
            parts = re.split(r'(".*?")', line)
            # Replace spaces between words in parts that are outside quotes and lower case
            parts = [
                (
                    re.sub(r"(?<=\w) (?=\w)", "_", part.lower())
                    if not part.startswith('"')
                    else part
                )
                for part in parts
            ]

            return "".join(parts)

        lines = input.split("[source")

        pattern = r"^(?![+\-!?.\t<]).*"
        lines[0] = re.sub(pattern, replace_spaces, lines[0], flags=re.MULTILINE)

        result = "[source".join(lines)

        return result

    # Load the ontology using owlready2
    def load_ontology(self, file_path: str) -> tuple:
        """Summary: Load the ontology using owlready2.

        Args:
            file_path (str): Path to the ontology file.

        Returns:
            _type_: Ontology and World objects.
        """
        world = World()
        ontology: Ontology = world.get_ontology(file_path)
        try:
            ontology.load(reload=True)
            set_render_func(render_using_label)
            with ontology:
                sync_reasoner()
        except Exception as e:
            pass

        return ontology, world

    def determine_concept_source(
        self, concept: owlready2.ThingClass, reference_onto_iri: str
    ) -> set[str]:
        """
        Determines the source of a given OWL concept based on its IRI and a reference ontology IRI.

        Args:
            concept (owlready2.ThingClass): The OWL concept whose source is to be determined.
            reference_onto_iri (str): The IRI of the reference ontology.

        Returns:
            set[str]: A set containing "self" if the concept's namespace matches the reference ontology IRI,
                    otherwise the concept's namespace and any additional sources defined by the concept.
        """
        iri = concept.iri
        namespace = iri.rsplit("#", 1)[0] if "#" in iri else iri.rsplit("/", 1)[0]
        reference_onto_iri = reference_onto_iri.rstrip("/#")
        source = {"self"} if namespace == reference_onto_iri else {namespace}
        source.update(concept.isDefinedBy)
        return list(source)

    def extract_ontology_information_classes(self, ontology: Ontology=None) -> dict:
        """
        Extracts information about ontology classes and returns it in a dictionary format.

        Args:
            ontology (Ontology): The ontology object from which to extract class information.

        Returns:
            dict: A dictionary containing information about the ontology classes. The dictionary
                  has the following structure:
                      "concepts": {
                          class_name: {
                              "concept": class_label,
                              "is a": [list_of_parent_classes],
                              "source": source_of_definition
                          },
                          ...
                  - class_name (str): The name of the ontology class.
                  - class_label (str): The label of the ontology class in the specified language.
                  - list_of_parent_classes (list): A list of names of parent classes.
                  - source_of_definition (set): A set containing the source(s) of the class definition,
                    including "self" if defined within the reference ontology.
        """
        result = {}

        ontology = self.ontology if ontology is None else ontology

        for cls in ontology.world.classes():

            result.setdefault("concepts", {}).update(
                {
                    cls.name: {
                        "concept": cls.label.get_lang_first(LANGUAGE),
                        "is a": [is_a.name for is_a in cls.is_a],
                        "source": self.determine_concept_source(cls, ontology.base_iri),
                    }
                }
            )

        return result

    def extract_ontology_information_object_properties(
        self, ontology: Ontology=None
    ) -> dict:
        """
        Extracts information about ontology object properties and returns it in a dictionary format.

        Args:
            ontology (Ontology): The ontology object from which to extract object property information.

        Returns:
            dict: A dictionary containing information about the ontology object properties. The dictionary
                  has the following structure:
                      "object properties": {
                          property_name: {
                              "property": property_label,
                              "domain": domain_class,
                              "range": range_class,
                              "inverse_property": inverse_property_name,
                              "source": source_of_definition
                          },
                          ...
                  - property_name (str): The name of the object property.
                  - property_label (str): The label of the object property in the specified language.
                  - domain_class (str): The name of the domain class of the object property.
                  - range_class (str): The name of the range class of the object property.
                  - inverse_property_name (str): The name of the inverse property of the object property.
                  - source_of_definition (set): A set containing the source(s) of the class definition,
                    including "self" if defined within the reference ontology.
        """
        result = {}

        ontology = self.ontology if ontology is None else ontology

        for prop in ontology.world.object_properties():
            result.setdefault("object properties", {}).update(
                {
                    prop.name: {
                        "property": prop.label.get_lang_first(LANGUAGE),
                        "domain": (
                            prop.domain.first().label.get_lang_first(LANGUAGE)
                            if prop.domain
                            else None
                        ),
                        "range": (
                            prop.range.first().label.get_lang_first(LANGUAGE)
                            if prop.range
                            else None
                        ),
                        "inverse_property": (
                            prop.inverse_property.name
                            if prop.inverse_property
                            else None
                        ),
                        "source": self.determine_concept_source(
                            prop, ontology.base_iri
                        ),
                    }
                }
            )

        return result

    def extract_ontology_information_data_properties(self, ontology: Ontology=None) -> dict:
        """
        Extracts information about ontology data properties and returns it in a dictionary format.

        Args:
            ontology (Ontology): The ontology object from which to extract data property information.

        Returns:
            dict: A dictionary containing information about the ontology data properties. The dictionary
                  has the following structure:
                      "data properties": {
                          property_name: {
                              "property": property_label,
                              "domain": domain_class,
                              "range": range_class,
                              "source": source_of_definition
                          },
                          ...
                  - property_name (str): The name of the data property.
                  - property_label (str): The label of the data property in the specified language.
                  - domain_class (str): The name of the domain class of the data property.
                  - range_class (str): The name of the range class of the data property.
                  - source_of_definition (set): A set containing the source(s) of the class definition,
                    including "self" if defined within the reference ontology.
        """
        result = {}

        ontology = self.ontology if ontology is None else ontology

        for prop in ontology.world.data_properties():
            result.setdefault("data properties", {}).update(
                {
                    prop.name: {
                        "property": prop.label.get_lang_first(LANGUAGE),
                        "domain": (
                            prop.domain.first().label.get_lang_first(LANGUAGE)
                            if prop.domain
                            else None
                        ),
                        "range": (prop.range.first() if prop.range else None),
                        "source": self.determine_concept_source(
                            prop, ontology.base_iri
                        ),
                    }
                }
            )

        return result

    def extract_ontology_information_individuals(self, ontology: Ontology=None) -> dict:
        result = {}

        ontology = self.ontology if ontology is None else ontology

        for individual in ontology.world.individuals():
            result.setdefault("individuals", {}).update(
                self.extract_ontology_information_individual(self.ontology, individual)
            )

            result.setdefault("individual_relations", {}).update(
                self.extract_ontology_information_individual_relations(
                    self.ontology, individual
                )
            )

        return result

    def extract_ontology_information_individual(
        self, ontology: Ontology, individual: owlready2.NamedIndividual
    ) -> dict:
        result = {}

        result.update(
            {
                individual.name: {
                    "name": individual.label.get_lang_first(LANGUAGE),
                    "type": individual.is_a[0].label.get_lang_first(LANGUAGE),
                    "source": self.determine_concept_source(
                        individual, ontology.base_iri
                    ),
                }
            }
        )

        return result

    def extract_ontology_information_individual_relations(
        self, ontology: Ontology, individual: owlready2.NamedIndividual
    ) -> dict:
        """ Summary: Extract individual relations from the ontology.

        Args:
            ontology (Ontology): The ontology object from which to extract individual relations.
            individual (owlready2.NamedIndividual): The individual for which to extract relations.

        Returns:
            dict: A dictionary containing information about the individual relations. The dictionary
                  has the following structure:
                      individual_name: {
                          property_name: {
                              "type": property_type,
                              "subject": individual_name,
                              "property": property_name,
                              "object": [list_of_objects],
                              "source": source_of_definition
                          },
                          ...
                      },
                  - individual_name (str): The name of the individual.
                  - property_name (str): The name of the property.
                  - property_type (str): The type of the property (object property or data property).
                  - list_of_objects (list): A list of names of related individuals or values.
                  - source_of_definition (set): A set containing the source(s) of the class definition,
                    including "self" if defined within the reference ontology.
        """
        result = {}

        for prop in individual.get_properties():
            related_individuals = prop[individual]
            for related in related_individuals:
                if not prop.label:
                    continue
                source_data = owlready2.AnnotatedRelation(
                    individual, prop, related
                ).isDefinedBy.first()
                if owlready2.ObjectProperty in prop.ancestors():
                    hash_val = hashlib.sha256("".join([str(prop), related.label.get_lang_first(LANGUAGE)]).encode()).hexdigest()
                else:
                    hash_val = hashlib.sha256("".join([str(prop), related]).encode()).hexdigest()
                result.setdefault(
                    hash_val,
                    {
                        "type": (
                            "object property"
                            if owlready2.ObjectProperty in prop.ancestors()
                            else "data property"
                        ),
                        "subject": individual.label.get_lang_first(LANGUAGE),
                        "property": prop.label.get_lang_first(LANGUAGE),
                        "object": related.label.get_lang_first(LANGUAGE) if owlready2.ObjectProperty in prop.ancestors() else related,
                        "source": source_data if source_data else "self",
                    },
                )

        result = {individual.name: result}

        return result

    # Extract concepts, relations, and individuals from the ontology
    def extract_ontology_information(self):
        """Summary: Extract concepts, properties, individuals, and individual relations from the ontology."""

        result = {}

        # Extract classes (concepts)
        result.update(self.extract_ontology_information_classes())

        # Extract object properties (relations) and their domain/range
        result.update(
            self.extract_ontology_information_object_properties()
        )

        # Extract data properties (relations) and their domain/range
        result.update(
            self.extract_ontology_information_data_properties()
        )

        # Extract individuals
        result.update(self.extract_ontology_information_individuals())

        return result

    def convert_ontology_concepts(self, data: dict = {}) -> list[str]:
        """Summary: Convert concepts to AgentSpeak representation.

        Args:
            data (dict): Dictionary containing concepts extracted from the ontology.

        Returns:
            list[str]: List of AgentSpeak representation of concepts.
        """
        converted_lines = []

        # Add concepts as facts
        for concept, features in data.items():
            converted_lines.append(
                f"concept({features.get('concept')})[source({features.get('source')})]."
            )
            if features.get("is a") and "Thing" not in features.get("is a"):
                for super_concept in features.get("is a"):
                    converted_lines.append(
                        f"is_a({features.get('concept')}, {data.get(super_concept).get('concept')})[source({features.get('source')})]."
                    )

        return converted_lines

    def convert_ontology_object_properties(self, data: dict = {}) -> list[str]:
        """Summary: Convert object properties to AgentSpeak representation.

        Args:
            data (dict): Dictionary containing object properties extracted from the ontology.

        Returns:
            list[str]: List of AgentSpeak representation of object properties.
        """
        converted_lines = []

        # Add relations
        for property, features in data.items():
            if (
                features.get("domain") is None
                and features.get("range") is None
                and features.get("inverse_property") is not None
            ):
                inverse_property_features = data.get(features.get("inverse_property"))
                converted_lines.append(
                    f"object_property({inverse_property_features.get('range')}, {features.get('property')}, {inverse_property_features.get('domain')})[source({features.get('source')})]."
                )
            else:
                converted_lines.append(
                    f"object_property({features.get('domain')}, {features.get('property')}, {features.get('range')})[source({features.get('source')})]."
                )

        return converted_lines

    def convert_ontology_data_properties(self, data: dict = {}) -> list[str]:
        """Summary: Convert data properties to AgentSpeak representation.

        Args:
            data (dict): Dictionary containing data properties extracted from the ontology.

        Returns:
            list[str]: List of AgentSpeak representation of data properties.
        """
        converted_lines = []

        # Add relations
        for property, features in data.items():
            pattern = r"<class '(\w+)'>"
            range_value = re.search(pattern, str(features.get("range")))
            converted_lines.append(
                f"data_property({features.get('domain')}, {features.get('property')}, {range_value.group(1)})[source({features.get('source')})]."
            )

        return converted_lines

    def convert_ontology_individuals(self, data: dict = {}) -> list[str]:
        """Summary: Convert individuals to AgentSpeak representation.

        Args:
            data (dict): Dictionary containing individuals extracted from the ontology.

        Returns:
            list[str]: List of AgentSpeak representation of individuals.
        """
        converted_lines = []

        # Add individuals as facts
        for individual, features in data.items():
            converted_lines.append(
                f"individual({features.get('name').replace(', ', ' ')}, {features.get('type')})[source({features.get('source')})]."
            )

        return converted_lines

    def convert_ontology_individual_relations(self, data: dict = {}) -> list[str]:
        """Summary: Convert individual relations to AgentSpeak representation.

        Args:
            data (dict): Dictionary containing individual relations extracted from the ontology.

        Returns:
            list[str]: List of AgentSpeak representation of individual relations.
        """
        converted_lines = []

        # Add individual relations
        for individual, relations in data.items():
            if (
                self.ontology["rule"]
                and individual in self.ontology["rule"].instances()
            ):
                rule_event, rule_context, rule_body = None, None, []
                for _, value in relations.items():
                    if value.get("property") == "rule has event":
                        rule_event = value.get("object")
                    elif value.get("property") == "rule has context":
                        rule_context = value.get("object")
                    elif value.get("property") == "rule has body":
                        rule_body.append(value.get("object"))

                converted_lines.append(
                    f"{rule_event} : {rule_context} <- {'; '.join(rule_body)}."
                )
            else:
                for features in relations.values():
                    if not features.get("property"):
                        continue
                    # for property_object in features.get("object"):
                    converted_lines.append(
                        f"relation({features.get('subject').replace(', ', ' ')}, {features.get('property')}, {features.get('object')})[source({features.get('source')})]."
                        if features.get("type") == "object property"
                        else f'relation({features.get("subject").replace(", ", " ")}, {features.get("property")}, "{features.get("object")}")[source({features.get("source")})].'
                    )

        return converted_lines

    # Convert extracted information
    def convert_ontology_information(self) -> str:
        """Summary: Convert extracted information to AgentSpeak representation.

        Returns:
            str: AgentSpeak representation of the ontology.
        """
        converted_lines = []

        # Add concepts as facts
        converted_lines.extend(
            self.convert_ontology_concepts(self.data.get("concepts", {}))
        )

        if self.data.get("object properties") is not None:
            # Add relations
            converted_lines.extend(
                self.convert_ontology_object_properties(
                    self.data.get("object properties", {})
                )
            )

        if self.data.get("data properties") is not None:
            # Add relations
            converted_lines.extend(
                self.convert_ontology_data_properties(
                    self.data.get("data properties", {})
                )
            )

        if self.data.get("individuals") is not None:
            # Add individuals as facts
            converted_lines.extend(
                self.convert_ontology_individuals(self.data.get("individuals", {}))
            )

        if self.data.get("individual_relations") is not None:
            # Add individual relations
            converted_lines.extend(
                self.convert_ontology_individual_relations(
                    self.data.get("individual_relations", {})
                )
            )

        converted_lines = self.clean_data(converted_lines)
        return "\n".join(converted_lines)

    def import_ontology(self, ontology_uri):
        try:
            imported_ontology = self.world.get_ontology(ontology_uri).load(reload=True)
            self.ontology.imported_ontologies.append(imported_ontology)
        except Exception as e:
            print(e)

    def create_concept(self, concept_name, parent_concept=None, source="self"):
        with self.ontology:
            if concept_name not in map(lambda x: x.name, self.ontology.world.classes()):
                new_concept = owlready2.types.new_class(
                    concept_name, (owlready2.Thing,)
                )
                new_concept.label.append(
                    locstr(concept_name.replace("_", " "), lang=LANGUAGE)
                )
                new_concept.isDefinedBy.append(source)

            if parent_concept is not None:
                if parent_concept not in map(
                    lambda x: x.name, self.ontology.world.classes()
                ):
                    raise ValueError(
                        f"Parent concept {parent_concept} not found in the ontology."
                    )

                the_concept = self.world.search_one(iri=f"*{concept_name}")
                the_concept.is_a.append(self.world.search_one(iri=f"*{parent_concept}"))
                if owlready2.Thing in the_concept.is_a:
                    the_concept.is_a.remove(owlready2.Thing)

        return self.ontology.world[concept_name]

    def create_object_property(
        self,
        property_name,
        property_domain="None",
        property_range="None",
        source="self",
    ):
        if property_name in map(
            lambda x: x.name, self.ontology.world.object_properties()
        ):
            if property_domain != "None":
                if (
                    property_domain
                    not in self.world.search_one(iri=f"*{property_name}").domain
                ):
                    self.world.search_one(iri=f"*{property_name}").domain.append(
                        self.world.search_one(iri=f"*{property_domain}")
                    )

            if property_range != "None":
                if (
                    property_range
                    not in self.world.search_one(iri=f"*{property_name}").range
                ):
                    self.world.search_one(iri=f"*{property_name}").range.append(
                        self.world.search_one(iri=f"*{property_range}")
                    )

            return self.world.search_one(iri=f"*{property_name}")

        with self.ontology:
            new_property = owlready2.types.new_class(
                property_name, (owlready2.ObjectProperty,)
            )
            new_property.label.append(
                locstr(property_name.replace("_", " "), lang=LANGUAGE)
            )

            if property_domain != "None":
                new_property.domain = [self.world.search_one(iri=f"*{property_domain}")]

            if property_range != "None":
                new_property.range = [self.world.search_one(iri=f"*{property_range}")]

            new_property.isDefinedBy.append(source)

        return new_property

    def create_data_property(
        self,
        property_name,
        property_domain="None",
        property_range="None",
        source="self",
    ):
        if property_name in map(
            lambda x: x.name, self.ontology.world.data_properties()
        ):
            return self.world.search_one(iri=f"*{property_name}")

        with self.ontology:
            new_property = owlready2.types.new_class(
                property_name, (owlready2.DataProperty,)
            )
            new_property.label.append(
                locstr(property_name.replace("_", " "), lang=LANGUAGE)
            )

            if property_domain != "None":
                new_property.domain = [self.world.search_one(iri=f"*{property_domain}")]

            if property_range != "None":
                if isinstance(property_range, list):
                    new_property.range = [property_range]
                else:
                    new_property.range = [type(property_range)]

            new_property.isDefinedBy.append(source)

        return new_property

    def create_individual(self, individual_name, concept_name, source="self"):
        if concept_name not in map(lambda x: x.name, self.ontology.world.classes()):
            self.create_concept(concept_name, source=source)

        with self.ontology:
            new_individual = self.world.search_one(iri=f"*{concept_name}")(
                individual_name
            )
            new_individual.label.append(
                locstr(individual_name.replace("_", " "), lang=LANGUAGE)
            )
            new_individual.isDefinedBy.append(source)

        return new_individual

    def add_object_property_to_individual(
        self, individual_name, property_name, target_individual_name, source="self"
    ):
        self.create_object_property(
            property_name=property_name,
            property_domain=self.world.search_one(iri=f"*{individual_name}")
            .is_a[0]
            .name,
            property_range=self.world.search_one(iri=f"*{target_individual_name}")
            .is_a[0]
            .name,
            source=source,
        )

        with self.ontology:
            individual = self.world.search_one(iri=f"*{individual_name}")
            target_individual = self.world.search_one(iri=f"*{target_individual_name}")
            property_ = self.world.search_one(iri=f"*{property_name}")
            property_[individual].append(target_individual)
            owlready2.AnnotatedRelation(
                individual, property_, target_individual
            ).isDefinedBy.append(source)

    def add_data_property_to_individual(
        self, individual_name, property_name, value, source="self"
    ):
        self.create_data_property(
            property_name=property_name,
            property_domain=self.world.search_one(iri=f"*{individual_name}")
            .is_a[0]
            .name,
            property_range=value,
            source=source,
        )

        with self.ontology:
            individual = self.world.search_one(iri=f"*{individual_name}")
            property_ = self.world.search_one(iri=f"*{property_name}")
            property_[individual].append(value)
            owlready2.AnnotatedRelation(
                individual, property_, value
            ).isDefinedBy.append(source)

    def create_agentspeak_plan(self, rule, event, context, body):
        rule_individual = self.create_individual(rule, "rule")
        self.add_data_property_to_individual(
            rule_individual.name, "rule_has_event", str(event)
        )
        self.add_data_property_to_individual(
            rule_individual.name, "rule_has_context", str(context)
        )
        for body_part in body:
            body_part = body_part.strip()
            self.add_data_property_to_individual(
                rule_individual.name, "rule_has_body", body_part
            )

        return rule_individual

    def save_ontology(self, file_path: Path):
        if file_path.exists():
            os.remove(file_path)
            print("File already exists. Overwriting.")

        self.ontology.save(file_path.resolve().as_posix())

        print(f"Output saved to {file_path.resolve()}")

    def parse_agentspeak_expressions(self, expressions):
        expressions = "\n".join(
            map(self.clean_data, expressions.split("\n"))
            # [self.clean_data(expression) for expression in expressions.split("\n")]
        )

        # Regex pattern to capture strings within the source part
        pattern = r"source\((.*?)\)"

        # Find all matches
        matches = re.findall(pattern, expressions)

        # Extract individual strings from matches
        source_strings = []
        for match in matches:
            # Remove brackets and split by comma if it's a list
            cleaned = match.strip("[]")
            if "," in cleaned:
                source_strings.extend(
                    [s.strip().strip("'") for s in cleaned.split(",")]
                )
            else:
                source_strings.append(cleaned.strip().strip("'"))

        url_or_file_uris = [
            s
            for s in set(source_strings)
            if s.startswith("http://")
            or s.startswith("https://")
            or s.startswith("file://")
        ]

        for external_source in url_or_file_uris:
            self.import_ontology(external_source)

        pattern_concepts = re.compile(
            r"^(?P<type>\w+)\((?P<elements>(?:\".*?\"|[^\"()])*)\)(?:\[source\((?P<source>\w+)\)\])?(?:\.|\n)?",
            re.MULTILINE,
        )
        matches = pattern_concepts.finditer(expressions)

        for match in matches:
            concept_type = match.group("type")
            # elements = match.group("elements").split(", ")
            elements = match.group("elements")
            elements_list = re.findall(r"\".*?\"|\'.*?\'|[^,]+", elements)
            elements = [element.strip().strip("'\"") for element in elements_list]

            source = match.group("source") if match.group("source") else "self"

            if concept_type == "concept":
                self.create_concept(elements[0], source=source)

            elif concept_type == "is_a":
                self.create_concept(elements[0], elements[1], source=source)

            elif concept_type == "object_property":
                self.create_object_property(
                    elements[1], elements[0], elements[2], source
                )

            elif concept_type == "data_property":
                self.create_data_property(elements[1], elements[0], elements[2], source)

            elif concept_type == "individual":
                self.create_individual(elements[0], elements[1], source)

            elif concept_type == "relation":
                if (
                    owlready2.DataProperty
                    in self.ontology.world.search_one(iri=f"*{elements[1]}").ancestors()
                ):
                    self.add_data_property_to_individual(
                        elements[0], elements[1], ", ".join(elements[2:]), source
                    )
                else:
                    self.add_object_property_to_individual(
                        elements[0], elements[1], elements[2], source
                    )

        pattern_plans = re.compile(
            r"(?P<event>[+\-!?]{1,2}[^.]+)\s*:\s*(?P<context>[^<-]+)\s*<-\s*(?P<body>([\S\s]*?))\.\n",
            re.DOTALL | re.MULTILINE,
        )

        matches = pattern_plans.finditer(expressions)

        for i, match in enumerate(matches, start=1):
            event = match.group("event").strip()
            pattern_whitespace = r"\s+"
            context = re.sub(pattern_whitespace, " ", match.group("context").strip())
            body = re.sub(pattern_whitespace, " ", match.group("body").strip()).split(
                ";"
            )

            self.create_agentspeak_plan(f"rule_{i}", event, context, body)

        print(f"Conversion complete.")

    # Main function to generate AgentSpeak representation
    def generate_agentspeak(self):
        # Extract information from the ontology
        self.data = self.extract_ontology_information()
        self.agentspeak_output = self.convert_ontology_information()

        if Path(self.output_data_path).resolve():
            if Path(self.output_data_path).exists():
                os.remove(self.output_data_path)
            Path(self.output_data_path).write_text(self.agentspeak_output)
            print(
                f"Conversion complete. Output saved to {Path(self.output_data_path).resolve()}"
            )
        else:
            return self.agentspeak_output

    def get_agentspeak_output(self):
        try:
            return self.prepare_response(
                status="success",
                message="Conversion complete.",
                output=self.agentspeak_output,
            )
        except Exception as e:
            return self.prepare_response(
                status="error",
                message=f"No AgentSpeak output found.\n{e}",
            )

    def prepare_response(self, **kwargs):
        self.response = {
            **kwargs,
        }

        return json.dumps(self.response, indent=4)

    def get_response(self):
        return self.response


# Run the main function
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert OWL ontology to AgentSpeak representation. Or AgentSpeak file to OWL ontology."
    )
    parser.add_argument(
        "input",
        help="Path to a file containing AgentSpeak expressions or an OWL ontology.",
        type=Path,
    )
    parser.add_argument(
        "output", help="Path to the output file.", type=Path, default=None, nargs="?"
    )
    args = parser.parse_args()

    BOWLDIConverter(args.input, args.output)