# SPEC-1-Digital Asset Banking Infrastructure

## Background

Digital Asset Banking (DAB) is envisioned as a decentralized personal data banking system that empowers users to create, manage, and trade unique digital assets—ranging from images and code to video and audio—and to manifest these assets as physical, high-quality trading cards. Assets are uploaded through a Streamlit-based frontend, stored in AWS S3, and their metadata and transaction records are maintained in a Snowflake data warehouse. The platform supports key workflows such as asset creation, secure storage (data banking), NFT-style marketplace transactions, and on-demand physical card printing with QR-code–based authentication.

## Requirements

**Must Have**

- **Regulatory & Compliance**:
  - Data residency in the United States (AWS us-east-1, Snowflake AWS\_US\_EAST) and Brazil (AWS sa-east-1, Snowflake AWS\_SA\_EAST).
  - Encryption at rest (AES-256) and in-transit (TLS 1.2+).
  - Compliance with GDPR, LGPD (Brazilian data protection law), and SOC 2 Type II.
  - Role-based access control (RBAC) and audit logging for all data and compute operations.
- **Infrastructure Availability & SLAs**:
  - 99.9% uptime SLA for the API and front-end services.
  - Recovery Time Objective (RTO) of <1 hour and Recovery Point Objective (RPO) of <15 minutes.
- **Scalability & Throughput**:
  - Support for at least 10,000 concurrent users in initial regions, scaling to 100,000 in global stage.
  - Auto-scaling policies on compute and serverless layers.

**Should Have**

- **Security**:
  - Integration with AWS KMS for key management.
  - Customer-managed keys for users running their own environments.
  - Multi-factor authentication (MFA) on all control-plane access.
- **Cost Management**:
  - Cost monitoring and budgets in AWS and Snowflake.
  - Resource tagging strategy for chargeback and visibility.

**Could Have**

- **Decentralized Deployment**:
  - Packaging as IaC modules (Terraform/CloudFormation) for users to self-deploy.
  - Public GitHub repository with CLI and Helm charts for Kubernetes deployments.
- **Marketplace Governance**:
  - Smart-contract patterns for peer-to-peer trading workflows (e.g., ERC-721 style).
  - On-chain metadata pointers with off-chain storage in S3.

**Won't Have (Initial MVP)**

- Fully centralized mobile-app–only experience (deferred to Stage 2).
- Native blockchain execution or consensus layer (deferred to Stage 3).

## Feature Inventory Format

To ensure consistent capture of user stories and associated features, please specify each feature in YAML using the following schema:

```yaml
- user_story: "<Title or brief of the user story>"
  actor: "<Actor performing the action, e.g., end_user, kernel_owner, admin>"
  feature_id: "<Unique identifier, e.g., FTR-001>"
  feature_name: "<Short name of the feature>"
  description: |
    <Detailed description of the feature and its purpose>
  priority: "<MoSCoW: must/should/could/won't>"
  acceptance_criteria:
    - "<Criterion 1>"
    - "<Criterion 2>"
  dependencies:
    - "<Related feature_id or external system>"
  notes: |
    <Any additional notes or assumptions>
```

Use this template for each feature derived from your user experience narratives. Once populated, we can map these features into our architecture and implementation plan.

## Method

### Architecture Overview

A multi-account AWS architecture for decentralization and scalability:

```plantuml
@startuml
!define AWSPUML https://raw.githubusercontent.com/awslabs/aws-icons-for-plantuml/v14.0/LATEST/AWSPUML
skinparam rectangle {
  Shadowing false
}
left to right direction

AWSPUML::Account(account1, "User AWS Account") {
  AWSPUML::S3(s3, "Asset Storage (S3)")
  AWSPUML::EC2(ec2, "Streamlit Frontend")
  AWSPUML::Lambda(lambda, "API (Lambda)")
}
AWSPUML::Account(account2, "Snowflake & Matillion Account") {
  AWSPUML::Database(snowflake, "Snowflake Data Warehouse")
  AWSPUML::AWSGeneric(matillion, "Matillion ETL")
}
AWSPUML::Account(account3, "Central Governance Account") {
  AWSPUML::IAM(iam, "IAM Roles & KMS")
  AWSPUML::CloudWatch(cw, "Logging & Metrics")
}

ec2 --> s3 : upload/download
lambda --> s3 : reads/writes
lambda --> snowflake : metadata queries
matillion --> snowflake : batch loads
lambda --> matillion : trigger ETL
iam --> s3
iam --> lambda
cw --> ec2
cw --> lambda
@enduml
```

