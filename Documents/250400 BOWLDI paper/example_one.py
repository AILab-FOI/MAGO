from bowldi import BOWLDIConverter

input_data = """
// Concepts and Hierarchies
concept(person).
concept(wizard).
is_a(wizard, person).

// Individual
individual(gandalf, wizard).

// Object Property
object_property(person, is_friend_with, person).

// Data Property
data_property(person, has_name, string)."""

converter = BOWLDIConverter(
    input_data=input_data,
)

converter.get_response()