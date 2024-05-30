"""
Main program
"""

import networkx as nx
import copy
from network import Network
from network_update import NetworkUpdate


def main():
    """
    Generate a plot showing the evolution of opinions in Barabasi-Albert, Watts-Strogatz, and Erdos-Renyi networks.
    """
    show_point_spread_in_time = True
    show_point_plot_spread = False
    only_final_plot = True
    max_iterations = 50
    single_population_repetitions = 10

    opinion_update = 500
    network_update = NetworkUpdate.STUDENT

    # agents_counts = [20, 50, 100, 200, 500, 1000, 2000, 5000]
    agents_counts = [20, 50]

    network_generators = [
        lambda agents_count: (
            nx.barabasi_albert_graph(agents_count, 2),
            "Barabasi-Albert",
        ),
        lambda agents_count: (
            nx.watts_strogatz_graph(agents_count, 4, 0.5),
            "Watts-Strogatz",
        ),
        lambda agents_count: (nx.erdos_renyi_graph(agents_count, 0.3), "Erdos-Renyi"),
    ]

    agents = []

    for agents_count in agents_counts:
        print(f"Agents count: {agents_count}")
        for network_generator in network_generators:
            print(f"    Network: {network_generator(5)[1]}")
            average_iterations_before_stabilization = 0
            for i in range(single_population_repetitions):
                nx_data = network_generator(agents_count)
                network = Network(
                    nx_data[0],
                    nx_data[1],
                    network_update,
                    opinion_update,
                    i,
                    True,
                )

                if len(agents) == 0 or len(agents) != len(network.agents):
                    agents = copy.deepcopy(network.agents)
                else:
                    network.agents = copy.deepcopy(agents)

                if show_point_spread_in_time:
                    point_spread, iterations_before_stabilization = (
                        network.show_point_spread_in_time(max_iterations)
                    )
                    if show_point_plot_spread:
                        network.plot_point_spread_in_time(
                            point_spread, iterations_before_stabilization
                        )
                    average_iterations_before_stabilization += (
                        iterations_before_stabilization
                    )
                else:
                    network.plot_opinions_evolution(max_iterations, only_final_plot)

            if show_point_spread_in_time:
                average_iterations_before_stabilization /= single_population_repetitions
                print(
                    f"        Average iterations: {average_iterations_before_stabilization}"
                )

        print()


if __name__ == "__main__":
    main()
