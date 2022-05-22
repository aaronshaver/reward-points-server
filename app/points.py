from collections import defaultdict


class Points:

    def __init__(self):
        # {"payer_name": points (int)}
        self.payer_points = defaultdict(lambda: 0)

        # [Transaction]
        self.transactions = defaultdict(lambda: [])
