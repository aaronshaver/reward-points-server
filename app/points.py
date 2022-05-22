class Points:

    def __init__(self):
        # {"payer_name": 100}
        self.payer_points = {}
        # {"payer_name": [{transaction},{transaction}]}
        self.transactions = {}
