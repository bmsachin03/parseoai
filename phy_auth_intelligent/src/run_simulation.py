from simulate_env import simulate_cfo, simulate_cir, simulate_rssi
from preprocess import normalize_vector
from klms_authenticator import KLMSAuthenticator

# Generate synthetic PHY attribute samples
n_samples = 200
cfo_samples = simulate_cfo(n_samples)
cir_samples = simulate_cir(n_samples)
rssi_samples = simulate_rssi(n_samples)

# Assume 0 = attacker, 1 = legitimate
labels = [1 if i < n_samples // 2 else 0 for i in range(n_samples)]

# Combine and normalize
authenticator = KLMSAuthenticator()
attr_names = ["CFO", "CIR", "RSSI"]
errors = []

for i in range(n_samples):
    sample = [cfo_samples[i], cir_samples[i], rssi_samples[i]]
    x = normalize_vector(sample, attr_names)
    y = labels[i]

    y_hat = authenticator.predict(x)
    err = authenticator.update(x, y)
    errors.append(abs(err))

    print(f"Sample {i+1}/{n_samples} | True: {y}, Predicted: {round(y_hat, 2)}, Error: {round(err, 2)}")

print("Simulation completed.")

