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
2. Use `pyenv` to install python 3.11.6
   ```
   pyenv install 3.11.6
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


----

# Actual Course:

## Why is this course important?
1. If data is too big, don't throw in the towel, you can process it using this ways
2. If you already process big data, maybe there are more efficient or cost effective ways to do it
3. Build the right solution for the right problem.

> **If you take this course:**<br>
> You will know how to process big data in multiple ways and which is the best
> choice for you.


## Objective:
We are receiving weather station data. We want to determine the average temperature
for any given range of dates. (Can be a single date, or many dates.)

Would be wasteful to re-calculate each time, or calculate every combination. Instead, we create a data mart which
looks like this:

| Date       | Station_name | Min | Mean | Max | Count |
|------------|--------------|-----|------|-----|-------|
| 2024-05-25 | Alexandria   | 8   | 20   | 26  | 20    |
| 2024-05-26 | Alexandria   | 6   | 21   | 26  | 10    |
| 2024-05-27 | Alexandria   | 9   | 19   | 27  | 15    |

This allows us to handle late arriving data. (Assuming we can get data for a previous date at any point.)

We'll materialize these partial calculations and store them somewhere. Then, whenever someone
needs to query for a certain date, we'll be able to give them their result.



## Themes:
1. Multiple ways to process a file
   1. in memory
   2. in chunks
   3. streaming
   4. map reduce
   5. massively parallel processing (MPP) _[out of scope]_
2. Big data is IO bound (when downloading/uploading big files)
   1. Compress when possible
   2. Move compute closer to the data (private network / VPC / access point / or, in the actual data center)
3. Don't do things twice
   1. Caching (via disk) - don't download a file twice
   2. Incrementalism: use your data to determine offsets - don't process data twice
4. Orchestrate pipelines instead of executing straight code
   1. Simplifies complex systems
   2. Allows delegation to other machines
5. Big powerful tools can be expensive - but sometimes they are worth it
   1. Perhaps demonstrate how to process this all in Snowflake or BigQuery

## Coding
1. Start with installation
   1. Prove things work with `src/start_here/main.py`
2. Download a small file manually and process in pandas
   1. in memory
   2. in chunks
   3. in stream
3. Process in polars
4. Mention dask
5. Now, we automate the download of the file (can read directly from url)
   1. but we have a new problem - process begins downloading the file all over again
   2. So we use a framework to _"look before you leap"_, downloads a file if needed
