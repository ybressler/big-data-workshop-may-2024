# -*- coding: utf-8 -*-
from dagster import (
    AssetSelection,
    Definitions,
    FilesystemIOManager,
    define_asset_job,
    load_assets_from_modules,
)

from src.dag import download_data


all_assets = load_assets_from_modules([download_data])

# Addition: define a job that will materialize the assets
my_job = define_asset_job(name="download_data", selection=AssetSelection.all())

defs = Definitions(assets=all_assets, jobs=[my_job], resources={"io_manager": FilesystemIOManager()})
