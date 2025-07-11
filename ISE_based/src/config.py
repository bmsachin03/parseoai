import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Data paths
RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "ue248_1950.csv")

RELEVANT_FEATURES = [
    "rsrp", "cqi", "pucchSnr", "rssi", "dlBytes", "dlMcs",
    "ulBytes", "ulMcs", "ulBler", "ri", "pcmax", "phr", "rsrq", "sinr", "puschSnr"
]
UE_ID_COL = "ueId"