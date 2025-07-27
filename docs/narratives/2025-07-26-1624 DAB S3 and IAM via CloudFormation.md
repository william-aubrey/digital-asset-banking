---
date: 2025-07-26
timestamp: "2025-07-26T15:50:00Z"
agent: ChatGPT o4-mini-high

session_metadata:
  session_id: "dab-infra-2025-07-26"
  started_at: "2025-07-26T14:30:00Z"
  last_updated: "2025-07-26T15:50:00Z"
  duration_minutes: 80
  messages_exchanged: 45
  model: "ChatGPT o4-mini"
  context_token_limit: 8192
  current_context_tokens: 6500
  hit_context_limit: false
  canvases_created: 2
  files_generated:
    - core_dab.py
    - cyoa_plugin.py
    - streamlit_app.py
    - infrastructure.yaml
    - dab-iam-policy.json
---

#  2025-07-26 DAB S3 and IAM via CloudFormation

 Saturday Afternoon

This document serves as a concise overview of the steps and artifacts we’ve created to provision and integrate AWS resources for the **Digital Asset Banking (DAB)** application, focusing on S3 and IAM via CloudFormation.

---

## 1. Core DAB Application

- **Streamlit app (`DAB_3.0.py`)** with:
  - **Generic asset banking**: Core functions to register, list, and purchase assets.
  - **CYOA plugin**: Optional NODE/EDGE/HOPTO conventions as an asset-type extension.
  - **S3 integration**: Uses `boto3` to upload files to S3 under `<asset_type>/<filename>` and records `s3_key` in metadata.

**Launch command**:

```bash
env AWS_S3_BUCKET=your-bucket-name \
  AWS_ACCESS_KEY_ID=… \
  AWS_SECRET_ACCESS_KEY=… \
  AWS_DEFAULT_REGION=us-east-1 \
  streamlit run DAB_3.0.py
```

---

## 2. IAM Policy for DAB Deployer

- **Least-privilege JSON policy** (`dab-iam-policy.json`) granting:
  - **CloudFormation**: Create/Update/Delete stacks prefixed `dab-infra*`.
  - **S3**: `CreateBucket`, `ListBucket`, `GetObject`, `PutObject`, `DeleteObject` on `digital-assets-william-ryan-aubrey`.

**Attach policy**:

```bash
aws iam put-user-policy \
  --user-name iam-dab-agent \
  --policy-name DABDeployerPolicy \
  --policy-document file://dab-iam-policy.json
```

---

## 3. CloudFormation Template (`infrastructure.yaml`)

A single YAML template with parameters and conditions to:

1. **S3 Bucket** (`AssetBucket`)
   - **Parameter** `BucketName` (default `digital-assets-william-ryan-aubrey`).
   - **Condition** `CreateBucket` (toggle via `UseExistingBucket`).
   - **Public access blocked** + **Retain** policies.

2. **Bucket Policy** (`AssetBucketPolicy`)
   - Always applied, principals reference either the new or existing IAM user.
   - Actions: `s3:ListBucket`, `s3:GetObject`, `s3:PutObject`.

3. **IAM User** (`AssetUser`)
   - **Parameter** `UseExistingUser` (default `false`) toggles creation.
   - **Parameter** `ExistingUserArn` to supply if reusing.
   - `AssetUserPolicy` and `AssetUserAccessKey` gated on `CreateUser`.

4. **Outputs**
   - `BucketName`, `IAMUserArn`, and (if created) `AccessKeyId`, `SecretAccessKey`.

**Deploy commands**:

- **Create both**:

  ```bash
  aws cloudformation deploy \
    --template-file infrastructure.yaml \
    --stack-name dab-infra \
    --capabilities CAPABILITY_NAMED_IAM
  ```

- **Reuse existing bucket & IAM**:

  ```bash
  aws cloudformation deploy \
    --template-file infrastructure.yaml \
    --stack-name dab-infra \
    --capabilities CAPABILITY_NAMED_IAM \
    --parameter-overrides \
        UseExistingBucket=true \
        UseExistingUser=true \
        ExistingUserArn=arn:aws:iam::123456789012:user/iam-dab-agent
  ```

- **Cleanup** (delete failed stack)

  ```bash
  aws cloudformation delete-stack --stack-name dab-infra
  aws cloudformation wait stack-delete-complete --stack-name dab-infra
  ```

---

## 4. Troubleshooting Notes

- **Rollback states** occur if:
  - Bucket or user already exist and CFN tries to recreate them.
  - Principal is blank because parameters not passed.
- **Fixes applied**:
  - Added `DeletionPolicy: Retain` to all resources.
  - Introduced `UseExistingBucket` and `UseExistingUser` conditions.
  - Adjusted default for `UseExistingUser` to `false` to force new-user creation initially.
  - Updated bucket policy to reference `${BucketName}` and conditional principals.

---

You can now start fresh by deploying the final `infrastructure.yaml` with the appropriate parameters, and then launch your Streamlit app connected to the provisioned S3 bucket and IAM user.

---

## Appendices

