import pandas as pd
import numpy as np

# ============================================================
# LOAD CLEAN DATA
# ============================================================

file_path = "../03_Data_Cleaning/mpeb_consumer_clean.csv"

df = pd.read_csv(
    file_path,
    parse_dates=["Connection Date", "Reading Date"]
)

print("CLEAN DATASET SHAPE:", df.shape)


# ============================================================
# STANDARDIZED LOAD IN KW
# ============================================================

df["Load KW Equivalent"] = np.where(
    df["Sanctioned Load Unit"] == "HP",
    df["Sanctioned Load"] * 0.746,
    df["Sanctioned Load"]
)


# ============================================================
# ZERO UNIT EXCEPTION FLAG
# ============================================================

df["Zero Unit Exception Flag"] = np.where(
    (df["Billed Unit"] == 0) &
    (df["Bill Type"] != "PDC"),
    1,
    0
)


# ============================================================
# READING MISSING FLAG
# ============================================================

df["Reading Missing Flag"] = np.where(
    df["Reading Type"].isna(),
    1,
    0
)


# ============================================================
# LEGACY CONNECTION DATE FLAG
# ============================================================

df["Legacy Date Flag"] = np.where(
    df["Connection Date"] == pd.Timestamp("1980-01-01"),
    1,
    0
)


# ============================================================
# CHARGE PER UNIT
# ============================================================

df["Charge Per Unit"] = np.where(
    df["Billed Unit"] > 0,
    df["Energy Charge"] / df["Billed Unit"],
    np.nan
)


# ============================================================
# VALIDATION
# ============================================================

print("\nFEATURE ENGINEERING VALIDATION")
print("-" * 50)

print(
    "Zero Unit Exception Records:",
    df["Zero Unit Exception Flag"].sum()
)

print(
    "Reading Missing Records:",
    df["Reading Missing Flag"].sum()
)

print(
    "Legacy Date Records:",
    df["Legacy Date Flag"].sum()
)

print(
    "Load KW Equivalent Minimum:",
    df["Load KW Equivalent"].min()
)

print(
    "Load KW Equivalent Maximum:",
    df["Load KW Equivalent"].max()
)

print(
    "Charge Per Unit Missing:",
    df["Charge Per Unit"].isna().sum()
)


# ============================================================
# CONSUMPTION SEGMENT
# ============================================================

df["Consumption Segment"] = pd.cut(
    df["Billed Unit"],
    bins=[-1, 0, 100, 300, 1000, np.inf],
    labels=[
        "ZERO",
        "LOW",
        "MEDIUM",
        "HIGH",
        "VERY HIGH"
    ]
)


# ============================================================
# LOAD SEGMENT
# ============================================================

df["Load Segment"] = pd.cut(
    df["Load KW Equivalent"],
    bins=[0, 1, 5, 10, 50, np.inf],
    labels=[
        "VERY LOW",
        "LOW",
        "MEDIUM",
        "HIGH",
        "VERY HIGH"
    ],
    include_lowest=True
)


# ============================================================
# BILLING EXCEPTION CATEGORY
# ============================================================

conditions = [
    df["Bill Type"] == "PDC",

    df["Reading Type"] == "PFL",

    (df["Bill Type"] == "ACTUAL BILL") &
    (df["Billed Unit"] == 0),

    (df["Reading Type"] == "NORMAL") &
    (df["Billed Unit"] == 0)
]

choices = [
    "PERMANENT DISCONNECTION",
    "PFL ZERO UNIT",
    "ACTUAL BILL ZERO UNIT",
    "NORMAL READING ZERO UNIT"
]

df["Billing Exception Category"] = np.select(
    conditions,
    choices,
    default="NO EXCEPTION"
)


# ============================================================
# SEGMENT VALIDATION
# ============================================================

print("\nANALYTICAL SEGMENT VALIDATION")
print("-" * 50)

print("\nConsumption Segment:")
print(df["Consumption Segment"].value_counts(dropna=False))

print("\nLoad Segment:")
print(df["Load Segment"].value_counts(dropna=False))

print("\nBilling Exception Category:")
print(df["Billing Exception Category"].value_counts(dropna=False))


# ============================================================
# CONNECTION AGE
# ============================================================

reference_date = pd.Timestamp("2024-12-31")

df["Future Connection Date Flag"] = np.where(
    df["Connection Date"] > reference_date,
    1,
    0
)

df["Connection Age Years"] = np.where(
    df["Connection Date"] <= reference_date,
    (
        (reference_date - df["Connection Date"]).dt.days
        / 365.25
    ).round(2),
    np.nan
)

# ============================================================
# CONNECTION ERA
# ============================================================

df["Connection Era"] = pd.cut(
    df["Connection Date"].dt.year,
    bins=[1969, 1989, 1999, 2009, 2019, 2026],
    labels=[
        "1970-1989",
        "1990-1999",
        "2000-2009",
        "2010-2019",
        "2020-2026"
    ]
)


# ============================================================
# CHARGE PER UNIT EXCEPTION FLAG
# ============================================================

charge_per_unit_q1 = df["Charge Per Unit"].quantile(0.25)
charge_per_unit_q3 = df["Charge Per Unit"].quantile(0.75)

charge_per_unit_iqr = (
    charge_per_unit_q3 - charge_per_unit_q1
)

charge_per_unit_upper_limit = (
    charge_per_unit_q3 +
    1.5 * charge_per_unit_iqr
)

df["High Charge Per Unit Flag"] = np.where(
    df["Charge Per Unit"] > charge_per_unit_upper_limit,
    1,
    0
)


# ============================================================
# FINAL FEATURE VALIDATION
# ============================================================

print("\nFINAL FEATURE VALIDATION")
print("-" * 50)

print(
    "Minimum Connection Age:",
    df["Connection Age Years"].min()
)

print(
    "Maximum Connection Age:",
    df["Connection Age Years"].max()
)

print("\nConnection Era:")
print(df["Connection Era"].value_counts(dropna=False))

print("\nCharge Per Unit Q1:", charge_per_unit_q1)
print("Charge Per Unit Q3:", charge_per_unit_q3)
print("Charge Per Unit IQR:", charge_per_unit_iqr)
print(
    "Charge Per Unit Upper Limit:",
    charge_per_unit_upper_limit
)

print(
    "High Charge Per Unit Records:",
    df["High Charge Per Unit Flag"].sum()
)

print(
    "Future Connection Date Records:",
    df["Future Connection Date Flag"].sum()
)

# ============================================================
# EXPORT FEATURE DATASET
# ============================================================

output_file = "../05_Feature_Engineering/mpeb_consumer_features.csv"

df.to_csv(
    output_file,
    index=False
)

print("\nFEATURE DATASET EXPORTED SUCCESSFULLY")
print("Final Dataset Shape:", df.shape)
print("Output File:", output_file)