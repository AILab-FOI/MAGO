from mago_thing import *


class Process(Thing):
    def __init__(self, *args, **kwargs):
        super().__init__(entity_type="process", *args, **kwargs)

    def get_process_action_behaviour_objective(self):
        process_dict = {}

        process_iri = self.onto_individual.iri

        # Get the process name
        process_name = (
            self.onto_individual.has_name
            if self.onto_individual.has_name
            else self.onto_individual.name
        )

        # Initialize the process entry
        process_entry = {"name": process_name, "actions": {}}

        # Get the actions associated with the process
        actions = self.onto_individual.requires_action
        for action in actions:
            action_iri = action.iri
            # Get the action name
            action_name = action.has_name if action.has_name else action.name

            # Initialize the action entry
            action_entry = {"name": action_name, "objectives": {}, "behaviours": {}}

            # Get the objectives associated with the action
            objectives = action.has_objective
            for objective in objectives:
                objective_iri = objective.iri
                # Get the objective name
                objective_name = (
                    objective.has_name if objective.has_name else objective.name
                )

                # Add the objective to the action's objectives
                action_entry["objectives"][objective_iri] = objective_name

            # Get the behaviours associated with the action
            behaviours = action.has_behaviour
            for behaviour in behaviours:
                behaviour_iri = behaviour.iri
                # Get the behaviour name
                behaviour_name = (
                    behaviour.has_name if behaviour.has_name else behaviour.name
                )

                # Add the behaviour to the action's behaviours
                action_entry["behaviours"][behaviour_iri] = behaviour_name

            # Add the action entry to the process's actions
            process_entry["actions"][action_iri] = action_entry

        # Add the process entry to the main dictionary
        process_dict[process_iri] = process_entry

        logging.info(f"Process {process_name} visited.")

        return process_dict
