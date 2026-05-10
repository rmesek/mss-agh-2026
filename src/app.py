"""
Interfejs Solara z ulepszonymi, stabilnymi wykresami Matplotlib.
Oba wykresy mają teraz spójny wygląd i stałe ramy.
"""

import solara
import matplotlib.figure as figure
from model import MarketModel
from mesa.visualization import Slider, SolaraViz

# 1. Konfiguracja parametrów modelu
model_params = {
    "population_size": Slider("Liczba Inwestorów (N)", 200, 50, 1000, 50),
    "epsilon": Slider("Innowacja (ε)", 0.01, 0.001, 0.1, 0.001),
    "delta": Slider("Naśladownictwo (δ)", 0.05, 0.01, 0.5, 0.01),
    "alpha": Slider("Wrażliwość rynku (α)", 0.5, 0.1, 5.0, 0.1),
}

# 2. Panel boczny (Sidebar) z przyciskiem Shock
def ControlPanelExtension(model):
    with solara.Sidebar():
        solara.Markdown("### Zdarzenia rynkowe")
        solara.Button(
            label="WYWOŁAJ KRACH (SHOCK)", 
            on_click=model.trigger_shock, 
            color="error",
            style={"width": "100%", "margin-top": "10px"}
        )
        solara.Markdown("Kliknięcie wymusza panikę u 40% populacji, co powinno być widoczne na obu wykresach.")

# 3. Ulepszony wykres Ceny (stabilny rozmiar)
def PricePlot(model):
    """Niestandardowy wykres ceny rynkowej."""
    fig = figure.Figure(figsize=(6, 4))
    ax = fig.subplots()
    df = model.datacollector.get_model_vars_dataframe()
    
    if not df.empty:
        ax.plot(df.index, df["Cena"], color="tab:blue", linewidth=2)
        ax.set_title("Ewolucja Ceny Rynkowej", fontsize=12, fontweight='bold')
        ax.set_xlabel("Krok symulacji")
        ax.set_ylabel("Cena ($)")
        ax.grid(True, linestyle='--', alpha=0.6)
        
        # Stabilizacja osi X
        ax.set_xlim(0, max(1, len(df) - 1))
        
        # Opcjonalnie: minimalny zakres osi Y, żeby wykres nie "pływał" przy małych zmianach
        current_price = model.price
        ax.set_ylim(min(900, current_price * 0.8), max(1100, current_price * 1.2))

    fig.tight_layout()
    return solara.FigureMatplotlib(fig)

# 4. Wykres proporcji sentymentu (Stacked Area)
def SentimentStackedPlot(model):
    """Wykres proporcji: Optymiści vs Pesymiści (stała wysokość = N)."""
    fig = figure.Figure(figsize=(6, 4))
    ax = fig.subplots()
    df = model.datacollector.get_model_vars_dataframe()
    
    if not df.empty:
        x = df.index
        y_opt = df["Optymiści"]
        y_pes = df["Pesymiści"]
        
        ax.stackplot(
            x, y_opt, y_pes, 
            labels=["Optymiści", "Pesymiści"], 
            colors=["#2ca02c", "#d62728"], # Wyraźna zieleń i czerwień
            alpha=0.8
        )
        
        ax.set_title("Struktura Sentymentu Populacji", fontsize=12, fontweight='bold')
        ax.set_xlabel("Krok symulacji")
        ax.set_ylabel("Liczba Agentów")
        
        # Stała wysokość odpowiadająca rozmiarowi populacji
        ax.set_ylim(0, model.population_size)
        ax.set_xlim(0, max(1, len(df) - 1))
        ax.legend(loc="upper left", frameon=True, facecolor='white', framealpha=0.9)
        ax.grid(axis='y', linestyle='--', alpha=0.3)

    fig.tight_layout()
    return solara.FigureMatplotlib(fig)

# 5. Inicjalizacja instancji modelu
model_inst = MarketModel()

# 6. Konfiguracja Dashboardu Solara
page = SolaraViz(
    model_inst,
    components=[
        PricePlot,              # Ulepszony wykres ceny
        SentimentStackedPlot,   # Wykres proporcji
        ControlPanelExtension   # Przycisk w panelu bocznym
    ],
    model_params=model_params,
    name="Symulacja Systemu Kirmana (Model ABM)",
)

page  # noqa