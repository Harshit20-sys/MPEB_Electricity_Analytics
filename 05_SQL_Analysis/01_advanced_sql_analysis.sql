-- ============================================================
-- 1. CONSUMER PORTFOLIO SUMMARY
-- ============================================================

SELECT
    COUNT(*) AS total_consumers,
    COUNT(*) FILTER (
        WHERE consumer_status = 'ACTIVE'
    ) AS active_consumers,
    COUNT(*) FILTER (
        WHERE consumer_status = 'INACTIVE'
    ) AS inactive_consumers,
    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE consumer_status = 'ACTIVE'
        ) / COUNT(*),
        2
    ) AS active_percentage
FROM electricity_consumers;



-- ============================================================
-- 2. AREA-WISE CONSUMER DISTRIBUTION
-- ============================================================

SELECT
    area_type,
    COUNT(*) AS total_consumers,
    ROUND(
        COUNT(*) * 100.0 /
        SUM(COUNT(*)) OVER (),
        2
    ) AS consumer_percentage
FROM electricity_consumers
GROUP BY area_type
ORDER BY total_consumers DESC;



-- ============================================================
-- 3. METERING GAP ANALYSIS
-- ============================================================

SELECT
    area_type,
    COUNT(*) AS total_consumers,
    COUNT(*) FILTER (
        WHERE metering_status = 'UNMETERED'
    ) AS unmetered_consumers,
    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE metering_status = 'UNMETERED'
        ) / COUNT(*),
        2
    ) AS unmetered_percentage
FROM electricity_consumers
GROUP BY area_type
ORDER BY unmetered_percentage DESC;



-- ============================================================
-- 4. TARIFF-WISE METERING ANALYSIS
-- ============================================================

SELECT
    tariff_category,
    COUNT(*) AS total_consumers,
    COUNT(*) FILTER (
        WHERE metering_status = 'METERED'
    ) AS metered_consumers,
    COUNT(*) FILTER (
        WHERE metering_status = 'UNMETERED'
    ) AS unmetered_consumers,
    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE metering_status = 'UNMETERED'
        ) / COUNT(*),
        2
    ) AS unmetered_percentage
FROM electricity_consumers
GROUP BY tariff_category
ORDER BY unmetered_percentage DESC;



-- ============================================================
-- 5. AREA + TARIFF COMBINED METERING ANALYSIS
-- ============================================================

SELECT
    area_type,
    tariff_category,
    COUNT(*) AS total_consumers,
    COUNT(*) FILTER (
        WHERE metering_status = 'UNMETERED'
    ) AS unmetered_consumers,
    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE metering_status = 'UNMETERED'
        ) / COUNT(*),
        2
    ) AS unmetered_percentage
FROM electricity_consumers
GROUP BY
    area_type,
    tariff_category
ORDER BY
    area_type,
    unmetered_percentage DESC;




-- ============================================================
-- 6. LOCATION-WISE UNMETERED RISK RANKING
-- ============================================================

WITH location_metering AS (
    SELECT
        location_code,
        COUNT(*) AS total_consumers,
        COUNT(*) FILTER (
            WHERE metering_status = 'UNMETERED'
        ) AS unmetered_consumers
    FROM electricity_consumers
    GROUP BY location_code
),

location_risk AS (
    SELECT
        location_code,
        total_consumers,
        unmetered_consumers,
        ROUND(
            100.0 * unmetered_consumers / total_consumers,
            2
        ) AS unmetered_percentage
    FROM location_metering
)

SELECT
    location_code,
    total_consumers,
    unmetered_consumers,
    unmetered_percentage,
    DENSE_RANK() OVER (
        ORDER BY unmetered_percentage DESC
    ) AS risk_rank
FROM location_risk
WHERE total_consumers >= 100
ORDER BY
    risk_rank,
    total_consumers DESC
LIMIT 20;



-- ============================================================
-- 7. LOCATION-WISE CONSUMPTION RANKING
-- ============================================================

