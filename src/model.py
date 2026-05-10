"""
Model rynkowy typu ABM (Kirman 1993).
Zarządza populacją agentów i dynamiką ceny bez przestrzeni 2D.
"""

from mesa import Model
from mesa.datacollection import DataCollector
from agents import Investor

class MarketModel(Model):
    """Główna klasa symulacji."""

    def __init__(
        self,
        population_size=200,
        epsilon=0.01,
        delta=0.05,
        alpha=0.5,
        seed=None,
    ):
        super().__init__(seed=seed)
        self.population_size = population_size
        self.epsilon = epsilon
        self.delta = delta
        self.alpha = alpha
        
        self.price = 1000.0

        # Tworzenie agentów bez umieszczania ich na siatce
        for _ in range(self.population_size):
            Investor(self)

        # Kolektor danych dla wykresów
        self.datacollector = DataCollector(
            model_reporters={
                "Cena": lambda m: m.price,
                "Optymiści": lambda m: sum(1 for a in m.agents if a.state == 1),
                "Pesymiści": lambda m: sum(1 for a in m.agents if a.state == 0),
            }
        )
        self.datacollector.collect(self)

    def trigger_shock(self):
        """Metoda wywołująca krach: 40% agentów staje się pesymistami."""
        shock_size = int(self.population_size * 0.4)
        chosen_agents = self.random.sample(list(self.agents), shock_size)
        for agent in chosen_agents:
            agent.state = 0
        self.update_price()
        self.datacollector.collect(self)

    def update_price(self):
        """Mechanizm ceny: P(t+1) = P(t) + alpha * (N_opt - N_pes)"""
        n_opt = sum(1 for a in self.agents if a.state == 1)
        n_pes = self.population_size - n_opt
        self.price += self.alpha * (n_opt - n_pes)
        if self.price < 0:
            self.price = 0.0

    def step(self):
        """Krok symulacji."""
        self.agents.shuffle_do("step")
        self.update_price()
        self.datacollector.collect(self)