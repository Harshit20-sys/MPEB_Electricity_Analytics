import pandas as pd
import numpy as np

file_path = "../01_Raw_Data/mpeb_consumer_raw.xlsx"

df = pd.read_excel(file_path)

print("Dataset Shape:", df.shape)
print("Total Rows:", len(df))
print("Total Columns:", len(df.columns))

print("\nCOLUMN NAMES")
print("-" * 50)

for i, column in enumerate(df.columns, start=1):
    print(f"{i}. {column}")




print("\nDATA TYPES")
print("-" * 50)
print(df.dtypes)

print("\nMISSING VALUES")
print("-" * 50)

missing_values = df.isnull().sum()
missing_percent = (missing_values / len(df)) * 100

missing_report = pd.DataFrame({
    "Missing Values": missing_values,
    "Missing Percentage": missing_percent
})

print(missing_report)

print("\nDUPLICATE ROWS")
print("-" * 50)
print("Total Duplicate Rows:", df.duplicated().sum())



print("\nREADING MISSING PATTERN ANALYSIS")
print("-" * 50)

print("\nReading Type Missing by Metering Status:")
print(pd.crosstab(
    df["Metering Status"],
    df["Reading Type"].isnull()
))

print("\nReading Date Missing by Metering Status:")
print(pd.crosstab(
    df["Metering Status"],
    df["Reading Date"].isnull()
))

print("\nReading Type Missing by Consumer Status:")
print(pd.crosstab(
    df["Consumer Status"],
    df["Reading Type"].isnull()
))

print("\nReading Type Missing by Bill Type:")
print(pd.crosstab(
    df["Bill Type"],
    df["Reading Type"].isnull()
))



print("\nREADING DATE MISSING BY BILL TYPE")
print("-" * 50)

print(pd.crosstab(
    df["Bill Type"],
    df["Reading Date"].isnull()
))

print("\nBILLED UNIT SUMMARY BY BILL TYPE")
print("-" * 50)

print(
    df.groupby("Bill Type")["Billed Unit"]
    .agg(["count", "mean", "median", "min", "max"])
)

print("\nZERO BILLED UNIT BY BILL TYPE")
print("-" * 50)

zero_unit_data = df[df["Billed Unit"] == 0]

print(zero_unit_data["Bill Type"].value_counts())



print("\nCATEGORICAL COLUMN AUDIT")
print("-" * 50)

categorical_columns = [
    "DIVISION",
    "Consumer Status",
    "Tariff Category",
    "Tariff Code",
    "Metering Status",
    "Beneficiary",
    "Connection Type",
    "Connection Phase",
    "Bill Type",
    "Area Type",
    "Sanctioned Load Unit",
    "Aadhaar available?",
    "Category",
    "Reading Type"
]

for column in categorical_columns:
    print(f"\n--- {column} ---")
    print("Unique Values:", df[column].nunique(dropna=False))
    print(df[column].value_counts(dropna=False))




print("\nRELATIONSHIP VALIDATION")
print("-" * 50)

print("\nConsumer Status vs Bill Type:")
print(pd.crosstab(
    df["Consumer Status"],
    df["Bill Type"]
))

print("\nMetering Status vs Reading Type:")
print(pd.crosstab(
    df["Metering Status"],
    df["Reading Type"],
    dropna=False
))

print("\nTariff Category vs Metering Status:")
print(pd.crosstab(
    df["Tariff Category"],
    df["Metering Status"]
))

print("\nSanctioned Load Unit vs Tariff Category:")
print(pd.crosstab(
    df["Sanctioned Load Unit"],
    df["Tariff Category"]
))

print("\nReading Type vs Zero Billed Unit:")
df["Zero Unit Flag Audit"] = np.where(
    df["Billed Unit"] == 0,
    "ZERO",
    "NON-ZERO"
)

print(pd.crosstab(
    df["Reading Type"].fillna("MISSING"),
    df["Zero Unit Flag Audit"]
))