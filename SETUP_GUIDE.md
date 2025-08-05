# Azure Databricks Asset Bundle Setup Guide

**Complete checklist for setting up Azure Databricks DAB with Unity Catalog from scratch**

## Prerequisites

### Required Tools
- [ ] **Azure CLI** - [Install Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
- [ ] **Databricks CLI** - [Install Databricks CLI](https://docs.databricks.com/en/dev-tools/cli/index.html)
- [ ] **Git** - For version control
- [ ] **Python 3.8+** - For pipeline development
- [ ] **Code Editor** - VS Code, PyCharm, or similar

### Required Permissions
- [ ] **Azure Subscription** - Contributor or Owner access
- [ ] **Azure Resource Group** - Create/manage resources
- [ ] **Azure Storage Account** - Create/manage storage
- [ ] **Azure Databricks Workspace** - Admin access

---

## Phase 1: Azure Infrastructure Setup

### Step 1: Azure Resource Group
```bash
# Login to Azure
az login

# Create resource group (replace with your values)
az group create \
  --name "rg-databricks-demo" \
  --location "East US"
```

- [ ] Resource group created successfully
- [ ] Note resource group name: `________________`
- [ ] Note Azure region: `________________`

### Step 2: Azure Storage Account
```bash
# Create storage account (name must be globally unique)
az storage account create \
  --name "sadatabricksdemo2024" \
  --resource-group "rg-databricks-demo" \
  --location "East US" \
  --sku "Standard_LRS" \
  --kind "StorageV2" \
  --hierarchical-namespace true
```

- [ ] Storage account created successfully
- [ ] Note storage account name: `________________`
- [ ] Enable hierarchical namespace (Data Lake Gen2)

### Step 3: Create Storage Container
```bash
# Create container for raw data
az storage container create \
  --name "raw" \
  --account-name "sadatabricksdemo2024" \
  --auth-mode login
```

- [ ] Container "raw" created successfully
- [ ] Verify container exists in Azure Portal

### Step 4: Create Sample Data Structure
```bash
# Create folder structure in storage account (via Azure Portal or Storage Explorer)
# Create: raw/demodata/insurance/dev/customers/
# Create: raw/demodata/insurance/staging/customers/
# Create: raw/demodata/insurance/prod/customers/
```

- [ ] Folder structure created: `raw/demodata/insurance/dev/customers/`
- [ ] Folder structure created: `raw/demodata/insurance/staging/customers/`
- [ ] Folder structure created: `raw/demodata/insurance/prod/customers/`

### Step 5: Upload Sample Customer Data
Create sample JSON file `customers.json`:
```json
{"customer_id": "CUST001", "first_name": "John", "last_name": "Smith", "email": "john.smith@email.com", "address": "123 Main St", "city": "Chicago", "state": "IL", "zip_code": "60601"}
{"customer_id": "CUST002", "first_name": "Jane", "last_name": "Doe", "email": "jane.doe@email.com", "address": "456 Oak Ave", "city": "New York", "state": "NY", "zip_code": "10001"}
{"customer_id": "CUST003", "first_name": "Bob", "last_name": "Johnson", "email": "bob.johnson@email.com", "address": "789 Pine St", "city": "Los Angeles", "state": "CA", "zip_code": "90210"}
```

- [ ] Sample `customers.json` file created
- [ ] File uploaded to: `raw/demodata/insurance/dev/customers/customers.json`
- [ ] File uploaded to: `raw/demodata/insurance/staging/customers/customers.json`
- [ ] File uploaded to: `raw/demodata/insurance/prod/customers/customers.json`

### Step 6: Azure Databricks Workspace
```bash
# Create Databricks workspace
az databricks workspace create \
  --resource-group "rg-databricks-demo" \
  --name "databricks-demo-workspace" \
  --location "East US" \
  --sku "premium"
```

- [ ] Databricks workspace created successfully
- [ ] Note workspace URL: `https://adb-________________.16.azuredatabricks.net`
- [ ] Can access workspace in browser
- [ ] Premium tier confirmed (required for Unity Catalog)

---

## Phase 2: Unity Catalog Configuration

### Step 7: Enable Unity Catalog
1. **Access Databricks Workspace** → Log into your workspace
2. **Admin Settings** → Click account name (top right) → Admin Settings
3. **Unity Catalog** → Enable Unity Catalog if not already enabled

- [ ] Unity Catalog enabled on workspace
- [ ] Confirm access to Catalog Explorer

### Step 8: Create Unity Catalog Metastore
1. **Catalog Explorer** → Click "Create Metastore" (if first time)
2. **Metastore Name**: `insurance-demo-metastore`
3. **Region**: Same as your workspace
4. **Storage Account**: Select your storage account
5. **Container**: Create new container `unity-catalog`

- [ ] Metastore created successfully
- [ ] Metastore assigned to workspace
- [ ] Note metastore ID: `________________`

### Step 9: Create Catalogs
```sql
-- In Databricks SQL Editor or Notebook
CREATE CATALOG IF NOT EXISTS insurance_demo_dev;
CREATE CATALOG IF NOT EXISTS insurance_demo_staging;  
CREATE CATALOG IF NOT EXISTS insurance_demo_prod;
```

- [ ] `insurance_demo_dev` catalog created
- [ ] `insurance_demo_staging` catalog created
- [ ] `insurance_demo_prod` catalog created
- [ ] All catalogs visible in Catalog Explorer

### Step 10: Create External Location
1. **Catalog Explorer** → **External Locations** → **Create Location**
2. **Location Name**: `demodata`
3. **URL**: `abfss://raw@<your-storage-account>.dfs.core.windows.net/demodata`
4. **Credential**: Create new credential with managed identity or service principal
5. **Test Connection** → Verify access

**Alternative: Using Service Principal**
```bash
# Create service principal
az ad sp create-for-rbac --name "databricks-unity-catalog-sp"

# Note the output:
# appId: <application-id>
# password: <password>  
# tenant: <tenant-id>
```

- [ ] External location `demodata` created successfully
- [ ] Connection test passed
- [ ] Note external location URL: `________________`

### Step 11: Grant Permissions on External Location
```sql
-- Grant permissions to users/groups
GRANT CREATE EXTERNAL TABLE ON EXTERNAL LOCATION `demodata` TO <user-or-group>;
GRANT READ FILES ON EXTERNAL LOCATION `demodata` TO <user-or-group>;
```

- [ ] Permissions granted to required users
- [ ] Test data access from notebook

---

## Phase 3: Development Environment Setup

### Step 12: Clone Repository
```bash
# Clone the working repository
git clone https://github.com/dwiltse/cicd_databricks_dabs_azure.git
cd cicd_databricks_dabs_azure
```

- [ ] Repository cloned successfully
- [ ] In project directory

### Step 13: Configure Environment Variables
```bash
# Copy environment template
cp .env.template .env

# Edit .env file with your values
```

**Update `.env` file:**
```bash
# Azure Databricks Configuration
DATABRICKS_HOST=https://adb-<your-workspace-id>.16.azuredatabricks.net
DATABRICKS_TOKEN=<your-personal-access-token>

# Notification Configuration  
NOTIFICATION_EMAIL=your-email@company.com

# Catalog Configuration
DEV_CATALOG=insurance_demo_dev
STAGING_CATALOG=insurance_demo_staging
PROD_CATALOG=insurance_demo_prod
```

- [ ] `.env` file created and configured
- [ ] All placeholders replaced with actual values
- [ ] File added to `.gitignore` (should already be there)

### Step 14: Create Databricks Personal Access Token
1. **Databricks Workspace** → User Settings (click your email)
2. **Developer** → **Access Tokens**
3. **Generate New Token**
   - **Comment**: `DAB Development Token`
   - **Lifetime**: 90 days (or per company security policy)
4. **Copy token** → Add to `.env` file

- [ ] Personal access token generated
- [ ] Token added to `.env` file
- [ ] Token details recorded securely

### Step 15: Update Project Configuration
**Edit `databricks.yml`** with your specific values:

```yaml
variables:
  databricks_host:
    description: "Azure Databricks workspace URL"
    default: "https://adb-<YOUR-WORKSPACE-ID>.16.azuredatabricks.net"
  # ... rest of configuration
```

- [ ] `databricks_host` updated with your workspace URL
- [ ] `notification_email` updated with your email
- [ ] External location names match your Unity Catalog setup

---

## Phase 4: Databricks CLI Configuration

### Step 16: Install and Configure Databricks CLI
```bash
# Install Databricks CLI (if not already installed)
pip install databricks-cli

# Configure authentication profile
databricks configure --profile <your-company>-insurance
```

**When prompted, enter:**
- **Host**: `https://adb-<your-workspace-id>.16.azuredatabricks.net`
- **Token**: Your personal access token from Step 14

- [ ] Databricks CLI installed
- [ ] Authentication profile configured
- [ ] Profile name: `________________`

### Step 17: Update Bundle Configuration for Profile
**Edit `databricks.yml`** to use your profile:

```yaml
targets:
  dev:
    mode: development
    default: true
    workspace:
      host: ${var.databricks_host}
      profile: <your-company>-insurance  # Your profile name
      # ... rest of configuration
```

- [ ] Profile name updated in all targets (dev, staging, prod)
- [ ] Configuration matches your setup

### Step 18: Test Authentication
```bash
# Test CLI authentication
databricks auth describe

# Should show your workspace and profile information
```

- [ ] Authentication test successful
- [ ] Workspace URL matches expectation
- [ ] Profile shows as configured

---

## Phase 5: DAB Deployment and Testing

### Step 19: Validate Bundle Configuration
```bash
# Validate the bundle configuration
databricks bundle validate --target dev
```

- [ ] Bundle validation successful
- [ ] No configuration errors reported

### Step 20: Deploy Development Environment
```bash
# Deploy to development
databricks bundle deploy --target dev
```

- [ ] Development deployment successful
- [ ] Pipeline created in workspace
- [ ] Job created in workspace
- [ ] No deployment errors

### Step 21: Verify Unity Catalog Resources
1. **Catalog Explorer** → Navigate to `insurance_demo_dev.customers`
2. **Check for schemas**: Should see `customers` schema
3. **Verify external location**: Can browse `demodata` location

- [ ] `insurance_demo_dev` catalog accessible
- [ ] `customers` schema exists
- [ ] External location `demodata` accessible
- [ ] Can see folder structure in external location

### Step 22: Test Pipeline Execution
```bash
# Run the customer pipeline job
databricks bundle run customer_pipeline_job --target dev
```

- [ ] Pipeline job started successfully
- [ ] Monitor progress in Databricks UI
- [ ] Pipeline completes without errors
- [ ] Tables created: `customers_bronze`, `customers_silver`, `customer_summary`

### Step 23: Verify Data Processing
```sql
-- In Databricks SQL Editor or Notebook
SELECT * FROM insurance_demo_dev.customers.customers_bronze LIMIT 10;
SELECT * FROM insurance_demo_dev.customers.customers_silver LIMIT 10;  
SELECT * FROM insurance_demo_dev.customers.customer_summary;
```

- [ ] Bronze table contains raw data
- [ ] Silver table shows cleaned/transformed data
- [ ] Gold table shows aggregated customer summary
- [ ] Data quality expectations passed

### Step 24: Test Email Notifications
1. **Trigger pipeline failure** (temporarily break something)
2. **Check email** for failure notification
3. **Fix issue and re-run** 
4. **Check email** for success notification

- [ ] Failure notification received
- [ ] Success notification received
- [ ] Email addresses correct

---

## Phase 6: Multi-Environment Setup (Optional)

### Step 25: Create Additional External Locations (If Using Separate Storage)
For staging and production, you may want separate external locations:

```bash
# Create staging external location
# URL: abfss://raw@<storage>.dfs.core.windows.net/staging-demodata

# Create production external location  
# URL: abfss://raw@<storage>.dfs.core.windows.net/prod-demodata
```

- [ ] Staging external location created (if applicable)
- [ ] Production external location created (if applicable)
- [ ] Permissions configured for each environment

### Step 26: Deploy Staging Environment
```bash
# Deploy to staging
databricks bundle deploy --target staging
```

- [ ] Staging deployment successful
- [ ] Staging catalog accessible
- [ ] Staging pipeline functional

### Step 27: Deploy Production Environment
```bash
# Deploy to production
databricks bundle deploy --target prod
```

- [ ] Production deployment successful
- [ ] Production catalog accessible
- [ ] Production pipeline functional

---

## Phase 7: Security and Best Practices

### Step 28: Set Up Proper Access Controls
```sql
-- Grant appropriate permissions
GRANT USE CATALOG ON CATALOG insurance_demo_dev TO `data-engineers`;
GRANT USE SCHEMA ON SCHEMA insurance_demo_dev.customers TO `data-engineers`;
GRANT SELECT ON TABLE insurance_demo_dev.customers.customers_silver TO `data-analysts`;
```

- [ ] User groups configured
- [ ] Appropriate catalog permissions granted
- [ ] Schema permissions configured
- [ ] Table-level permissions set

### Step 29: Configure Monitoring and Alerting
1. **Pipeline Monitoring** → Set up additional monitoring
2. **Cost Monitoring** → Configure cost alerts
3. **Performance Monitoring** → Set up query performance tracking

- [ ] Pipeline monitoring configured
- [ ] Cost alerts set up
- [ ] Performance tracking enabled

### Step 30: Document Environment-Specific Details
Create documentation for your specific environment:

- [ ] **Workspace URL**: `________________`
- [ ] **Storage Account**: `________________`
- [ ] **External Locations**: `________________`
- [ ] **Service Principals**: `________________`
- [ ] **Key Contacts**: `________________`
- [ ] **Escalation Procedures**: `________________`

---

## Troubleshooting Guide

### Common Issues and Solutions

**Issue: Bundle validation fails**
```bash
# Check YAML syntax
databricks bundle validate --verbose --target dev
```

**Issue: Authentication failures**
```bash
# Verify profile configuration
databricks auth profiles
databricks auth describe --profile <your-profile>
```

**Issue: External location access denied**
- Verify service principal permissions
- Check storage account access controls
- Confirm external location URL is correct

**Issue: Pipeline fails with path errors**
- Verify external location name matches configuration
- Check folder structure in storage account
- Confirm data files exist in expected locations

**Issue: Unity Catalog permissions**
- Verify user has access to catalogs/schemas
- Check external location permissions
- Confirm service principal has storage access

---

## Success Criteria Checklist

### Development Environment Ready
- [ ] ✅ Bundle deploys successfully
- [ ] ✅ Pipeline processes sample data
- [ ] ✅ All three tables created (bronze, silver, gold)
- [ ] ✅ Data quality expectations pass
- [ ] ✅ Email notifications working
- [ ] ✅ Can query tables in SQL editor

### Security Configured
- [ ] ✅ Personal access tokens secured
- [ ] ✅ Service principals configured
- [ ] ✅ Unity Catalog permissions set
- [ ] ✅ External locations secured
- [ ] ✅ No credentials in git repository

### Ready for Team Collaboration
- [ ] ✅ Documentation complete
- [ ] ✅ Multiple environments available
- [ ] ✅ CI/CD ready (Phase 2)
- [ ] ✅ Monitoring configured
- [ ] ✅ Team access granted

---

## Next Steps

Once this setup is complete, you're ready for:

1. **🚀 Phase 2: Advanced DAB Patterns**
   - Add policy and claims data pipelines
   - Implement complex data transformations
   - Set up data lineage tracking

2. **🔄 CI/CD Implementation**
   - GitHub Actions integration
   - Automated testing
   - Multi-environment promotion

3. **📊 Advanced Analytics**
   - Machine learning pipelines
   - Real-time streaming
   - Advanced monitoring and alerting

4. **🏢 Enterprise Features**
   - Advanced security controls
   - Data governance
   - Compliance and auditing

---

## Support and Resources

- **Databricks Documentation**: [docs.databricks.com](https://docs.databricks.com)
- **Unity Catalog Guide**: [Unity Catalog Documentation](https://docs.databricks.com/data-governance/unity-catalog/)
- **Asset Bundles**: [DAB Documentation](https://docs.databricks.com/dev-tools/bundles/)
- **Azure Integration**: [Azure Databricks Documentation](https://docs.microsoft.com/en-us/azure/databricks/)

**Repository**: https://github.com/dwiltse/cicd_databricks_dabs_azure

---

*This setup guide ensures a secure, scalable, and maintainable Azure Databricks environment ready for enterprise data processing.*