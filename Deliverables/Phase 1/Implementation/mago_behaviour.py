from mago_thing import *


class Behaviour(Thing):
    """A class containing all the data describing a MAGO agent behaviour. Contains all the methods and attributes common to all the behaviour types."""

    def __init__(self, cycling: bool = False, period: int = None, *args, **kwargs):
        super(Behaviour, self).__init__(entity_type="behaviour", *args, **kwargs)

        if self.onto_individual is None:
            raise ValueError("Ontology individual must be supplied.")

        self.cycling = self.onto_individual.is_repeating
        self.period = self.onto_individual.has_period
        self.behaviour_type: str = self.determine_behaviour_type()

    def determine_behaviour_type(self):
        """Determines the type of behaviour based on the ontology individual and agent attributes.

        Returns:
            str: The name of the behaviour type.
        """
        if self.onto_individual.is_before_state or self.onto_individual.is_after_state:
            return "State"
        elif self.onto_individual.has_initial_state:
            return "FSMBehaviour"
        else:
            key = (bool(self.cycling), bool(self.period))
            behaviour_mapping = {
                (False, False): "OneShotBehaviour",
                (False, True): "TimeOutBehaviour",
                (True, False): "CyclicBehaviour",
                (True, True): "PeriodicBehaviour",
            }
            return behaviour_mapping.get(key, "UnknownBehaviour")

    def get_fsm_states(self):
        states = set()
        transitions = []
        visited = set()
        initial_state = None

        initial_state = self.onto_individual.has_initial_state

        stack = list(initial_state)
        while stack:
            current_state = stack.pop()
            if current_state in visited:
                continue
            visited.add(current_state)
            states.add(current_state)

            # Get next states
            next_states = current_state.is_before_state
            transitions.extend([(current_state, ns) for ns in next_states])
            stack.extend(next_states)

        return initial_state, states, transitions

    def render_fsm_implementation(self):
        initial_state, states, transitions = self.get_fsm_states()

        implementation = []

        state_names = {}
        state_names.update(
            {
                state: (
                    clean_string(state.has_name)
                    if state.has_name
                    else clean_string(state.name)
                )
                for state in states
            }
        )

        print(state_names)

        for state in states:
            state_name = state_names.get(state)
            class_name = f"{state_name}()"
            is_initial = state in initial_state
            if is_initial:
                code_line = f"self.add_state(name='{state_name}', state={class_name}, initial=True)"
            else:
                code_line = f"self.add_state(name='{state_name}', state={class_name})"
            implementation.append(code_line)

        for source_state, dest_state in transitions:
            source_name = state_names.get(source_state)
            dest_name = state_names.get(dest_state)
            code_line = (
                f"self.add_transition(source='{source_name}', dest='{dest_name}')"
            )
            implementation.append(code_line)

        # Join the code lines into a single string
        return textwrap.indent(text="\n".join(implementation), prefix="        ")

    def prepare_behaviour_implementation_template(self):
        template = [
            """
class $name(${behaviour_type}):"""
        ]

        template.append(
            """
    async def on_start(self) -> None:
        print("Starting behaviour.")"""
        )

        template.append(
            """
    async def on_end(self) -> None:
        print("Ending behaviour.")"""
        )

        if "FSM" not in self.behaviour_type:
            template.append(
                """
    async def run(self) -> None:
        print("Running the behaviour.")"""
            )

        if "FSM" in self.behaviour_type:
            template.append(
                f"""
    async def state_setup(self):
{self.render_fsm_implementation()}
                """
            )

        return "\n".join(template)

    def render_behaviour_implementation(self):
        implementation_template = self.prepare_behaviour_implementation_template()
        self.set_implementation_template(implementation_template)
        self.render_implementation()
        implementation = self.get_implementation()
        logging.info(f"Behaviour {self.name} implementation rendered.")
        return implementation
