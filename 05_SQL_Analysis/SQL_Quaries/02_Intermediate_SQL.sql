-- =====================================================
-- MPEB Electricity Analytics Project
-- 02_Intermediate_SQL.sql
-- =====================================================

-- QUESTION 01
SELECT tariff_category, COUNT(*) AS total_consumers
FROM consumer_data
GROUP BY tariff_category
HAVING COUNT(*) > 1000;

-- QUESTION 02
SELECT area_type, AVG(billed_unit) AS avg_billed_unit
FROM consumer_data
GROUP BY area_type;

-- QUESTION 03
SELECT bill_type, AVG(energy_charge) AS avg_energy_charge
FROM consumer_data
GROUP BY bill_type;

-- QUESTION 04
SELECT tariff_category, SUM(energy_charge) AS total_energy_charge
FROM consumer_data
GROUP BY tariff_category
ORDER BY total_energy_charge DESC;

-- QUESTION 05
SELECT location_code, SUM(billed_unit) AS total_units
FROM consumer_data
GROUP BY location_code
ORDER BY total_units DESC
LIMIT 10;

-- QUESTION 06
SELECT area_type, metering_status, COUNT(*)
FROM consumer_data
GROUP BY area_type, metering_status;

-- QUESTION 07
SELECT reading_type, COUNT(*)
FROM consumer_data
GROUP BY reading_type;

-- QUESTION 08
SELECT tariff_category, AVG(charge_per_unit)
FROM consumer_data
GROUP BY tariff_category;

-- QUESTION 09
SELECT *
FROM consumer_data
WHERE billed_unit > 500;

-- QUESTION 10
SELECT *
FROM consumer_data
WHERE energy_charge > 5000;
