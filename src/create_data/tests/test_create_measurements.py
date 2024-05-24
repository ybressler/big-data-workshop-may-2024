# -*- coding: utf-8 -*-
import pytest
import polars as pl

from src.create_data.create_measurements import CreateMeasurement


@pytest.fixture(scope="module")
def create_measurements():
    return CreateMeasurement(seed=123)


@pytest.mark.parametrize(("std_dev", "records"), [(0, 10_000), (10, 10_000), (20, 10_000), (1, 100_000), (100, 10_000)])
def test_generate_batch(std_dev, records, create_measurements):
    """
    Tests functionality of generate_batch
    """
    batch: pl.DataFrame = create_measurements.generate_batch(std_dev, records)
    assert batch.height == records

    mean_std = batch.groupby("names").agg(pl.col("temperature").std()).mean().item(0, 1)
    assert round(mean_std, 0) == std_dev
