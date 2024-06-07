"""
Script which analyzes a CSV file
"""

import csv
import os
from collections.abc import Sequence
from tabulate import tabulate
import matplotlib.pyplot as plt


def print_file_as_table(file: str) -> None:
    """
    Prints the contents of a CSV file as a formatted table.

    Args:
        file (str): The file object to read the CSV data from.

    Returns:
        None
    """
    csv_reader = csv.reader(file)
    data = list(csv_reader)
    print(tabulate(data, headers="firstrow"))


def print_file_rows(file: str) -> None:
    """
    Prints the rows of a CSV file as a formatted table.

    Args:
        file (str): The file object to read the CSV data from.

    Returns:
        None
    """
    csv_reader = csv.DictReader(file)

    column_names: Sequence[str] | None = csv_reader.fieldnames
    if column_names is None:
        return

    for column in column_names:
        print(column, end="\t")
    print()

    for row in csv_reader:
        for column in column_names:
            print(row[column], end="\t")
        print()


def generate_plot_title(data: dict) -> str:
    """
    Generates a plot title based on the provided data.

    Args:
        data (dict): A dictionary containing the following keys:
            - "Network Name" (str): The name of the network.
            - "Update parameter" (str): The update parameter.
            - "Agent Count" (int): The count of agents.
            - "Simulation Number" (int): The simulation number.
            - "Update method" (str): The update method.

    Returns:
        str: The generated plot title.
    """
    return f"""
Network Name: {data["Network Name"]}, Update parameter: {data["Update parameter"]}
Agent Count: {data["Agent Count"]}, Simulation Number: {data["Simulation Number"]}
Update method: {data["Update method"]}
"""


def show_result_plot(file: str) -> None:
    """
    Generates a scatter plot of the final state of agents based on the data in the provided CSV file.

    Args:
        file (str): The path to the CSV file containing the agent data.

    Returns:
        None

    Raises:
        FileNotFoundError: If the provided file path does not exist.
    """
    csv_reader = csv.DictReader(file)
    agent_count = int(next(csv_reader)["Agent Count"]) * -1
    agent_final_state = list(csv_reader)[agent_count:]
    plot_title: str = generate_plot_title(agent_final_state[0])
    agent_x: list[float] = [float(agent["Agent X"]) for agent in agent_final_state]
    agent_y: list[float] = [float(agent["Agent Y"]) for agent in agent_final_state]

    plt.scatter(agent_x, agent_y)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.subplots_adjust(top=0.8)
    plt.title(plot_title)
    plt.show()


def main() -> None:
    """
    This function reads all the CSV files in the './csv' directory,
    and displays a scatter plot of the final state of agents for each file.

    The function first initializes a list of CSV files by filtering the files that end with '.csv'.
    It then iterates over each file in the list and opens it using the 'utf-8' encoding.
    For each file, it generates a scatter plot of the final state of agents based on the data in the file.

    Parameters:
        None

    Returns:
        None
    """
    csv_files_path = "./csv"
    csv_files: list[str] = [
        file for file in os.listdir(csv_files_path) if file.endswith(".csv")
    ]

    for csv_file in csv_files:
        with open(f"{csv_files_path}/{csv_file}", "r", encoding="utf-8") as file:
            # print_file_as_table(file)
            # print_file_rows(file)
            show_result_plot(file)


if __name__ == "__main__":
    main()
