"""
Main program
"""

import networkx as nx
from network import Network


def create_barabasi_albert_network(agents_count):
    """
    Create a Barabasi-Albert network with the specified number of agents.

    Parameters:
    - agents_count: int, the number of agents in the network.

    Returns:
    - Network: the Barabasi-Albert network created.
    """
    return Network(nx.barabasi_albert_graph(agents_count, 2), "Barabasi-Albert")


def create_watts_strogatz_network(agents_count):
    """
    Create a Watts-Strogatz network with the given number of agents.
    Parameters:
        agents_count: int - the number of agents in the network
    Returns:
        Network - the Watts-Strogatz network
    """
    return Network(nx.watts_strogatz_graph(agents_count, 4, 0.5), "Watts-Strogatz")


def create_erdos_renyi_network(agents_count):
    """
    Creates an Erdos-Renyi network based on the number of agents and returns it.

    Parameters:
    - agents_count: int, the number of agents in the network

    Returns:
    - Network: the Erdos-Renyi network generated
    """
    return Network(nx.erdos_renyi_graph(agents_count, 0.3), "Erdos-Renyi")


def main():
    """
    Generate a plot showing the evolution of opinions in Barabasi-Albert, Watts-Strogatz, and Erdos-Renyi networks.
    """
    show_point_spread_in_time = False
    only_final_plot = True
    max_iterations = 50
    if show_point_spread_in_time:
        agents_counts = [20, 50, 100, 200, 500, 1000, 2000, 5000]
    else:
        agents_counts = [50]
    single_population_repetitions = 10
    network_generators = [
        create_barabasi_albert_network,
        create_watts_strogatz_network,
        create_erdos_renyi_network,
    ]

    for network_generator in network_generators:
        print(f"Network: {network_generator(5).network_name}")
        for agents_count in agents_counts:
            average_iterations_before_stabilization = 0
            for _ in range(single_population_repetitions):
                network = network_generator(agents_count)
                if show_point_spread_in_time:
                    point_spread, iterations_before_stabilization = (
                        network.show_point_spread_in_time(max_iterations)
                    )
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
                    f"- Population: {agents_count}, Average iterations: {average_iterations_before_stabilization}"
                )

        print()


if __name__ == "__main__":
    main()
