import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from agent import Agent
from constants import AGENTS_COUNT


class Network:
    graph: nx.Graph
    agents: list[Agent]
    network_name: str

    def __init__(self, graph: nx.Graph, network_name: str):
        self.graph = graph
        self.agents = self.generate_agents()
        self.network_name = network_name

    def generate_agents(self) -> list[Agent]:
        agents = []
        for _ in self.graph.nodes:
            agent = Agent(
                influence=np.random.uniform(),
                flexibility=np.random.beta(0.1, 1.0),
                opinion=np.random.uniform(size=2),
            )
            agents.append(agent)
        return agents

    def update_opinions(self):
        for i, agent in enumerate(self.agents):
            neighbors = list(self.graph.neighbors(i))
            neighbor_opinions = np.mean(
                [self.agents[neighbor].opinion for neighbor in neighbors], axis=0
            )
            neighbor_influence = np.mean(
                [self.agents[neighbor].influence for neighbor in neighbors], axis=0
            )
            agent_population_share = self.graph.degree[i] / self.graph.number_of_nodes()
            mode_modifier = (
                agent_population_share + neighbor_influence
            ) * agent.flexibility
            new_opinion = []
            ## triangular distribution
            for i in range(2):
                opinion_range = abs(agent.opinion[i] - neighbor_opinions[i])
                lower_opinion = min(neighbor_opinions[i], agent.opinion[i])

                new_opinion.append(
                    np.random.triangular(
                        left=lower_opinion,
                        mode=lower_opinion + (opinion_range * mode_modifier),
                        right=max(neighbor_opinions[i], agent.opinion[i]),
                    )
                )

            agent.opinion = new_opinion

    def plot_opinions(self, title):
        # Get the positions of the agents
        pos = {i: self.agents[i].opinion for i in range(AGENTS_COUNT)}
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

    def plot_opinions_evolution(self, iterations):
        # Update opinions using Glauber Dynamics for `iterations` iterations and plot the opinions for each network
        for i in range(iterations):
            self.update_opinions()
            self.plot_opinions(
                f"Opinions of Agents in the {self.network_name} Network (Iteration {i+1})"
            )