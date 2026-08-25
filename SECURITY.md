# Security Policy

## Read-only design

The default project policy uses read-only AWS API actions. The tool does not release Elastic IPs, delete EBS volumes, terminate EC2 instances, resize resources, or modify AWS infrastructure.

## Credentials

Do not store or commit:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- session tokens
- `~/.aws/credentials`
- `.env` files containing secrets
- exported billing/account datasets containing sensitive information

Use AWS CLI profiles, IAM roles, IAM Identity Center, or other standard AWS credential providers.

## Reporting vulnerabilities

Please open a private security advisory in GitHub rather than posting credentials or sensitive account details in a public issue.
