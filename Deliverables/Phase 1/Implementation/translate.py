import os
from owlready2 import World, Ontology, onto_path, set_render_func, sync_reasoner
from mago_world import World as MAGO_World


def render_using_label(entity):
    return entity.label.first() or entity.name


def render_using_iri(entity):
    return entity.iri


def main():
    onto_path.append(os.getcwd())
    # print(onto_path)

    mago_world = World()
    onto: Ontology = mago_world.get_ontology("MAGO-Ag.owx").load(reload=True)

    set_render_func(render_using_label)

    sync_reasoner()

    template_folder = os.path.join(os.getcwd(), "Template")
    if not os.path.exists(template_folder):
        os.makedirs(template_folder)

    aMAGOWorld = MAGO_World(ontology=onto, name="World")
    aMAGOWorld.write_implementation_to_disk()


if __name__ == "__main__":
    main()
