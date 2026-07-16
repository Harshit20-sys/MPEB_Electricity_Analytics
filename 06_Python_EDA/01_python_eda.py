import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# LOAD FEATURE DATASET
# ============================================================

file_path = "../05_Feature_Engineering/mpeb_consumer_features.csv"

df = pd.read_csv(
    file_path,
    parse_dates=["Connection Date", "Reading Date"]
)

print("DATASET LOADED SUCCESSFULLY")
print("-" * 50)

print("Dataset Shape:", df.shape)
print("Total Rows:", len(df))
print("Total Columns:", len(df.columns))

print("\nMissing Billed Unit:", df["Billed Unit"].isnull().sum())
print("Missing Energy Charge:", df["Energy Charge"].isnull().sum())

print("\nConsumer Status:")
print(df["Consumer Status"].value_counts())

print("\nBill Type:")
print(df["Bill Type"].value_counts())



# ============================================================
# EDA 1: CONSUMER STATUS DISTRIBUTION
# ============================================================

consumer_status_counts = df["Consumer Status"].value_counts()

print("\nCONSUMER STATUS DISTRIBUTION")
print("-" * 50)

print(consumer_status_counts)

consumer_status_counts.plot(
    kind="bar"
)

plt.title("Consumer Status Distribution")
plt.xlabel("Consumer Status")
plt.ylabel("Number of Consumers")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()


# ============================================================
# EDA 2: AREA-WISE METERING GAP
# ============================================================

area_metering = pd.crosstab(
    df["Area Type"],
    df["Metering Status"],
    normalize="index"
) * 100

print("\nAREA-WISE METERING PERCENTAGE")
print("-" * 50)
print(area_metering.round(2))

area_metering.plot(
    kind="bar"
)

plt.title("Metering Status by Area Type")
plt.xlabel("Area Type")
plt.ylabel("Percentage of Consumers")
plt.xticks(rotation=0)
plt.legend(title="Metering Status")
plt.tight_layout()
plt.show()


# ============================================================
# EDA 3: TARIFF-WISE BILLED UNIT ANALYSIS
# ============================================================

