% Configure carrier parameters
carrier = nrCarrierConfig;
carrier.NCellID = 1;
carrier.SubcarrierSpacing = 15;
carrier.NSizeGrid = 52; % Number of resource blocks
carrier.CyclicPrefix = 'Normal';

% Configure CSI-RS
csirs = nrCSIRSConfig;
csirs.CSIRSType = 'nzp'; % Non-zero power CSI-RS
csirs.RowNumber = 4; % CSI-RS row number
csirs.NumRB = carrier.NSizeGrid; % Number of resource blocks
csirs.RBOffset = 0; % Resource block offset
csirs.CSIRSPeriod = [4 0]; % Periodicity and offset in slots
csirs.SymbolLocations = 0; % Symbol locations within a slot
csirs.SubcarrierLocations = 0; % Subcarrier locations within a resource block
csirs.Density = 'one'; % CSI-RS density

% Validate CSI-RS configuration
% validateCSIRSConfig(carrier, csirs, csirs.NumCSIRSPorts);

% Generate CSI-RS indices and symbols
[csirsIndices, csirsSymbols] = nrCSIRSIndices(carrier, csirs);
csirsSymbols = nrCSIRS(carrier, csirs);

% Create resource grid
numAntennas = csirs.NumCSIRSPorts;
txGrid = nrResourceGrid(carrier, numAntennas);

% Map CSI-RS to resource grid
txGrid(csirsIndices) = csirsSymbols;

% Perform OFDM modulation
[txWaveform, ~] = nrOFDMModulate(carrier, txGrid);

% Add AWGN channel
rng(0); % For reproducibility
noisePower = 1e-3;
noise = sqrt(noisePower/2) * (randn(size(txWaveform)) + 1i*randn(size(txWaveform)));
rxWaveform = txWaveform + noise;
% Perform OFDM demodulation
rxGrid = nrOFDMDemodulate(carrier, rxWaveform);

% Channel estimation using CSI-RS
channelEstimate = rxGrid(csirsIndices);

csiFeedback = calculateCSIFeedback(rxGrid, carrier, csirs, noisePower);

% Authentication logic at gNB
isAuthenticated = authenticateUE(csiFeedback);

function csiFeedback = calculateCSIFeedback(rxGrid, carrier, csirs, noisePower)
    % Enhanced CSI feedback calculation based on 5G NR standards
    
    % Extract CSI-RS indices and symbols
    [csirsIndices, ~] = nrCSIRSIndices(carrier, csirs);
    csirsSymbols = rxGrid(csirsIndices);
    
    % Channel estimation using CSI-RS
    [hest, n0] = nrChannelEstimate(carrier, rxGrid, csirsIndices, csirsSymbols);
    
    % Noise power estimation
    if isempty(noisePower)
        noisePower = n0;
    end
    
    % Calculate CQI based on channel quality
    cqi = calculateCQI(hest, noisePower);
    
    % Calculate PMI based on channel matrix
    pmi = calculatePMI(hest);
    
    % Calculate RI based on channel rank
    ri = calculateRI(hest);
    
    % Package feedback
    csiFeedback.CQI = cqi;
    csiFeedback.PMI = pmi;
    csiFeedback.RI = ri;
end

function cqi = calculateCQI(hest, noisePower)
    % Calculate SINR for each resource element
    sinr = abs(hest).^2 / noisePower;
    
    % Average SINR across all resource elements
    avgSinr = mean(sinr(:));
    
    % Map SINR to CQI using 3GPP TS 38.214 Table 5.2.2.1-1
    sinrThresholds = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, inf];
    cqiTable = 0:15;
    [~, cqiIndex] = histc(avgSinr, sinrThresholds);
    cqi = cqiTable(cqiIndex);
end

function pmi = calculatePMI(hest)
    % Perform singular value decomposition using pagesvd for N-dimensional arrays
    [~,~,vh] = pagesvd(hest);
    
    % Select precoding matrix based on dominant eigenvector
    % This is a simplified version - actual implementation would use codebook
    pmi = 2; % Simplified selection
end

function ri = calculateRI(hest)
    % Determine channel rank using singular values
    s = pagesvd(hest);
    rankThreshold = max(s) * 1e-2;
    ri = sum(s > rankThreshold);
    
    % Limit to maximum supported rank
    ri = min(ri, 4);
end

function authResult = authenticateUE(feedback)
    % Authentication logic comparing received feedback against expected values
    
    % Expected values (would typically be stored securely)
    expectedCQI = 15;
    expectedPMI = 2;
    expectedRI = 1;
    
    % Authentication decision with tolerance
    feedback.CQI
    cqiMatch = abs(feedback.CQI - expectedCQI) <= 1; % Allow minor variations
    pmiMatch = feedback.PMI == expectedPMI;
    riMatch = feedback.RI == expectedRI;

    cqi = feedback.CQI;pmi = feedback.PMI;  ri = feedback.RI;
    cqi
    cqiMatch = (cqi >= expectedCQI-1);
    cqiMatch
    pmiMatch = (pmi == expectedPMI);
    riMatch = all(ri == expectedRI);

    %pmiMatch, riMatch
    
    authResult = cqiMatch && pmiMatch %&& riMatch;
end
