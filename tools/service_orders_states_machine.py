
class ServiceOrderStatesMachine:
    def __init__(self):
        self.states = [
            'open',
            'assigned',
            'in_progress',
            'on_hold',
            'completed',
            'cancelled'
        ]

        self.valid_transitions = {
            'new': ['new','assigned', 'cancelled'],
            'assigned': ['assigned','in_progress', 'cancelled'],
            'in_progress': ['in_progress','on_hold', 'completed', 'cancelled'],
            'on_hold': ['on_hold', 'in_progress', 'cancelled'],
            'completed': [],
            'cancelled': [],
        }

    def validate_transition(self, actual_state, desired_state):
        if desired_state not in self.valid_transitions[actual_state]:
            return False
        return True
