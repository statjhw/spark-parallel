# 최종 spark.py (서비스 계정 키 직접 사용 방식)
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg
from dotenv import load_dotenv

def main():
    load_dotenv()
    try:
        key_file_path = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
        s3_bucket = os.environ['S3_BUCKET']
        gcp_project_id = os.environ['GCP_PROJECT_ID']
        aws_access_key = os.environ['AWS_ACCESS_KEY_ID']
        aws_secret_key = os.environ['AWS_SECRET_ACCESS_KEY']
        aws_region = os.environ.get('AWS_DEFAULT_REGION', 'us-east-1')
        print(f"환경 변수: key_file_path={key_file_path}, s3_bucket={s3_bucket}, project_id={gcp_project_id}")
        if not os.path.exists(key_file_path):
            raise FileNotFoundError(f"서비스 계정 키 파일을 찾을 수 없습니다: {key_file_path}")
    except KeyError as e:
        print(f"❌ 오류: .env 파일에서 필수 환경 변수를 찾을 수 없습니다: {e}")
        return
    except FileNotFoundError as e:
        print(f"❌ 오류: {e}")
        return

    spark = None
    try:
        # 1. SparkSession 생성 (BigQuery + S3 설정)
        spark = SparkSession.builder \
            .appName("BigQueryS3Integration") \
            .master("spark://spark-master:7077") \
            .config("spark.hadoop.google.cloud.auth.service.account.enable", "true") \
            .config("spark.hadoop.google.cloud.auth.service.account.json.keyfile", key_file_path) \
            .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
            .config("spark.hadoop.fs.s3a.access.key", aws_access_key) \
            .config("spark.hadoop.fs.s3a.secret.key", aws_secret_key) \
            .config("spark.hadoop.fs.s3a.endpoint.region", aws_region) \
            .config("spark.hadoop.fs.s3a.path.style.access", "true") \
            .config("spark.executorEnv.GOOGLE_APPLICATION_CREDENTIALS", key_file_path) \
            .config("spark.driverEnv.GOOGLE_APPLICATION_CREDENTIALS", key_file_path) \
            .config("spark.jars", "/jars/spark-bigquery-with-dependencies_2.12-0.34.0.jar,/jars/hadoop-aws-3.3.4.jar,/jars/aws-java-sdk-bundle-1.12.262.jar") \
            .config("spark.executor.extraJavaOptions", f"-Dgoogle.cloud.auth.service.account.json.keyfile={key_file_path} -Dgoogle.cloud.auth.service.account.enable=true") \
            .config("spark.driver.extraJavaOptions", f"-Dgoogle.cloud.auth.service.account.json.keyfile={key_file_path} -Dgoogle.cloud.auth.service.account.enable=true") \
            .getOrCreate()

        # 2. BigQuery 및 S3 설정
        spark.conf.set("temporaryGcsBucket", s3_bucket)  # BigQuery still uses this config name but can point to S3
        spark.conf.set("parentProject", gcp_project_id)
        spark.conf.set("spark.hadoop.google.cloud.auth.service.account.json.keyfile", key_file_path)
        print(f"S3 버킷 설정: {s3_bucket}, 프로젝트 ID: {gcp_project_id}")

        # 3. BigQuery 데이터 읽기
        table = "bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2022"
        print(f"테이블 {table}을(를) 읽어옵니다.")
        df = spark.read.format("bigquery").option("table", table).load()
        df.show(5)

        # 4. 데이터 처리
        print("승객 수별 평균 요금을 계산합니다.")
        filtered_df = df.filter((col("passenger_count").isNotNull()) & (col("passenger_count") > 0))
        result_df = filtered_df.groupBy("passenger_count") \
            .agg(avg("total_amount").alias("avg_total_amount")) \
            .orderBy("passenger_count")
        result_df.show()

        # 5. 처리 결과 S3에 Parquet 파일로 저장
        # S3 버킷 내에 results라는 폴더를 만들고 그 안에 저장합니다.
        output_path = f"s3a://{s3_bucket}/results/nyc_taxi_fare_by_passenger/"
        print(f"처리 결과를 S3에 저장합니다: {output_path}")
        
        # .write.mode().parquet()를 사용하여 S3에 직접 씁니다.
        result_df.write.mode("overwrite").parquet(output_path)

        print("✅ 작업이 성공적으로 완료되었습니다.")

    except Exception as e:
        print(f"❌ 작업 중 오류가 발생했습니다: {e}")
    finally:
        if spark:
            spark.stop()
            print("Spark 세션이 종료되었습니다.")

if __name__ == "__main__":
    main()