import os
import pandas as pd
from predictor import predict_winner

TOTAL_EXPERIMENTS = 12

results = []

correct = 0

print("=" * 70)
print("A/B TEST OUTCOME EVALUATION")
print("=" * 70)

for experiment in range(1, TOTAL_EXPERIMENTS + 1):

    early_winner, early_prob = predict_winner(
        experiment,
        percentage=0.40,
    )

    final_winner, final_prob = predict_winner(
        experiment,
        percentage=1.00,
    )

    is_correct = early_winner == final_winner

    if is_correct:
        correct += 1

    results.append({
        "Experiment": experiment,
        "Early Winner": early_winner,
        "Final Winner": final_winner,
        "Early Probability": round(early_prob, 4),
        "Final Probability": round(final_prob, 4),
        "Correct": "Yes" if is_correct else "No"
    })

    print(
        f"Experiment {experiment:2d} | "
        f"Early: {early_winner:10s} "
        f"| Final: {final_winner:10s} "
        f"| {'✅' if is_correct else '❌'}"
    )

accuracy = correct / TOTAL_EXPERIMENTS * 100

print("\n" + "=" * 70)
print(f"Experiments Evaluated : {TOTAL_EXPERIMENTS}")
print(f"Correct Predictions   : {correct}")
print(f"Accuracy              : {accuracy:.2f}%")
print("=" * 70)

# -----------------------------
# Save Report
# -----------------------------

os.makedirs("outputs/reports", exist_ok=True)

report = pd.DataFrame(results)

report.to_csv(
    "outputs/reports/evaluation_report.csv",
    index=False
)

print("\nReport saved successfully!")
print("Location: outputs/reports/evaluation_report.csv")