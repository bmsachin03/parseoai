import pandas as pd

# Read the CSV file
#df = pd.read_csv('/mnt/sachin/PLA/ISE-based/data/Book1.csv', dtype=str)


df = pd.read_csv('/mnt/sachin/PLA/ISE-based/data/Book1.csv', delimiter=';', dtype=str, on_bad_lines='skip')
print("Columns found in CSV:")
print(df.columns.tolist())
# Function to clean and convert values
def clean_and_format(val):
    try:
        val = val.lstrip("'").replace(',', '.')
        return f"{float(val):.10f}"
    except:
        return val  # In case of invalid data, return as-is

# Apply to both columns
for col in ['dlBler', 'ulBler']:
    if col in df.columns:
        df[col] = df[col].apply(clean_and_format)

for col in ['dlBler', 'ulBler']:
    df[col] = df[col].str.replace(',', '.', regex=False).astype(float)
    df[col] = df[col].map(lambda x: f"{x:.10f}")

# Save to new CSV
df.to_csv('/mnt/sachin/PLA/ISE-based/data/Book1_converted.csv', index=False, sep=';')

print("Conversion completed. Output saved to 'output.csv'")
