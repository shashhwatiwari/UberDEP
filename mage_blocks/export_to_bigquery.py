from google.cloud import bigquery
from pandas import DataFrame

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_big_query(data, **kwargs) -> None:
    # Authenticates via Application Default Credentials (the VM's attached
    # service account) — no key file required.
    client = bigquery.Client()

    for key, value in data.items():
        table_id = 'uber-data-analytics-501621.uber_data_engineering.{}'.format(key)
        job = client.load_table_from_dataframe(
            DataFrame(value),
            table_id,
            job_config=bigquery.LoadJobConfig(write_disposition='WRITE_TRUNCATE'),
        )
        job.result()  # wait for the load job to complete