tariff_consumption = (
    df[df["Bill Type"] != "PDC"]
    .groupby("Tariff Category", observed=True)["Billed Unit"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTARIFF-WISE TOTAL BILLED UNITS")
print("-" * 50)

print(tariff_consumption.round(2))

tariff_consumption.plot(
    kind="bar"
)

plt.title("Total Billed Units by Tariff Category")
plt.xlabel("Tariff Category")
plt.ylabel("Total Billed Units")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()


# ============================================================
# EDA 4: TARIFF-WISE AVERAGE BILLED UNIT
# ============================================================

tariff_average_consumption = (
    df[df["Bill Type"] != "PDC"]
    .groupby("Tariff Category", observed=True)["Billed Unit"]
    .mean()
    .sort_values(ascending=False)
)

print("\nTARIFF-WISE AVERAGE BILLED UNIT")
print("-" * 50)

print(tariff_average_consumption.round(2))

tariff_average_consumption.plot(
    kind="bar"
)

plt.title("Average Billed Unit by Tariff Category")
plt.xlabel("Tariff Category")
plt.ylabel("Average Billed Unit")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()


# ============================================================
# EDA 5: BILLING EXCEPTION CATEGORY ANALYSIS
# ============================================================

exception_counts = (
    df["Billing Exception Category"]
    .value_counts()
)

print("\nBILLING EXCEPTION CATEGORY")
print("-" * 50)

print(exception_counts)

exception_counts.plot(
    kind="bar"
)

plt.title("Billing Exception Category Distribution")
plt.xlabel("Billing Exception Category")
plt.ylabel("Number of Records")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()


# ============================================================
# EDA 6: CHARGE PER UNIT DISTRIBUTION
# ============================================================

charge_data = df[
    (df["Bill Type"] != "PDC") &
    (df["Charge Per Unit"].notna())
]["Charge Per Unit"]

print("\nCHARGE PER UNIT DISTRIBUTION")
print("-" * 50)

print(charge_data.describe())

print(
    "\nHigh Charge Per Unit Records:",
    df["High Charge Per Unit Flag"].sum()
)

plt.hist(
    charge_data,
    bins=50
)

plt.title("Charge Per Unit Distribution")
plt.xlabel("Charge Per Unit")
plt.ylabel("Number of Consumers")
plt.tight_layout()
plt.show()


# ============================================================
# EDA 7: EXTREME CHARGE PER UNIT INVESTIGATION
# ============================================================

extreme_charge_records = (
    df[
        (df["Bill Type"] != "PDC") &
        (df["Charge Per Unit"].notna())
    ]
    .sort_values(
        "Charge Per Unit",
        ascending=False
    )
    [
        [
            "Consumer No",
            "Tariff Category",
            "Bill Type",
            "Reading Type",
            "Billed Unit",
            "Energy Charge",
            "Charge Per Unit"
        ]
    ]
    .head(20)
)

print("\nTOP 20 EXTREME CHARGE PER UNIT RECORDS")
print("-" * 50)

print(
    extreme_charge_records.to_string(
        index=False
    )
)



# ============================================================
# EDA 8: TINY CONSUMPTION IMPACT ANALYSIS
# ============================================================

tiny_consumption = df[
    (df["Bill Type"] != "PDC") &
    (df["Billed Unit"] > 0) &
    (df["Billed Unit"] < 1)
]

print("\nTINY CONSUMPTION IMPACT ANALYSIS")
print("-" * 50)

print(
    "Records With Billed Unit Between 0 and 1:",
    len(tiny_consumption)
)

print(
    "Average Charge Per Unit:",
    tiny_consumption["Charge Per Unit"].mean()
)

print(
    "Median Charge Per Unit:",
    tiny_consumption["Charge Per Unit"].median()
)

print("\nTariff Distribution:")
print(
    tiny_consumption["Tariff Category"]
    .value_counts()
)


# ============================================================
# EDA 9: CONSUMPTION SEGMENT ANALYSIS
# ============================================================

consumption_segment_analysis = (
    df[df["Bill Type"] != "PDC"]
    .groupby(
        "Consumption Segment",
        observed=True
    )
    .agg(
        Total_Consumers=("Consumer No", "count"),
        Average_Billed_Unit=("Billed Unit", "mean"),
        Average_Energy_Charge=("Energy Charge", "mean")
    )
)

print("\nCONSUMPTION SEGMENT ANALYSIS")
print("-" * 50)

print(
    consumption_segment_analysis.round(2)
)

consumption_segment_analysis[
    "Total_Consumers"
].plot(
    kind="bar"
)

plt.title("Consumer Distribution by Consumption Segment")
plt.xlabel("Consumption Segment")
plt.ylabel("Number of Consumers")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()


# ============================================================
# EDA 10: AREA-WISE CONSUMPTION AND CHARGE ANALYSIS
# ============================================================

area_analysis = (
    df[df["Bill Type"] != "PDC"]
    .groupby("Area Type")
    .agg(
        Total_Consumers=("Consumer No", "count"),
        Total_Billed_Unit=("Billed Unit", "sum"),
        Average_Billed_Unit=("Billed Unit", "mean"),
        Average_Energy_Charge=("Energy Charge", "mean"),
        Zero_Unit_Exceptions=("Zero Unit Exception Flag", "sum")
    )
)

area_analysis["Zero_Unit_Exception_Percentage"] = (
    area_analysis["Zero_Unit_Exceptions"]
    / area_analysis["Total_Consumers"]
    * 100
)

print("\nAREA-WISE CONSUMPTION AND CHARGE ANALYSIS")
print("-" * 50)

print(area_analysis.round(2))

area_analysis[
    "Average_Billed_Unit"
].plot(
    kind="bar"
)

plt.title("Average Billed Unit by Area Type")
plt.xlabel("Area Type")
plt.ylabel("Average Billed Unit")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# ============================================================
# EDA 11: TOP LOCATIONS BY ZERO UNIT EXCEPTION RATE
# ============================================================

location_exception_analysis = (
    df[df["Bill Type"] != "PDC"]
    .groupby("Location Code")
    .agg(
        Total_Consumers=("Consumer No", "count"),
        Zero_Unit_Exceptions=("Zero Unit Exception Flag", "sum")
    )
)

location_exception_analysis = location_exception_analysis[
    location_exception_analysis["Total_Consumers"] >= 100
].copy()

location_exception_analysis["Exception_Percentage"] = (
    location_exception_analysis["Zero_Unit_Exceptions"]
    / location_exception_analysis["Total_Consumers"]
    * 100
)

top_exception_locations = (
    location_exception_analysis
    .sort_values(
        "Exception_Percentage",
        ascending=False
    )
    .head(10)
)

print("\nTOP 10 LOCATIONS BY ZERO UNIT EXCEPTION RATE")
print("-" * 50)

print(
    top_exception_locations.round(2)
)

top_exception_locations[
    "Exception_Percentage"
].plot(
    kind="bar"
)

plt.title("Top 10 Locations by Zero Unit Exception Rate")
plt.xlabel("Location Code")
plt.ylabel("Exception Percentage")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()