import pymc as pm
import arviz as az
import matplotlib.pyplot as plt
from data_loader import load_experiment


def bayesian_ab_test(df):

    # Split data
    group_A = df[df["group"] == "A"]
    group_B = df[df["group"] == "B"]

    # Successes and trials
    conversions_A = group_A["converted"].sum()
    conversions_B = group_B["converted"].sum()

    trials_A = len(group_A)
    trials_B = len(group_B)

    with pm.Model():

        # Prior distributions
        theta_A = pm.Beta("theta_A", alpha=1, beta=1)
        theta_B = pm.Beta("theta_B", alpha=1, beta=1)

        # Likelihood
        pm.Binomial(
            "obs_A",
            n=trials_A,
            p=theta_A,
            observed=conversions_A
        )

        pm.Binomial(
            "obs_B",
            n=trials_B,
            p=theta_B,
            observed=conversions_B
        )

        # Posterior sampling
        trace = pm.sample(
            draws=3000,
            tune=1000,
            chains=2,
            random_seed=42,
            progressbar=True
        )

    # Probability that B is better than A
    theta_A_samples = trace.posterior["theta_A"].values.flatten()
    theta_B_samples = trace.posterior["theta_B"].values.flatten()

    probability = (theta_B_samples > theta_A_samples).mean()

    print("=" * 60)
    print("BAYESIAN A/B TEST RESULTS")
    print("=" * 60)

    print(f"Users in Group A : {trials_A}")
    print(f"Users in Group B : {trials_B}")

    print(f"\nConversions A : {conversions_A}")
    print(f"Conversions B : {conversions_B}")

    print(f"\nProbability B > A : {probability:.4f}")

    if probability > 0.95:
        print("\nRecommendation : Stop Experiment")
        print("Winner : Group B")

    elif probability < 0.05:
        print("\nRecommendation : Stop Experiment")
        print("Winner : Group A")

    else:
        print("\nRecommendation : Continue collecting data")

    # Posterior plot
    #pm.plot_posterior(
       # trace,
       # var_names=["theta_A", "theta_B"]
   # )
   # plt.show()


if __name__ == "__main__":

    df = load_experiment(1)

    bayesian_ab_test(df)