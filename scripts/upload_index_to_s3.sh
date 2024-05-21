#!/bin/bash

# Define variables
bucket_name="yb-big-data-workshop-1"
profile_name="yb-personal"
index_file="index.html"

# Generate index.html
aws s3 ls "s3://${bucket_name}/" --recursive --profile "${profile_name}" | \
awk '{$1=$2=$3=""; print "<li><a href=\"https://${bucket_name}.s3.amazonaws.com" $4 "\">" $4 "</a></li>"}' \
> "${index_file}"

# Upload index.html to S3 bucket
aws s3 cp "${index_file}" "s3://${bucket_name}/${index_file}" --profile "${profile_name}"

echo "Index.html generated and uploaded successfully!"

# Remove index.html from local machine
rm "${index_file}"

echo "Index.html removed from local machine!"

# Print public URL for index.html
public_url="https://${bucket_name}.s3.amazonaws.com/${index_file}"
echo "Public URL for index.html: ${public_url}"