WITH location_consumption AS (
    SELECT
        location_code,
        COUNT(*) AS total_consumers,
        SUM(billed_unit) AS total_billed_units,
        AVG(billed_unit) AS average_billed_unit
    FROM electricity_consumers
    WHERE bill_type <> 'PDC'
    GROUP BY location_code
)

SELECT
    location_code,
    total_consumers,
    ROUND(total_billed_units, 2) AS total_billed_units,
    ROUND(average_billed_unit, 2) AS average_billed_unit,
    DENSE_RANK() OVER (
        ORDER BY total_billed_units DESC
    ) AS consumption_rank
FROM location_consumption
WHERE total_consumers >= 100
ORDER BY consumption_rank
LIMIT 20;





-- ============================================================
-- 8. LOCATION-WISE ZERO UNIT EXCEPTION RANKING
-- ============================================================

WITH location_exceptions AS (
    SELECT
        location_code,
        COUNT(*) FILTER (
            WHERE bill_type <> 'PDC'
        ) AS non_pdc_consumers,
        COUNT(*) FILTER (
            WHERE zero_unit_exception_flag = 1
        ) AS zero_unit_exceptions
    FROM electricity_consumers
    GROUP BY location_code
)

SELECT
    location_code,
    non_pdc_consumers,
    zero_unit_exceptions,
    ROUND(
        100.0 * zero_unit_exceptions /
        NULLIF(non_pdc_consumers, 0),
        2
    ) AS exception_percentage,
    DENSE_RANK() OVER (
        ORDER BY
            100.0 * zero_unit_exceptions /
            NULLIF(non_pdc_consumers, 0) DESC
    ) AS exception_rank
FROM location_exceptions
WHERE non_pdc_consumers >= 100
ORDER BY
    exception_rank,
    non_pdc_consumers DESC
LIMIT 20;



-- ============================================================
-- 9. TARIFF-WISE CONSUMPTION & CHARGE RANKING
-- ============================================================

WITH tariff_performance AS (
    SELECT
        tariff_category,
        COUNT(*) FILTER (
            WHERE bill_type <> 'PDC'
        ) AS non_pdc_consumers,
        SUM(billed_unit) FILTER (
            WHERE bill_type <> 'PDC'
        ) AS total_billed_units,
        SUM(energy_charge) FILTER (
            WHERE bill_type <> 'PDC'
        ) AS total_energy_charge,
        AVG(billed_unit) FILTER (
            WHERE bill_type <> 'PDC'
        ) AS average_billed_unit
    FROM electricity_consumers
    GROUP BY tariff_category
)

SELECT
    tariff_category,
    non_pdc_consumers,
    ROUND(total_billed_units, 2) AS total_billed_units,
    ROUND(total_energy_charge, 2) AS total_energy_charge,
    ROUND(average_billed_unit, 2) AS average_billed_unit,

    DENSE_RANK() OVER (
        ORDER BY total_billed_units DESC
    ) AS consumption_rank,

    DENSE_RANK() OVER (
        ORDER BY total_energy_charge DESC
    ) AS charge_rank

FROM tariff_performance
ORDER BY consumption_rank;



-- ============================================================
-- 10. LOCATION RISK QUARTILE SEGMENTATION
-- ============================================================

WITH location_metrics AS (
    SELECT
        location_code,
        COUNT(*) FILTER (
            WHERE bill_type <> 'PDC'
        ) AS non_pdc_consumers,
        COUNT(*) FILTER (
            WHERE zero_unit_exception_flag = 1
        ) AS zero_unit_exceptions
    FROM electricity_consumers
    GROUP BY location_code
),

exception_rates AS (
    SELECT
        location_code,
        non_pdc_consumers,
        zero_unit_exceptions,
        ROUND(
            100.0 * zero_unit_exceptions /
            NULLIF(non_pdc_consumers, 0),
            2
        ) AS exception_percentage
    FROM location_metrics
    WHERE non_pdc_consumers >= 100
),

