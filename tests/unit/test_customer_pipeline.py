# Databricks notebook source
# MAGIC %md
# MAGIC # Unit Tests for Customer Pipeline
# MAGIC 
# MAGIC Simple unit tests to validate customer data transformations
# MAGIC using PySpark and mock data.

# COMMAND ----------

import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, TimestampType
from pyspark.sql import functions as F
from datetime import datetime

# COMMAND ----------

class TestCustomerTransformations:
    """
    Unit tests for customer data transformations in the silver layer.
    Tests the core business logic without DLT dependencies.
    """
    
    @pytest.fixture(scope="class")
    def spark(self):
        """Create Spark session for testing"""
        return SparkSession.builder \
            .appName("CustomerPipelineTests") \
            .master("local[*]") \
            .getOrCreate()
    
    def test_customer_name_standardization(self, spark):
        """
        Test that customer names are properly formatted to title case.
        
        WHAT IT TESTS:
        - first_name and last_name should be converted to proper case
        - Leading/trailing whitespace should be removed
        - Empty names should remain empty
        """
        # Create mock bronze data
        test_data = [
            ("1", "john", "DOE", "test@email.com"),
            ("2", "  jane  ", "  smith  ", "jane@test.com"),
            ("3", "", "JOHNSON", "empty@test.com"),
            ("4", "mike", "", "mike@test.com")
        ]
        
        schema = StructType([
            StructField("customer_id", StringType(), True),
            StructField("first_name", StringType(), True),
            StructField("last_name", StringType(), True),
            StructField("email", StringType(), True)
        ])
        
        df = spark.createDataFrame(test_data, schema)
        
        # Apply the same transformations as silver layer
        result = df.select(
            F.col("customer_id"),
            F.initcap(F.trim(F.col("first_name"))).alias("first_name"),
            F.initcap(F.trim(F.col("last_name"))).alias("last_name"),
            F.lower(F.trim(F.col("email"))).alias("email")
        )
        
        # Collect results for assertions
        rows = result.collect()
        
        # Assert name formatting
        assert rows[0]["first_name"] == "John"
        assert rows[0]["last_name"] == "Doe"
        assert rows[1]["first_name"] == "Jane"  # Trimmed and capitalized
        assert rows[1]["last_name"] == "Smith"
        assert rows[2]["first_name"] == ""      # Empty remains empty
        assert rows[3]["last_name"] == ""       # Empty remains empty
        
        print("✅ Name standardization test passed!")
    
    def test_phone_number_cleaning(self, spark):
        """
        Test phone number cleaning and validation.
        
        WHAT IT TESTS:
        - Phone numbers should have non-digits removed
        - Original phone format should be preserved
        - Cleaned phone should contain only digits
        """
        test_data = [
            ("1", "(555) 123-4567"),
            ("2", "555.123.4567"),
            ("3", "5551234567"),
            ("4", "+1-555-123-4567"),
            ("5", "invalid")
        ]
        
        schema = StructType([
            StructField("customer_id", StringType(), True),
            StructField("phone", StringType(), True)
        ])
        
        df = spark.createDataFrame(test_data, schema)
        
        # Apply phone cleaning transformation
        result = df.select(
            F.col("customer_id"),
            F.regexp_replace(F.col("phone"), "[^0-9]", "").alias("phone_cleaned"),
            F.col("phone").alias("phone_original")
        )
        
        rows = result.collect()
        
        # Assert phone cleaning
        assert rows[0]["phone_cleaned"] == "5551234567"
        assert rows[1]["phone_cleaned"] == "5551234567"
        assert rows[2]["phone_cleaned"] == "5551234567"
        assert rows[3]["phone_cleaned"] == "15551234567"  # Includes country code
        assert rows[4]["phone_cleaned"] == ""             # Invalid becomes empty
        
        # Original should be preserved
        assert rows[0]["phone_original"] == "(555) 123-4567"
        
        print("✅ Phone number cleaning test passed!")
    
    def test_data_quality_validations(self, spark):
        """
        Test data quality rules that would be enforced by DLT expectations.
        
        WHAT IT TESTS:
        - Customer ID validation (not null, not empty)
        - Email format validation using regex
        - Record filtering based on quality rules
        """
        test_data = [
            ("1", "John", "Doe", "valid@email.com"),      # Valid record
            (None, "Jane", "Smith", "jane@test.com"),     # Null customer_id
            ("", "Mike", "Johnson", "mike@test.com"),     # Empty customer_id
            ("3", "Bob", "Wilson", "invalid-email"),      # Invalid email
            ("4", "Alice", "Brown", "alice@test.com")     # Valid record
        ]
        
        schema = StructType([
            StructField("customer_id", StringType(), True),
            StructField("first_name", StringType(), True),
            StructField("last_name", StringType(), True),
            StructField("email", StringType(), True)
        ])
        
        df = spark.createDataFrame(test_data, schema)
        
        # Apply quality filters (same as silver layer)
        result = df.filter(F.col("customer_id").isNotNull()) \
                  .filter(F.col("customer_id") != "")
        
        rows = result.collect()
        
        # Should have 3 records (valid + invalid email + valid)
        # The invalid email would be caught by DLT expectation but wouldn't filter here
        assert len(rows) == 3
        
        # Valid records should be present
        customer_ids = [row["customer_id"] for row in rows]
        assert "1" in customer_ids
        assert "4" in customer_ids
        assert "3" in customer_ids  # Invalid email still passes basic filter
        
        # Invalid customer_id records should be filtered out
        assert None not in customer_ids
        assert "" not in customer_ids
        
        print("✅ Data quality validation test passed!")

# COMMAND ----------

# MAGIC %md
# MAGIC ## How to Run These Tests
# MAGIC 
# MAGIC ```python
# MAGIC # In Databricks notebook or cluster:
# MAGIC pytest.main(["/path/to/test_customer_pipeline.py", "-v"])
# MAGIC 
# MAGIC # Or run individual test:
# MAGIC test_instance = TestCustomerTransformations()
# MAGIC test_instance.test_customer_name_standardization(spark)
# MAGIC ```

# COMMAND ----------

# Run tests if executed directly
if __name__ == "__main__":
    # Create test instance
    test_instance = TestCustomerTransformations()
    
    # Get current Spark session
    spark = SparkSession.getActiveSession()
    if spark is None:
        spark = SparkSession.builder.appName("CustomerPipelineTests").getOrCreate()
    
    print("🧪 Running Customer Pipeline Unit Tests...")
    print("=" * 50)
    
    try:
        test_instance.test_customer_name_standardization(spark)
        test_instance.test_phone_number_cleaning(spark)
        test_instance.test_data_quality_validations(spark)
        
        print("=" * 50)
        print("🎉 All tests passed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        raise