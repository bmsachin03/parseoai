import pandas as pd
import re

def parse_log(log_text):
    data = []
    lcid_data = []
    
    lines = log_text.strip().split("\n")
    ue_id = None
    
    for line in lines:
        line = line.strip()
        if line.startswith("UE RNTI"):
            match = re.search(r'UE RNTI ([0-9a-fA-F]+)', line)
            if match:
                ue_id = match.group(1)
            
        elif line.startswith("UE") and "MAC:" in line:
            continue  # Skip redundant MAC identifier line
        
        elif line.startswith("UE"):
            key_values = re.findall(r'(\S+): ([^,]+)', line)
            for key, value in key_values:
                data.append({"UE RNTI": ue_id, "Field": key, "Value": value})
        
        elif line.startswith("UE") and "LCID" in line:
            match = re.search(r'UE ([0-9a-fA-F]+): LCID (\d+): TX\s+(\d+) RX\s+(\d+) bytes', line)
            if match:
                lcid_data.append({
                    "UE RNTI": match.group(1),
                    "LCID": match.group(2),
                    "TX bytes": match.group(3),
                    "RX bytes": match.group(4)
                })
    
    return data, lcid_data

def save_to_csv(data, lcid_data, filename_prefix="parsed_output"):
    df_main = pd.DataFrame(data)
    df_lcid = pd.DataFrame(lcid_data)
    df_main.to_csv(f"{filename_prefix}_general.csv", index=False)
    df_lcid.to_csv(f"{filename_prefix}_lcid.csv", index=False)

# Sample log data
log_text = """[NR_MAC]   Frame.Slot 896.0
UE RNTI 8f53 CU-UE-ID 1 in-sync PH 52 dB PCMAX 22 dBm, average RSRP -83 (32 meas)
UE 8f53: UL-RI 1, TPMI 0
UE 8f53: dlsch_rounds 142/0/0/0, dlsch_errors 0, pucch0_DTX 0, BLER 0.00000 MCS (1) 9
UE 8f53: ulsch_rounds 591/19/0/0, ulsch_errors 0, ulsch_DTX 15, BLER 0.12171 MCS (1) 6 (Qm 4 deltaMCS 0 dB) NPRB 5  SNR 19.5 dB
UE 8f53: MAC:    TX          29535 RX          86789 bytes
UE 8f53: LCID 1: TX            913 RX           2270 bytes
UE 8f53: LCID 2: TX              6 RX            116 bytes
UE 8f53: LCID 4: TX              0 RX              0 bytes
UE 8f53: LCID 5: TX            126 RX           3246 bytes"""

data, lcid_data = parse_log(log_text)
save_to_csv(data, lcid_data)
