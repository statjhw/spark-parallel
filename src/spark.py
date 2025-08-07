from pyspark.sql import SparkSession

def main():
    """
    Main function to initialize Spark, create an RDD, and print its contents.
    """
    # SparkSession is the modern entry point for Spark applications
    spark = SparkSession.builder \
        .appName("SimpleSparkApp") \
        .getOrCreate()

    # You can get the SparkContext from the SparkSession
    sc = spark.sparkContext

    print("Creating an RDD from a list of numbers.")
    rdd = sc.parallelize([1, 2, 3, 4, 5])

    print("Collecting and printing the RDD contents:")
    collected_rdd = rdd.collect()
    print(collected_rdd)

    # It's a good practice to stop the SparkSession to release resources
    spark.stop()
    print("Spark session stopped.")

if __name__ == "__main__":
    main()