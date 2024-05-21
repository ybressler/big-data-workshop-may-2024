# Big Data Workshop
Placeholder for something meaningful.

## Getting Started:
1. Prerequisites:
   1. poetry is installed
2. Run `make setup`
3. Install pre-commit hooks: `pre-commit run -a`


# Make Data
We're going to create "a lot" of data and store it in S3
```shell
make create-data
```
View data here: https://yb-big-data-workshop-1.s3-us-west-2.amazonaws.com/index.html

## Compressing data
Compressing the data decreases its size by 10X. We can compress it when writing directly in polars
using `pgzip.open(...)`. (Note: `pgzip` is the parallel implementation of `gzip`.)
