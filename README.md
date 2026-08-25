<div align="center">

# 🔎 AWS CostLens

### Lightweight, read-only AWS cost & resource visibility CLI
AWS 비용과 주요 비용 발생 서비스를 분석하고, 유휴·미사용 리소스와 잠재적 낭비 요소를 확인하는 가벼운 읽기 전용 CLI 도구입니다. 프로모션 크레딧의 잔액과 만료일을 모니터링하고, EC2·RDS·S3 태깅 상태를 점검하여 비용 현황과 관리 항목을 빠르게 확인할 수 있습니다
<br>

[![Release](https://img.shields.io/github/v/release/aws-all-star/aws-costlens?style=flat-square)](https://github.com/aws-all-star/aws-costlens/releases)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![AWS](https://img.shields.io/badge/AWS-FinOps-FF9900?style=flat-square&logo=amazonwebservices&logoColor=white)](https://aws.amazon.com/)
[![License](https://img.shields.io/github/license/aws-all-star/aws-costlens?style=flat-square)](LICENSE)

<br>

**Cost Visibility** · **Credit Monitoring** · **Waste Detection** · **Resource Tagging**

</div>

---

## Overview

**AWS CostLens** is a lightweight, read-only CLI for reviewing AWS cost and
resource information without making changes to your environment.

It provides a simple terminal-based view of:

| Area | What it shows |
|---|---|
| 💰 **Cost** | Current month cost, previous month cost, change rate, and top service drivers |
| 💳 **Credit** | Available AWS promotional credits, estimated remaining amounts, and expiration dates |
| 🩺 **Waste** | Potentially unused or unnecessary AWS resources |
| 🏷️ **Tags** | Tagging status for selected EC2, RDS, and S3 resources |

> [!NOTE]
> AWS CostLens is designed for **visibility and review**.  
> It does not modify, stop, delete, resize, or tag AWS resources.

---

## Quick Start

### Homebrew

```bash
brew tap aws-all-star/tap
brew install aws-costlens
