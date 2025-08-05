# Databricks Asset Bundle - Insurance Customer Pipeline (Azure)

## Project Overview
This project implements a production-ready Databricks Asset Bundle with Lakeflow declarative pipelines to process synthetic insurance company data on Azure. Migrated from the working AWS S3 version with enhanced job orchestration and Azure Blob Storage integration.

**Current Phase**: Complete Azure migration with enhanced DAB patterns
**Future Phases**: Add insurance claims and policy data, advanced monitoring, CI/CD automation

## Architecture Improvements Over AWS Version
- **Enhanced Job Orchestration**: Added job wrapper pattern for better pipeline management
- **Email Notifications**: Success/failure notifications for both pipelines and jobs
- **Multi-Environment Support**: Dev, staging, and production configurations
- **Azure Integration**: Native Azure Blob Storage connectivity via external connections
- **Enterprise Features**: Leverages full Azure Databricks capabilities (no Community Edition limitations)

## Project Architecture
- **Data Source**: Azure Blob Storage with synthetic insurance data (JSON format)
- **Pipeline**: Lakeflow declarative pipeline using Delta Live Tables with Auto Loader
- **Environments**: Dev, Staging, and Prod catalogs with proper isolation
- **Governance**: Unity Catalog with comprehensive data quality expectations
- **Orchestration**: Job wrapper pattern for pipeline management and monitoring

## Data Sources
- **Customer Data**: JSON format in Azure Blob Storage
- **Access Method**: Unity Catalog external connections (no direct storage account access)
- **Future Data**: Policies and Claims tables (Phase 2)
- **Schema Evolution**: Auto Loader handles schema changes automatically

## Essential Commands

### Bundle Management
```bash
# Validate bundle configuration
databricks bundle validate

# Deploy to development environment
databricks bundle deploy --target dev

# Deploy to staging environment  
databricks bundle deploy --target staging

# Deploy to production environment
databricks bundle deploy --target prod

# Run pipeline via job orchestration in dev
databricks bundle run customer_pipeline_job --target dev

# Run pipeline directly in dev
databricks bundle run customer_dlt_pipeline --target dev
```

### Development Workflow
```bash
# Check bundle status
databricks bundle summary

# View deployed resources
databricks bundle resources

# Destroy development deployment
databricks bundle destroy --target dev --auto-approve

# Validate before deployment (recommended in CI/CD)
databricks bundle validate --target prod
```

### Pipeline Management
```bash
# Refresh pipeline manually (if not using job wrapper)
databricks pipelines update <pipeline-id>

# Get pipeline status
databricks pipelines get <pipeline-id>

# List pipeline runs
databricks pipelines list-updates <pipeline-id>

# Get detailed pipeline run info  
databricks pipelines get-update <pipeline-id> <update-id>
```

## Project Structure
```
cicd_databricks_dabs_azure/
├── databricks.yml                      # Enhanced bundle configuration with multi-env
├── resources/
│   └── customer_pipeline.yml           # Pipeline + Job resources for Azure
├── src/
│   └── pipelines/
│       └── customer_azure_pipeline.py  # Azure Blob Storage pipeline code
├── tests/
│   └── unit/
│       └── test_customer_pipeline.py   # Unit tests (identical to AWS version)
├── CLAUDE.md                           # This documentation file
└── .env.template                       # Environment configuration template
```

## Configuration Setup

### 1. Azure Workspace Configuration
Update `databricks.yml` with your Azure workspace details:
```yaml
targets:
  dev:
    workspace:
      host: https://your-azure-workspace.azuredatabricks.net
```

### 2. External Connection Setup
Before deploying, create Azure Blob Storage external connections in Databricks:

**In Databricks UI > Data > External Connections:**
1. Create connection named `azure_blob_customer_data`
2. Configure with your Azure storage account and credentials
3. Test connection to ensure proper access
4. Repeat for staging/prod environments if using separate storage

