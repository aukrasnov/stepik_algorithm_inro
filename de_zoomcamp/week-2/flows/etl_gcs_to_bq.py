from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials


@task(retries=3)
def extract_from_gcs(color: str, year: int, month: int) -> Path:
    """Download trip data from GCS"""
    gcs_path = f"/de-zoomcamp-4/{color}_tripdata_{year}-{month:02}.parquet"
    gcs_block = GcsBucket.load("zoom-gcs")
    gcs_block.get_directory(from_path=gcs_path, local_path=f"../data/")
    return Path(f"../data/{gcs_path}")


@task()
def transform(path: Path) -> pd.DataFrame:
    """Data cleaning example"""
    df = pd.read_parquet(path)
    print(f"pre: missing passenger count: {df['passenger_count'].isna().sum()}")
    df["passenger_count"].fillna(0, inplace=True)
    print(f"post: missing passenger count: {df['passenger_count'].isna().sum()}")
    return df


@task()
def write_bq(df: pd.DataFrame, color) -> None:
    """Write DataFrame to BiqQuery"""

    gcp_credentials_block = GcpCredentials.load("zoom-gcp-creds")

    df.to_gbq(
        destination_table=f"trips_data_all.{color}_tripdata",
        project_id="de-zoomcamp-3756212",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append",
    )


@flow(log_prints=True)
def etl_gcs_to_bq():
    """Main ETL flow to load data into Big Query"""
    colors = ["green", "yellow"]
    years = [2019, 2020]
    months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    i = 0
    for color in colors:
        for year in years:
            for month in months:
                # path = extract_from_gcs(color, year, month)
                path = Path(f"/Users/aleksandr/dev_dao/de_zoomcamp/week-2/flows/data/{color}/{color}_tripdata_{year}-{month:02}.parquet")
                df = transform(path)
                i += df.shape[0]
                print(f"Current total rows {i}")
                write_bq(df, color)


if __name__ == "__main__":
    etl_gcs_to_bq()
