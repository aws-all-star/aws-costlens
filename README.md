<div align="center">

# 🔎 AWS CostLens

### Lightweight, read-only AWS cost & resource visibility CLI
**AWS 클라우드 비용을 분석하고 주요 비용 발생 서비스를 파악하며, 유휴·미사용 리소스와 잠재적인 비용 낭비 요소를 확인할 수 있는 가벼운 읽기 전용(Read-only) CLI 도구입니다. 프로모션 크레딧의 잔액과 만료일을 지속적으로 확인하고, EC2·RDS·S3 리소스의 태깅 상태까지 함께 점검하여 AWS 환경의 비용 현황과 관리가 필요한 항목을 터미널에서 쉽고 빠르게 확인할 수 있습니다.**<br>

[![Release](https://img.shields.io/github/v/release/aws-all-star/aws-costlens?style=flat-square)](https://github.com/aws-all-star/aws-costlens/releases)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![AWS](https://img.shields.io/badge/AWS-FinOps-FF9900?style=flat-square&logo=amazonwebservices&logoColor=white)](https://aws.amazon.com/)
[![License](https://img.shields.io/github/license/aws-all-star/aws-costlens?style=flat-square)](LICENSE)

<br>

**Cost Visibility** · **Credit Monitoring** · **Waste Detection** · **Resource Tagging**

</div>

---

## Overview

**AWS CostLens**는 AWS 비용을 검토하기 위한 가볍고 읽기 전용 CLI입니다.환경을 변경하지 않고 자원 정보를 제공합니다.

간단한 터미널 기반 뷰를 제공합니다.:

| Area | What it shows |
|---|---|
| 💰 **Cost** | 현재 월 비용, 전월 비용, 변동 비율 및 주요 서비스 요인 |
| 💳 **Credit** | 사용 가능한 AWS 프로모션 크레딧, 예상 남은 금액 및 만료 날짜 |
| 🩺 **Waste** | 잠재적으로 사용되지 않거나 불필요한 AWS 리소스 |
| 🏷️ **Tags** | 선택된 EC2, RDS 및 S3 리소스에 대한 태깅 상태 |

> [!NOTE]
> AWS CostLens는 **가시성 및 빠른 검토**를 위해 가볍게 설계되었습니다. 
> AWS 리소스를 수정하거나 중지하거나 삭제하거나 크기를 조정하거나 태그를 지정하지 않습니다.

---

## Quick Start

### Homebrew

```bash
brew tap aws-all-star/tap
brew install aws-costlens