### Component Descriptions

- **AWS S3**: Stores raw assets (images, code, audio). Versioning and lifecycle policies for archival.
- **Streamlit EC2**: Hosts the user-facing frontend, auto-scaled behind an Application Load Balancer.
- **API (Lambda)**: Serverless endpoints for asset CRUD, transaction processing, and QR code generation.
- **Snowflake**: Houses asset metadata, transaction history, and user profiles in region-specific virtual warehouses.
- **Matillion**: Orchestrates ELT pipelines to transform and normalize asset usage metrics.
- **IAM & KMS**: Centralized identity management with cross-account roles; customer-managed keys.
- **CloudWatch**: Aggregates logs, custom metrics, and alarms for SLAs and auditing.

### Network Topology & Security

- VPCs per account with public/private subnets; NAT gateways for outbound access.
- Security Groups restricting traffic to required ports (HTTPS, SSH via bastion).
- AWS WAF on ALB to protect against web exploits.
- Cross-account IAM roles for Snowflake and Matillion provisioning.

## Implementation

1. **AWS Account & IAM Provisioning**

   - Terraform modules for User, Analytics, Governance accounts with roles/policies.
   - Cross-account roles: `RoleUserDeploy`, `RoleAnalyticsAdmin`, `RoleGovernanceAudit`.

   **Terraform Module: **``

   ``

   ```hcl
   provider "aws" {
     alias  = "user"
     region = var.region
   }
   resource "aws_vpc" "main" {
     provider   = aws.user
     cidr_block = var.vpc_cidr
     tags       = var.tags
   }
   resource "aws_subnet" "public" {
     provider          = aws.user
     count             = length(var.public_subnets)
     vpc_id            = aws_vpc.main.id
     cidr_block        = var.public_subnets[count.index]
     availability_zone = var.azs[count.index]
     map_public_ip_on_launch = true
   }
   resource "aws_s3_bucket" "assets" {
     provider = aws.user
     bucket   = var.asset_bucket_name
     acl      = "private"
     versioning { enabled = true }
     server_side_encryption_configuration {
       rule { apply_server_side_encryption_by_default { sse_algorithm = "AES256" } }
     }
     tags = var.tags
   }
   ```

   ``

   ```hcl
   variable "region" { type = string }
   variable "vpc_cidr" { type = string }
   variable "public_subnets" { type = list(string) }
   variable "azs" { type = list(string) }
   variable "asset_bucket_name" { type = string }
   variable "tags" { type = map(string) }
   ```

2. **Networking & Security**

   - Terraform for VPC, subnets, NAT gateways, Security Groups, NACLs.
   - AWS WAF and ALB rule sets via Terraform.

3. **Compute & Storage**

   - EC2 Auto Scaling Group for Streamlit with User Data.
   - Packaged Lambda functions with GitHub Actions and CloudFormation.

4. **Snowflake & Matillion**

   - Snowflake Terraform provider: databases, warehouses, roles.
   - Matillion project via CLI: job definitions in GitHub, deployed in CI.

5. **CI/CD (GitHub Actions)**

   - **IaC Pipeline**: `terraform fmt/plan`, `tflint`, apply on merge.
   - **App Pipeline**: Build/test containers, deploy Lambdas.
   - **ELT Pipeline**: Validate Matillion jobs, push via CLI.

6. **Secrets & Key Management**

   - GitHub Secrets with AWS KMS encryption.
   - AWS Secrets Manager for Snowflake credentials.

7. **Monitoring & Alerts**

   - CloudWatch dashboards, alarms (EC2, Lambda, Snowflake credits).
   - SNS for on-call notifications.

## Milestones

- **Phase 1 (2w)**: Accounts & networking.
- **Phase 2 (2w)**: Snowflake & Matillion setup.
- **Phase 3 (2w)**: CI/CD & E2E testing.
- **Phase 4 (1w)**: Compliance & monitoring.
- **Phase 5 (1w)**: Documentation & handoff.

## Gathering Results

- **Uptime**: CloudWatch SLA reports.
- **Performance**: Load testing (Locust) for 10k users.
- **Cost**: Usage vs budget.
- **Security**: Pentest & audit logs.
- **Feedback**: User deployment surveys.

## Need Professional Help?

Contact me at [sammuti.com](https://sammuti.com) :)

```
```
