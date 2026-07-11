import pandas as pd


def load_experiment(experiment_id):
    """
    Load an experiment CSV file.

    Parameters:
        experiment_id (int): Experiment number

    Returns:
        pandas.DataFrame
    """

    file_path = f"data/experiment_{experiment_id}.csv"

    df = pd.read_csv(file_path)

    return df
if __name__ == "__main__":

    df = load_experiment(1)

    print(df.head())

    print("\nDataset Information")
    print(df.info())

    print("\nSummary Statistics")
    print(df.describe())

    print("\nMissing Values")
    print(df.isnull().sum())