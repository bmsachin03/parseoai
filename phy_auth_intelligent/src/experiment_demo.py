# 🧪 PHY Layer Authentication: Experiment Demo
# This script simulates the intelligent authentication scheme and visualizes ROC curve and error statistics.

import sys
sys.path.append("../src")  # Adjust path if running outside notebooks

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
from simulate_env import simulate_cfo, simulate_cir, simulate_rssi
from preprocess import normalize_vector
from klms_authenticator import KLMSAuthenticator

# Simulate data
n_samples = 300
cfo = simulate_cfo(n_samples)
cir = simulate_cir(n_samples)
rssi = simulate_rssi(n_samples)

# 0 = attacker, 1 = legitimate
labels = np.array([1 if i < n_samples // 2 else 0 for i in range(n_samples)])

authenticator = KLMSAuthenticator()
attr_names = ["CFO", "CIR", "RSSI"]

predictions = []
errors = []

for i in range(n_samples):
    sample = [cfo[i], cir[i], rssi[i]]
    x = normalize_vector(sample, attr_names)
    y = labels[i]
    y_hat = authenticator.predict(x)
    predictions.append(y_hat)
    err = authenticator.update(x, y)
    errors.append(abs(err))

# Plot ROC Curve
fpr, tpr, thresholds = roc_curve(labels, predictions)
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, label=f"ROC Curve (AUC = {roc_auc:.2f})")
plt.plot([0, 1], [0, 1], 'k--')
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve for KLMS Authenticator")
plt.legend()
plt.grid(True)
plt.show()

# Plot prediction errors
plt.figure(figsize=(10, 4))
plt.plot(errors, label='Prediction Error')
plt.title("KLMS Prediction Error per Sample")
plt.xlabel("Sample Index")
plt.ylabel("Error Magnitude")
plt.grid(True)
plt.legend()
plt.show()

