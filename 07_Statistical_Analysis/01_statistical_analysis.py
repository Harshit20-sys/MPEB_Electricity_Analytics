import pandas as pd
import numpy as np

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


# ============================================================
# DESCRIPTIVE STATISTICS
# ============================================================

analysis_data = df[
    df["Bill Type"] != "PDC"
]

statistical_columns = [
    "Billed Unit",
    "Energy Charge",
    "Load KW Equivalent",
    "Charge Per Unit"
]

descriptive_statistics = (
    analysis_data[statistical_columns]
    .describe(
        percentiles=[
            0.01,
            0.05,
            0.25,
            0.50,
            0.75,
            0.95,
            0.99
        ]
    )
    .T
)

print("\nDESCRIPTIVE STATISTICS")
print("-" * 50)

print(
    descriptive_statistics.to_string()
)



# ============================================================
# SKEWNESS ANALYSIS
# ============================================================

skewness_results = (
    analysis_data[
        statistical_columns
    ]
    .skew()
    .sort_values(
        ascending=False
    )
)

print("\nSKEWNESS ANALYSIS")
print("-" * 50)

print(skewness_results)

print("\nSKEWNESS INTERPRETATION")

for column, skewness in skewness_results.items():

    if skewness > 1:
        interpretation = "HIGHLY RIGHT-SKEWED"

    elif skewness > 0.5:
        interpretation = "MODERATELY RIGHT-SKEWED"

    elif skewness < -1:
        interpretation = "HIGHLY LEFT-SKEWED"

    elif skewness < -0.5:
        interpretation = "MODERATELY LEFT-SKEWED"

    else:
        interpretation = "APPROXIMATELY SYMMETRIC"

    print(
        f"{column}: "
        f"{skewness:.2f} -> "
        f"{interpretation}"
    )



# ============================================================
# IQR OUTLIER ANALYSIS
# ============================================================

print("\nIQR OUTLIER ANALYSIS")
print("-" * 50)

iqr_results = []

for column in statistical_columns:

    column_data = analysis_data[column].dropna()

    q1 = column_data.quantile(0.25)
    q3 = column_data.quantile(0.75)

    iqr = q3 - q1

    lower_limit = q1 - (1.5 * iqr)
    upper_limit = q3 + (1.5 * iqr)

    outlier_count = (
        (column_data < lower_limit) |
        (column_data > upper_limit)
    ).sum()

    outlier_percentage = (
        outlier_count /
        len(column_data)
    ) * 100

    iqr_results.append({
        "Metric": column,
        "Q1": q1,
        "Q3": q3,
        "IQR": iqr,
        "Lower Limit": lower_limit,
        "Upper Limit": upper_limit,
        "Outlier Count": outlier_count,
        "Outlier Percentage": outlier_percentage
    })

iqr_results_df = pd.DataFrame(iqr_results)

print(
    iqr_results_df
    .round(2)
    .to_string(index=False)
)


# ============================================================
# SPEARMAN CORRELATION ANALYSIS
# ============================================================

correlation_columns = [
    "Billed Unit",
    "Energy Charge",
    "Load KW Equivalent"
]

spearman_correlation = (
    analysis_data[correlation_columns]
    .corr(method="spearman")
)

print("\nSPEARMAN CORRELATION ANALYSIS")
print("-" * 50)

print(
    spearman_correlation
    .round(4)
    .to_string()
)


# ============================================================
# READING TYPE-WISE SPEARMAN CORRELATION
# ============================================================

print("\nREADING TYPE-WISE SPEARMAN CORRELATION")
print("-" * 50)

reading_types = [
    "NORMAL",
    "ASSESSMENT"
]

for reading_type in reading_types:

    reading_data = analysis_data[
        analysis_data["Reading Type"] == reading_type
    ]

    correlation = reading_data[
        [
            "Billed Unit",
            "Energy Charge"
        ]
    ].corr(
        method="spearman"
    ).iloc[0, 1]

    print(
        f"{reading_type}: "
        f"{correlation:.4f}"
    )


# ============================================================
# RURAL VS URBAN ROBUST STATISTICAL COMPARISON
# ============================================================

rural_billed_units = analysis_data[
    analysis_data["Area Type"] == "RURAL"
]["Billed Unit"]

urban_billed_units = analysis_data[
    analysis_data["Area Type"] == "URBAN"
]["Billed Unit"]

print("\nRURAL VS URBAN ROBUST STATISTICAL COMPARISON")
print("-" * 50)

print("Rural Consumer Count:", len(rural_billed_units))
print("Urban Consumer Count:", len(urban_billed_units))

