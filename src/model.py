from mesa import Model
from mesa.datacollection import DataCollector
from agents import Investor

class MarketModel(Model):
    def __init__(self, population_size=100, epsilon=0.01, delta=0.02, alpha=0.5, seed=None):
        super().__init__(seed=seed)
        self.population_size = population_size
        self.epsilon = epsilon
        self.delta = delta
        self.alpha = alpha
        self.price = 1000.0

        for _ in range(self.population_size):
            Investor(self)

        self.datacollector = DataCollector(
            model_reporters={
                "Price": lambda m: m.price,
                "Optimists": lambda m: sum(1 for a in m.agents if a.state == 1),
                "Pessimists": lambda m: sum(1 for a in m.agents if a.state == 0),
            }
        )
        # Initial data collection
        self.datacollector.collect(self)

    def trigger_shock(self):
        """Forces panic (state 0) in 40% of the population."""
        shock_size = int(self.population_size * 0.4)
        chosen_agents = self.random.sample(list(self.agents), shock_size)
        for agent in chosen_agents:
            agent.state = 0
        self.update_price()

    def trigger_optimism(self):
        """Forces euphoria (state 1) in 40% of the population."""
        surge_size = int(self.population_size * 0.4)
        chosen_agents = self.random.sample(list(self.agents), surge_size)
        for agent in chosen_agents:
            agent.state = 1
        self.update_price()

    def update_price(self):
        """Updates the price based on sentiment."""
        n_opt = sum(1 for a in self.agents if a.state == 1)
        n_pes = self.population_size - n_opt
        self.price += self.alpha * (n_opt - n_pes)
        if self.price < 0: 
            self.price = 0.0

    def step(self):
        """Simulation step."""
        self.agents.shuffle_do("step")
        self.update_price()
        self.datacollector.collect(self)
