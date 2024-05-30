# -*- coding: utf-8 -*-
import json
from pathlib import Path
from typing import Any, List

from dagster import AssetExecutionContext, MaterializeResult, MetadataValue, asset

from src.download_data.main import (
    RAW_DATA_PATH,
    convert_txt_to_parquet,
    decompress_file,
    get_all_urls,
    get_data_for_url,
)
from src.process_data.duckdb.main import DuckDBInterface

dst_dir = Path(RAW_DATA_PATH)
clean_dir = Path("tmp/clean")
result_dir = Path("tmp/results")

for p in [dst_dir, clean_dir, result_dir]:
    p.mkdir(parents=True, exist_ok=True)


@asset
def dg_get_all_urls() -> List[str]:
    all_urls = get_all_urls()
    return all_urls


@asset
def df_get_data_for_url(context: AssetExecutionContext, dg_get_all_urls: Any) -> MaterializeResult:
    all_urls = dg_get_all_urls

    n_download_data = 0
    file_locations = []

    for i, url in enumerate(all_urls):
        dst_file_name = dst_dir / url.split(".com/")[1]
        if dst_file_name.exists():
            context.log.info(f"already downloaded '{url}'")
        else:
            get_data_for_url(url, dst_file_name)
            n_download_data += 1

        file_locations.append(dst_file_name)

    return MaterializeResult(
        metadata={"n_download_data": n_download_data, "file_locations": MetadataValue.md(json.dumps(file_locations))}
    )


@asset(deps=[df_get_data_for_url])
def dg_decompress_file(context: AssetExecutionContext):
    for file_name in dst_dir.iterdir():
        if file_name.suffix != ".gz":
            continue
        dst_file_name = file_name.with_suffix("")
        if dst_file_name.exists():
            context.log.info(f"already decompressed '{file_name}'")
        else:
            decompress_file(file_name, True)


@asset(deps=[dg_decompress_file])
def dg_convert_to_parquet(context: AssetExecutionContext) -> MaterializeResult:
    parquet_file_names = []

    for file_name in dst_dir.iterdir():
        if file_name.suffix != ".txt":
            continue

        new_parts = ["clean" if x == "raw" else x for x in file_name.parts]
        dst_file_name = Path(*new_parts).with_suffix(".parquet")
        dst_file_name.parent.mkdir(parents=True, exist_ok=True)

        if dst_file_name.exists():
            context.log.info(f"already converted '{file_name}' to parquet --> {dst_file_name}")
        else:
            convert_txt_to_parquet(file_name, dst_file_name)
            context.log.info(f"finished converting '{file_name}' to parquet --> {dst_file_name}")
        parquet_file_names.append(dst_file_name)

    return MaterializeResult(
        metadata={
            "n_files": len(parquet_file_names),
            "file_names": [x.as_posix() for x in parquet_file_names],
        }
    )


@asset(deps=[dg_convert_to_parquet])
def calculate_parquet(context: AssetExecutionContext) -> MaterializeResult:
    """
    Performs main calculation and stores results in a csv file
    """

    for parquet_file_name in clean_dir.iterdir():
        context.log.info(f"Processing data for '{parquet_file_name}'")
        result = DuckDBInterface().in_memory(parquet_file_name.as_posix())
        context.log.info(result.query("station_name == 'Alexandria'").head().to_markdown())

        # save results
        result_path = result_dir / Path(parquet_file_name).with_suffix(".csv").name
        result.to_csv(result_path)

        return MaterializeResult(
            metadata={
                "n_rows": len(result),
                "preview": MetadataValue.md(result.head().to_markdown()),
                "result_file_location": result_path.as_posix(),
            }
        )
