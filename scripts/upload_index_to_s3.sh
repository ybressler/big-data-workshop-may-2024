#!/bin/bash

# Define variables
bucket_name="yb-big-data-workshop-1"
profile_name="yb-personal"
index_file="index.html"

# Generate index.html
echo "<h1>Big Data Workshop</h1>" > "${index_file}"
echo "<p>Click on a file name to download it. Click on a directory to open it.</p>" > "${index_file}"
echo "<ul>" > "${index_file}"
aws s3 ls "s3://${bucket_name}/" --recursive --profile "${profile_name}" | \
awk '{sub(/^ +/, "", $0); for (i=4; i<=NF; i++) printf "%s%s", $i, (i<NF ? OFS : "\n")}' | \
while read -r line; do
    echo "<li><a href=\"https://${bucket_name}.s3.amazonaws.com/${line}\">${line}</a></li>" >> "${index_file}"
done
echo "</ul>" >> "${index_file}"

# Upload index.html to S3 bucket
aws s3 cp "${index_file}" "s3://${bucket_name}/${index_file}" --profile "${profile_name}"

echo "Index.html generated and uploaded successfully!"

# Remove index.html from local machine
rm "${index_file}"

echo "Index.html removed from local machine!"

# Print public URL for index.html
public_url="https://${bucket_name}.s3.amazonaws.com/${index_file}"
echo "Public URL for index.html: ${public_url}"
