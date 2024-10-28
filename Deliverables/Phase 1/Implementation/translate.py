import os
import argparse
from owlready2 import World, Ontology, onto_path, set_render_func, sync_reasoner
from mago_workspace import Workspace


def render_using_label(entity):
    return entity.label.first() or entity.name


def render_using_iri(entity):
    return entity.iri


def main(ontology_name="MAGO-Ag.owx"):
    onto_path.append(os.getcwd())

    mago_world = World()
    onto: Ontology = mago_world.get_ontology(ontology_name).load(reload=True)

    set_render_func(render_using_label)

    sync_reasoner()

    template_folder = os.path.join(os.getcwd(), "Template")
    if not os.path.exists(template_folder):
        os.makedirs(template_folder)

    aMAGOWorld = Workspace(ontology=onto, name="World")
    aMAGOWorld.write_implementation_to_disk()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="MAGO-Ag ontology translation framework"
    )
    parser.add_argument(
        "-o",
        "--ontology-name",
        type=str,
        default="MAGO-Ag.owx",
        help="Optional name of the ontology file to be used, string argument with default value 'MAGO-Ag.owx'",
    )

    args = parser.parse_args()
    main(args.ontology_name)
