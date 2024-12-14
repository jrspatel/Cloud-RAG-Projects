from pyspark.sql import SparkSession
from synapse.ml.cognitive import AnalyzeDocument

# Initialize Spark session with necessary packages
spark = SparkSession.builder \
    .appName("AzureBlobPDFProcessing") \
    .config("spark.jars.packages", "com.microsoft.azure:azure-storage:8.6.5") \
    .getOrCreate()

# Define your Azure Blob Storage credentials
account_name = "Z"
account_key = "Z"
container_name = "data"
blob_name = "support.pdf"
pdf_url = f"wasbs://{container_name}@{account_name}.blob.core.windows.net/{blob_name}"

# Set up SynapseML AnalyzeDocument
analyze_document = AnalyzeDocument() \
    .setSubscriptionKey("your_form_recognizer_key") \
    .setLocation("eastus") \
    .setModelId("prebuilt-layout") \
    .setInputCol("pdf_url") \
    .setOutputCol("output_content")

# Create a DataFrame with the URL of the PDF in Blob Storage
pdf_df = spark.createDataFrame([(pdf_url,)], ["pdf_url"])

print(pdf_df)
# Use SynapseML's AnalyzeDocument transformer to extract the content
processed_df = analyze_document.transform(pdf_df)

# Show the extracted content
processed_df.select("output_content").show(truncate=False)
