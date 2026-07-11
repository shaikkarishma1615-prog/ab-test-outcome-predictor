import pandas as pd
import pymc as pm
from data_loader import load_experiment


def predict_winner(experiment_id, percentage=1.0):

    df = load_experiment(experiment_id)

    rows = int(len(df) * percentage)
    df = df.iloc[:rows]

    group_A = df[df["group"] == "A"]
    group_B = df[df["group"] == "B"]

    conversions_A = group_A["converted"].sum()
    conversions_B = group_B["converted"].sum()

    trials_A = len(group_A)
    trials_B = len(group_B)

    with pm.Model():

        theta_A = pm.Beta("theta_A", alpha=1, beta=1)
        theta_B = pm.Beta("theta_B", alpha=1, beta=1)

        pm.Binomial(
            "obs_A",
            n=trials_A,
            p=theta_A,
            observed=conversions_A,
        )

        pm.Binomial(
            "obs_B",
            n=trials_B,
            p=theta_B,
            observed=conversions_B,
        )

        trace = pm.sample(
            draws=1000,
            tune=500,
            chains=2,
            progressbar=False,
            random_seed=42,
        )

    theta_A_samples = trace.posterior["theta_A"].values.flatten()
    theta_B_samples = trace.posterior["theta_B"].values.flatten()

    probability = (theta_B_samples > theta_A_samples).mean()

    if probability >= 0.90:
        winner = "B"

    elif probability <= 0.10:
        winner = "A"

    else:
        winner = "Undecided"

    return winner, probability