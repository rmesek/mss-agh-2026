# Simulation of a Socioeconomic System

This project presents a simulation of a socioeconomic system using agent-based modeling (ABM) to investigate the impact of microeconomic interactions on macroscopic phenomena in financial markets. The proposed solution is based on Alan Kirman's stochastic recruitment model, implemented in Python (using the Mesa framework) and extended with a dynamic price-formation mechanism driven by shifts in agent sentiment. As a part of the research, experiments were conducted across varying parameters of innovation (independent opinion change) and imitation (herding behavior) to analyze price evolution, sentiment dynamics, and market resilience to sudden external shocks (such as induced panic). The results show that the artificial market exhibits counter-intuitive resilience against imposed trends: continuous activity by even a small fraction of "innovators" offsets the impact of panic and forces the system to return to its typical oscillations.

## Results and Report

The problem breakdown and detailed findings are available in [the report](Modelowanie_i_symulacja_systemów.pdf) (in Polish).

## Running the Simulation

The project uses the [uv Python package and project manager](https://docs.astral.sh/uv/). 

Run the simulation in a web browser:
```sh
$ uv run solara run src/app.py
```
