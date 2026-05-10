"""
Agent inwestora dla modelu Kirmana (1993).
Logika: Innowacja (epsilon) i Naśladownictwo (1 - delta).
"""

from mesa import Agent

class Investor(Agent):
    """Agent rynkowy podejmujący decyzje w oparciu o herding."""

    def __init__(self, model):
        super().__init__(model)
        # Początkowy stan: 1 (Optymista), 0 (Pesymista)
        self.state = self.random.choice([0, 1])

    def step(self):
        """Krok decyzyjny agenta."""
        epsilon = self.model.epsilon
        delta = self.model.delta

        r = self.random.random()

        # 1. Innowacja (niezależna zmiana zdania z prawdopodobieństwem ε)
        if r < epsilon:
            self.state = 1 - self.state
        
        # 2. Naśladownictwo (pobranie stanu od innego agenta z prawdopodobieństwem 1 - δ)
        elif r < epsilon + (1 - delta):
            random_agent = self.random.choice(list(self.model.agents))
            self.state = random_agent.state