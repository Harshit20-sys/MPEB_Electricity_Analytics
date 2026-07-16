-- =====================================================
-- MPEB Electricity Analytics Project
-- 01_Basic_SQL.sql
-- Basic SQL Interview Questions + Queries
-- =====================================================

-- QUESTION 01
-- Display all consumer records.
SELECT * FROM consumer_data;

-- QUESTION 02
-- Display ACTIVE consumers.
SELECT *
FROM consumer_data
WHERE consumer_status = 'ACTIVE';

-- QUESTION 03
-- Display INACTIVE consumers.
SELECT *
FROM consumer_data
WHERE consumer_status = 'INACTIVE';

-- QUESTION 04
-- Count total consumers.
SELECT COUNT(*) AS total_consumers
FROM consumer_data;

-- QUESTION 05
-- Show distinct tariff categories.
SELECT DISTINCT tariff_category
FROM consumer_data;

-- QUESTION 06
-- Count consumers by tariff category.
SELECT tariff_category, COUNT(*) AS total_consumers
FROM consumer_data
GROUP BY tariff_category;

-- QUESTION 07
-- Count consumers by area type.
SELECT area_type, COUNT(*) AS total_consumers
FROM consumer_data
GROUP BY area_type;

-- QUESTION 08
-- Count consumers by metering status.
SELECT metering_status, COUNT(*) AS total_consumers
FROM consumer_data
GROUP BY metering_status;

-- QUESTION 09
-- Count consumers by bill type.
SELECT bill_type, COUNT(*) AS total_consumers
FROM consumer_data
GROUP BY bill_type;

-- QUESTION 10
-- Find average billed unit.
SELECT AVG(billed_unit) AS avg_billed_unit
FROM consumer_data;
