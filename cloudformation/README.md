# aws-glue
Repository contains AWS glue cloud formation template for AWS public provider.
AWS Glue is a fully managed extract, transform, and load (ETL) service that makes it easy for customers to prepare and load their data for analytics.


## Prerequisites
Please download example data to your S3 bucket. You can find them under following URL
[here](https://download.bls.gov/pub/time.series/oe).

## Filling the Template
**AuroraStack** - The stack name for Aurora stack.

**CrawlerName** - AWS Glue Crawler name.

**CrawlerDatabaseName** - AWS Glue Crawler database name.

**CrawlerTableName** - AWS Glue Crawler table name.

**TablePrefixName** - Prefix for AWS Glue Crawler table.