### 3. Email Notifications
Update notification email in `databricks.yml`:
```yaml
variables:
  notification_email:
    description: "Email address for pipeline notifications"
    default: "your-email@company.com"
```

## Data Pipeline Architecture

### Bronze Layer (Raw Ingestion)
- **Source**: Azure Blob Storage JSON files via external connection
- **Method**: Auto Loader with cloudFiles format
- **Schema**: Explicit customer schema definition
- **Features**: Metadata capture, ingestion timestamping

### Silver Layer (Cleaned Data)
- **Transformations**: Name standardization, email normalization, phone cleaning
- **Quality Gates**: Data quality expectations with fail-fast behavior
- **Validation**: Customer ID, email format, zip code, phone number checks
- **Performance**: Optimized with Photon and auto-optimization

### Gold Layer (Analytics Ready)
- **Purpose**: Customer summary metrics by geography
- **Ready for**: Insurance claims and policy data integration
- **Aggregations**: Customer counts, geographic distribution, processing metrics

## Data Quality Expectations

### Critical (Fail-Fast)
- `valid_customer_id`: Customer ID must not be null or empty
- `valid_email_format`: Email must match standard regex pattern

### Warning (Log Only)
- `valid_zip_code`: Zip code should be 5 digits when present
- `valid_phone_format`: Phone should have at least 10 digits when cleaned

## Enhanced Features vs AWS Version

### Job Orchestration
```yaml
# New job wrapper pattern for better management
jobs:
  customer_pipeline_job:
    tasks:
      - pipeline_task:
          pipeline_id: ${resources.pipelines.customer_dlt_pipeline.id}
    email_notifications:
      on_success: ["${var.notification_email}"]
      on_failure: ["${var.notification_email}"]
```

### Multi-Environment Support
- **Development**: Full featured dev environment
- **Staging**: Pre-production validation environment  
- **Production**: Production deployment with separate resources

### Azure Integration Benefits
- **No Community Edition Limitations**: Full Unity Catalog and pipeline features
- **Enterprise Monitoring**: Advanced observability and alerting
- **Serverless Compute**: Cost-effective auto-scaling compute
- **Native Azure Integration**: Seamless Blob Storage connectivity

## Environment Variables Template

Create `.env` file (not in git) with your specific values:
```bash
# Azure Databricks Configuration
DATABRICKS_HOST=https://your-azure-workspace.azuredatabricks.net
DATABRICKS_TOKEN=your-personal-access-token

# Azure Storage Configuration  
AZURE_EXTERNAL_LOCATION_DEV=azure_blob_customer_data
AZURE_EXTERNAL_LOCATION_STAGING=azure_blob_customer_data_staging
AZURE_EXTERNAL_LOCATION_PROD=azure_blob_customer_data_prod

# Notification Configuration
NOTIFICATION_EMAIL=your-email@company.com

# Catalog Configuration
DEV_CATALOG=insurance_demo_dev
STAGING_CATALOG=insurance_demo_staging
PROD_CATALOG=insurance_demo_prod
```

## Troubleshooting

