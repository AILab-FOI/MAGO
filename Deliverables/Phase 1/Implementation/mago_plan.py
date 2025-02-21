from mago_thing import *


class Plan(Thing):
    def __init__(self, *args, **kwargs):
        super().__init__(entity_type="plan", *args, **kwargs)

    def get_plan_activity_behaviour_objective(self):
        plan_dict = {}

        plan_iri = self.onto_individual.iri

        # Get the plan name
        plan_name = (
            self.onto_individual.has_name
            if self.onto_individual.has_name
            else self.onto_individual.name
        )

        # Initialize the plan entry
        plan_entry = {"name": plan_name, "activities": {}}

        # Get the activities associated with the plan
        activities = self.onto_individual.requires_activity
        for activity in activities:
            activity_iri = activity.iri
            # Get the activity name
            activity_name = activity.has_name if activity.has_name else activity.name

            # Initialize the activity entry
            activity_entry = {"name": activity_name, "objectives": {}, "behaviours": {}}

            # Get the objectives associated with the activity
            objectives = activity.has_objective
            for objective in objectives:
                objective_iri = objective.iri
                # Get the objective name
                objective_name = (
                    objective.has_name if objective.has_name else objective.name
                )

                # Add the objective to the activity's objectives
                activity_entry["objectives"][objective_iri] = objective_name

            # Get the behaviours associated with the activity
            behaviours = activity.has_behaviour
            for behaviour in behaviours:
                behaviour_iri = behaviour.iri
                # Get the behaviour name
                behaviour_name = (
                    behaviour.has_name if behaviour.has_name else behaviour.name
                )

                # Add the behaviour to the activity's behaviours
                activity_entry["behaviours"][behaviour_iri] = behaviour_name

            # Add the activity entry to the plan's activities
            plan_entry["activities"][activity_iri] = activity_entry

        # Add the plan entry to the main dictionary
        plan_dict[plan_iri] = plan_entry

        logging.info(f"Plan {plan_name} visited.")

        return plan_dict
