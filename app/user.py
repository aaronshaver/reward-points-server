import uuid
import json
from collections import defaultdict


class User:

    def __init__(self):
        self.user_id = str(uuid.uuid4())  # don't need full UUID type
        self.payer_points = defaultdict(lambda: 0)  # {"payer": points (int)}
        self.transactions = []  # [Transaction]

    def __str__(self):
        return json.dumps(self.__dict__)
