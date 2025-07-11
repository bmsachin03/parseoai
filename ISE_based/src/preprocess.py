import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

def load_and_clean_data(filepath: str, feature_list: list, ue_id_col: str) -> pd.DataFrame:
    df = pd.read_csv(filepath, sep=';', decimal='.', engine='python')

    if len(df.columns) == 1:
        header_line = df.columns[0]
        columns = [col.strip() for col in header_line.split(';') if col.strip()]
        df = pd.read_csv(filepath, sep=';', decimal='.', names=columns, header=1, engine='python')

    df.columns = df.columns.str.strip()

    for col in feature_list:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(',', '.', regex=False)
            df[col] = pd.to_numeric(df[col], errors='coerce')

    existing_cols = [col for col in feature_list + [ue_id_col] if col in df.columns]
    df = df.dropna(subset=existing_cols)
    return df


def get_numerical_features(df: pd.DataFrame, feature_list: list) -> pd.DataFrame:
    # Exclude ID-like columns from numerical features but retain them in df
    exclude_cols = {'ueId', 'id', 'rnti', '_id.$oid'}
    features = [col for col in feature_list if col not in exclude_cols and col in df.columns]
    return df[features].copy()


def mahalanobis_reconstruction(X):
    cov_matrix = np.cov(X.T)
    U, S, Vt = np.linalg.svd(cov_matrix)
    S_inv_sqrt = np.diag(1.0 / np.sqrt(S))
    A_tilde = (U @ S_inv_sqrt @ U.T @ X.T).T
    return A_tilde


def detect_anomalies(X: pd.DataFrame, contamination: float = 0.05) -> pd.Series:
    clf = IsolationForest(contamination=contamination, random_state=42)
    preds = clf.fit_predict(X)
    return pd.Series(preds, index=X.index, name='anomaly')

def convert_to_float(x):
    try:
        # Remove dots (thousands separator), replace comma with dot (decimal), then convert
        return float(str(x).replace('.', '').replace(',', '.'))
    except:
        return np.nan