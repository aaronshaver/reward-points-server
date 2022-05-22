import uuid
import json
from uuid import UUID
from .points import Points


class User:

    def __init__(self):
        self.user_id = str(uuid.uuid4())  # don't need static typing of UUID
        self.points = Points()

    def __str__(self):
        return json.dumps(self.__dict__)
