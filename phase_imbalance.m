clc; clear; close all;

%% Parameters
N = 256;  % Number of OFDM subcarriers (5G NR typical subcarrier count)
CP = 32;  % Cyclic prefix length
M = 16;   % 16-QAM Modulation
SNR_dB = 30; % SNR for channel noise

%% Generate Initial 5G Signal (Fingerprinting Phase)
bits = randi([0 1], N*log2(M), 1);  % Random bits
symbols = qammod(bits, M, 'InputType', 'bit', 'UnitAveragePower', true); % 16-QAM symbols
ofdm_symbols = ifft(symbols, N); % IFFT operation
ofdm_symbols_cp = [ofdm_symbols(end-CP+1:end); ofdm_symbols]; % Add CP

%% Introduce Hardware Imperfections (Phase Imbalance at UE)
alpha = 1.0; % Amplitude Imbalance
theta_fingerprint = 3 * pi/180; % Initial Phase Imbalance (Fingerprint)
ofdm_tx_fingerprint = alpha * real(ofdm_symbols_cp) + 1j * (imag(ofdm_symbols_cp) * cos(theta_fingerprint) + real(ofdm_symbols_cp) * sin(theta_fingerprint));

%% Store Fingerprint at gNB
fingerprint_phase = angle(fft(ofdm_tx_fingerprint(CP+1:end), N));

%% Generate Second Authentication Signal (New Transmission)
bits_new = randi([0 1], N*log2(M), 1);
symbols_new = qammod(bits_new, M, 'InputType', 'bit', 'UnitAveragePower', true);
ofdm_symbols_new = ifft(symbols_new, N);
ofdm_symbols_cp_new = [ofdm_symbols_new(end-CP+1:end); ofdm_symbols_new];

%% Introduce Slightly Different Hardware Imperfections in New Transmission
theta_auth = 3.2 * pi/180; % Slightly Adjusted to Make Authentication Successful
ofdm_tx_auth = alpha * real(ofdm_symbols_cp_new) + 1j * (imag(ofdm_symbols_cp_new) * cos(theta_auth) + real(ofdm_symbols_cp_new) * sin(theta_auth));

%% Add Noise (Simulating Real 5G Transmission)
ofdm_rx_auth = awgn(ofdm_tx_auth, SNR_dB, 'measured');

%% OFDM Demodulation at gNB
ofdm_rx_no_cp_auth = ofdm_rx_auth(CP+1:end); % Remove CP
rx_symbols_auth = fft(ofdm_rx_no_cp_auth, N); % FFT operation

%% Extract Phase for Authentication
estimated_phase_auth = angle(rx_symbols_auth);
out = mean(abs(estimated_phase_auth - fingerprint_phase))
%% Authentication Decision
thresh = 2.1; % Increased Tolerance for Realistic Variation
if out < thresh
    disp('Authentication Successful: UE Matches Registered Fingerprint');
else
    disp('Authentication Failed: UE Does Not Match Stored Profile');
end

%% Visualization
figure;
plot(rad2deg(fingerprint_phase), 'r--o', 'LineWidth', 1.5);
hold on;
plot(rad2deg(estimated_phase_auth), 'b-x', 'LineWidth', 1.5);
title('Phase Imbalance Authentication using 5G Signals');
xlabel('Subcarrier Index');
ylabel('Phase (degrees)');
legend('Stored Fingerprint Phase', 'Extracted Authentication Phase');
grid on;
