# Team Work Assignments - Insurance Data Pipeline Project

## Project Overview
This document tracks team assignments and responsibilities for the Databricks Asset Bundle implementation of the insurance customer data pipeline on Azure.

## Team Roles and Assignments

### Core Team Structure

#### DevOps and Infrastructure
- **Lead**: *[To be assigned]*
- **Responsibilities**:
  - Azure Databricks workspace configuration
  - Service principal management (`sp-poc-deploy`)
  - CI/CD pipeline setup and maintenance
  - External connections and Unity Catalog configuration
  - Environment management (dev/staging/prod)

#### Data Engineering
- **Lead**: *[To be assigned]*
- **Team Members**: *[To be assigned]*
- **Responsibilities**:
  - DLT pipeline development and maintenance
  - Data quality expectations and validation
  - Schema evolution management
  - Performance optimization
  - Bronze/Silver/Gold layer architecture

#### Quality Assurance
- **Lead**: *[To be assigned]*
- **Responsibilities**:
  - Integration testing
  - Data quality validation
  - Pipeline testing automation
  - Production deployment validation
  - End-to-end testing scenarios

#### Security and Governance
- **Lead**: *[To be assigned]*
- **Responsibilities**:
  - Unity Catalog permissions management
  - Group management (`engineers`, `insurance_team_admins`)
  - External location security
  - Credential rotation and management
  - Compliance and audit support

## Resource Ownership Matrix

### Databricks Resources

| Resource Type | Owner | Managers | Viewers | Notes |
|---------------|-------|----------|---------|-------|
| **Pipelines** | `sp-poc-deploy` | `insurance_team_admins` | `engineers` | Automated deployment via service principal |
| **Jobs** | `sp-poc-deploy` | `insurance_team_admins` | `engineers` | Engineers can manage runs |
| **Dev Schemas** | Individual developers | Self | Team | Personal development environments |
| **Staging Schema** | DevOps team | `insurance_team_admins` | `engineers` | Shared integration testing |
| **Prod Schema** | DevOps team | `insurance_team_admins` | Limited access | Production environment |

### External Resources

| Resource | Owner | Access Level | Purpose |
|----------|-------|--------------|---------|
| **Azure Blob Storage** | DevOps team | Connection-based | Source data storage |
| **External Connections** | DevOps team | Admin only | Unity Catalog integration |
| **GitHub Repository** | Development team | Branch-based | Source code and CI/CD |

## Environment-Specific Assignments

### Development Environment
- **Target**: `dev`
- **Schema Pattern**: `dev_${workspace.current_user.short_name}`
- **Assignees**: All engineering team members
- **Purpose**: Individual development and testing
- **Root Path**: `/Workspace/Users/${workspace.current_user.userName}/.bundle/${bundle.name}/dev`

### Staging Environment
- **Target**: `staging`
- **Schema**: `customers`
- **Assignees**: QA team (lead), DevOps team
- **Purpose**: Integration testing and validation
- **Root Path**: `/Workspace/Shared/.bundle/${bundle.name}/staging`

### Production Environment
- **Target**: `prod`
- **Schema**: `customers`
- **Assignees**: DevOps team (lead), designated admins
- **Purpose**: Production data processing
- **Root Path**: `/Workspace/Shared/.bundle/${bundle.name}/prod`

## Workflow Assignments

### Daily Operations
| Task | Assigned To | Frequency | Notes |
|------|-------------|-----------|-------|
| **Pipeline Monitoring** | DevOps team | Daily | Check for failures and performance |
| **Data Quality Review** | Data Engineering team | Daily | Monitor expectations and alerts |
| **Cost Monitoring** | DevOps team | Weekly | Azure resource usage review |
| **Security Review** | Security team | Monthly | Permissions and access audit |

### Development Workflow
| Phase | Primary Assignee | Secondary | Approval Required |
|-------|------------------|-----------|-------------------|
| **Feature Development** | Individual developer | N/A | PR review |
| **Integration Testing** | QA team | Data Engineering | QA approval |
| **Staging Deployment** | DevOps team | Development team | Automated |
| **Production Deployment** | DevOps team | Management | Manual approval |

## Contact Information

### Emergency Contacts
- **Production Issues**: *[To be assigned - DevOps lead]*
- **Data Quality Issues**: *[To be assigned - Data Engineering lead]*
- **Security Incidents**: *[To be assigned - Security lead]*
- **Business Impact**: *[To be assigned - Project manager]*

### Team Communication
- **Primary Channel**: *[To be assigned - Slack/Teams channel]*
- **Escalation**: *[To be assigned - Management contact]*
- **After Hours**: *[To be assigned - On-call rotation]*

## Assignment Change Process

### Adding New Team Members
1. Update this document with new assignments
2. Configure Databricks workspace access
3. Add to appropriate Azure AD groups
4. Grant Unity Catalog permissions
5. Provide onboarding documentation

### Changing Responsibilities
1. Document change request and rationale
2. Get approval from affected team leads
3. Update permissions in Databricks and Azure
4. Update this document
5. Communicate changes to team

### Removing Team Members
1. Remove from all Azure AD groups
2. Revoke Databricks workspace access
3. Transfer ownership of personal resources
4. Update this document
5. Archive access credentials

## Integration with Asset Bundle

This team assignment structure is integrated with the Databricks Asset Bundle configuration through:

- **Service Principal**: `${var.service_principal_name}` = `sp-poc-deploy`
- **Engineering Group**: `${var.engineering_group}` = `engineers`
- **Admin Group**: `${var.admin_group}` = `insurance_team_admins`

These variables are used in the permissions blocks of pipelines and jobs to automatically assign appropriate access levels based on team roles.

## Last Updated
- **Date**: *[To be updated when changes are made]*
- **Updated By**: *[Name of person making updates]*
- **Changes**: *[Brief description of what changed]*

---

*This document should be updated whenever team assignments change and reviewed monthly to ensure accuracy.*