"""
Main program
"""

import copy
import networkx as nx
from network import Network
from network_update import NetworkUpdate


def main():
    """
    Generate a plot showing the evolution of opinions in Barabasi-Albert, Watts-Strogatz, and Erdos-Renyi networks.
    """
    show_point_spread_in_time = True
    show_point_plot_spread = False
    only_final_plot = True
    max_iterations: int = 50
    single_population_repetitions = 10

    opinion_updates = [0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]
    network_update = NetworkUpdate.STUDENT

    agents_counts = [20, 50, 100, 200, 500, 1000, 2000, 5000]

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
    print_spaces = ""
    agents = []

    for opinion_update in opinion_updates:
        print(f"Opinion update: {opinion_update}")
        for agents_count in agents_counts:
            print_spaces += "  "
            print(f"{print_spaces}Agents count: {agents_count}")
            for network_generator in network_generators:
                print_spaces += "  "
                print(f"{print_spaces}Network: {network_generator(5)[1]}")
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
                    average_iterations_before_stabilization /= (
                        single_population_repetitions
                    )
                    print_spaces += "  "
                    print(
                        f"{print_spaces}Average iterations: {average_iterations_before_stabilization}"
                    )
                    print_spaces = print_spaces[:-2]
                print_spaces = print_spaces[:-2]
            print_spaces = print_spaces[:-2]
            print()


if __name__ == "__main__":
    main()
