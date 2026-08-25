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

**AWS CostLens**는 AWS 비용을 검토하기 위한 가볍고 읽기 전용 CLI입니다. 기존 사용자 환경을 최대한 변경하지 않고 자원 정보를 제공합니다.

간단한 터미널 기반 뷰를 제공합니다.:

| Area | What it shows |
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

주요 기능은 다음과 같습니다:
*   **💰 AWS 비용 현황 한눈에 보기:** 이번 달 누적 비용과 이전 달 비용을 비교하고, 증감률과 서비스별 비용을 함께 확인합니다.
<img width="1498" height="1136" alt="image" src="https://github.com/user-attachments/assets/a13f6292-59c8-4e75-9b7b-1afe1c26bbc6" />

*   **💳 Promotional Credit 잔액 및 만료일 확인:** AWS Promotional Credit의 최초 금액, 현재 잔액, 예상 잔액과 만료일을 한눈에 확인합니다.
<img width="647" height="121" alt="image" src="https://github.com/user-attachments/assets/40d313d4-1790-4d8c-8da1-8e2926498142" />

*   **🩺 미사용 리소스 및 태깅 상태 점검:** 태그 적용 여부도 함께 확인하여 태그가 누락된 리소스와 현재 적용된 태그를 쉽게 구분할 수 있습니다.
<img width="717" height="257" alt="image" src="https://github.com/user-attachments/assets/156c96bb-6caf-4262-adc8-a2c92ee89e99" />


<br>

---

## 시작하기
Get up and running in under a minute:
```bash
# Trusted formula
brew trust --formula aws-all-star/tap/aws-costlens

# Install
brew tap aws-all-star/tap
brew install aws-costlens

# Check this month's AWS costs and compare with last month
aws-costlens cost

# Check AWS promotional credit balance and expiration
aws-costlens credit

# Check unused resources and resource tagging status
aws-costlens waste

# Run a complete AWS CostLens checkup
aws-costlens check
```

## 설치하기
### use Homebrew (macOS):
```bash
brew tap aws-all-star/tap
brew install aws-costlens
```



