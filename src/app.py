import solara
import matplotlib.figure as figure
import numpy as np
from model import MarketModel
from mesa.visualization import Slider, SolaraViz

# 1. Parameter configuration (N=100 for compatibility with Figure I)
model_params = {
    "population_size": Slider("Number of Investors (N)", 100, 10, 500, 10),
    "epsilon": Slider("Innovation (ε)", 0.005, 0.001, 0.2, 0.001),
    "delta": Slider("Imitation (δ)", 0.01, 0.001, 0.5, 0.001),
    "alpha": Slider("Market sensitivity (α)", 0.5, 0.1, 5.0, 0.1),
}

# 2. Side panel with event buttons
def ControlPanelExtension(model):
    with solara.Sidebar():
        solara.Markdown("### Interactive Control")
        
        solara.Button(
            label="TRIGGER EUPHORIA (BUY)", 
            on_click=model.trigger_optimism, 
            color="success", 
            style={"width": "100%", "margin-bottom": "10px"}
        )
        
        solara.Button(
            label="TRIGGER CRASH (SELL)", 
            on_click=model.trigger_shock, 
            color="error", 
            style={"width": "100%", "margin-bottom": "20px"}
        )
        
        eta = model.epsilon / model.delta if model.delta != 0 else 0
        solara.Markdown(
            "---\n\n"
            f"**Theoretical η (ε/δ):** `{eta:.3f}`\n\n"
            "- **η < 1:** U-shaped distribution (bimodal)\n"
            "- **η > 1:** Bell-shaped distribution"
        )

# 3. Price Plot with axis descriptions
def PricePlot(model):
    fig = figure.Figure(figsize=(6, 3.5))
    ax = fig.subplots()
    df = model.datacollector.get_model_vars_dataframe()
    
    if not df.empty:
        ax.plot(df.index, df["Price"], color="tab:blue", linewidth=1.5)
        ax.set_title("Market Price Evolution", fontweight='bold')
        ax.set_xlabel("Simulation step (Time)")
        ax.set_ylabel("Price ($)")
        ax.set_xlim(0, max(1, len(df)-1))
        ax.grid(True, linestyle='--', alpha=0.5)
    
    fig.tight_layout()
    return solara.FigureMatplotlib(fig)

# 4. Sentiment Plot (Stacked) with axis descriptions
def SentimentStackedPlot(model):
    fig = figure.Figure(figsize=(6, 3.5))
    ax = fig.subplots()
    df = model.datacollector.get_model_vars_dataframe()
    
    if not df.empty:
        ax.stackplot(
            df.index, df["Optimists"], df["Pessimists"], 
            labels=["Optimists", "Pessimists"],
            colors=["#2ca02c", "#d62728"], 
            alpha=0.8
        )
        ax.set_title("Population Sentiment Structure", fontweight='bold')
        ax.set_xlabel("Simulation step (Time)")
        ax.set_ylabel("Number of Agents")
        ax.set_ylim(0, model.population_size)
        ax.set_xlim(0, max(1, len(df)-1))
        ax.legend(loc="upper left", frameon=True, framealpha=0.8)
    
    fig.tight_layout()
    return solara.FigureMatplotlib(fig)

# 5. Distribution Plot (Dynamic) with axis descriptions
def DynamicDistributionPlot(model):
    fig = figure.Figure(figsize=(6, 4))
    ax = fig.subplots()
    df = model.datacollector.get_model_vars_dataframe()
    
    if len(df) > 5:
        fractions = df["Optimists"] / model.population_size
        ax.hist(
            fractions, 
            bins=np.linspace(0, 1, 21), 
            density=True, 
            color="purple", 
            alpha=0.6, 
            edgecolor="black"
        )
        
        # # Try to add a trend line (KDE)
        # try:
        #     from scipy.stats import gaussian_kde
        #     kde = gaussian_kde(fractions)
        #     x_range = np.linspace(0, 1, 100)
        #     ax.plot(x_range, kde(x_range), color="black", linewidth=2)
        # except:
        #     pass

    ax.set_title("Empirical State Distribution (PDF)", fontweight='bold')
    ax.set_xlabel("Fraction of Optimists in the system [0-1]")
    ax.set_ylabel("Occurrence Density")
    ax.set_xlim(0, 1)
    ax.grid(axis='y', alpha=0.3)
    
    fig.tight_layout()
    return solara.FigureMatplotlib(fig)

# Initialize the model
model_inst = MarketModel(epsilon=0.005, delta=0.01)

# Compose the dashboard
page = SolaraViz(
    model_inst,
    components=[
        PricePlot,
        SentimentStackedPlot,
        DynamicDistributionPlot,
        ControlPanelExtension
    ],
    model_params=model_params,
    name="Kirman Model Simulation (1993)",
)
page