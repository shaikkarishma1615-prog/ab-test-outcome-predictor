import numpy as np
import pandas as pd
import os


def generate_experiment(experiment_id, num_users, conversion_rate_A, conversion_rate_B):

    user_ids = np.arange(1, num_users + 1)

    groups = np.random.choice(['A', 'B'], size=num_users)

    conversions = []

    for group in groups:
        if group == 'A':
            converted = np.random.binomial(1, conversion_rate_A)
        else:
            converted = np.random.binomial(1, conversion_rate_B)

        conversions.append(converted)

    df = pd.DataFrame({
        "user_id": user_ids,
        "group": groups,
        "converted": conversions
    })

    os.makedirs("data", exist_ok=True)

    df.to_csv(f"data/experiment_{experiment_id}.csv", index=False)

    print(f"Experiment {experiment_id} saved successfully!")


if __name__ == "__main__":

    for i in range(1, 13):

        generate_experiment(
            experiment_id=i,
            num_users=5000,
            conversion_rate_A=0.10,
            conversion_rate_B=0.12
        )