import uuid
import json
from uuid import UUID


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return str(obj)
        return json.JSONEncoder.default(self, obj)

class User:

    def __init__(self):
        self.user_id = uuid.uuid4()

    def __str__(self):
        return json.dumps(self.__dict__, cls=UUIDEncoder)