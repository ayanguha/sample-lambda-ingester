## This Document describes How to run the application

## Functionality
This code is a sample starter project to give an idea how following features can be implemented in AWS

- Use AWS Lambda to connect to an API using API_KEY
- Store API_KEY in AWS Secret Manager and retrieve it at run time
- Read the data and put in AWS S3 Target Bucket
- Handle IAM roles and gives an indication of 2 roles required
- Deployment using `serverless` framework

## Requirements

1. AWS creds are present in ~/.aws/credentials file
2. This credential is used for Lambda deployment, so it should have full access on following services
- Cloudformation (For Stack creation)
- S3 (For initial zip upload)
- Lambda
- Cloudwatch (Create Log Groups)
- IAM (If IAM roles are added)

(Preferably create a role and assign to the user running serverless. This role is also called "deploymentRole")

3. A role should be created for Lambda to assume (LambdaAssumeRole). This role is assumed by Lambda at run time.
- Create a policy using LambdaAssumeRole_policy.json. Replace XXXXXXXXXXXX with your Account Id
- Create a Role. Trusted Entity: Lambda. Permission - Use above role
- Default name of this role is `Sample-Ingester-Managed-Role`. Update `serverless.yml` - Provider/IAM section if you use something else


4. Pre-create target bucket. Default name is`sample-api-ingester-target`. Update `serverless.yml` - Environment Variable section if you use something else

5. A key in AWS Secret Manager should be created in advance. By default, the key name is `MY_API_KEY`. Update `serverless.yml` - Environment Variable section if you use something else

6. Serverless framework should be installed from https://www.serverless.com/

## Deployment
- Clone this repo
- Run `serverless deploy`