print(
    "Rural Median Billed Unit:",
    rural_billed_units.median()
)

print(
    "Urban Median Billed Unit:",
    urban_billed_units.median()
)

print(
    "Rural Q1:",
    rural_billed_units.quantile(0.25)
)

print(
    "Rural Q3:",
    rural_billed_units.quantile(0.75)
)

print(
    "Urban Q1:",
    urban_billed_units.quantile(0.25)
)

print(
    "Urban Q3:",
    urban_billed_units.quantile(0.75)
)

median_difference = (
    urban_billed_units.median()
    - rural_billed_units.median()
)

print(
    "Median Difference (Urban - Rural):",
    median_difference
)




# ============================================================
# BOOTSTRAP CONFIDENCE INTERVAL FOR MEDIAN DIFFERENCE
# ============================================================

np.random.seed(42)

bootstrap_iterations = 1000
bootstrap_median_differences = []

for _ in range(bootstrap_iterations):

    rural_sample = np.random.choice(
        rural_billed_units,
        size=5000,
        replace=True
    )

    urban_sample = np.random.choice(
        urban_billed_units,
        size=5000,
        replace=True
    )

    median_difference_sample = (
        np.median(urban_sample)
        - np.median(rural_sample)
    )

    bootstrap_median_differences.append(
        median_difference_sample
    )

confidence_interval_lower = np.percentile(
    bootstrap_median_differences,
    2.5
)

confidence_interval_upper = np.percentile(
    bootstrap_median_differences,
    97.5
)

print("\nBOOTSTRAP CONFIDENCE INTERVAL")
print("-" * 50)

print(
    "Observed Median Difference:",
    median_difference
)

print(
    "95% Confidence Interval Lower:",
    confidence_interval_lower
)

print(
    "95% Confidence Interval Upper:",
    confidence_interval_upper
)



# ============================================================
# TARIFF CATEGORY ROBUST STATISTICAL COMPARISON
# ============================================================

tariff_statistics = (
    analysis_data
    .groupby(
        "Tariff Category",
        observed=True
    )["Billed Unit"]
    .agg(
        Consumer_Count="count",
        Mean="mean",
        Median="median",
        Standard_Deviation="std"
    )
)

tariff_q1 = (
    analysis_data
    .groupby(
        "Tariff Category",
        observed=True
    )["Billed Unit"]
    .quantile(0.25)
)

tariff_q3 = (
    analysis_data
    .groupby(
        "Tariff Category",
        observed=True
    )["Billed Unit"]
    .quantile(0.75)
)

tariff_statistics["Q1"] = tariff_q1
tariff_statistics["Q3"] = tariff_q3

tariff_statistics = tariff_statistics.sort_values(
    "Median",
    ascending=False
)

print("\nTARIFF CATEGORY ROBUST STATISTICAL COMPARISON")
print("-" * 50)

print(
    tariff_statistics
    .round(2)
    .to_string()
)


# ============================================================
# LV4 CONSUMPTION PATTERN INVESTIGATION
# ============================================================

lv4_data = analysis_data[
    analysis_data["Tariff Category"] == "LV4"
]

print("\nLV4 CONSUMPTION PATTERN INVESTIGATION")
print("-" * 50)

print("LV4 Total Consumers:", len(lv4_data))

print("\nTop Billed Unit Values:")
print(
    lv4_data["Billed Unit"]
    .value_counts()
    .head(10)
)

print("\nReading Type Distribution:")
print(
    lv4_data["Reading Type"]
    .value_counts(
        dropna=False
    )
)

print("\nBill Type Distribution:")
print(
    lv4_data["Bill Type"]
    .value_counts()
)

print("\nArea Type Distribution:")
print(
    lv4_data["Area Type"]
    .value_counts()
)



# ============================================================
# REPEATED BILLED UNIT CONCENTRATION ANALYSIS
# ============================================================

print("\nREPEATED BILLED UNIT CONCENTRATION ANALYSIS")
print("-" * 50)

tariff_concentration_results = []

for tariff in analysis_data["Tariff Category"].unique():

    tariff_data = analysis_data[
        analysis_data["Tariff Category"] == tariff
    ]

    billed_unit_counts = (
        tariff_data["Billed Unit"]
        .value_counts()
    )

    top_value = billed_unit_counts.index[0]
    top_value_count = billed_unit_counts.iloc[0]

    concentration_percentage = (
        top_value_count /
        len(tariff_data)
        * 100
    )

    tariff_concentration_results.append({
        "Tariff Category": tariff,
        "Total Records": len(tariff_data),
        "Most Frequent Billed Unit": top_value,
        "Frequency": top_value_count,
        "Concentration Percentage": concentration_percentage
    })

