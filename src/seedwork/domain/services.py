import uuid


def next_id() -> uuid.UUID:
    return uuid.uuid4()
