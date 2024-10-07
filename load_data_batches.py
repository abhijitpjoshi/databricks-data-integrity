from pyspark.sql import SparkSession

# Initialize Spark session
spark = SparkSession.builder.appName("LoadDataBatches").getOrCreate()

# Load data from Delta Lake or S3
df = spark.read.format("delta").load("s3://your-bucket/your-dataset")
batch_size = 10000  # Adjust based on cluster memory limitations

df_batches = df.randomSplit([0.1]*10)

# Show a sample
for i, df_batch in enumerate(df_batches):
    print(f"Processing Batch {i+1}")
    df_batch.show(5)
