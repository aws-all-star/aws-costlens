# Security Policy

## Read-only design
기본 프로젝트 정책은 읽기 전용 AWS API 작업을 사용합니다. 이 도구는 Elastic IP를 해제하지 않으며, EBS 볼륨을 삭제하지 않고, EC2 인스턴스를 종료하지 않으며, 리소스 크기를 조정하거나 AWS 인프라를 수정하지 않습니다.

## Credentials

저장하거나 Commit하지 마십시오:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- session tokens
- `~/.aws/credentials`
- `.env` 비밀이 포함된 파일
- 민감한 정보를 포함한 내보낸 청구/계정 데이터 세트

AWS CLI 프로필, IAM 역할, IAM Identity Center 또는 기타 표준 AWS 자격 증명 제공자를 사용하십시오.

## Reporting vulnerabilities

GitHub에서 개인 보안 자문을 개설해 주시고, 공개 이슈에 자격 증명이나 민감한 계정 정보를 게시하지 말아 주시기 바랍니다.
