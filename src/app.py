import solara
import matplotlib.figure as figure
import numpy as np
from model import MarketModel
from mesa.visualization import Slider, SolaraViz

# 1. Konfiguracja parametrów (N=100 dla zgodności z Rysunkiem I)
model_params = {
    "population_size": Slider("Liczba Inwestorów (N)", 100, 10, 500, 10),
    "epsilon": Slider("Innowacja (ε)", 0.005, 0.001, 0.2, 0.001),
    "delta": Slider("Naśladownictwo (δ)", 0.01, 0.001, 0.5, 0.001),
    "alpha": Slider("Wrażliwość rynku (α)", 0.5, 0.1, 5.0, 0.1),
}

# 2. Panel boczny z przyciskami zdarzeń
def ControlPanelExtension(model):
    with solara.Sidebar():
        solara.Markdown("### Sterowanie Interaktywne")
        
        solara.Button(
            label="WYWOŁAJ EUFORIĘ (BUY)", 
            on_click=model.trigger_optimism, 
            color="success", 
            style={"width": "100%", "margin-bottom": "10px"}
        )
        
        solara.Button(
            label="WYWOŁAJ KRACH (SELL)", 
            on_click=model.trigger_shock, 
            color="error", 
            style={"width": "100%", "margin-bottom": "20px"}
        )
        
        solara.Markdown("---")
        eta = model.epsilon / model.delta if model.delta != 0 else 0
        solara.Markdown(f"**Teoretyczne η (ε/δ):** {eta:.3f}")
        solara.Markdown("> η < 1: Rozkład U-kształtny (bimodalny)\n> η > 1: Rozkład dzwonowy")

# 3. Wykres Ceny z opisami osi
def PricePlot(model):
    fig = figure.Figure(figsize=(6, 3.5))
    ax = fig.subplots()
    df = model.datacollector.get_model_vars_dataframe()
    
    if not df.empty:
        ax.plot(df.index, df["Cena"], color="tab:blue", linewidth=1.5)
        ax.set_title("Ewolucja Ceny Rynkowej", fontweight='bold')
        ax.set_xlabel("Krok symulacji (Czas)")
        ax.set_ylabel("Cena ($)")
        ax.set_xlim(0, max(1, len(df)-1))
        ax.grid(True, linestyle='--', alpha=0.5)
    
    fig.tight_layout()
    return solara.FigureMatplotlib(fig)

# 4. Wykres Sentymentu (Stacked) z opisami osi
def SentimentStackedPlot(model):
    fig = figure.Figure(figsize=(6, 3.5))
    ax = fig.subplots()
    df = model.datacollector.get_model_vars_dataframe()
    
    if not df.empty:
        ax.stackplot(
            df.index, df["Optymiści"], df["Pesymiści"], 
            labels=["Optymiści", "Pesymiści"],
            colors=["#2ca02c", "#d62728"], 
            alpha=0.8
        )
        ax.set_title("Struktura Sentymentu Populacji", fontweight='bold')
        ax.set_xlabel("Krok symulacji (Czas)")
        ax.set_ylabel("Liczba Agentów")
        ax.set_ylim(0, model.population_size)
        ax.set_xlim(0, max(1, len(df)-1))
        ax.legend(loc="upper left", frameon=True, framealpha=0.8)
    
    fig.tight_layout()
    return solara.FigureMatplotlib(fig)

# 5. Wykres Rozkładu (Dynamiczny) z opisami osi
def DynamicDistributionPlot(model):
    fig = figure.Figure(figsize=(6, 4))
    ax = fig.subplots()
    df = model.datacollector.get_model_vars_dataframe()
    
    if len(df) > 5:
        fractions = df["Optymiści"] / model.population_size
        ax.hist(
            fractions, 
            bins=np.linspace(0, 1, 21), 
            density=True, 
            color="purple", 
            alpha=0.6, 
            edgecolor="black"
        )
        
        # Próba dodania linii trendu (KDE)
        try:
            from scipy.stats import gaussian_kde
            kde = gaussian_kde(fractions)
            x_range = np.linspace(0, 1, 100)
            ax.plot(x_range, kde(x_range), color="black", linewidth=2)
        except:
            pass

    ax.set_title("Empiryczny Rozkład Stanów (PDF)", fontweight='bold')
    ax.set_xlabel("Frakcja Optymistów w systemie [0-1]")
    ax.set_ylabel("Gęstość występowania")
    ax.set_xlim(0, 1)
    ax.grid(axis='y', alpha=0.3)
    
    fig.tight_layout()
    return solara.FigureMatplotlib(fig)

# Inicjalizacja modelu
model_inst = MarketModel(epsilon=0.005, delta=0.01)

# Składanie dashboardu
page = SolaraViz(
    model_inst,
    components=[
        PricePlot,
        SentimentStackedPlot,
        DynamicDistributionPlot,
        ControlPanelExtension
    ],
    model_params=model_params,
    name="Symulacja Modelu Kirmana (1993)",
)
page