"""
Interfejs Solara z przyciskiem Shock w panelu Controls.
"""

import solara
from model import MarketModel
from mesa.visualization import Slider, SolaraViz, make_plot_component

# Konfiguracja suwaków
model_params = {
    "population_size": Slider("Liczba Inwestorów (N)", 200, 50, 1000, 50),
    "epsilon": Slider("Innowacja (ε)", 0.01, 0.001, 0.1, 0.001),
    "delta": Slider("Naśladownictwo (δ)", 0.05, 0.01, 0.5, 0.01),
    "alpha": Slider("Wrażliwość rynku (α)", 0.5, 0.1, 5.0, 0.1),
}

def ControlPanelExtension(model):
    """
    Komponent, który wstrzykuje dodatkowe elementy do bocznego panelu (Controls).
    """
    with solara.Sidebar():
        solara.Markdown("### Zdarzenia rynkowe")
        solara.Button(
            label="WYWOŁAJ KRACH (SHOCK)", 
            on_click=model.trigger_shock, 
            color="error",
            style={"width": "100%", "margin-top": "10px"}
        )
        solara.Markdown("Wymusza nagły wzrost pesymizmu w systemie.")

# Inicjalizacja modelu
model_inst = MarketModel()

# Konfiguracja Dashboardu
page = SolaraViz(
    model_inst,
    components=[
        make_plot_component("Cena"),
        make_plot_component({"Optymiści": "green", "Pesymiści": "red"}),
        ControlPanelExtension # Ten komponent doda przycisk do paska bocznego
    ],
    model_params=model_params,
    name="System Społeczno-Ekonomiczny (Kirman 1993)",
)

page  # noqa