### Common Issues
1. **Bundle Validation Fails**
   - Check YAML syntax in databricks.yml and resources/*.yml
   - Verify all referenced files exist
   - Run: `databricks bundle validate --verbose`

2. **Azure External Connection Issues**
   - Verify external connection is configured in Databricks UI
   - Check Azure storage account permissions and network access
   - Test connection: Navigate to Data > External Connections in UI

3. **Pipeline Deployment Fails**  
   - Check Unity Catalog permissions for target catalog/schema
   - Verify serverless compute is enabled in workspace
   - Review pipeline logs in Databricks UI

4. **Data Ingestion Issues**
   - Verify Azure Blob Storage path and file formats
   - Check external connection has proper read permissions
   - Review Auto Loader schema inference settings

### Debug Commands
```bash
# Verbose validation with detailed error messages
databricks bundle validate --verbose --target dev

# Detailed deployment information
databricks bundle deploy --target dev --verbose

# Check pipeline events and errors
databricks pipelines list-updates <pipeline-id> --max-results 10
```

## Testing

### Unit Tests
Run the comprehensive unit test suite:
```bash
# In Databricks workspace or cluster
python tests/unit/test_customer_pipeline.py

# Tests cover:
# - Name standardization logic
# - Phone number cleaning
# - Data quality validations
# - Filtering logic
```

### Integration Testing
```bash
# Deploy to dev and run full pipeline
databricks bundle deploy --target dev
databricks bundle run customer_pipeline_job --target dev

# Verify data quality in Unity Catalog
# Check customers_bronze, customers_silver, customer_summary tables
```

## Next Steps (Future Phases)

### Phase 2: Insurance Data Expansion
1. Add policies table pipeline with customer joins
2. Add claims table pipeline with policy relationships  
3. Implement comprehensive gold layer analytics
4. Add advanced data quality monitoring

### Phase 3: Production Automation
1. Set up Azure DevOps or GitHub Actions CI/CD
2. Implement automated testing in staging
3. Add production deployment approvals
4. Configure advanced monitoring and alerting

### Phase 4: Advanced Analytics
1. Add machine learning pipelines for fraud detection
2. Implement customer risk scoring
3. Create real-time dashboards and reporting
4. Add predictive analytics for claims

## Migration Notes from AWS Version

### What Changed
- **Data Source**: S3 bucket → Azure Blob Storage external connection
- **Path References**: S3 URIs → Unity Catalog external location references
- **Job Orchestration**: Added job wrapper pattern for better management
- **Multi-Environment**: Enhanced dev/staging/prod configuration
- **Notifications**: Added comprehensive email notification system

### What Stayed Identical
- **Pipeline Logic**: All transformation code remains identical
- **Data Quality Expectations**: Same quality rules and validation logic
- **Unit Tests**: No changes needed - tests validate transformation logic
- **Schema Definitions**: Identical customer data schema
- **Unity Catalog Patterns**: Same governance and naming conventions

## Unity Catalog Best Practices

**CRITICAL: This project follows Unity Catalog best practices:**
- **NEVER use DBFS paths** (dbfs:/) - uses Unity Catalog external locations
- **ALWAYS use external connections** for data sources, not direct storage access
- **Use managed storage within catalogs** for checkpoint and intermediate data
- **External locations must be pre-configured** in Unity Catalog before deployment
- **Follow catalog.schema.table format** for all data references
- **Use proper RBAC** with groups and service principals, not individual users

### Correct Unity Catalog Patterns Used
```python
# CORRECT - Unity Catalog external location
azure_external_location = spark.conf.get("azure_external_location")
source_path = f"{azure_external_location}/customers/"

# CORRECT - Managed Unity Catalog tables
target: "${var.catalog}.${var.schema}"

# WRONG - Legacy patterns (NOT used in this project)
# .load("dbfs:/FileStore/data/")  # Don't use DBFS
# .load("abfss://container@account.blob.core.windows.net/path")  # Don't use direct storage URIs
```

## Useful Links
- [Databricks Asset Bundles Documentation](https://docs.databricks.com/en/dev-tools/bundles/)
- [Lakeflow Declarative Pipelines](https://docs.databricks.com/en/dlt/)
- [Azure Databricks External Connections](https://docs.microsoft.com/en-us/azure/databricks/external-data/)
- [Unity Catalog Best Practices](https://docs.databricks.com/en/data-governance/unity-catalog/best-practices.html)
- [Delta Live Tables](https://docs.databricks.com/en/delta-live-tables/)

## Project Memories and Best Practices
- **Always use Unity Catalog** when working with Databricks, never DBFS
- **Use job wrapper pattern** for better pipeline management and monitoring
- **Configure email notifications** for both success and failure scenarios
- **Test external connections** before deploying pipelines
- **Use serverless compute** for cost optimization and performance
- **Follow multi-environment patterns** for proper dev/staging/prod separation