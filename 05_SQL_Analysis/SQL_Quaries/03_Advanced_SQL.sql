-- =====================================================
-- MPEB Electricity Analytics Project
-- 03_Advanced_SQL.sql
-- =====================================================

-- QUESTION 01 : ROW_NUMBER
SELECT consumer_no,
       energy_charge,
       ROW_NUMBER() OVER(ORDER BY energy_charge DESC) AS rn
FROM consumer_data;

-- QUESTION 02 : RANK
SELECT consumer_no,
       billed_unit,
       RANK() OVER(ORDER BY billed_unit DESC) AS rnk
FROM consumer_data;

-- QUESTION 03 : DENSE_RANK
SELECT consumer_no,
       billed_unit,
       DENSE_RANK() OVER(ORDER BY billed_unit DESC) AS dense_rank
FROM consumer_data;

-- QUESTION 04 : Running Total
SELECT consumer_no,
       energy_charge,
       SUM(energy_charge) OVER(ORDER BY consumer_no) AS running_total
FROM consumer_data;

-- QUESTION 05 : Average by Tariff
SELECT consumer_no,
       tariff_category,
       energy_charge,
       AVG(energy_charge) OVER(PARTITION BY tariff_category) AS tariff_avg
FROM consumer_data;

-- QUESTION 06 : LAG
SELECT consumer_no,
       billed_unit,
       LAG(billed_unit) OVER(ORDER BY consumer_no) AS previous_billed_unit
FROM consumer_data;

-- QUESTION 07 : LEAD
SELECT consumer_no,
       billed_unit,
       LEAD(billed_unit) OVER(ORDER BY consumer_no) AS next_billed_unit
FROM consumer_data;

-- QUESTION 08 : CTE
WITH area_summary AS (
    SELECT area_type,
           COUNT(*) AS total_consumers
    FROM consumer_data
    GROUP BY area_type
)
SELECT *
FROM area_summary;

-- QUESTION 09 : Top 5 Consumers by Tariff
WITH ranked AS (
SELECT consumer_no,
       tariff_category,
       energy_charge,
       ROW_NUMBER() OVER(PARTITION BY tariff_category ORDER BY energy_charge DESC) rn
FROM consumer_data)
SELECT *
FROM ranked
WHERE rn<=5;

-- QUESTION 10 : Percentage Contribution
SELECT tariff_category,
       SUM(energy_charge) AS total_energy_charge,
       ROUND(100.0 * SUM(energy_charge) /
       SUM(SUM(energy_charge)) OVER(),2) AS contribution_percent
FROM consumer_data
GROUP BY tariff_category;
