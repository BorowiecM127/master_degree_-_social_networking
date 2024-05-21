"""
Agent class
"""


class Agent:
    """
    Agent class, contains network agent's attributes
    """

    influence: float
    flexibility: float
    opinion: list[float]

    def __init__(
        self, influence: float, flexibility: float, opinion: list[float]
    ) -> None:
        """
        Initializes an instance of the Agent class with the given influence, flexibility, and opinion.

        Parameters:
            influence (float): The influence of the agent.
            flexibility (float): The flexibility of the agent.
            opinion (list[float]): The opinion of the agent.

        Returns:
            None
        """
        self.influence = influence
        self.flexibility = flexibility
        self.opinion = opinion
