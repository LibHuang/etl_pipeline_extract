# ETL pipeline Extract Overview

The Extract Service is a modular, production-ready component of a broader ETL/ELT data pipeline, designed to interface with AWS S3 and Snowflake. This service is responsible for sourcing raw data from external systems and making it available for downstream transformation and loading processes. Built with scalability and observability in mind, it aligns with enterprise data architecture standards.

**Project**

In this example we will be extracting ASOS data from a RAPID API seemlessly from API straight to S3 Cloud without any local computer processes. ASOS is a global online fashion and cosmetic retailer headquartered in the United Kingdom. It offers a wide range of clothing, accessories, and beauty products aimed primarily at young adults. Known for its trend-driven collections and inclusive sizing, ASOS operates a direct-to-consumer e-commerce model and serves customers in over 200 countries.

I will be using this API and dataset because it provides rich, comprehensive data well-suited for a business project of this nature. The nature of this API offers cost-effective results without requiring access to sensitive information, while adhering to relevant compliance standards.

# Architecture 

**Procedure**

The process will entail Extracting from the API with reliability standards seemlessly to S3 bucket.

1. S3_setup.py details the loading process to connect to my S3 Bucket.

2. API_Data_Extraction.py handles the extraction of JSON data from the API and uses io.BytesIO() to create an in-memory buffer for direct upload to S3 via boto3.

**Features**

• Secure and reliable data extraction

• Supports batch and incremental extraction strategies

• Environment-aware (Dev, QA, Prod)

• Error handling, logging, and retry mechanisms

• Built-in observability and alerting support

• Easy integration with orchestration tools (e.g., Airflow, Autosys)

**Prerequisites** 
• Python >= 3.10

• AWS credentials (with access to S3)

• Snowflake user with read access

**Security**

• Credentials managed via environment variables

• Compliant with enterprise access policies

