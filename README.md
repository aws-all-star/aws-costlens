<div align="center">

# 🔎 AWS CostLens

### Lightweight, read-only AWS cost & resource visibility CLI
**AWS 클라우드 비용을 분석하고 주요 비용 발생 서비스를 파악하며, 유휴·미사용 리소스와 잠재적인 비용 낭비 요소를 확인할 수 있는 읽기 전용(Read-only) CLI 도구입니다. 프로모션 크레딧의 잔액과 만료일을 지속적으로 확인하고, EC2·RDS·S3 리소스의 태깅 상태까지 함께 점검하여 AWS 환경의 비용 현황과 관리가 필요한 항목을 터미널에서 쉽고 빠르게 확인할 수 있습니다.**<br>

[![Release](https://img.shields.io/github/v/release/aws-all-star/aws-costlens?style=flat-square)](https://github.com/aws-all-star/aws-costlens/releases)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![AWS](https://img.shields.io/badge/AWS-FinOps-FF9900?style=flat-square&logo=amazonwebservices&logoColor=white)](https://aws.amazon.com/)
[![License](https://img.shields.io/github/license/aws-all-star/aws-costlens?style=flat-square)](LICENSE)

<br>

**Cost Visibility** · **Credit Monitoring** · **Waste Detection** · **Resource Tagging**

</div>

---

## 살펴보기

**AWS CostLens**는 비용(Cost)과 렌즈(관찰하다) 합성어로 뭐라도 이름이 필요할거 같아 지어 봤습니다.😁 <br>
AWS 비용을 검토하기 위한 가볍고 읽기 전용 CLI이고 기존 사용자 환경을 최대한 변경하지 않고 자원 정보를 제공합니다.

- 간단한 터미널 기반 뷰를 제공합니다.:
  
| 구분 | 내용 |
|---|---|
| 💰 **Cost** | 현재 월 비용, 전월 비용, 변동 비율 및 주요 서비스 요인 |
| 💳 **Credit** | 사용 가능한 AWS 프로모션 크레딧, 예상 남은 금액 및 만료 날짜 |
| 🩺 **Waste** | 잠재적으로 사용되지 않거나 불필요한 AWS 리소스 |
| 🏷️ **Tags** | 선택된 EC2, RDS 및 S3 리소스에 대한 태깅 상태 |

> [!NOTE]
> AWS 리소스를 수정하거나 중지하거나 삭제하거나 크기를 조정하거나 태그를 지정하지 않습니다.

<br>

## 시작은 작은 불편에서
다양한 AWS 신기능 검증과 PoC를 수행하면서 여러 서비스를 반복적으로 생성하고 삭제하다 보니, 비용 변화뿐 아니라 **Promotional Credit의 잔액과 만료 시점**을 지속적으로 확인해야 할 필요가 생겼습니다.
또한 테스트가 반복될수록 사용이 끝난 리소스가 남아 있거나 태그가 누락되는 경우가 생겼고, 이것들을 비용과 함께 한 번에 확인할 수 있으면 좋겠다는 생각이 들었습니다.
AWS CostLens는 이런 작은 불편에서 시작했습니다. 여러 AWS Console 화면을 오가는 대신 **비용 · 크레딧 · 미사용 리소스 · 태깅 상태를 터미널에서 가볍게 확인하는 것**, 그것이 이 도구를 만든 가장 큰 이유입니다.

</br>

주요 기능은 다음과 같습니다:
*   **💰 AWS 비용 현황 한눈에 보기:** 이번 달 누적 비용과 이전 달 비용을 간단하게 비교하고, 증감률과 서비스별 비용을 함께 확인합니다.
<img width="1000" height="758" alt="image" src="https://github.com/user-attachments/assets/9093efba-a150-4808-8d00-b88cdf0f8f4d" />

*   **💳 Promotional Credit 잔액 및 만료일 확인:** AWS Promotional Credit의 최초 금액, 현재 잔액, 예상 잔액과 만료일을 한눈에 확인합니다.
<img width="1000" height="187" alt="image" src="https://github.com/user-attachments/assets/e1aed430-8895-4520-99ad-ae9592384485" />

*   **🩺 미사용 리소스 및 태깅 상태 점검:** 태그 적용 여부도 함께 확인하여 태그가 누락된 리소스와 현재 적용된 태그를 쉽게 구분할 수 있습니다.
<img width="1000" height="358" alt="image" src="https://github.com/user-attachments/assets/ab464fac-d582-4895-90bc-e1814195e63d" />

<br>

---

## 간단하게 시작하기
1분 이내에 바로 시작해보기:
```bash
# 신뢰할 수 있는 공식
brew trust --formula aws-all-star/tap/aws-costlens

# 설치하다
brew tap aws-all-star/tap
brew install aws-costlens

# 이번 달 AWS 비용을 확인하고 지난 달과 비교하십시오.
aws-costlens cost

# AWS 프로모션 크레딧 잔액 및 만료를 확인하십시오
aws-costlens credit

# 미사용 리소스 및 리소스 태깅 상태를 확인하십시오.
aws-costlens waste

# 전체 AWS CostLens 점검을 실행하십시오.
aws-costlens check
```
------

## 설치하기
#### Homebrew를 사용하십시오 (macOS):
```bash
brew tap aws-all-star/tap
brew install aws-costlens
```
<br>

## ⚡ 전제 조건 확인

> [!IMPORTANT]
> 다음과 같은 **읽기 전용 권한**을 가진 AWS 자격 증명이 필요합니다.

- **Python 3.8 이상**: 필요한 Python 버전이 설치되어 있는지 확인하십시오.
- **AWS CLI가 명명된 프로파일**: 원활한 통합을 위해 AWS CLI 프로파일을 설정하십시오
- **AWS 자격 증명 및 권한**:
  - `sts:GetCallerIdentity`
  - `ce:GetCostAndUsage`
  - `billing:GetCredits`
  - `ec2:DescribeInstances`
  - `ec2:DescribeVolumes`
  - `ec2:DescribeAddresses`
  - `rds:DescribeDBInstances`
  - `rds:ListTagsForResource`
  - `s3:ListAllMyBuckets`
  - `s3:GetBucketLocation`
  - `s3:GetBucketTagging`

------

### 명령줄 옵션
`aws-costlens`와 그 뒤에 옵션을 사용하여 스크립트를 실행하십시오:

```bash
aws-costlens [options]
```

| 옵션 / 명령어 | 설명 |
|---|---|
| `aws-costlens check` | AWS 비용, 프로모션 크레딧, 미사용 리소스, 리소스 태깅 상태 및 권고사항을 한 번에 점검합니다. |
| `aws-costlens cost` | 이번 달 AWS 비용 현황과 서비스별 비용을 확인합니다. |
| `aws-costlens credit` | 사용 가능한 AWS 프로모션 크레딧의 잔액과 만료 정보를 확인합니다. |
| `aws-costlens waste` | 유휴·미사용 리소스를 탐지하고 EC2, RDS, S3 리소스의 태깅 상태를 점검합니다. |
| `--install-completion` | 현재 Shell에 명령어 자동 완성 기능을 설치합니다. |
| `--show-completion` | 현재 Shell의 자동 완성 스크립트를 출력합니다. |
| `--help` | 사용 가능한 명령어와 옵션에 대한 도움말을 표시합니다. |

### 공통 명령 옵션
각 AWS CostLens 명령에서 다음 옵션을 사용할 수 있습니다.

| 옵션 | 설명 | 기본값 |
|---|---|---|
| `--profile TEXT` | 인증에 사용할 AWS CLI Profile을 지정합니다. | AWS 기본 인증 정보 |
| `--region TEXT` | 리소스 및 Waste 점검에 사용할 AWS Region을 지정합니다. | `ap-northeast-2` |
| `--help` | 선택한 명령어의 도움말을 표시합니다. | — |

<br>
