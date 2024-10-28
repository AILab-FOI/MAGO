import spade
from Agent_Factory_Agent import *
from Agent_Recipe_Agent import *


async def main():
    agent_individuals = {}
    agent = Factory_Agent("Osijek@localhost", "tajna")
    agent.uri = "http://dragon.foi.hr/mago-a.owx#OWLNamedIndividual_d910535c_5b5e_4af4_b95f_e6dab7023ddd"
    agent.knowledge_artefact_uris = {'Personal knowledge': 'https://ai.foi.hr/PersonalOntology.owx', 'The other ontology': 'https://ai.foi.hr/MAGO-Ag.owx'}
    agent.available_roles_and_behaviours = {'http://dragon.foi.hr/mago-a.owx#OWLNamedIndividual_3a6da667_46f7_421b_84b9_afdae9406a3b': {'name': 'Service provider', 'behaviours': {}}, 'http://dragon.foi.hr/mago-a.owx#OWLNamedIndividual_caa11e73_a20b_4e88_8068_63ae9cfe2e4c': {'name': 'Scout', 'behaviours': {'http://dragon.foi.hr/mago-a.owx#OWLNamedIndividual_c17807e1_7a97_4b2c_b0ef_354af3ac8e55': 'Receive messages', 'http://dragon.foi.hr/mago-a.owx#OWLNamedIndividual_cedc48c8_e579_4079_abbb_a9ba8a420fcd': 'Send message'}}}
    agent.system_features = None
    agent_individuals.setdefault("localhost", {}).update({"Osijek": agent})
    agent = Factory_Agent("Rijeka@localhost", "tajna")
    agent.uri = "http://dragon.foi.hr/mago-a.owx#OWLNamedIndividual_f892df91_9c0d_4345_9dcd_e7aa86062631"
    agent.knowledge_artefact_uris = {'The other ontology': 'https://ai.foi.hr/MAGO-Ag.owx'}
    agent.available_roles_and_behaviours = {'http://dragon.foi.hr/mago-a.owx#OWLNamedIndividual_3a6da667_46f7_421b_84b9_afdae9406a3b': {'name': 'Service provider', 'behaviours': {}}, 'http://dragon.foi.hr/mago-a.owx#OWLNamedIndividual_caa11e73_a20b_4e88_8068_63ae9cfe2e4c': {'name': 'Scout', 'behaviours': {'http://dragon.foi.hr/mago-a.owx#OWLNamedIndividual_c17807e1_7a97_4b2c_b0ef_354af3ac8e55': 'Receive messages', 'http://dragon.foi.hr/mago-a.owx#OWLNamedIndividual_cedc48c8_e579_4079_abbb_a9ba8a420fcd': 'Send message'}}}
    agent.system_features = None
    agent_individuals.setdefault("localhost", {}).update({"Rijeka": agent})
    agent = Factory_Agent("Zagreb@localhost", "tajna")
    agent.uri = "http://dragon.foi.hr/mago-a.owx#Broj%20jedan"
    agent.knowledge_artefact_uris = {'Personal knowledge': 'https://ai.foi.hr/PersonalOntology.owx', 'Main ontology': 'https://raw.githubusercontent.com/AILab-FOI/MAGO/main/Deliverables/Phase%201/Implementation/MAGO-Ag.owx', 'The other ontology': 'https://ai.foi.hr/MAGO-Ag.owx'}
    agent.available_roles_and_behaviours = {'http://dragon.foi.hr/mago-a.owx#OWLNamedIndividual_3a6da667_46f7_421b_84b9_afdae9406a3b': {'name': 'Service provider', 'behaviours': {}}, 'http://dragon.foi.hr/mago-a.owx#OWLNamedIndividual_caa11e73_a20b_4e88_8068_63ae9cfe2e4c': {'name': 'Scout', 'behaviours': {'http://dragon.foi.hr/mago-a.owx#OWLNamedIndividual_c17807e1_7a97_4b2c_b0ef_354af3ac8e55': 'Receive messages', 'http://dragon.foi.hr/mago-a.owx#OWLNamedIndividual_cedc48c8_e579_4079_abbb_a9ba8a420fcd': 'Send message'}}}
    agent.system_features = {'money': 100, 'recipe': [2, 3, 9]}
    agent_individuals.setdefault("localhost", {}).update({"Zagreb": agent})
    agent = Recipe_Agent("Recipe_003@localhost", "tajna")
    agent.uri = "http://dragon.foi.hr/mago-a.owx#OWLNamedIndividual_12c619ee_d747_4d66_8165_25991df28f70"
    agent.knowledge_artefact_uris = {'Personal knowledge': 'https://ai.foi.hr/PersonalOntology.owx', 'Main ontology': 'https://raw.githubusercontent.com/AILab-FOI/MAGO/main/Deliverables/Phase%201/Implementation/MAGO-Ag.owx', 'The other ontology': 'https://ai.foi.hr/MAGO-Ag.owx'}
    agent.available_roles_and_behaviours = {'http://dragon.foi.hr/mago-a.owx#OWLNamedIndividual_83d43aa5_243d_4472_8111_16f642b55228': {'name': 'Warrior', 'behaviours': {'http://dragon.foi.hr/mago-a.owx#OWLNamedIndividual_7bdd32fb_271c_4f2c_aafd_d20c74aa22b9': 'Produce part'}}, 'http://dragon.foi.hr/mago-a.owx#OWLNamedIndividual_caa11e73_a20b_4e88_8068_63ae9cfe2e4c': {'name': 'Scout', 'behaviours': {'http://dragon.foi.hr/mago-a.owx#OWLNamedIndividual_c17807e1_7a97_4b2c_b0ef_354af3ac8e55': 'Receive messages', 'http://dragon.foi.hr/mago-a.owx#OWLNamedIndividual_cedc48c8_e579_4079_abbb_a9ba8a420fcd': 'Send message'}}}
    agent.system_features = None
    agent_individuals.setdefault("localhost", {}).update({"Recipe_003": agent})
    agent = Recipe_Agent("Recipe_001@localhost", "tajna")
    agent.uri = "http://dragon.foi.hr/mago-a.owx#OWLNamedIndividual_9e8b35f2_d0ca_42f0_82dd_5dd72cf9e7c4"
    agent.knowledge_artefact_uris = {'The other ontology': 'https://ai.foi.hr/MAGO-Ag.owx'}
    agent.available_roles_and_behaviours = {'http://dragon.foi.hr/mago-a.owx#OWLNamedIndividual_caa11e73_a20b_4e88_8068_63ae9cfe2e4c': {'name': 'Scout', 'behaviours': {'http://dragon.foi.hr/mago-a.owx#OWLNamedIndividual_c17807e1_7a97_4b2c_b0ef_354af3ac8e55': 'Receive messages', 'http://dragon.foi.hr/mago-a.owx#OWLNamedIndividual_cedc48c8_e579_4079_abbb_a9ba8a420fcd': 'Send message'}}}
    agent.system_features = None
    agent_individuals.setdefault("localhost", {}).update({"Recipe_001": agent})
    agent = Recipe_Agent("Recipe_002@localhost", "tajna")
    agent.uri = "http://dragon.foi.hr/mago-a.owx#r9lwurkbsftwsmlpcoplgzt1"
    agent.knowledge_artefact_uris = {'Main ontology': 'https://raw.githubusercontent.com/AILab-FOI/MAGO/main/Deliverables/Phase%201/Implementation/MAGO-Ag.owx', 'The other ontology': 'https://ai.foi.hr/MAGO-Ag.owx'}
    agent.available_roles_and_behaviours = {'http://dragon.foi.hr/mago-a.owx#OWLNamedIndividual_83d43aa5_243d_4472_8111_16f642b55228': {'name': 'Warrior', 'behaviours': {'http://dragon.foi.hr/mago-a.owx#OWLNamedIndividual_7bdd32fb_271c_4f2c_aafd_d20c74aa22b9': 'Produce part'}}, 'http://dragon.foi.hr/mago-a.owx#OWLNamedIndividual_caa11e73_a20b_4e88_8068_63ae9cfe2e4c': {'name': 'Scout', 'behaviours': {'http://dragon.foi.hr/mago-a.owx#OWLNamedIndividual_c17807e1_7a97_4b2c_b0ef_354af3ac8e55': 'Receive messages', 'http://dragon.foi.hr/mago-a.owx#OWLNamedIndividual_cedc48c8_e579_4079_abbb_a9ba8a420fcd': 'Send message'}}}
    agent.system_features = None
    agent_individuals.setdefault("localhost", {}).update({"Recipe_002": agent})
    for agent in [agent for host_dict in agent_individuals.values() for agent in host_dict.values()]:
        agent.plan_action_behaviour_objective = {'http://dragon.foi.hr/mago-a.owx#OWLNamedIndividual_4ce555df_0daa_451c_8cee_3869fb46f599': {'name': 'Produce plan', 'actions': {'http://dragon.foi.hr/mago-a.owx#OWLNamedIndividual_395d25cd_dd02_43da_9c3e_c558a17cf629': {'name': 'Request service', 'objectives': {'http://dragon.foi.hr/mago-a.owx#OWLNamedIndividual_644f18d0_b719_4ce3_9f18_5ed00cfaf3e7': 'Request service'}, 'behaviours': {'http://dragon.foi.hr/mago-a.owx#OWLNamedIndividual_44e0578c_c818_4c97_a1cf_081d31543933': 'Request service'}}, 'http://dragon.foi.hr/mago-a.owx#OWLNamedIndividual_a5438295_391f_4d36_b6f9_b163ade1b2e5': {'name': 'Find service', 'objectives': {'http://dragon.foi.hr/mago-a.owx#OWLNamedIndividual_5ea5abf1_cf9f_4fe0_8842_25b90ea7beac': 'Find service'}, 'behaviours': {'http://dragon.foi.hr/mago-a.owx#OWLNamedIndividual_77064793_551f_4645_8bc4_7d69c3908246': 'Find service'}}, 'http://dragon.foi.hr/mago-a.owx#OWLNamedIndividual_af1dbcdc_a9f4_4c0d_87b1_ecb111fca6ea': {'name': 'Consume service', 'objectives': {'http://dragon.foi.hr/mago-a.owx#OWLNamedIndividual_d37cd96b_e3f8_41e6_860a_821b97903d66': 'Consume service'}, 'behaviours': {'http://dragon.foi.hr/mago-a.owx#OWLNamedIndividual_d422ba16_c564_422e_bca8_9e793add1c0b': 'Consume service'}}}}, 'http://dragon.foi.hr/mago-a.owx#OWLNamedIndividual_df91a3a0_7a62_46fb_ac02_75dde4d82493': {'name': 'Manufacturing Plan', 'actions': {'http://dragon.foi.hr/mago-a.owx#OWLNamedIndividual_42465976_d81c_4bd1_8ed9_6a94dbd2958f': {'name': 'Communicate', 'objectives': {'http://dragon.foi.hr/mago-a.owx#OWLNamedIndividual_1db58781_1969_4eb6_8b3c_24f81f921806': 'OWLNamedIndividual_1db58781_1969_4eb6_8b3c_24f81f921806', 'http://dragon.foi.hr/mago-a.owx#OWLNamedIndividual_ab6715e3_2bf2_4b4e_a00a_45a0ae4a8428': 'OWLNamedIndividual_ab6715e3_2bf2_4b4e_a00a_45a0ae4a8428'}, 'behaviours': {'http://dragon.foi.hr/mago-a.owx#OWLNamedIndividual_c17807e1_7a97_4b2c_b0ef_354af3ac8e55': 'Receive messages', 'http://dragon.foi.hr/mago-a.owx#OWLNamedIndividual_cedc48c8_e579_4079_abbb_a9ba8a420fcd': 'Send message'}}}}}
        await agent.start()

spade.run(main())