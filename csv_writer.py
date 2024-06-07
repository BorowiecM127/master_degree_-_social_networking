"""
CSVWriter class
"""

import os
import csv


class CSVWriter:
    """
    Class for writing data to a CSV file.
    """

    def __init__(
        self,
        network_name: str,
        update_method: str,
        update_parameter: float,
        agent_count: str,
        simulation_number: str,
    ) -> None:
        """
        Initializes a new instance of the CSVWriter class.

        Args:
            network_name (str): The name of the network.
            update_method (str): The method used for updating the network.
            update_parameter (float): The parameter used for updating the network.
            agent_count (str): The number of agents in the network.
            simulation_number (str): The number of the simulation.

        Returns:
            None
        """
        self.network_name = network_name
        self.update_method = update_method
        self.update_parameter = update_parameter
        self.agent_count = agent_count
        self.simulation_number = simulation_number
        self.path = f"./csv/{self.network_name}_{self.update_method}_{self.update_parameter}_{self.agent_count}_{self.simulation_number}.csv"

    def create_new_file(self) -> None:
        """
        Creates a new CSV file with the specified column names.

        This function initializes a new CSV file with the given column names.
        The column names represent the headers of the file.
        The file is created in the specified filename with the UTF-8 encoding.

        Parameters:
            self (CSVWriter): The CSVWriter instance.

        Returns:
            None
        """
        column_names = [
            "Network Name",
            "Update method",
            "Update parameter",
            "Agent Count",
            "Simulation Number",
            "Iteration Number",
            "Agent Number",
            "Agent X",
            "Agent Y",
        ]

        if not os.path.exists("./csv"):
            os.makedirs("./csv")

        with open(self.path, "w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(column_names)

    def update_file(
        self,
        iteration_number: int,
        agent_number: int,
        agent_x: float,
        agent_y: float,
    ) -> None:
        """
        Updates the CSV file with the given iteration number, agent number, agent x-coordinate, and agent y-coordinate.

        Args:
            iteration_number (int): The current iteration number.
            agent_number (int): The number of the agent.
            agent_x (float): The x-coordinate of the agent.
            agent_y (float): The y-coordinate of the agent.

        Returns:
            None
        """
        with open(self.path, "a", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    self.network_name,
                    self.update_method,
                    self.update_parameter,
                    self.agent_count,
                    self.simulation_number,
                    iteration_number,
                    agent_number,
                    agent_x,
                    agent_y,
                ]
            )
