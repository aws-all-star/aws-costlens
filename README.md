<div align="center">

# 🔎 AWS CostLens

### Lightweight, read-only AWS cost & resource visibility CLI
AWS 비용을 분석하고, 프로모션 크레딧을 모니터링하며, 잠재적인 낭비 리소스를 식별하고, 리소스 태깅 상태를 터미널에서 직접 확인합니다.

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
