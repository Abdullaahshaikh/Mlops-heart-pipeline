print("Drift detector running successfully")
import pandas as pd
import numpy as np
from scipy.stats import entropy


# ===============================
# PSI CALCULATION
# ===============================
def calculate_psi(expected, actual, bins=10):

    breakpoints = np.linspace(0, 100, bins + 1)

    expected_bins = np.percentile(expected, breakpoints)

    expected_counts, _ = np.histogram(expected, expected_bins)
    actual_counts, _ = np.histogram(actual, expected_bins)

    expected_ratio = expected_counts / len(expected)
    actual_ratio = actual_counts / len(actual)

    psi = np.sum(
        (expected_ratio - actual_ratio)
        * np.log((expected_ratio + 1e-6) /
                 (actual_ratio + 1e-6))
    )

    return psi


# ===============================
# KL DIVERGENCE
# ===============================
def kl_divergence(p, q):

    p_hist, _ = np.histogram(p, bins=20, density=True)
    q_hist, _ = np.histogram(q, bins=20, density=True)

    return entropy(p_hist + 1e-6, q_hist + 1e-6)


# ===============================
# DRIFT DETECTION ENGINE
# ===============================
def detect_drift():

    print("\nChecking data drift...\n")

    train_df = pd.read_csv("data/train_reference.csv")
    prod_df = pd.read_csv("data/production_data.csv")

    report = {}

    for col in train_df.columns:

        psi = calculate_psi(train_df[col], prod_df[col])
        kl = kl_divergence(train_df[col], prod_df[col])

        report[col] = {
            "PSI": float(psi),
            "KL": float(kl)
        }

        print(f"{col} - PSI: {psi:.4f} | KL: {kl:.4f}")

    return report


# ===============================
# DRIFT THRESHOLD CHECK
# ===============================
def drift_detected(report):

    for feature, metrics in report.items():

        if metrics["PSI"] > 0.25:
            print(f"\nDRIFT DETECTED in feature: {feature}")
            return True

    print("\n✅ No significant drift detected")
    return False


# ===============================
# MAIN EXECUTION
# ===============================
if __name__ == "__main__":

    report = detect_drift()
    drift_detected(report)