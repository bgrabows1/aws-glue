# aws-glue
Repository contains AWS glue cloud formation template for AWS public provider.
AWS Glue is a fully managed extract, transform, and load (ETL) service that makes it easy for customers to prepare and load their data for analytics.


## Prerequisites
Please download example data to your S3 bucket. You can find them under following URL
[here](https://download.bls.gov/pub/time.series/oe).

## Filling the Template for Aurora stack
**AuroraDBName** - Aurora database name.

**AuroraDBUsername** - Admin user for Aurora database.

**AuroraDBPassword** - Aurora database password.

**AuroraDBInstanceType** - Aurora database instance class.

**DBEngineVersion** - Aurora database engine version.

**AlertSnsTopicArn** - AWS SNS topic for CloudWatch notifications.

**EmailAddress** - Email address used to configure a SNS topic for sending cloudwatch alarm and RDS Event notifications.

## Filling the Template for AWS Glue stack
**AuroraStack** - The stack name for Aurora stack.

**CrawlerName** - AWS Glue Crawler name.

**CrawlerDatabaseName** - AWS Glue Crawler database name.

**CrawlerTableName** - AWS Glue Crawler table name.

**TablePrefixName** - Prefix for AWS Glue Crawler table.

**JDBCConnectionName** - JDBC connection name.

**JDBCString** - JDBC connection string.

**JDBCUser** - JDBC user name.

**JDBCPassword** - JDBC password.

**S3Name** - S3 path for AWS Glue crawlers.
