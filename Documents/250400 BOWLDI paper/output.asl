concept(wizard)[source("https://raw.githubusercontent.com/AILab-FOI/MAGO/refs/heads/main/Documents/250320%20Class/lotr_example.owl")].
is_a(wizard, person)[source("https://raw.githubusercontent.com/AILab-FOI/MAGO/refs/heads/main/Documents/250320%20Class/lotr_example.owl")].
concept(human)[source("https://raw.githubusercontent.com/AILab-FOI/MAGO/refs/heads/main/Documents/250320%20Class/lotr_example.owl")].
is_a(human, person)[source("https://raw.githubusercontent.com/AILab-FOI/MAGO/refs/heads/main/Documents/250320%20Class/lotr_example.owl")].
concept(elf)[source("https://raw.githubusercontent.com/AILab-FOI/MAGO/refs/heads/main/Documents/250320%20Class/lotr_example.owl")].
is_a(elf, person)[source("https://raw.githubusercontent.com/AILab-FOI/MAGO/refs/heads/main/Documents/250320%20Class/lotr_example.owl")].
concept(kingdom)[source("https://raw.githubusercontent.com/AILab-FOI/MAGO/refs/heads/main/Documents/250320%20Class/lotr_example.owl")].
concept(person)[source("https://raw.githubusercontent.com/AILab-FOI/MAGO/refs/heads/main/Documents/250320%20Class/lotr_example.owl")].
concept(ring)[source("https://raw.githubusercontent.com/AILab-FOI/MAGO/refs/heads/main/Documents/250320%20Class/lotr_example.owl")].
concept(dwarf)[source("https://raw.githubusercontent.com/AILab-FOI/MAGO/refs/heads/main/Documents/250320%20Class/lotr_example.owl")].
is_a(dwarf, person)[source("https://raw.githubusercontent.com/AILab-FOI/MAGO/refs/heads/main/Documents/250320%20Class/lotr_example.owl")].
concept(hobbit)[source("https://raw.githubusercontent.com/AILab-FOI/MAGO/refs/heads/main/Documents/250320%20Class/lotr_example.owl")].
is_a(hobbit, person)[source("https://raw.githubusercontent.com/AILab-FOI/MAGO/refs/heads/main/Documents/250320%20Class/lotr_example.owl")].
object_property(person, is_friend_with, person)[source("https://raw.githubusercontent.com/AILab-FOI/MAGO/refs/heads/main/Documents/250320%20Class/lotr_example.owl")].
object_property(kingdom, has_king, person)[source("https://raw.githubusercontent.com/AILab-FOI/MAGO/refs/heads/main/Documents/250320%20Class/lotr_example.owl")].
object_property(person, is_in_team_with, person)[source("https://raw.githubusercontent.com/AILab-FOI/MAGO/refs/heads/main/Documents/250320%20Class/lotr_example.owl")].
object_property(person, has_ring, ring)[source("https://raw.githubusercontent.com/AILab-FOI/MAGO/refs/heads/main/Documents/250320%20Class/lotr_example.owl")].
object_property(person, fights_against, person)[source("https://raw.githubusercontent.com/AILab-FOI/MAGO/refs/heads/main/Documents/250320%20Class/lotr_example.owl")].
data_property(person, has_name, str)[source("https://raw.githubusercontent.com/AILab-FOI/MAGO/refs/heads/main/Documents/250320%20Class/lotr_example.owl")].
data_property(ring, description, str)[source("https://raw.githubusercontent.com/AILab-FOI/MAGO/refs/heads/main/Documents/250320%20Class/lotr_example.owl")].
individual(gandalf_the_grey, wizard)[source("self")].
individual(aragorn_son_of_arathorn, human)[source("self")].
individual(legolas, elf)[source("self")].
relation(gandalf_the_grey, has_name, "Gandalf the Grey")[source("Bogdan")].
relation(gandalf_the_grey, has_name, "Mithrandir")[source("self")].
relation(aragorn_son_of_arathorn, is_friend_with, gandalf_the_grey)[source("self")].
relation(aragorn_son_of_arathorn, is_friend_with, legolas)[source("self")].
relation(aragorn_son_of_arathorn, has_name, "Aragorn, son of Arathorn")[source("self")].
relation(legolas, has_name, "Legolas Greenleaf")[source("self")].