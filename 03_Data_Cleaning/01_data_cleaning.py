import pandas as pd
import numpy as np

# ============================================================
# LOAD RAW DATA
# ============================================================

file_path = "../01_Raw_Data/mpeb_consumer_raw.xlsx"

df = pd.read_excel(file_path)

print("RAW DATASET SHAPE:", df.shape)


# ============================================================
# REMOVE NON-ANALYTICAL COLUMNS
# ============================================================

columns_to_remove = [
    "DIVISION",
    "Consumer Name",
    "Address"
]

df.drop(columns=columns_to_remove, inplace=True)

print("\nREMOVED COLUMNS:")
for column in columns_to_remove:
    print("-", column)

print("\nDATASET SHAPE AFTER COLUMN REMOVAL:", df.shape)

print("\nREMAINING COLUMNS:")
for i, column in enumerate(df.columns, start=1):
    print(f"{i}. {column}")



# ============================================================
# DATE QUALITY AUDIT
# ============================================================

print("\nDATE QUALITY AUDIT")
print("-" * 50)

date_columns = [
    "Connection Date",
    "Reading Date"
]

for column in date_columns:

    print(f"\n--- {column} ---")

    print("Current Data Type:", df[column].dtype)

    converted_date = pd.to_datetime(
        df[column],
        errors="coerce"
    )

    print("Missing Before Conversion:", df[column].isnull().sum())
    print("Invalid Dates After Conversion:", converted_date.isnull().sum())

    print("Minimum Date:", converted_date.min())
    print("Maximum Date:", converted_date.max())

    print("\nTop 10 Most Frequent Dates:")
    print(converted_date.value_counts().head(10))



# ============================================================
# STANDARDIZE TEXT COLUMNS
# ============================================================

text_columns = [
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

for column in text_columns:
    df[column] = (
        df[column]
        .astype("string")
        .str.strip()
        .str.upper()
    )


# ============================================================
# STANDARDIZE DATE COLUMNS
# ============================================================

df["Connection Date"] = pd.to_datetime(
    df["Connection Date"],
    errors="coerce"
)

df["Reading Date"] = pd.to_datetime(
    df["Reading Date"],
    errors="coerce"
)


# ============================================================
# VALIDATION
# ============================================================

print("\nTEXT AND DATE STANDARDIZATION COMPLETE")
print("-" * 50)

print("\nConnection Date Type:", df["Connection Date"].dtype)
print("Reading Date Type:", df["Reading Date"].dtype)

print("\nReading Type Values:")
print(df["Reading Type"].value_counts(dropna=False))

print("\nBill Type Values:")
print(df["Bill Type"].value_counts(dropna=False))



# ============================================================
# NUMERIC COLUMN VALIDATION
# ============================================================

numeric_columns = [
    "Sanctioned Load",
    "Billed Unit",
    "Energy Charge"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

print("\nNUMERIC VALIDATION")
print("-" * 50)

for column in numeric_columns:
    print(f"\n--- {column} ---")
    print("Missing Values:", df[column].isnull().sum())
    print("Negative Values:", (df[column] < 0).sum())
    print("Minimum:", df[column].min())
    print("Maximum:", df[column].max())


# ============================================================
# BUSINESS RULE VALIDATION
# ============================================================

print("\nBUSINESS RULE VALIDATION")
print("-" * 50)

pdc_invalid_units = df[
    (df["Bill Type"] == "PDC") &
    (df["Billed Unit"] != 0)
]

print(
    "PDC Records With Non-Zero Billed Unit:",
    len(pdc_invalid_units)
)

zero_unit_non_pdc = df[
    (df["Billed Unit"] == 0) &
    (df["Bill Type"] != "PDC")
]

print(
    "Non-PDC Zero Billed Unit Records:",
    len(zero_unit_non_pdc)
)

zero_unit_positive_charge = df[
    (df["Billed Unit"] == 0) &
    (df["Energy Charge"] > 0)
]

print(
    "Zero Unit With Positive Energy Charge:",
    len(zero_unit_positive_charge)
)


# ============================================================
# EXPORT CLEAN DATASET
# ============================================================

output_file = "../03_Data_Cleaning/mpeb_consumer_clean.csv"

df.to_csv(
    output_file,
    index=False
)

print("\nCLEAN DATASET EXPORTED SUCCESSFULLY")
print("Final Dataset Shape:", df.shape)
print("Output File:", output_file)