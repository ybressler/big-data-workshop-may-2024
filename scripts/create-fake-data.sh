#!/bin/bash

# Default values
r=$((10 ** 9))
file_name="measurements.txt"

# Parse command-line arguments
while getopts "r:f:" opt; do
    case ${opt} in
        r )
            r=$OPTARG
            ;;
        f )
            file_name=$OPTARG
            ;;
        \? )
            echo "Usage: $0 [-r number] [-f filename]"
            exit 1
            ;;
    esac
done



poetry run python src/create_data/create_measurements.py -o "$file_name" -r "$r"
