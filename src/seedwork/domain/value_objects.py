

class ValueObject:
    """Base class for value objects."""

    def __post_init__(self):
        self.validate()

    def validate(self): ...
