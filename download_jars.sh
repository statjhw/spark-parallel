#!/bin/bash

# JAR 파일 다운로드 스크립트
# 이 스크립트는 필요한 JAR 파일들을 자동으로 다운로드합니다.

echo "🚀 Spark JAR 파일들을 다운로드합니다..."

# jars 디렉토리 생성
mkdir -p jars

# Spark BigQuery Connector
echo "📦 Spark BigQuery Connector 다운로드 중..."
wget -O jars/spark-bigquery-with-dependencies_2.12-0.34.0.jar \
  "https://repo1.maven.org/maven2/com/google/cloud/spark/spark-bigquery-with-dependencies_2.12/0.34.0/spark-bigquery-with-dependencies_2.12-0.34.0.jar"

# Hadoop AWS
echo "📦 Hadoop AWS 다운로드 중..."
wget -O jars/hadoop-aws-3.3.4.jar \
  "https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar"

# AWS Java SDK Bundle
echo "📦 AWS Java SDK Bundle 다운로드 중..."
wget -O jars/aws-java-sdk-bundle-1.12.262.jar \
  "https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.262/aws-java-sdk-bundle-1.12.262.jar"

# GCS Connector (선택사항)
echo "📦 GCS Connector 다운로드 중..."
wget -O jars/gcs-connector-3.0.9-shaded.jar \
  "https://repo1.maven.org/maven2/com/google/cloud/bigdataoss/gcs-connector/3.0.9/gcs-connector-3.0.9-shaded.jar"

echo "✅ 모든 JAR 파일 다운로드 완료!"
echo "💡 이제 'docker-compose up -d'로 Spark 클러스터를 시작할 수 있습니다."
