# Bitnami Spark 이미지 활용
FROM bitnami/spark:3.4

# 패키지 설치를 위해 root 권한 사용
USER root

# requirements.txt 파일 복사
COPY ../../requirements.txt .

# .env 파일 복사
COPY ../../.env /.env

# 파이썬 라이브러리 설치
RUN pip install --no-cache-dir -r requirements.txt

COPY ../../.secrets/service_account.json /secrets/service_account.json

RUN chmod 644 /secrets/service_account.json

COPY ../../jars/*.jar /jars/
# -------------------------------
# 다시 기본 사용자로 변경
USER 1001