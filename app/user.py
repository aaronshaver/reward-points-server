import uuid
import json
from uuid import UUID
from .points import Points
from .encoder_helpers import UUIDEncoder


class User:

    def __init__(self):
        self.user_id = uuid.uuid4()
        self.points = Points()

    def __str__(self):
        return json.dumps(self.__dict__, cls=UUIDEncoder)