tariff_concentration_df = pd.DataFrame(
    tariff_concentration_results
)

tariff_concentration_df = (
    tariff_concentration_df
    .sort_values(
        "Concentration Percentage",
        ascending=False
    )
)

print(
    tariff_concentration_df
    .round(2)
    .to_string(index=False)
)


# ============================================================
# OVERALL BILLED UNIT VALUE CONCENTRATION
# ============================================================

billed_unit_frequency = (
    analysis_data["Billed Unit"]
    .value_counts()
    .head(15)
)

billed_unit_frequency_percentage = (
    billed_unit_frequency
    / len(analysis_data)
    * 100
)

billed_unit_concentration = pd.DataFrame({
    "Frequency": billed_unit_frequency,
    "Percentage": billed_unit_frequency_percentage
})

print("\nOVERALL BILLED UNIT VALUE CONCENTRATION")
print("-" * 50)

print(
    billed_unit_concentration
    .round(2)
    .to_string()
)


# ============================================================
# ROBUST CHARGE PER UNIT THRESHOLD ANALYSIS
# ============================================================

charge_analysis = analysis_data[
    analysis_data["Charge Per Unit"].notna()
].copy()

standard_charge_data = charge_analysis[
    charge_analysis["Billed Unit"] >= 1
]

tiny_unit_charge_data = charge_analysis[
    (charge_analysis["Billed Unit"] > 0) &
    (charge_analysis["Billed Unit"] < 1)
]

print("\nROBUST CHARGE PER UNIT THRESHOLD ANALYSIS")
print("-" * 50)

print("All Valid Charge Records:", len(charge_analysis))

print(
    "All Records Median Charge Per Unit:",
    charge_analysis["Charge Per Unit"].median()
)

print(
    "All Records Mean Charge Per Unit:",
    charge_analysis["Charge Per Unit"].mean()
)

print("\nBilled Unit >= 1 Records:", len(standard_charge_data))

print(
    "Thresholded Median Charge Per Unit:",
    standard_charge_data["Charge Per Unit"].median()
)

print(
    "Thresholded Mean Charge Per Unit:",
    standard_charge_data["Charge Per Unit"].mean()
)

print("\nTiny Unit Records:", len(tiny_unit_charge_data))

print(
    "Tiny Unit Median Charge Per Unit:",
    tiny_unit_charge_data["Charge Per Unit"].median()
)

print(
    "Tiny Unit Mean Charge Per Unit:",
    tiny_unit_charge_data["Charge Per Unit"].mean()
)



# ============================================================
# FINAL STATISTICAL FINDINGS EXPORT
# ============================================================

statistical_findings = pd.DataFrame({
    "Analysis": [
        "Billed Unit Skewness",
        "Energy Charge Skewness",
        "Load KW Equivalent Skewness",
        "Charge Per Unit Skewness",
        "Rural Median Billed Unit",
        "Urban Median Billed Unit",
        "Urban Rural Median Difference",
        "Bootstrap CI Lower",
        "Bootstrap CI Upper",
        "Spearman Billed Unit vs Energy Charge",
        "Spearman Energy Charge vs Load",
        "Tiny Unit Record Count",
        "Thresholded Charge Per Unit Mean",
        "LV4 Top Value Concentration"
    ],
    "Result": [
        analysis_data["Billed Unit"].skew(),
        analysis_data["Energy Charge"].skew(),
        analysis_data["Load KW Equivalent"].skew(),
        analysis_data["Charge Per Unit"].skew(),
        rural_billed_units.median(),
        urban_billed_units.median(),
        median_difference,
        confidence_interval_lower,
        confidence_interval_upper,
        spearman_correlation.loc[
            "Billed Unit",
            "Energy Charge"
        ],
        spearman_correlation.loc[
            "Energy Charge",
            "Load KW Equivalent"
        ],
        len(tiny_unit_charge_data),
        standard_charge_data["Charge Per Unit"].mean(),
        tariff_concentration_df.loc[
            tariff_concentration_df["Tariff Category"] == "LV4",
            "Concentration Percentage"
        ].iloc[0]
    ]
})

output_path = (
    "../08_Statistical_Analysis/"
    "statistical_findings.csv"
)

statistical_findings.to_csv(
    output_path,
    index=False
)

print("\nFINAL STATISTICAL FINDINGS")
print("-" * 50)

print(
    statistical_findings
    .round(4)
    .to_string(index=False)
)

print("\nSTATISTICAL FINDINGS EXPORTED SUCCESSFULLY")
print("Output File:", output_path)