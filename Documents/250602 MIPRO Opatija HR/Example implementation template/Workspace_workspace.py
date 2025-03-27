import spade
from Agent_Agent_Farmer import *
from Agent_Agent_Drone import *


async def main():
    agent_individuals = {}
    agent = Agent_Farmer("Beatriz@localhost", "secret")
    agent.uri = "https://raw.githubusercontent.com/AILab-FOI/MAGO/refs/heads/main/Documents/2506%20MIPRO/example.owx#OWLNamedIndividual_cf4d7c8a_5cd2_4f78_90b7_4350e310e08e"
    agent.knowledge_artefact_uris = {'Crop growth knowledge': 'https://example.com/crop-growth.owx'}
    agent.available_roles_and_behaviours = {'https://raw.githubusercontent.com/AILab-FOI/MAGO/refs/heads/main/Documents/2506%20MIPRO/example.owx#OWLNamedIndividual_2c03a469_e5f6_4457_88fd_ea52baa92d90': {'name': 'Field manager', 'behaviours': {'https://raw.githubusercontent.com/AILab-FOI/MAGO/refs/heads/main/Documents/2506%20MIPRO/example.owx#OWLNamedIndividual_4a3838ca_d779_4bae_96fb_414192faacfe': 'Task planning behaviour'}}, 'https://raw.githubusercontent.com/AILab-FOI/MAGO/refs/heads/main/Documents/2506%20MIPRO/example.owx#OWLNamedIndividual_a35965ca_0692_4e10_9aae_2b6623493223': {'name': 'Agronomist', 'behaviours': {'https://raw.githubusercontent.com/AILab-FOI/MAGO/refs/heads/main/Documents/2506%20MIPRO/example.owx#OWLNamedIndividual_4a3838ca_d779_4bae_96fb_414192faacfe': 'Task planning behaviour', 'https://raw.githubusercontent.com/AILab-FOI/MAGO/refs/heads/main/Documents/2506%20MIPRO/example.owx#OWLNamedIndividual_4da682c1_d958_4515_a6b7_9ea1f6b3c440': None}}}
    agent.system_features = None
    agent_individuals.setdefault("localhost", {}).update({"Beatriz": agent})
    agent = Agent_Farmer("Antonio@localhost", "secret")
    agent.uri = "https://raw.githubusercontent.com/AILab-FOI/MAGO/refs/heads/main/Documents/2506%20MIPRO/example.owx#OWLNamedIndividual_d4ea876c_7bcc_465c_a63c_7feaf7e18b78"
    agent.knowledge_artefact_uris = {'Local weather knowledge': './weather.owx'}
    agent.available_roles_and_behaviours = {'https://raw.githubusercontent.com/AILab-FOI/MAGO/refs/heads/main/Documents/2506%20MIPRO/example.owx#OWLNamedIndividual_a35965ca_0692_4e10_9aae_2b6623493223': {'name': 'Agronomist', 'behaviours': {'https://raw.githubusercontent.com/AILab-FOI/MAGO/refs/heads/main/Documents/2506%20MIPRO/example.owx#OWLNamedIndividual_4a3838ca_d779_4bae_96fb_414192faacfe': 'Task planning behaviour', 'https://raw.githubusercontent.com/AILab-FOI/MAGO/refs/heads/main/Documents/2506%20MIPRO/example.owx#OWLNamedIndividual_4da682c1_d958_4515_a6b7_9ea1f6b3c440': None}}}
    agent.system_features = {'location': {'x': 42, 'y': 13}, 'prompt': 'You are a farmer with the knowledge of the local weather working on a farm with several colleague farmers and a couple of drones at your disposal.'}
    agent_individuals.setdefault("localhost", {}).update({"Antonio": agent})
    agent = Agent_Drone("Drone_002@localhost", "secret")
    agent.uri = "https://raw.githubusercontent.com/AILab-FOI/MAGO/refs/heads/main/Documents/2506%20MIPRO/example.owx#OWLNamedIndividual_c22d49d5_7dc1_472e_a3c2_63fbee4509d0"
    agent.knowledge_artefact_uris = {}
    agent.available_roles_and_behaviours = {'https://raw.githubusercontent.com/AILab-FOI/MAGO/refs/heads/main/Documents/2506%20MIPRO/example.owx#OWLNamedIndividual_5e0fbf47_0d58_4c8e_848d_6323c50fe5a1': {'name': 'Surveyor', 'behaviours': {'https://raw.githubusercontent.com/AILab-FOI/MAGO/refs/heads/main/Documents/2506%20MIPRO/example.owx#OWLNamedIndividual_e159d657_91bf_4f28_8f92_f2b5dbc6550a': 'Navigation behaviour', 'https://raw.githubusercontent.com/AILab-FOI/MAGO/refs/heads/main/Documents/2506%20MIPRO/example.owx#OWLNamedIndividual_e5a6ab40_d803_4b60_8c3f_59f4e0e6cdcd': 'Aerial survey behaviour'}}}
    agent.system_features = None
    agent_individuals.setdefault("localhost", {}).update({"Drone_002": agent})
    agent = Agent_Drone("Drone_001@localhost", "secret")
    agent.uri = "https://raw.githubusercontent.com/AILab-FOI/MAGO/refs/heads/main/Documents/2506%20MIPRO/example.owx#OWLNamedIndividual_d85cd524_e1b2_4b91_ab4f_4685a12bd3ad"
    agent.knowledge_artefact_uris = {}
    agent.available_roles_and_behaviours = {'https://raw.githubusercontent.com/AILab-FOI/MAGO/refs/heads/main/Documents/2506%20MIPRO/example.owx#OWLNamedIndividual_5e0fbf47_0d58_4c8e_848d_6323c50fe5a1': {'name': 'Surveyor', 'behaviours': {'https://raw.githubusercontent.com/AILab-FOI/MAGO/refs/heads/main/Documents/2506%20MIPRO/example.owx#OWLNamedIndividual_e159d657_91bf_4f28_8f92_f2b5dbc6550a': 'Navigation behaviour', 'https://raw.githubusercontent.com/AILab-FOI/MAGO/refs/heads/main/Documents/2506%20MIPRO/example.owx#OWLNamedIndividual_e5a6ab40_d803_4b60_8c3f_59f4e0e6cdcd': 'Aerial survey behaviour'}}}
    agent.system_features = None
    agent_individuals.setdefault("localhost", {}).update({"Drone_001": agent})
    for agent in [agent for host_dict in agent_individuals.values() for agent in host_dict.values()]:
        agent.plan_activity_behaviour_objective = {}
        await agent.start()

spade.run(main())