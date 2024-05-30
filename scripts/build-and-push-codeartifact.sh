#!/bin/bash


# Variables
DOMAIN="python"
DOMAIN_OWNER="399199735604"
REPOSITORY="big-data-workshop"


aws codeartifact login --tool pip --domain $DOMAIN --domain-owner $DOMAIN_OWNER --repository $REPOSITORY  --region us-west-2 --profile yb-personal

poetry publish --build
