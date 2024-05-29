# Big Data Workshop
Placeholder for something meaningful.

## Getting Started:
1. Prerequisites:
   1. poetry is installed
      ```bash
      which poetry
      ```
      If poetry not found, install it using [pipx](https://pipx.pypa.io/stable/installation/):
      ```
      brew install pipx
      pipx install poetry
      pipx ensurepath
      source ~/.zshrc
      ```
   2. `pyenv` is installed
      ```bash
      pyenv --version
      ```
      If not, install it
      ```bash
      brew install pyenv
      ```
2. Install python 3.11
   ```
   pyenv install 3.11
   ```
2. Run `make setup`
3. Install pre-commit hooks:
   ```shell
   pipx install pre-commit
   pre-commit install
   ```
4. Install pre-commit hooks: `pre-commit run -a`


# Make Data
We're going to create "a lot" of data and store it in S3
```shell
make create-data
```
View data here: https://yb-big-data-workshop-1.s3-us-west-2.amazonaws.com/index.html

## Compressing data
Compressing the data decreases its size by 10X. We can compress it when writing directly in polars
using `pgzip.open(...)`. (Note: `pgzip` is the parallel implementation of `gzip`.)


## Resources:
This article is inspiration: [Python One Billion Row Challenge — From 10 Minutes to 4 Seconds](https://medium.com/towards-data-science/python-one-billion-row-challenge-from-10-minutes-to-4-seconds-0718662b303e)
