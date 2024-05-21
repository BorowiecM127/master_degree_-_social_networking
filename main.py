"""
Main program
"""

import networkx as nx
from network import Network
from network_update import NetworkUpdate


def create_barabasi_albert_network(
    agents_count: int,
    update_type: NetworkUpdate,
    update_parameter: float,
    simulation_number: int,
    use_csv_writer: bool = False,
) -> Network:
    """
    Create a Barabasi-Albert network with the specified number of agents.

    Parameters:
    - agents_count (int): The number of agents in the network.
    - update_type (NetworkUpdate): The type of update to be applied to the network.
    - update_parameter (float): The parameter used for updating the network.
    - simulation_number (int): The number of the simulation.
    - use_csv_writer (bool, optional): Whether to use a CSV file for logging. Defaults to False.

    Returns:
    - Network: The Barabasi-Albert network created.
    """

    return Network(
        nx.barabasi_albert_graph(agents_count, 2),
        "Barabasi-Albert",
        update_type,
        update_parameter,
        simulation_number,
        use_csv_writer,
    )


def create_watts_strogatz_network(
    agents_count: int,
    update_type: NetworkUpdate,
    update_parameter: float,
    simulation_number: int,
    use_csv_writer: bool = False,
) -> Network:
    """
    Create a Watts-Strogatz network with the specified number of agents.

    Parameters:
    - agents_count (int): The number of agents in the network.
    - update_type (NetworkUpdate): The type of update to be applied to the network.
    - update_parameter (float): The parameter used for updating the network.
    - simulation_number (int): The number of the simulation.
    - use_csv_writer (bool, optional): Whether to use a CSV file for logging. Defaults to False.

    Returns:
    - Network: The Watts-Strogatz network created.
    """

    return Network(
        nx.watts_strogatz_graph(agents_count, 4, 0.5),
        "Watts-Strogatz",
        update_type,
        update_parameter,
        simulation_number,
        use_csv_writer,
    )


def create_erdos_renyi_network(
    agents_count: int,
    update_type: NetworkUpdate,
    update_parameter: float,
    simulation_number: int,
    use_csv_writer: bool = False,
) -> Network:
    """
    Create an Erdos-Renyi network with the specified number of agents.

    Args:
        agents_count (int): The number of agents in the network.
        update_type (NetworkUpdate): The type of update to be applied to the network.
        update_parameter (float): The parameter used for updating the network.
        simulation_number (int): The number of the simulation.
        use_csv_writer (bool, optional): Whether to use a CSV file for logging. Defaults to False.

    Returns:
        Network: The Erdos-Renyi network created.
    """

    return Network(
        nx.erdos_renyi_graph(agents_count, 0.3),
        "Erdos-Renyi",
        update_type,
        update_parameter,
        simulation_number,
        use_csv_writer,
    )


def main():
    """
    Generate a plot showing the evolution of opinions in Barabasi-Albert, Watts-Strogatz, and Erdos-Renyi networks.
    """
    # show_point_spread_in_time = False
    show_point_spread_in_time = True
    only_final_plot = True
    max_iterations = 50
    if show_point_spread_in_time:
        agents_counts = [20, 50, 100, 200, 500, 1000, 2000, 5000]
        # agents_counts = [20, 50]
    else:
        agents_counts = [50]
    single_population_repetitions = 10
    network_generators = [
        create_barabasi_albert_network,
        create_watts_strogatz_network,
        create_erdos_renyi_network,
    ]

    for network_generator in network_generators:
        print(f"Network: {network_generator(5, None, None, None).network_name}")
        for agents_count in agents_counts:
            average_iterations_before_stabilization = 0
            for i in range(single_population_repetitions):
                network = network_generator(
                    agents_count=agents_count,
                    update_type=NetworkUpdate.STUDENT,
                    update_parameter=500,
                    simulation_number=i,
                    use_csv_writer=True,
                )
                # network = network_generator(
                #     agents_count=agents_count,
                #     update_type=NetworkUpdate.PROFESSOR,
                #     update_parameter=20,
                #     simulation_number=i,
                #     use_csv_writer=True,
                # )
                if show_point_spread_in_time:
                    point_spread, iterations_before_stabilization = (
                        network.show_point_spread_in_time(max_iterations)
                    )
                    # network.plot_point_spread_in_time(
                    #     point_spread, iterations_before_stabilization
                    # )
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
