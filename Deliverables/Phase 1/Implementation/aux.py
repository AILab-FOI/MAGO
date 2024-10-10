from owlready2 import World


def clean_string(data: str) -> str:
    if not data or not isinstance(data, str):
        return data

    return data.replace(" ", "_")


def execute_sparql(world: World, query: str, parameters: list = None) -> list:
    """Execute a SPARQL query in the provided owlready2 World instance.

    Args:
        world (World): An owlready2 World instance containing the relevant data.
        query (str): The SPARQL query to be executed. Parameters are designated as `??`.
        parameters (list, optional): Parameters to be sequentially provided to the query. Defaults to None.

    Returns:
        list: The result of the query.
    """

    prepared_query = world.prepare_sparql(sparql=query)
    column_names = [name.replace("?", "") for name in prepared_query.column_names]

    query_res = prepared_query.execute(params=parameters)
    query_res = [dict(zip(column_names, result)) for result in query_res]

    return query_res


def get_related_knowledge_artefact_uris(onto_individual) -> dict:
    """Retrieves all the knowledge artefacts the individual can access.

    Args:
        onto_individual (Agent individual): The agent individual.

    Returns:
        dict: Dictionary with artefact names and URIs.
    """

    artefacts = set()
    artefacts.update(onto_individual.can_access_artefact)
    organisational_artefacts = [
        role.can_access_artefact
        for role in onto_individual.can_play_role
    ]
    artefacts.update(artefact for artefacts in organisational_artefacts for artefact in artefacts)

    artefact_names_uris = {
        artefact.has_name: artefact.has_uri
        for artefact in artefacts
        if "Knowledge" in str(artefact.is_a[0].label[0])
    }

    return artefact_names_uris
