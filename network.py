"""
Network class
"""

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from agent import Agent
from network_update import NetworkUpdate
from csv_writer import CSVWriter


class Network:
    """
    Network class, contains networkx graph and agents related to each graph node.
    """

    graph: nx.Graph
    agents: list[Agent]
    network_name: str
    update_type: NetworkUpdate

    def __init__(
        self,
        graph: nx.Graph,
        network_name: str,
        update_type: NetworkUpdate,
        update_parameter: float,
        simulation_number: int,
        use_csv_writer: bool = False,
    ) -> None:
        """
        Initializes a new instance of the Network class with the given parameters.

        Args:
            graph (nx.Graph): The networkx graph representing the network.
            network_name (str): The name of the network.
            update_type (NetworkUpdate): The type of update to be applied to the network.
            update_parameter (float): The parameter used for updating the network.
            simulation_number (int): The number of the simulation.
            use_csv_writer (bool, optional): Whether to use a CSV file for logging. Defaults to False.

        Returns:
            None
        """
        self.graph = graph
        self.agents = self._generate_agents()
        self.network_name = network_name
        self.update_type = update_type
        self.update_parameter = update_parameter
        self.use_csv_writer = use_csv_writer

        if self.use_csv_writer:
            self.csv_writer = CSVWriter(
                network_name=self.network_name,
                update_method=self.update_type,
                update_parameter=self.update_parameter,
                agent_count=self.graph.number_of_nodes(),
                simulation_number=simulation_number,
            )
            self.csv_writer.create_new_file()

    def plot_opinions(self, title: str) -> None:
        """
        Plot the opinions of the agents on a 2D scatter plot,
        including political party points and edges between vertices.

        Parameters:
            title (str): The title of the plot.

        Returns:
            None
        """
        # Get the positions of the agents
        pos = {i: self.agents[i].opinion for i in range(self.graph.number_of_nodes())}
        opinions = np.array([agent.opinion for agent in self.agents])

        # Create the plot
        plt.figure(figsize=(10, 10))
        plt.scatter(
            opinions[:, 0],
            opinions[:, 1],
            s=300,
            c="green",
        )
        plt.xlabel("Economic Freedom Opinion")
        plt.ylabel("Personal Freedom Opinion")
        plt.title(title)

        # Add political party points with labels
        political_parties = {
            "Authoritarian": [0.1, 0.1],
            "Conservative": [0.9, 0.1],
            "Libertarian": [0.9, 0.9],
            "Liberal": [0.1, 0.9],
        }

        for party, position in political_parties.items():
            plt.scatter(position[0], position[1], color="red", s=100, label=party)
            plt.text(position[0], position[1], party, fontsize=12)

        # Display edges between vertices
        for u, v in self.graph.edges:
            plt.plot(
                [pos[u][0], pos[v][0]],
                [pos[u][1], pos[v][1]],
                color="gray",
                linewidth=0.5,
            )

        # Display vertex degree
        for node in self.graph.nodes:
            degree = self.graph.degree[node]
            plt.text(
                pos[node][0],
                pos[node][1],
                degree,
                fontsize=12,
                ha="center",
                va="center",
            )

        plt.show()

    def plot_opinions_evolution(
        self, iterations: int, only_final_plot: bool = False
    ) -> None:
        """
        Update opinions using Glauber Dynamics for `iterations` iterations and plot the opinions for each network
        """
        for i in range(iterations):
            self._update_opinions(i)
            if not only_final_plot:
                self.plot_opinions(
                    f"Opinions of Agents in the {self.network_name} Network (Iteration {i+1})"
                )
            elif i == iterations - 1:
                self.plot_opinions(
                    f"Opinions of Agents in the {self.network_name} Network (Iteration {i+1})"
                )

    def show_point_spread_in_time(self, max_iterations: int) -> None:
        """
        Update the point spread until they values reaches below 0.1,
        and return the point spread and the number of iterations before stabilization.

        Parameters:
            max_iterations (int): The maximum number of iterations to perform.

        Returns:
            tuple: The point spread and the number of iterations before stabilization.
        """
        iterations_before_stabilization = 0
        point_spread = {"x": [], "y": []}
        for i in range(max_iterations):
            self._update_opinions(i)
            opinion_spread = self._opinion_spread()
            if opinion_spread["x"] <= 0.1 and opinion_spread["y"] <= 0.1:
                iterations_before_stabilization = i
                break

            point_spread["x"].append(opinion_spread["x"])
            point_spread["y"].append(opinion_spread["y"])

        iterations_before_stabilization = (
            max_iterations
            if iterations_before_stabilization == 0
            else iterations_before_stabilization
        )

        return point_spread, iterations_before_stabilization

    def plot_point_spread_in_time(
        self, point_spread: dict, iterations_before_stabilization: int
    ) -> None:
        """
        Plot the point spread in time for X and Y axes based on the number of max_iterations.

        Parameters:
            max_iterations (int): The maximal number of iterations to perform.

        Returns:
            None
        """
        for i, axis in enumerate(["x", "y"]):
            plt.subplot(2, 1, i + 1)
            plt.plot(range(iterations_before_stabilization), point_spread[axis])
            plt.xticks(range(iterations_before_stabilization))
            plt.title(f"{axis.upper()} axis")
            plt.xlabel("Iterations")
            plt.ylabel(f"{axis.upper()}-axis spread")

        plt.suptitle(
            f"Point spread in time for {self.network_name} network. Population: {self.graph.number_of_nodes()} agents."
        )
        plt.tight_layout()
        plt.show()

    def _update_opinions(self, update_index: int) -> None:
        """
        Update opinions of agents based on their neighbors' opinions and influences.

        It uses neighbors and agent properties to generate new opinion from triangular distribution.
        Neighbors average opinion and their average influence is pretty self-explanatory.

        In mode_modifier triangular distribution mode is modified by agent population share,
        its flexibility and neighbors influence.
        Agent population share is number of agent degree divided by number of all nodes.
        Its purpose is to strengthen neighbors influence on nodes, which have more neighbors.
        Agent flexibility lowers change of mind for specific node, because it is generated by Beta distribution.
        """

        for i, agent in enumerate(self.agents):
            if self.use_csv_writer:
                self.csv_writer.update_file(
                    update_index, i, agent.opinion[0], agent.opinion[1]
                )

            neighbors = list(self.graph.neighbors(i))
            neighbor_opinions = np.average(
                [self.agents[neighbor].opinion for neighbor in neighbors],
                weights=[self.agents[neighbor].influence for neighbor in neighbors],
                axis=0,
            )
            neighbor_influence = np.mean(
                [self.agents[neighbor].influence for neighbor in neighbors], axis=0
            )
            agent_population_share = self.graph.degree[i] / self.graph.number_of_nodes()
            mode_modifier = (
                np.mean([agent_population_share, neighbor_influence])
            ) * agent.flexibility
            new_opinion = []
            ## exponential distribution
            for i in range(2):
                if self.update_type == NetworkUpdate.STUDENT:
                    opinion_range = abs(agent.opinion[i] - neighbor_opinions[i])
                    lower_opinion = min(neighbor_opinions[i], agent.opinion[i])
                    upper_opinion = max(neighbor_opinions[i], agent.opinion[i])

                    opinion = lower_opinion + np.random.exponential(
                        scale=(opinion_range * mode_modifier * self.update_parameter)
                    )
                    opinion = max(opinion, lower_opinion)
                    opinion = min(opinion, upper_opinion)
                else:
                    opinion_range = neighbor_opinions[i] - agent.opinion[i]
                    # print('{:.4e}'.format(opinion_range))
                    val = np.random.exponential(
                        scale=mode_modifier * self.update_parameter
                    )
                    opinion = agent.opinion[i] + val * opinion_range
                    # print('scale = {:.3e}; val ={:.3f}'.format(mode_modifier, val))

                new_opinion.append(opinion)

            agent.opinion = new_opinion

    def _generate_agents(self) -> list[Agent]:
        """
        Generates a list of Agent objects based on the graph's nodes.

        Returns:
            list[Agent]: The list of generated Agent objects.
        """
        agents = []
        for _ in self.graph.nodes:
            agent = Agent(
                influence=np.random.uniform(),
                flexibility=np.random.beta(0.1, 1.0),
                opinion=np.random.uniform(size=2),
            )
            agents.append(agent)
        return agents

    def _opinion_spread(self) -> dict[float]:
        """
        Calculate the spread of opinions in the network along the X and Y axes.

        Returns:
            dict: A dictionary containing the spread of opinions along the X and Y axes.
        """
        opinions = np.array([agent.opinion for agent in self.agents])
        return {
            "x": max(opinions[:, 0]) - min(opinions[:, 0]),
            "y": max(opinions[:, 1]) - min(opinions[:, 1]),
        }
