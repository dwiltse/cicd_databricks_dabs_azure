-- Databricks notebook source
-- MAGIC %python
-- MAGIC my_catalog = dbutils.widgets.get('catalog_name')
-- MAGIC target = dbutils.widgets.get('display_target')
-- MAGIC
-- MAGIC set_default_catalog = spark.sql(f'USE CATALOG {my_catalog}')
-- MAGIC
-- MAGIC print(f'Using the {my_catalog} catalog.')
-- MAGIC print(f'Deploying as the {target} pipeline.')

-- COMMAND ----------

DROP TABLE IF EXISTS nyctaxi_bronze;

CREATE TABLE nyctaxi_bronze AS
SELECT 
  *,
  _metadata.file_modification_time as file_modification_time,
  _metadata.file_name as file_name
FROM nyctaxi_raw

-- COMMAND ----------

SELECT * 
FROM nyctaxi_bronze 
LIMIT 10;

-- COMMAND ----------

DROP TABLE IF EXISTS nyctaxi_silver;

CREATE TABLE nyctaxi_silver AS
SELECT 
  * EXCEPT (file_modification_time, file_name),
  round(try_divide(fare_amount,trip_distance),2) AS price_per_mile
FROM nyctaxi_bronze;

-- COMMAND ----------

SELECT * 
FROM nyctaxi_silver;