import solara
import matplotlib.figure as figure
import numpy as np
from model import MarketModel
from mesa.visualization import Slider, SolaraViz

# 1. Konfiguracja parametrów zgodnie z wartościami z artykułu (N=100)
model_params = {
    "population_size": Slider("Liczba Inwestorów (N)", 100, 10, 500, 10),
    "epsilon": Slider("Innowacja (ε)", 0.01, 0.001, 0.2, 0.001),
    "delta": Slider("Naśladownictwo (δ)", 0.02, 0.001, 0.5, 0.001),
    "alpha": Slider("Wrażliwość rynku (α)", 0.5, 0.1, 5.0, 0.1),
}

def ControlPanelExtension(model):
    with solara.Sidebar():
        solara.Markdown("### Sterowanie")
        solara.Button(label="WYWOŁAJ KRACH", on_click=model.trigger_shock, color="error", style={"width": "100%"})
        solara.Markdown(f"**Aktualne η (ε/δ):** {model.epsilon/model.delta:.3f}")

def PricePlot(model):
    fig = figure.Figure(figsize=(6, 3))
    ax = fig.subplots()
    df = model.datacollector.get_model_vars_dataframe()
    if not df.empty:
        ax.plot(df.index, df["Cena"], color="tab:blue")
        ax.set_title("Cena Rynkowa")
        ax.set_xlim(0, max(1, len(df)-1))
    fig.tight_layout()
    return solara.FigureMatplotlib(fig)

def SentimentStackedPlot(model):
    fig = figure.Figure(figsize=(6, 3))
    ax = fig.subplots()
    df = model.datacollector.get_model_vars_dataframe()
    if not df.empty:
        ax.stackplot(df.index, df["Optymiści"], df["Pesymiści"], colors=["#2ca02c", "#d62728"], alpha=0.8)
        ax.set_title("Dynamika Sentymentu (Populacja)")
        ax.set_ylim(0, model.population_size)
        ax.set_xlim(0, max(1, len(df)-1))
    fig.tight_layout()
    return solara.FigureMatplotlib(fig)

# 2. NOWY: Dynamiczny wykres rozkładu (obliczany z historii kroków)
def DynamicDistributionPlot(model):
    """Oblicza empiryczny rozkład stanów systemu na podstawie historii kroków."""
    fig = figure.Figure(figsize=(6, 4))
    ax = fig.subplots()
    df = model.datacollector.get_model_vars_dataframe()
    
    if len(df) > 5: # Potrzebujemy kilku kroków, aby histogram miał sens
        # Pobieramy frakcję optymistów z każdego kroku historii
        fractions = df["Optymiści"] / model.population_size
        
        # Tworzymy histogram (gęstość)
        counts, bins, patches = ax.hist(
            fractions, 
            bins=np.linspace(0, 1, 25), 
            density=True, 
            color="purple", 
            alpha=0.6, 
            edgecolor="black"
        )
        
        # Opcjonalnie: wygładzona linia trendu (KDE)
        try:
            from scipy.stats import gaussian_kde
            kde = gaussian_kde(fractions)
            x_range = np.linspace(0, 1, 100)
            ax.plot(x_range, kde(x_range), color="black", linewidth=2)
        except:
            pass

    ax.set_title("Empiryczny Rozkład Stanów (Dynamiczny)")
    ax.set_xlabel("Frakcja Optymistów")
    ax.set_ylabel("Częstotliwość występowania")
    ax.set_xlim(0, 1)
    ax.grid(axis='y', alpha=0.3)
    
    fig.tight_layout()
    return solara.FigureMatplotlib(fig)

model_inst = MarketModel(epsilon=0.005, delta=0.01) # Startowe wartości dla przypadku 'a'

page = SolaraViz(
    model_inst,
    components=[
        PricePlot,
        SentimentStackedPlot,
        DynamicDistributionPlot, # Wykres obliczany na żywo
        ControlPanelExtension
    ],
    model_params=model_params,
    name="Model Kirmana - Analiza Empiryczna",
)
page