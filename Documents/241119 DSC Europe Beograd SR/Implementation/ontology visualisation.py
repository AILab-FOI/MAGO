from owlready2 import get_ontology
from graphviz import Digraph

# Load the OWL ontology
ontology_path = "ontology.owx"  # Replace with your OWL/XML file path
onto = get_ontology(ontology_path).load()

# Initialize a Graphviz Digraph
dot = Digraph(format="png")
dot.attr(size="14,14")  # Define a square canvas
dot.attr(rankdir="BT", fontsize="10", fontname="Helvetica")  # Bottom-to-top layout
dot.attr(layout="neato")  # Use 'neato' layout for a balanced, square arrangement
dot.attr(sep="+1")
dot.attr(overlap="false")


# Add classes and subclass relationships
for cls in onto.classes():
    dot.node(cls.name, cls.name, shape="ellipse", style="filled", fillcolor="lightblue")
    for sub_cls in cls.subclasses():
        dot.edge(cls.name, sub_cls.name, label="subClassOf")

# Add object properties and their domain/range relationships
for prop in onto.object_properties():
    # dot.node(prop.name, prop.name, shape="box", style="filled", fillcolor="lightgreen")
    for domain in prop.domain:
        for range_ in prop.range:
            print(domain.name, range_.name, prop.name)
            dot.edge(domain.name, range_.name, label=prop.name)

# Add individuals and their relationships
for ind in onto.individuals():
    dot.node(ind.name, ind.name, shape="diamond", style="filled", fillcolor="plum")
    for cls in ind.is_a:
        dot.edge(ind.name, cls.name, label="instanceOf")

# Save and render the graph
output_file = "ontology_visualization"
dot.render(output_file, view=True)  # Opens the image after rendering
print(f"Ontology visualization saved as {output_file}.png")
