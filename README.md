# Databricks Asset Bundle - Insurance Customer Pipeline (Azure)

## Project Overview

This project implements a production-ready Databricks Asset Bundle with Lakeflow declarative pipelines to process synthetic insurance company data on Azure. The project demonstrates modern data engineering best practices using Delta Live Tables, Unity Catalog, and Azure Blob Storage integration.

**Key Features:**
- 🏗️ **Databricks Asset Bundles (DAB)** for Infrastructure as Code
- 🔄 **Delta Live Tables (DLT)** for declarative data pipelines  
- 🛡️ **Unity Catalog** for data governance and security
- ☁️ **Azure Integration** with Blob Storage and managed identities
- 🚀 **Multi-Environment Support** (dev, staging, production)
- 📧 **Email Notifications** for pipeline success/failure monitoring

## Architecture

```
Azure Blob Storage → DLT Pipeline → Unity Catalog Tables
     (JSON)             ↓              (Bronze/Silver/Gold)
                  Auto Loader         
                     +                    📊 Analytics Ready
                Data Quality              📈 Customer Insights
                Expectations              📋 Reporting
```

## Data Pipeline

- **Bronze Layer**: Raw customer data ingestion from Azure Blob Storage
- **Silver Layer**: Cleaned and validated customer data with quality checks
- **Gold Layer**: Aggregated customer analytics and summary metrics

## Project Contributors

| Name | GitHub Username | Assigned Task |
|------|----------------|---------------|
| David Wiltse | @dwiltse | Project Lead & Architecture |
| Alice Johnson | @alice-dev | DLT Pipeline Development |
| Bob Smith | @bob-data | CI/CD Configuration |
| Carol Davis | @carol-azure | Azure Infrastructure Setup |
| Dan Wilson | @dan-test | Testing & Quality Assurance |
| Eva Martinez | @eva-docs | Documentation & Training |

## Quick Start

### Prerequisites
- Azure Databricks workspace (Premium tier)
- Unity Catalog enabled
- Azure Blob Storage account
- Databricks CLI installed

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/dwiltse/cicd_databricks_dabs_azure.git
   cd cicd_databricks_dabs_azure
   ```

2. **Configure environment**
   ```bash
   cp .env.template .env
   # Edit .env with your Azure/Databricks details
   ```

3. **Deploy to development**
   ```bash
   databricks bundle validate --target dev
   databricks bundle deploy --target dev
   ```

4. **Run the pipeline**
   ```bash
   databricks bundle run customer_pipeline_job --target dev
   ```

## Project Structure

```
├── databricks.yml                      # Bundle configuration
├── resources/
│   └── customer_pipeline.yml           # Pipeline and job definitions
├── src/
│   └── pipelines/
│       └── customer_azure_pipeline.py  # DLT pipeline implementation
├── tests/
│   └── unit/
│       └── test_customer_pipeline.py   # Unit tests
├── SETUP_GUIDE.md                      # Detailed setup instructions
└── README.md                           # This file
```

## Environments

- **Development**: Individual developer workspaces with isolated schemas
- **Staging**: Shared staging environment for integration testing  
- **Production**: Production environment with strict access controls

## Data Quality

The pipeline implements comprehensive data quality expectations:

- ✅ **Customer ID validation** (fail-fast)
- ✅ **Email format validation** (fail-fast)  
- ⚠️ **ZIP code format checks** (warnings)
- ⚠️ **Phone number format validation** (warnings)

## Contributing

1. Create a feature branch from `main`
2. Make your changes following the project patterns
3. Test locally using `databricks bundle validate`
4. Submit a pull request with detailed description
5. Ensure all CI/CD checks pass

## Documentation

- [📋 Setup Guide](SETUP_GUIDE.md) - Complete step-by-step setup instructions
- [🛠️ Setup Instructions](setup_instructions.md) - Quick setup reference
- [🧠 Project Architecture](CLAUDE.md) - Detailed technical documentation
- [👥 Team Strategy](TEAM_CICD_STRATEGY.md) - CI/CD and collaboration guidelines

## Support

For questions, issues, or contributions:

- 📧 **Email**: your-email@company.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/dwiltse/cicd_databricks_dabs_azure/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/dwiltse/cicd_databricks_dabs_azure/discussions)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

*Built with ❤️ using Databricks Asset Bundles and Azure Data Platform*