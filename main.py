import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


# Helper function to update agent's opinion using Glauber Dynamics with influence on neighbors
def update_opinion(agent, opinions, graph, beta=0.1):
    neighbors = list(graph.neighbors(agent))
    neighbor_opinions = np.mean(opinions[neighbors], axis=0)
    new_opinions = (1 - beta) * neighbor_opinions + beta * opinions[agent]
    return new_opinions


# Function to visualize the agents' opinions in a 2D plot
def plot_opinions(opinions, title, graph):
    # Get the positions of the agents
    pos = {i: opinions[i] for i in range(AGENTS_COUNT)}

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
    for u, v in graph.edges:
        plt.plot(
            [pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]], color="gray", linewidth=0.5
        )

    # Display vertex degree
    for node in graph.nodes:
        degree = graph.degree[node]
        plt.text(
            pos[node][0], pos[node][1], degree, fontsize=12, ha="center", va="center"
        )

    plt.show()


def plot_opinions_evolution(network, network_name, iterations):
    # Define the economic and personal freedom opinions for each agent
    opinions = np.random.uniform(size=(AGENTS_COUNT, 2))

    # Update opinions using Glauber Dynamics for `iterations` iterations and plot the opinions for each network
    for i in range(iterations):
        opinions = np.array(
            [update_opinion(agent, opinions, network) for agent in range(AGENTS_COUNT)]
        )
        plot_opinions(
            opinions,
            f"Opinions of Agents in the {network_name} Network (Iteration {i+1})",
            network,
        )


if __name__ == "__main__":
    # Define the number of agents
    AGENTS_COUNT = 20
    EVOLUTION_ITERATIONS = 5

    # Create Barabasi-Albert, Watts-Strogatz, and Erdos-Renyi networks with 20 nodes each
    barabasi_albert = nx.barabasi_albert_graph(AGENTS_COUNT, 2)
    watts_strogatz = nx.watts_strogatz_graph(AGENTS_COUNT, 4, 0.5)
    erdos_renyi = nx.erdos_renyi_graph(AGENTS_COUNT, 0.3)

    # Plot the opinions evolution for each network
    plot_opinions_evolution(barabasi_albert, "Barabasi-Albert", EVOLUTION_ITERATIONS)
    plot_opinions_evolution(watts_strogatz, "Watts-Strogatz", EVOLUTION_ITERATIONS)
    plot_opinions_evolution(erdos_renyi, "Erdos-Renyi", EVOLUTION_ITERATIONS)
