# Big Data Workshop
Placeholder for something meaningful.

## Getting Started: (Mac Users)
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
## Getting Started: (Windows Users)
1. Install [scoop](https://scoop.sh/)
2. Use `scoop` to install poetry and make:
   ```shell
   scoop install pipx
   scoop install make
   ```
3. Use `pipx` to install poetry:
   ```shell
   pipx install poetry
   pipx ensurepath
   ```
4. Install [pyenv-win](https://github.com/pyenv-win/pyenv-win):
5. Reload your terminal

## Getting Started: (All Users)
2. Use `pyenv` to install python 3.11
   ```
   pyenv install 3.11
   ```
2. Install everything with: `make`:
   ```shell
   make setup
   ```
3. Install pre-commit hooks:
   ```shell
   pipx install pre-commit
   pipx ensurepath
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
