class StateItem():
    # Item which holds the data from a dict as attributes of the object.
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


def history_callback(current_state, show_from, show_count, target_time):
    show_limit = show_from + show_count
    if current_state.iteration >= show_from and current_state.iteration <= show_limit:
        return current_state
    if target_time == current_state.iteration:
        return current_state
    return None
