aws ecr get-login-password --region us-west-2 --profile yb-personal | docker login --username AWS --password-stdin 399199735604.dkr.ecr.us-west-2.amazonaws.com
docker build -t big-data-workshop-create-data .
docker tag big-data-workshop-create-data:latest 399199735604.dkr.ecr.us-west-2.amazonaws.com/yb-python:latest
docker push 399199735604.dkr.ecr.us-west-2.amazonaws.com/yb-python:latest
