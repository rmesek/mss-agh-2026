"""
Model rynkowy typu ABM (Kirman 1993).
Dodano funkcje wyzwalania euforii (optimism).
"""

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
                "Cena": lambda m: m.price,
                "Optymiści": lambda m: sum(1 for a in m.agents if a.state == 1),
                "Pesymiści": lambda m: sum(1 for a in m.agents if a.state == 0),
            }
        )
        self.datacollector.collect(self)

    def trigger_shock(self):
        """Wymusza panikę (stan 0) u 40% populacji."""
        shock_size = int(self.population_size * 0.4)
        chosen_agents = self.random.sample(list(self.agents), shock_size)
        for agent in chosen_agents:
            agent.state = 0
        self.update_price()
        self.datacollector.collect(self)

    def trigger_optimism(self):
        """Wymusza euforię (stan 1) u 40% populacji."""
        surge_size = int(self.population_size * 0.4)
        chosen_agents = self.random.sample(list(self.agents), surge_size)
        for agent in chosen_agents:
            agent.state = 1
        self.update_price()
        self.datacollector.collect(self)

    def update_price(self):
        n_opt = sum(1 for a in self.agents if a.state == 1)
        n_pes = self.population_size - n_opt
        self.price += self.alpha * (n_opt - n_pes)
        if self.price < 0: self.price = 0.0

    def step(self):
        self.agents.shuffle_do("step")
        self.update_price()
        self.datacollector.collect(self)