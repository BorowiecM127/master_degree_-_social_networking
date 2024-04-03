"""
Main program
"""

import networkx as nx
from network import Network
from constants import AGENTS_COUNT, EVOLUTION_ITERATIONS


def main():
    """
    Generate a plot showing the evolution of opinions in Barabasi-Albert, Watts-Strogatz, and Erdos-Renyi networks.
    """
    barabasi_albert = Network(
        nx.barabasi_albert_graph(AGENTS_COUNT, 2), "Barabasi-Albert"
    )
    watts_strogatz = Network(
        nx.watts_strogatz_graph(AGENTS_COUNT, 4, 0.5), "Watts-Strogatz"
    )
    erdos_renyi = Network(nx.erdos_renyi_graph(AGENTS_COUNT, 0.3), "Erdos-Renyi")

    barabasi_albert.plot_opinions_evolution(EVOLUTION_ITERATIONS)
    watts_strogatz.plot_opinions_evolution(EVOLUTION_ITERATIONS)
    erdos_renyi.plot_opinions_evolution(EVOLUTION_ITERATIONS)


if __name__ == "__main__":
    main()
