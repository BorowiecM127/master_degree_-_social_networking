class Agent:
    influence: float
    flexibility: float
    opinion: list[float]

    def __init__(self, influence, flexibility, opinion):
        self.influence = influence
        self.flexibility = flexibility
        self.opinion = opinion
