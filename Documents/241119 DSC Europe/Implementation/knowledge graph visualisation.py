from graphviz import Digraph

# Initialize a directed graph
dot = Digraph(format="png")
dot.attr(size="14,14")  # Define a square canvas
dot.attr(layout="neato")  # Use 'neato' layout for a balanced, square arrangement
dot.attr(overlap="false")
# dot.attr(sep="-5")

# Define nodes and relationships
characters = {
    "Hobbits": ["Frodo", "Samwise", "Merry", "Pippin"],
    "Elf": ["Legolas"],
    "Humans": ["Aragorn", "Boromir"],
    "Dwarf": ["Gimli"],
    "Wizard": ["Gandalf"],
}

titles = {
    "Frodo": "Ring-bearer",
    "Samwise": "Gardener",
    "Merry": "Knight of Rohan",
    "Pippin": "Guard of Gondor",
    "Legolas": "Prince of Mirkwood",
    "Aragorn": "King of Gondor",
    "Boromir": "Captain of Gondor",
    "Gimli": "Warrior",
    "Gandalf": "Wizard",
}

weapons = {
    "Frodo": "Sting",
    "Samwise": "Sword",
    "Merry": "Sword",
    "Pippin": "Sword",
    "Legolas": "Bow",
    "Aragorn": "Andúril",
    "Boromir": "Sword and Shield",
    "Gimli": "Axe",
    "Gandalf": "Staff and Glamdring",
}

origins = {
    "Frodo": "Shire",
    "Samwise": "Shire",
    "Merry": "Shire",
    "Pippin": "Shire",
    "Legolas": "Mirkwood",
    "Aragorn": "Dúnedain",
    "Boromir": "Gondor",
    "Gimli": "Lonely Mountain",
    "Gandalf": "Valinor",
}

# Add character nodes and their group labels
for group, members in characters.items():
    dot.node(group, shape="box", style="filled", color="skyblue")
    for name in members:
        dot.node(name, shape="ellipse", style="filled", color="lightgreen")
        dot.edge(group, name)

# Add titles, weapons, and origins as separate concepts
for character, title in titles.items():
    dot.node(title, shape="diamond", style="filled", color="lightcoral")
    dot.edge(character, title)

for character, weapon in weapons.items():
    dot.node(weapon, shape="hexagon", style="filled", color="gold")
    dot.edge(character, weapon)

for character, origin in origins.items():
    dot.node(origin, shape="circle", style="filled", color="plum")
    dot.edge(character, origin)

dot.node("Race", shape="box", style="filled", color="blue")
for character in characters.keys():
    dot.edge("Race", character)

# Render the graph
dot.render("lotr_taxonomy_square", view=True)
