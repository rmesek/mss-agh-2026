from mesa import Agent

class Investor(Agent):
    """Market agent making decisions based on herding."""

    def __init__(self, model):
        super().__init__(model)
        # Initial state: 1 (Optimist), 0 (Pessimist)
        self.state = self.random.choice([0, 1])

    def step(self):
        """Agent's decision step."""
        epsilon = self.model.epsilon
        delta = self.model.delta

        r = self.random.random()

        # 1. Innovation (independent change of mind with probability ε)
        if r < epsilon:
            self.state = 1 - self.state
        
        # 2. Imitation (fetching state from another agent with probability 1 - δ)
        elif r < epsilon + (1 - delta):
            random_agent = self.random.choice(list(self.model.agents))
            self.state = random_agent.state