risk_quartiles AS (
    SELECT
        *,
        NTILE(4) OVER (
            ORDER BY exception_percentage DESC
        ) AS risk_quartile
    FROM exception_rates
)

SELECT
    location_code,
    non_pdc_consumers,
    zero_unit_exceptions,
    exception_percentage,
    risk_quartile,
    CASE
        WHEN risk_quartile = 1 THEN 'HIGH RISK'
        WHEN risk_quartile = 2 THEN 'MEDIUM-HIGH RISK'
        WHEN risk_quartile = 3 THEN 'MEDIUM-LOW RISK'
        ELSE 'LOW RISK'
    END AS risk_category
FROM risk_quartiles
ORDER BY
    risk_quartile,
    exception_percentage DESC;




-- ============================================================
-- 11. TARIFF CONSUMPTION COMPARISON USING LAG
-- ============================================================

WITH tariff_consumption AS (
    SELECT
        tariff_category,
        COUNT(*) FILTER (
            WHERE bill_type <> 'PDC'
        ) AS non_pdc_consumers,
        AVG(billed_unit) FILTER (
            WHERE bill_type <> 'PDC'
        ) AS average_billed_unit
    FROM electricity_consumers
    GROUP BY tariff_category
),

tariff_comparison AS (
    SELECT
        tariff_category,
        non_pdc_consumers,
        average_billed_unit,

        LAG(average_billed_unit) OVER (
            ORDER BY average_billed_unit DESC
        ) AS previous_average_billed_unit

    FROM tariff_consumption
)

SELECT
    tariff_category,
    non_pdc_consumers,
    ROUND(average_billed_unit, 2) AS average_billed_unit,
    ROUND(previous_average_billed_unit, 2)
        AS previous_average_billed_unit,

    ROUND(
        average_billed_unit - previous_average_billed_unit,
        2
    ) AS difference_from_previous

FROM tariff_comparison
ORDER BY average_billed_unit DESC;


-- ============================================================
-- 12. BILLING EXCEPTION ANALYSIS
-- ============================================================

SELECT
    billing_exception_category,
    COUNT(*) AS total_records,
    ROUND(
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (),
        2
    ) AS record_percentage,
    ROUND(AVG(billed_unit), 2) AS average_billed_unit,
    ROUND(AVG(energy_charge), 2) AS average_energy_charge
FROM electricity_consumers
GROUP BY billing_exception_category
ORDER BY total_records DESC;



-- ============================================================
-- 13. HIGH CHARGE PER UNIT ANALYSIS
-- ============================================================

SELECT
    tariff_category,
    COUNT(*) AS total_consumers,
    COUNT(*) FILTER (
        WHERE high_charge_per_unit_flag = 1
    ) AS high_charge_records,
    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE high_charge_per_unit_flag = 1
        ) / COUNT(*),
        2
    ) AS high_charge_percentage,
    ROUND(
        AVG(charge_per_unit) FILTER (
            WHERE high_charge_per_unit_flag = 1
        ),
        2
    ) AS avg_high_charge_per_unit
FROM electricity_consumers
WHERE bill_type <> 'PDC'
GROUP BY tariff_category
ORDER BY high_charge_percentage DESC;


-- ============================================================
-- 14. FINAL CONSUMER ANALYTICAL VIEW
-- ============================================================

CREATE OR REPLACE VIEW vw_consumer_analytics AS

SELECT
    consumer_no,
    location_code,
    consumer_status,
    tariff_category,
    tariff_code,
    metering_status,
    beneficiary,
    connection_type,
    connection_phase,
    bill_type,
    area_type,
    load_kw_equivalent,
    consumption_segment,
    load_segment,
    billing_exception_category,
    zero_unit_exception_flag,
    reading_missing_flag,
    legacy_date_flag,
    future_connection_date_flag,
    high_charge_per_unit_flag,
    billed_unit,
    energy_charge,
    charge_per_unit
FROM electricity_consumers;