# Azure Databricks DABs Setup Instructions

## Prerequisites
1. **Azure Databricks Workspace**: Full (non-Community) Azure Databricks workspace
2. **Azure Storage Account**: With blob storage containers for data
3. **Databricks CLI**: Installed and authenticated
4. **Unity Catalog**: Enabled in your Azure Databricks workspace

## Step-by-Step Setup

### 1. Configure Environment Variables
```bash
# Copy the environment template
cp .env.template .env

# Edit .env with your specific values
nano .env
```

**Required Updates in .env:**
- `DATABRICKS_HOST`: Your Azure Databricks workspace URL
- `DATABRICKS_TOKEN`: Your personal access token
- `NOTIFICATION_EMAIL`: Your email for pipeline notifications
- `AZURE_STORAGE_ACCOUNT`: Your Azure storage account name
- `AZURE_CONTAINER_*`: Your blob container names

### 2. Update databricks.yml Configuration
Edit `databricks.yml` and replace placeholder values:

```yaml
# Update workspace host in all targets
targets:
  dev:
    workspace:
      host: https://YOUR-WORKSPACE.azuredatabricks.net
```

### 3. Create Azure External Connections

**In Databricks UI (Data > External Connections):**

1. **Development Connection**:
   - Name: `azure_blob_customer_data`
   - Connection Type: Azure Blob Storage  
   - Storage Account: `yourstorageaccountname`
   - Container: `customer-data-dev`
   - Authentication: Managed Identity or Service Principal

2. **Staging Connection** (Optional):
   - Name: `azure_blob_customer_data_staging`
   - Container: `customer-data-staging`

3. **Production Connection**:
   - Name: `azure_blob_customer_data_prod`
   - Container: `customer-data-prod`

### 4. Create Unity Catalog Structure

**In Databricks UI (Data > Catalogs):**

```sql
-- Create development catalog
CREATE CATALOG IF NOT EXISTS insurance_demo_dev;

-- Create schema for customer data
CREATE SCHEMA IF NOT EXISTS insurance_demo_dev.customers;

-- Grant permissions (adjust as needed)
GRANT USE CATALOG ON CATALOG insurance_demo_dev TO `your-team-group`;
GRANT USE SCHEMA ON SCHEMA insurance_demo_dev.customers TO `your-team-group`;
```

Repeat for staging and production catalogs if using separate environments.

### 5. Upload Sample Data

Upload sample customer JSON files to your Azure Blob Storage:

**Sample customer.json structure:**
```json
{
  "customer_id": "CUST001",
  "first_name": "John",
  "last_name": "Doe", 
  "email": "john.doe@email.com",
  "phone": "(555) 123-4567",
  "address": "123 Main St",
  "city": "Springfield",
  "state": "IL",
  "zip_code": "62701"
}
```

**Upload to container path:** `customers/customer.json`

### 6. Deploy and Test

```bash
# Validate configuration
databricks bundle validate --target dev

# Deploy to development
databricks bundle deploy --target dev

# Run the pipeline job
databricks bundle run customer_pipeline_job --target dev

# Or run pipeline directly
databricks bundle run customer_dlt_pipeline --target dev
```

### 7. Verify Results

**Check pipeline execution:**
1. Go to Databricks UI > Workflows > Delta Live Tables
2. Find your pipeline: `customer-data-pipeline-dev`
3. Verify successful execution
4. Check tables created in Unity Catalog

**Expected tables:**
- `insurance_demo_dev.customers.customers_bronze`
- `insurance_demo_dev.customers.customers_silver`
- `insurance_demo_dev.customers.customer_summary`

## Troubleshooting

### External Connection Issues
- Verify Azure storage account permissions
- Check Databricks workspace managed identity has blob access
- Test connection in Databricks UI before deploying

### Unity Catalog Permissions
- Ensure workspace has Unity Catalog enabled
- Verify catalog creation permissions
- Check schema and table permissions

### Pipeline Deployment Errors
- Check YAML syntax with `databricks bundle validate --verbose`
- Verify all external connection names match configuration
- Review pipeline logs in Databricks UI

## Next Steps

Once the basic pipeline is working:
1. Add more customer data files to test streaming ingestion
2. Deploy to staging/production environments
3. Set up CI/CD pipeline automation
4. Add insurance claims and policy data (Phase 2)

## Security Best Practices

- Never commit `.env` file to git
- Use service principals for production deployments
- Implement proper RBAC in Unity Catalog
- Use Azure Key Vault for secrets management
- Enable audit logging for compliance