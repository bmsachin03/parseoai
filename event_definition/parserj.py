import json
import pandas as pd
import sys

json_file = "gNB_logs_28-02-2025_20-26-35__28-02-2025_20-38-29.json"
with open(json_file) as json_data:
    feature_data = json.load(json_data)["_buffer"]
    json_data.close()

flat_data = []

# print(feature_data)

# import sys
# sys.exit()
flat_data = []
for entry in feature_data:
    for ue in entry["ues"]:
        print(ue)
        flat_entry = {
            "ueId": ue["ueId"] if "ueId" in ue else "",
            "rnti": ue["rnti"] if "rnti" in ue else "",
            "inSync": ue["inSync"] if "inSync" in ue else "",
            "dlBytes": ue["dlBytes"] if "dlBytes" in ue else "",
            "dlMcs": ue["dlMcs"] if "dlMcs" in ue else "",
            "dlBler": ue["dlBler"] if "dlBler" in ue else "",
            "ulBytes": ue["ulBytes"] if "ulBytes" in ue else "",
            "ulMcs": ue["ulMcs"] if "ulMcs" in ue else "",
            "ulBler": ue["ulBler"] if "ulBler" in ue else "",
            "ri": ue["ri"] if "ri" in ue else "",
            "pmi": ue["pmi"] if "pmi" in ue else "",
            "phr": ue["phr"] if "phr" in ue else "",
            "pcmax": ue["pcmax"] if "pcmax" in ue else "",
            "rsrq": ue["rsrq"] if "rsrq" in ue else "",
            "sinr": ue["sinr"] if "sinr" in ue else "",
            "rsrp": ue["rsrp"] if "rsrp" in ue else "",
            "rssi": ue["rssi"] if "rssi" in ue else "",
            "cqi": ue["cqi"] if "cqi" in ue else "",
            "pucchSnr": ue["pucchSnr"] if "pucchSnr" in ue else "",
            "puschSnr": ue["puschSnr"] if "puschSnr" in ue else "",
            "id": entry["id"] if "id" in entry else "",
            "frame": entry["frame"] if "frame" in entry else "",
            "slot": entry["slot"] if "slot" in entry else "",
            "pci": entry["pci"] if "pci" in entry else "",
            "dlCarrierFreq": entry["dlCarrierFreq"] if "dlCarrierFreq" in entry else "",
            "ulCarrierFreq": entry["ulCarrierFreq"] if "ulCarrierFreq" in entry else "",
            "avgLdpcIterations": entry["avgLdpcIterations"] if "avgLdpcIterations" in entry else "",
            "timestamp": entry["timestamp"] if "timestamp" in entry else "",
        }
        flat_data.append(flat_entry)
        
df = pd.DataFrame(flat_data)

df.to_csv("feature_vector.csv", index=False)

print("CSV file saved successfully!")