import pandas as pd
from scipy.stats import norm
from data_loader import load_experiment


def classical_ab_test(df):
    """
    Perform a classical A/B test using a two-proportion Z-test.
    """

    # Split data into Group A and Group B
    group_A = df[df["group"] == "A"]
    group_B = df[df["group"] == "B"]

    # Number of users
    n_A = len(group_A)
    n_B = len(group_B)

    # Conversion rates
    conversion_A = group_A["converted"].mean()
    conversion_B = group_B["converted"].mean()

    print("=" * 50)
    print("CLASSICAL A/B TEST RESULTS")
    print("=" * 50)

    print(f"Users in Group A      : {n_A}")
    print(f"Users in Group B      : {n_B}")
    print(f"Conversion Rate A     : {conversion_A:.4f}")
    print(f"Conversion Rate B     : {conversion_B:.4f}")

    # Number of conversions
    conversions_A = group_A["converted"].sum()
    conversions_B = group_B["converted"].sum()

    # Pooled conversion rate
    pooled_conversion = (
        conversions_A + conversions_B
    ) / (n_A + n_B)

    # Standard Error
    standard_error = (
        pooled_conversion
        * (1 - pooled_conversion)
        * (1 / n_A + 1 / n_B)
    ) ** 0.5

    # Z-score
    z_score = (
        conversion_B - conversion_A
    ) / standard_error

    # Two-tailed p-value
    p_value = 2 * (1 - norm.cdf(abs(z_score)))

    print(f"\nZ-Score              : {z_score:.4f}")
    print(f"P-Value              : {p_value:.6f}")

    # Decision
    if p_value < 0.05:
        print("\nResult               : Statistically Significant")

        if conversion_B > conversion_A:
            print("Winner               : Group B")
        else:
            print("Winner               : Group A")

    else:
        print("\nResult               : Not Statistically Significant")
        print("Recommendation       : Continue the experiment")

    print("=" * 50)


if __name__ == "__main__":

    df = load_experiment(1)

    classical_ab_test(df)