import os
import dotenv
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg

dotenv.load_dotenv()
key_file_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
gcs_bucket = os.getenv("GCS_BUCKET")

def main():
    try:
        spark = SparkSession.builder \
            .appName("BigQueryIntegration") \
            .master("spark://spark-master:7077") \
            .getOrCreate()
    except Exception as e:
        print(f"Error creating SparkSession: {e}")
        return
    
    try:
        #BigQuery 인증
        spark.config.set("credentialsFile", key_file_path)

        #GCS 인증
        spark.config.set("temporaryGcsBucket", gcs_bucket)
    except Exception as e:
        print(f"Error setting up SparkSession: {e}")
        return
    
    try:
        #BigQuery 데이터를 읽어오기
        table = "bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2022"
        print(f"테이블 {table}를 읽어옵니다.")
        
        df = spark.read.format("bigquery").option("table", table).load()
        
        print(f"테이블 {table}를 읽었습니다.")

        print("데이터 스키마:")
        df.printSchema()

        print("데이터의 일부를 보여줍니다:")
        df.show(5)
    except Exception as e:
        print(f"Error reading BigQuery table: {e}")
        return
    
    try:
        #데이터 처리 : 승객 수(passenger_count)별 평균 요금
        filtered_df = df.filter((col("passenger_count").isNotNull()) & (col("passenger_count") > 0))

        print("승객 수별 평균 요금을 계산합니다")
        result_df = filtered_df.groupBy("passenger_count") \
            .agg(avg("total_amount").alias("avg_total_amount")) \
            .orderBy("passenger_count") 
        
        print("====처리 결과====")
        result_df.show()
        print("================")

    except Exception as e:
        print(f"Error processing data: {e}")
        return
    
    try:
        #처리 결과 BigQuery에 저장
        output_table = "my_sark_results.nyc_taxi_fare_by_passenger"
        
        print(f"처리결과를 BigQuery에 저장합니다: {output_table}")

        result_df.write.format("bigquery") \
            .option("table", output_table) \
            .mode("overwrite") \
            .save()

        print("작업이 성공적으로 완료되었습니다")        
        spark.stop()
    except Exception as e:
        print(f"Error writing to BigQuery: {e}")
        return

if __name__ == "__main__":
    main()     
