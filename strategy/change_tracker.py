class ChangeTracker:
    def __init__(self):
        self.changed = False

    def set_changed(self):
        self.changed = True

    def is_changed(self) -> bool:
        return self.changed
