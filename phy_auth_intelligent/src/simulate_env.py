"""
Simulates PHY layer attributes (CFO, CIR, RSSI) under varying conditions.
"""

import numpy as np

def simulate_cfo(n_samples, mean=0, std=2.35e-7 * 2.5e9):
    return np.random.normal(loc=mean, scale=std, size=n_samples)

def simulate_cir(n_samples, taps=12):
    amp = np.random.rayleigh(scale=1.0, size=(n_samples, taps))
    phase = np.random.uniform(0, 2 * np.pi, size=(n_samples, taps))
    cir = np.sum(amp * np.exp(1j * phase), axis=1)
    return np.real(cir)

def simulate_rssi(n_samples, d_range=(1, 100)):
    d = np.random.uniform(*d_range, size=n_samples)
    rssi = -36.1 * np.log10(d / 10) - 75
    return rssi
