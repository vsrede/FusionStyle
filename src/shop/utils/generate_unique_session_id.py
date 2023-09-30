import uuid


def generate_unique_session_id():
    return str(uuid.uuid4())