### Appendix A: infrastructure.yaml
```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: >
  CloudFormation template to create or update an S3 bucket and manage an IAM user
  (optionally using existing resources). Supports safe updates without failures when
  resources already exist.

Parameters:
  BucketName:
    Type: String
    Description: S3 bucket name (created if UseExistingBucket is false)
    Default: digital-assets-william-ryan-aubrey
  UseExistingBucket:
    Type: String
    AllowedValues: ["true","false"]
    Default: "true"
    Description: "Set to 'true' to use an existing bucket; 'false' to create a new one."
  UserName:
    Type: String
    Description: IAM user name to create if UseExistingUser is 'false'
    Default: iam-dab-agent
  UseExistingUser:
    Type: String
    AllowedValues: ["true","false"]
    Default: "false"
    Description: "Set to 'true' to use an existing IAM user; 'false' to create a new one."
  ExistingUserArn:
    Type: String
    Description: ARN of an existing IAM user (required if UseExistingUser is 'true')
    Default: ""

Conditions:
  CreateBucket: !Equals [ !Ref UseExistingBucket, "false" ]
  CreateUser:   !Equals [ !Ref UseExistingUser,   "false" ]

Resources:
  AssetBucket:
    Condition: CreateBucket
    Type: AWS::S3::Bucket
    DeletionPolicy: Retain
    UpdateReplacePolicy: Retain
    Properties:
      BucketName: !Ref BucketName
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true

  AssetBucketPolicy:
    Type: AWS::S3::BucketPolicy
    DeletionPolicy: Retain
    UpdateReplacePolicy: Retain
    Properties:
      Bucket: !Ref BucketName
      PolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Sid: AllowUserList
            Effect: Allow
            Principal:
              AWS: !If [ CreateUser, !GetAtt AssetUser.Arn, !Ref ExistingUserArn ]
            Action:
              - s3:ListBucket
            Resource: !Sub arn:aws:s3:::${BucketName}
          - Sid: AllowUserObjects
            Effect: Allow
            Principal:
              AWS: !If [ CreateUser, !GetAtt AssetUser.Arn, !Ref ExistingUserArn ]
            Action:
              - s3:GetObject
              - s3:PutObject
            Resource:
              - !Sub arn:aws:s3:::${BucketName}/*

  AssetUser:
    Condition: CreateUser
    Type: AWS::IAM::User
    DeletionPolicy: Retain
    Properties:
      UserName: !Ref UserName
      Path: /

  AssetUserPolicy:
    Condition: CreateUser
    Type: AWS::IAM::Policy
    DeletionPolicy: Retain
    Properties:
      PolicyName: S3AccessPolicy
      Users: [ !Ref AssetUser ]
      PolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Action:
              - s3:ListBucket
              - s3:GetObject
              - s3:PutObject
            Resource:
              - !Sub arn:aws:s3:::${BucketName}
              - !Sub arn:aws:s3:::${BucketName}/*

  AssetUserAccessKey:
    Condition: CreateUser
    Type: AWS::IAM::AccessKey
    DeletionPolicy: Retain
    Properties:
      UserName: !Ref AssetUser

Outputs:
  BucketName:
    Description: S3 bucket name in use
    Value: !Ref BucketName

  IAMUserArn:
    Description: ARN of the IAM user (created or existing)
    Value: !If [ CreateUser, !GetAtt AssetUser.Arn, !Ref ExistingUserArn ]

  AccessKeyId:
    Condition: CreateUser
    Description: Access Key ID for the new user
    Value: !Ref AssetUserAccessKey

  SecretAccessKey:
    Condition: CreateUser
    Description: Secret Access Key for the new user
    Value: !GetAtt AssetUserAccessKey.SecretAccessKey
```


### Appendix B: dab-iam-policy.json
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowCloudFormationOperations",
      "Effect": "Allow",
      "Action": [
        "cloudformation:CreateStack",
        "cloudformation:UpdateStack",
        "cloudformation:DescribeStacks",
        "cloudformation:ListStacks",
        "cloudformation:DeleteStack"
      ],
      "Resource": "arn:aws:cloudformation:*:*:stack/dab-infra*"
    },
    {
      "Sid": "AllowS3BucketManagement",
      "Effect": "Allow",
      "Action": [
        "s3:CreateBucket",
        "s3:ListBucket",
        "s3:GetBucketLocation",
        "s3:PutEncryptionConfiguration",
        "s3:PutBucketPublicAccessBlock"
      ],
      "Resource": "arn:aws:s3:::digital-assets-william-ryan-aubrey"
    },
    {
      "Sid": "AllowS3ObjectAccess",
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket",
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": [
        "arn:aws:s3:::digital-assets-william-ryan-aubrey/*"
      ]
    }
  ]
}
```

---

## Epilogue
This document captures the full history of provisioning your DAB infrastructure with AWS CloudFormation and IAM guidance.

### Session Metadata
Below is a YAML representation of key session details and context:

```yaml
session_metadata:
  session_id: "dab-infra-2025-07-26"
  started_at: "2025-07-26T14:30:00Z"
  last_updated: "2025-07-26T15:50:00Z"
  duration_minutes: 80
  messages_exchanged: 45
  model: "ChatGPT o4-mini"
  context_token_limit: 8192
  current_context_tokens: 6500
  hit_context_limit: false
  canvases_created: 2
  files_generated:
    - core_dab.py
    - cyoa_plugin.py
    - streamlit_app.py
    - infrastructure.yaml
    - dab-iam-policy.json
```
