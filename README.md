# Spark 병렬 분석 플랫폼

[![Apache Spark](https://img.shields.io/badge/Apache%20Spark-3.4.0-E25A1C.svg?style=flat&logo=apache-spark&logoColor=white)](https://spark.apache.org/)
[![Google BigQuery](https://img.shields.io/badge/BigQuery-Latest-4285F4.svg?style=flat&logo=google-cloud&logoColor=white)](https://cloud.google.com/bigquery)
[![Amazon S3](https://img.shields.io/badge/Amazon%20S3-Latest-569A31.svg?style=flat&logo=amazon-s3&logoColor=white)](https://aws.amazon.com/s3/)
[![Docker](https://img.shields.io/badge/Docker-Latest-2496ED.svg?style=flat&logo=docker&logoColor=white)](https://docker.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB.svg?style=flat&logo=python&logoColor=white)](https://python.org/)
[![PySpark](https://img.shields.io/badge/PySpark-3.4.0-E25A1C.svg?style=flat&logo=apache-spark&logoColor=white)](https://spark.apache.org/docs/latest/api/python/)

> 🚀 ** 도커 환경에서 분산 데이터 처리 ** - 대규모 데이터 처리를 위한 Apache Spark 분산 환경 실험과 클라우드 통합

## 🌟 프로젝트 개요

**Spark Parallel**은 대용량 데이터셋에 대한 고속 분석을 수행하는 분산 데이터 처리 플랫폼입니다. 이 프로젝트는 Google Cloud Platform의 BigQuery와 Amazon S3를 통합하여 컨테이너화된 서비스로 구성된 아키텍처를 보여줍니다.

### 🎯 핵심 기능

- **대규모 데이터 처리**: 분산 Spark 클러스터로 데이터셋 처리
- **멀티 클라우드 아키텍처**: GCP BigQuery와 AWS S3 생태계의 원활한 통합
- **컨테이너 네이티브**: 수평 확장 가능한 Docker 기반 배포

## 🏗️ 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│                    Spark 클러스터 아키텍처                   │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │ Spark Master│    │   Worker 1  │    │   Worker 2  │      │
│  │   :8080     │◄───┤   :8081     │    │   :8082     │      │
│  │   :7077     │    │             │    │             │      │
│  └─────────────┘    └─────────────┘    └─────────────┘      │
│         ▲                   ▲                   ▲           │
│         │                   │                   │           │
│  ┌─────────────────────────────────────────────────────────┐│
│  │              Spark 애플리케이션 컨테이너                 ││
│  │               (PySpark 분석 엔진)                       || 
│  └─────────────────────────────────────────────────────────┘|
└─────────────────────────────────────────────────────────────┘
                 ▲                           ▼
    ┌─────────────────────┐         ┌─────────────────────┐
    │   Google BigQuery   │         │     Amazon S3       │
    │   (데이터 웨어하우스)│         │   (결과 저장소)      │
    │   NYC 택시 데이터셋  │         │  Parquet 분석 결과   │
    └─────────────────────┘         └─────────────────────┘
```

### 🔧 기술 스택

| 구성 요소 | 기술 | 버전 | 목적 |
|-----------|------|------|------|
| **컴퓨팅 엔진** | Apache Spark | 3.4.0 | 분산 처리 |
| **언어 런타임** | Python | 3.x | 애플리케이션 개발 |
| **데이터 웨어하우스** | Google BigQuery | Latest | 소스 데이터 플랫폼 |
| **객체 스토리지** | Amazon S3 | Latest | 결과 지속성 |
| **컨테이너화** | Docker Compose | Latest | 서비스 오케스트레이션 |
| **네트워킹** | Custom Bridge | - | 서비스 간 통신 |

## 🚀 빠른 시작

### 사전 요구사항

- Docker & Docker Compose 설치
- BigQuery 권한이 있는 GCP 서비스 계정
- S3 액세스 권한이 있는 AWS 자격 증명
- 최적 성능을 위해 16GB+ RAM 권장

### 1. 환경 설정

```bash
# 저장소 복제
git clone <repository-url>
cd spark-parallel

# 비밀 디렉토리 생성
mkdir -p .secrets

# GCP 서비스 계정 키 추가
cp /path/to/your/service-account.json .secrets/service_account.json
```

### 2. 구성

클라우드 자격 증명으로 `.env` 파일을 생성하세요:

```env
# Google Cloud Platform 구성
GOOGLE_APPLICATION_CREDENTIALS=/secrets/service_account.json
GCP_PROJECT_ID=your-project-id

# AWS S3 구성
S3_BUCKET=your-bucket-name
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_DEFAULT_REGION=us-east-1
```

### 3. 플랫폼 시작

**jar 파일을 필수적으로 업로드해야 합니다** 
```bash
# JAR 파일 다운로드
./download_jars.sh
```

```bash
# 전체 Spark 생태계 시작
./run.sh up

# 클러스터 상태 확인
./run.sh status

# 클러스터 상태 모니터링
./run.sh logs

# 특정 서비스 로그 확인
./run.sh logs spark-master

# Spark Master UI 접속
open http://localhost:8080
```

## 💻 사용 예시

### 기본 분석 파이프라인

플랫폼은 자동으로 정교한 분석 파이프라인을 실행합니다:

1. **데이터 수집**: BigQuery의 공개 NYC 택시 데이터셋에 연결
2. **분산 처리**: 승객 수별 요금 분석 수행
3. **결과 지속성**: 최적화된 Parquet 파일을 S3에 저장

### 커스텀 분석

`src/spark.py`를 수정하여 자신만의 처리 로직을 구현하세요:

```python
# 예시: 커스텀 BigQuery 데이터셋 처리
df = spark.read.format("bigquery") \
    .option("table", "your-project.dataset.table") \
    .load()

# 변환 적용
result = df.groupBy("category") \
    .agg(avg("value").alias("avg_value")) \
    .orderBy("avg_value", ascending=False)

# S3에 저장
result.write.mode("overwrite") \
    .parquet(f"s3a://{bucket}/custom-analytics/")
```

## 🔧 고급 구성

### 워커 확장

```yaml
# docker-compose.yml - 더 많은 워커 추가
spark-worker-3:
  image: bitnami/spark:3.4.0
  environment:
    - SPARK_MODE=worker
    - SPARK_MASTER_URL=spark://spark-master:7077
```

### 커스텀 JAR 의존성

`jars/` 디렉토리에 추가 Spark 커넥터를 추가하세요:

- `spark-bigquery-with-dependencies_2.12-0.34.0.jar`
- `gcs-connector-3.0.9-shaded.jar`
- `hadoop-aws-3.3.4.jar` (향상된 S3 지원용)

## 🛡️ 보안 기능

- **Zero-Trust 인증**: 서비스 계정 키 로테이션
- **암호화된 전송**: 모든 클라우드 통신을 위한 TLS/SSL
- **컨테이너 격리**: 샌드박스 실행 환경
- **자격 증명 관리**: 환경 기반 비밀 주입

## 📈 모니터링 및 관측성

- **Spark Master UI**: http://localhost:8080 - 클러스터 개요
- **워커 노드 UI**: http://localhost:8081, http://localhost:8082 - 노드 지표
- **애플리케이션 로그**: `./run.sh logs spark-app` - 런타임 진단

## 🔄 개발 워크플로우

```bash
# 개발 사이클
./run.sh down          # 서비스 중지
# src/spark.py 편집     # 애플리케이션 로직 수정
./run.sh build         # 컨테이너 재빌드
./run.sh up            # 변경사항 배포

# 기타 유용한 명령어
./run.sh restart       # 서비스 재시작
./run.sh cleanup       # 모든 컨테이너 및 이미지 정리
./run.sh help          # 사용 가능한 명령어 확인
```

## 📋 관리 명령어

`run.sh` 스크립트는 다음과 같은 명령어를 지원합니다:

| 명령어 | 설명 |
|--------|------|
| `up`, `start` | Spark 클러스터 시작 |
| `down`, `stop` | Spark 클러스터 중지 |
| `restart` | 클러스터 재시작 |
| `build` | Docker 이미지 빌드 |
| `logs [service]` | 로그 확인 (서비스 이름 선택 가능) |
| `status`, `ps` | 컨테이너 상태 확인 |
| `cleanup` | 컨테이너 및 이미지 정리 |
| `help` | 도움말 표시 |

서비스 이름: `spark-master`, `spark-worker-1`, `spark-worker-2`, `spark-app`

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 라이선스가 부여됩니다 - 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

