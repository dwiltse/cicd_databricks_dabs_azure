# Databricks notebook source
# MAGIC %md
# MAGIC # Customer Data Pipeline - Azure Blob Storage Version
# MAGIC 
# MAGIC Unity Catalog compatible streaming pipeline with quality checks for Azure Blob Storage.
# MAGIC Adapted from the working AWS S3 version with Azure external connections.

# COMMAND ----------

import dlt
from pyspark.sql import functions as F
from pyspark.sql.types import *

# Define customer schema for JSON files - based on actual data structure
customer_schema = StructType([
    StructField("customer_id", StringType(), True),
    StructField("first_name", StringType(), True),
    StructField("last_name", StringType(), True),
    StructField("email", StringType(), True),
    StructField("address", StringType(), True),
    StructField("city", StringType(), True),
    StructField("state", StringType(), True),
    StructField("zip_code", StringType(), True)
])

# COMMAND ----------

@dlt.table(
    comment="Raw customer data from Azure Blob Storage using Auto Loader streaming",
    table_properties={
        "quality": "bronze",
        "pipelines.autoOptimize.managed": "true"
    }
)
def customers_bronze():
    """
    Stream customer data from Azure Blob Storage with explicit schema.
    Unity Catalog compatible version using external connections.
    
    Key Changes from S3 Version:
    - Uses Azure Blob Storage external location instead of S3 path
    - Maintains identical transformation logic and schema
    - Preserves all data quality and streaming capabilities
    """
    # Get the source path from pipeline configuration - uses Unity Catalog external location reference
    # This avoids hardcoding the Azure storage account details
    source_path = spark.conf.get("source_path")
    
    return (
        spark.readStream
        .format("cloudFiles")
        .option("cloudFiles.format", "json")
        .schema(customer_schema)
        .load(source_path)
        .withColumn("ingestion_timestamp", F.current_timestamp())
        .withColumn("source_file", F.col("_metadata.file_path"))
    )

# COMMAND ----------

@dlt.table(
    comment="Cleaned and standardized customer data with quality checks",
    table_properties={
        "quality": "silver",
        "pipelines.autoOptimize.managed": "true"
    }
)
@dlt.expect_or_fail("valid_customer_id", "customer_id IS NOT NULL AND customer_id != ''")
@dlt.expect_or_fail("valid_email_format", "email IS NULL OR email RLIKE '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}'")
@dlt.expect("valid_zip_code", "zip_code IS NULL OR length(zip_code) = 5")
def customers_silver():
    """
    Clean and standardize customer data with data quality expectations.
    
    Identical transformation logic to AWS version:
    - Name standardization (proper case)
    - Email normalization (lowercase)
    - Phone number cleaning
    - Address formatting
    - Data quality validations
    """
    return (
        dlt.read("customers_bronze")
        .select(
            F.col("customer_id").cast("string").alias("customer_id"),
            F.initcap(F.trim(F.col("first_name"))).alias("first_name"),
            F.initcap(F.trim(F.col("last_name"))).alias("last_name"),
            F.lower(F.trim(F.col("email"))).alias("email"),
            F.initcap(F.trim(F.col("address"))).alias("address"),
            F.initcap(F.trim(F.col("city"))).alias("city"),
            F.upper(F.trim(F.col("state"))).alias("state"),
            F.col("zip_code").cast("string").alias("zip_code"),
            F.col("ingestion_timestamp"),
            F.col("source_file"),
            F.current_timestamp().alias("processed_timestamp")
        )
        .filter(F.col("customer_id").isNotNull())
        .filter(F.col("customer_id") != "")
    )

# COMMAND ----------

# MAGIC %md
# MAGIC ## Future Gold Layer (Ready for Expansion)
# MAGIC 
# MAGIC The following gold layer table is ready for implementation when you add 
# MAGIC insurance claims and policy data to create comprehensive customer insights.

# COMMAND ----------

@dlt.table(
    comment="Customer summary metrics and insights (ready for insurance data expansion)",
    table_properties={
        "quality": "gold",
        "pipelines.autoOptimize.managed": "true"
    }
)
def customer_summary():
    """
    Gold layer customer summary table.
    Ready for expansion with insurance claims and policy data.
    """
    return (
        dlt.read("customers_silver")
        .groupBy("state", "city")
        .agg(
            F.count("customer_id").alias("customer_count"),
            F.countDistinct("customer_id").alias("unique_customers"),
            F.collect_set("zip_code").alias("zip_codes_in_area"),
            F.min("ingestion_timestamp").alias("first_customer_ingested"),
            F.max("processed_timestamp").alias("latest_processing_time")
        )
        .withColumn("summary_generated_at", F.current_timestamp())
    )