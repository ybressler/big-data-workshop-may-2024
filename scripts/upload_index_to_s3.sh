#!/bin/bash

# Define variables
bucket_name="yb-big-data-workshop-1"
profile_name="yb-personal"
index_file="index.html"

# first remove index
aws s3 rm "s3://${bucket_name}/${index_file}" --profile "${profile_name}" --only-show-errors

# Generate index.html
echo "<h1>Big Data Workshop</h1>" > "${index_file}"
echo "<p>Click on a file name to download it. Click on a directory to open it.</p>" >> "${index_file}"
echo "<p>The S3 path for these files begins with <b><code>s3://yb-big-data-workshop-1/</code></b>
  So the file <span style='color: #1E90FF'><code>2024-05-21 12-00-00 measurements.txt</code></span> becomes \
   <b><code>s3://yb-big-data-workshop-1/<span style='color: #1E90FF;'>2024-05-21 12-00-00 measurements.txt</code></span></b> \
  </p>" >> "${index_file}"
echo "<ul>" >> "${index_file}"
aws s3 ls "s3://${bucket_name}/" --recursive --human-readable --profile "${profile_name}" | sort -k1 | \
awk '{sub(/^ +/, "", $0); print}' | \
while read -r line; do
    file_date=$(echo "${line}" | awk '{print $5, $6}')
    file_name=$(echo "${line}" | awk '{print $5, $6, $7}')
    file_size=$(echo "${line}" | awk '{print $3, $4}')
    echo "<li><a href=\"https://${bucket_name}.s3.amazonaws.com/${file_name}\">${file_name}</a> - ${file_size}</li>" >> "${index_file}"
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
