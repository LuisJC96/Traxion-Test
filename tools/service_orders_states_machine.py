
class ServiceOrderStatesMachine:
    def __init__(self):
        self.states = [
            'OPEN',
            'ASSIGNED',
            'IN_PROGRESS',
            'ON_HOLD',
            'COMPLETED',
            'CANCELLED'
        ]

        self.valid_transitions = {
            'OPEN': ['OPEN','ASSIGNED', 'CANCELLED'],
            'ASSIGNED': ['ASSIGNED','IN_PROGRESS', 'CANCELLED'],
            'IN_PROGRESS': ['IN_PROGRESS','ON_HOLD', 'COMPLETED', 'CANCELLED'],
            'ON_HOLD': ['ON_HOLD', 'IN_PROGRESS', 'CANCELLED'],
            'COMPLETED': [],
            'CANCELLED': [],
        }

    def validate_transition(self, actual_state, desired_state):
        if desired_state not in self.valid_transitions[actual_state]:
            return False
        return True
