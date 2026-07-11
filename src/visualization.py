import pandas as pd
import matplotlib.pyplot as plt
from data_loader import load_experiment
def plot_group_distribution(df):
    group_counts = df["group"].value_counts()

    plt.figure(figsize=(6, 4))
    group_counts.plot(kind="bar")

    plt.title("Users in Group A and Group B")
    plt.xlabel("Group")
    plt.ylabel("Number of Users")

    plt.tight_layout()
    plt.show()
def plot_conversion_counts(df):
    conversion_counts = df["converted"].value_counts()

    plt.figure(figsize=(6,4))
    conversion_counts.plot(kind="bar")

    plt.title("Conversion Results")
    plt.xlabel("Converted")
    plt.ylabel("Number of Users")

    plt.tight_layout()
    plt.show()
def plot_conversion_rate(df):

    conversion_rate = (
        df.groupby("group")["converted"]
        .mean() * 100
    )

    plt.figure(figsize=(6,4))
    conversion_rate.plot(kind="bar")

    plt.title("Conversion Rate by Group")
    plt.xlabel("Group")
    plt.ylabel("Conversion Rate (%)")

    plt.tight_layout()
    plt.show()
if __name__ == "__main__":

    df = load_experiment(1)

    plot_group_distribution(df)

    plot_conversion_counts(df)

    plot_conversion_rate(df)